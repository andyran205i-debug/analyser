from app import db
from app.models import Match, Team, Prediction
from app.services.api_service import APIService
from typing import Dict, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataService:
    """Service for managing data synchronization and storage."""
    
    def __init__(self):
        self.api_service = APIService()
    
    # ============================================
    # SYNC OPERATIONS
    # ============================================
    
    def sync_live_matches(self) -> bool:
        """Sync all live matches from API-FOOTBALL into database."""
        try:
            # Fetch from API-FOOTBALL
            live_matches = self.api_service.get_live_matches()
            
            if not live_matches or 'response' not in live_matches:
                logger.warning("No live matches data received")
                return False
            
            count = 0
            for match_data in live_matches['response']:
                if self._process_match_data(match_data):
                    count += 1
            
            db.session.commit()
            logger.info(f"Synced {count} live matches")
            return True
        except Exception as e:
            logger.error(f"Sync error: {str(e)}")
            db.session.rollback()
            return False
    
    def sync_scheduled_matches(self, days_ahead: int = 7) -> bool:
        """Sync scheduled matches for the next N days."""
        try:
            scheduled_matches = self.api_service.get_scheduled_matches(days_ahead)
            
            if not scheduled_matches or 'response' not in scheduled_matches:
                logger.warning("No scheduled matches data received")
                return False
            
            count = 0
            for match_data in scheduled_matches['response']:
                if self._process_match_data(match_data):
                    count += 1
            
            db.session.commit()
            logger.info(f"Synced {count} scheduled matches")
            return True
        except Exception as e:
            logger.error(f"Scheduled sync error: {str(e)}")
            db.session.rollback()
            return False
    
    def sync_league_matches(self, league_id: int, season: int) -> bool:
        """Sync all matches from a specific league and season."""
        try:
            league_matches = self.api_service.get_fixtures_by_league(league_id, season)
            
            if not league_matches or 'response' not in league_matches:
                logger.warning(f"No matches data for league {league_id}, season {season}")
                return False
            
            count = 0
            for match_data in league_matches['response']:
                if self._process_match_data(match_data):
                    count += 1
            
            db.session.commit()
            logger.info(f"Synced {count} matches from league {league_id}, season {season}")
            return True
        except Exception as e:
            logger.error(f"League sync error: {str(e)}")
            db.session.rollback()
            return False
    
    # ============================================
    # DATA PROCESSING
    # ============================================
    
    def _process_match_data(self, match_data: Dict) -> bool:
        """Process and store individual match data."""
        try:
            fixture = match_data.get('fixture', {})
            teams = match_data.get('teams', {})
            goals = match_data.get('goals', {})
            league = match_data.get('league', {})
            
            if not all([fixture.get('id'), teams.get('home'), teams.get('away')]):
                logger.warning("Incomplete match data")
                return False
            
            # Get or create teams
            home_team = self._get_or_create_team(
                teams['home'].get('id'),
                teams['home'].get('name'),
                teams['home'].get('logo')
            )
            
            away_team = self._get_or_create_team(
                teams['away'].get('id'),
                teams['away'].get('name'),
                teams['away'].get('logo')
            )
            
            if not home_team or not away_team:
                return False
            
            # Get or create match
            match = Match.query.filter_by(api_id=fixture['id']).first()
            
            if not match:
                try:
                    match_date = datetime.fromisoformat(fixture['date'].replace('Z', '+00:00'))
                except:
                    match_date = datetime.utcnow()
                
                match = Match(
                    api_id=fixture['id'],
                    home_team_id=home_team.id,
                    away_team_id=away_team.id,
                    league=league.get('name', 'Unknown'),
                    season=league.get('season'),
                    match_date=match_date,
                    status=fixture.get('status', {}).get('short', 'NS')
                )
                db.session.add(match)
            else:
                match.status = fixture.get('status', {}).get('short', 'NS')
            
            # Update match stats
            match.home_goals = goals.get('home')
            match.away_goals = goals.get('away')
            
            db.session.add(match)
            return True
        except Exception as e:
            logger.error(f"Error processing match data: {str(e)}")
            return False
    
    def _get_or_create_team(self, api_id: int, name: str, logo_url: Optional[str]) -> Optional[Team]:
        """Get or create a team in the database."""
        try:
            if not api_id or not name:
                return None
            
            team = Team.query.filter_by(api_id=api_id).first()
            
            if not team:
                team = Team(
                    api_id=api_id,
                    name=name,
                    logo_url=logo_url
                )
                db.session.add(team)
            
            return team
        except Exception as e:
            logger.error(f"Error creating/fetching team: {str(e)}")
            return None
    
    # ============================================
    # DATA RETRIEVAL
    # ============================================
    
    def get_live_matches_with_predictions(self) -> List[Dict]:
        """Get all live matches with their predictions."""
        try:
            matches = Match.query.filter(
                Match.status.in_(['LIVE', 'NS', '1H', '2H', 'HT'])
            ).all()
            
            result = []
            for match in matches:
                match_dict = match.to_dict()
                
                # Add team info
                home_team = Team.query.get(match.home_team_id)
                away_team = Team.query.get(match.away_team_id)
                
                match_dict['home_team'] = home_team.to_dict() if home_team else {}
                match_dict['away_team'] = away_team.to_dict() if away_team else {}
                
                # Get associated prediction
                prediction = Prediction.query.filter_by(match_id=match.id).first()
                if prediction:
                    match_dict['prediction'] = prediction.to_dict()
                
                result.append(match_dict)
            
            return result
        except Exception as e:
            logger.error(f"Error fetching live matches: {str(e)}")
            return []
    
    def get_scheduled_matches_with_predictions(self, days_ahead: int = 7) -> List[Dict]:
        """Get scheduled matches for the next N days with predictions."""
        try:
            from datetime import timedelta
            future_date = datetime.utcnow() + timedelta(days=days_ahead)
            
            matches = Match.query.filter(
                Match.match_date <= future_date,
                Match.status == 'NS'
            ).order_by(Match.match_date).all()
            
            result = []
            for match in matches:
                match_dict = match.to_dict()
                
                # Add team info
                home_team = Team.query.get(match.home_team_id)
                away_team = Team.query.get(match.away_team_id)
                
                match_dict['home_team'] = home_team.to_dict() if home_team else {}
                match_dict['away_team'] = away_team.to_dict() if away_team else {}
                
                # Get associated prediction
                prediction = Prediction.query.filter_by(match_id=match.id).first()
                if prediction:
                    match_dict['prediction'] = prediction.to_dict()
                
                result.append(match_dict)
            
            return result
        except Exception as e:
            logger.error(f"Error fetching scheduled matches: {str(e)}")
            return []
    
    def get_match_details(self, match_id: int) -> Optional[Dict]:
        """Get detailed information for a specific match."""
        try:
            match = Match.query.get(match_id)
            if not match:
                return None
            
            match_dict = match.to_dict()
            
            # Add team info
            home_team = Team.query.get(match.home_team_id)
            away_team = Team.query.get(match.away_team_id)
            
            match_dict['home_team'] = home_team.to_dict() if home_team else {}
            match_dict['away_team'] = away_team.to_dict() if away_team else {}
            
            # Get prediction
            prediction = Prediction.query.filter_by(match_id=match.id).first()
            if prediction:
                match_dict['prediction'] = prediction.to_dict()
            
            return match_dict
        except Exception as e:
            logger.error(f"Error fetching match details: {str(e)}")
            return None
    
    def get_league_matches(self, league_name: str) -> List[Dict]:
        """Get all matches from a specific league."""
        try:
            matches = Match.query.filter_by(league=league_name).all()
            
            result = []
            for match in matches:
                match_dict = match.to_dict()
                
                home_team = Team.query.get(match.home_team_id)
                away_team = Team.query.get(match.away_team_id)
                
                match_dict['home_team'] = home_team.to_dict() if home_team else {}
                match_dict['away_team'] = away_team.to_dict() if away_team else {}
                
                result.append(match_dict)
            
            return result
        except Exception as e:
            logger.error(f"Error fetching league matches: {str(e)}")
            return []
    
    def get_team_matches(self, team_id: int) -> List[Dict]:
        """Get all matches for a specific team."""
        try:
            matches = Match.query.filter(
                (Match.home_team_id == team_id) | (Match.away_team_id == team_id)
            ).all()
            
            result = []
            for match in matches:
                match_dict = match.to_dict()
                
                home_team = Team.query.get(match.home_team_id)
                away_team = Team.query.get(match.away_team_id)
                
                match_dict['home_team'] = home_team.to_dict() if home_team else {}
                match_dict['away_team'] = away_team.to_dict() if away_team else {}
                
                result.append(match_dict)
            
            return result
        except Exception as e:
            logger.error(f"Error fetching team matches: {str(e)}")
            return []
    
    # ============================================
    # ENRICHMENT
    # ============================================
    
    def enrich_match_with_api_data(self, match_id: int, fixture_id: int) -> bool:
        """Enrich match data with additional API-FOOTBALL information."""
        try:
            # Fetch predictions and odds
            predictions = self.api_service.get_match_predictions(fixture_id)
            statistics = self.api_service.get_match_statistics(fixture_id)
            
            # Update match record with enriched data
            match = Match.query.get(match_id)
            if match and statistics and 'response' in statistics:
                # You can extend the Match model to store additional stats
                pass
            
            return True
        except Exception as e:
            logger.error(f"Error enriching match data: {str(e)}")
            return False
    
    def get_api_status(self) -> bool:
        """Check if API-FOOTBALL is accessible."""
        return self.api_service.is_api_key_valid()
