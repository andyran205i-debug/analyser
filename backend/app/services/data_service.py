from app import db
from app.models import Match, Team, Prediction
from app.services.api_service import APIService
from typing import Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataService:
    """Service for managing data synchronization and storage."""
    
    def __init__(self):
        self.api_service = APIService()
    
    def sync_live_matches(self) -> bool:
        """Sync live matches from API into database."""
        try:
            # Fetch from API-FOOTBALL
            live_matches = self.api_service.get_live_matches_api_football()
            
            if not live_matches or 'response' not in live_matches:
                logger.warning("No live matches data received")
                return False
            
            for match_data in live_matches['response']:
                self._process_match_data(match_data)
            
            db.session.commit()
            logger.info(f"Synced {len(live_matches['response'])} matches")
            return True
        except Exception as e:
            logger.error(f"Sync error: {str(e)}")
            db.session.rollback()
            return False
    
    def _process_match_data(self, match_data: Dict) -> None:
        """Process and store individual match data."""
        try:
            fixture = match_data['fixture']
            teams = match_data['teams']
            goals = match_data['goals']
            league = match_data['league']
            
            # Get or create teams
            home_team = self._get_or_create_team(
                teams['home']['id'],
                teams['home']['name'],
                teams['home'].get('logo')
            )
            
            away_team = self._get_or_create_team(
                teams['away']['id'],
                teams['away']['name'],
                teams['away'].get('logo')
            )
            
            # Get or create match
            match = Match.query.filter_by(api_id=fixture['id']).first()
            
            if not match:
                match = Match(
                    api_id=fixture['id'],
                    home_team_id=home_team.id,
                    away_team_id=away_team.id,
                    league=league['name'],
                    season=league['season'],
                    match_date=datetime.fromisoformat(fixture['date'].replace('Z', '+00:00')),
                    status=fixture['status']
                )
                db.session.add(match)
            else:
                match.status = fixture['status']
            
            # Update match stats
            match.home_goals = goals['home']
            match.away_goals = goals['away']
            
            db.session.add(match)
        except Exception as e:
            logger.error(f"Error processing match data: {str(e)}")
    
    def _get_or_create_team(self, api_id: int, name: str, logo_url: Optional[str]) -> Team:
        """Get or create a team in the database."""
        team = Team.query.filter_by(api_id=api_id).first()
        
        if not team:
            team = Team(
                api_id=api_id,
                name=name,
                logo_url=logo_url
            )
            db.session.add(team)
        
        return team
    
    def get_live_matches_with_predictions(self) -> list:
        """Get all live matches with their predictions."""
        try:
            matches = Match.query.filter(
                Match.status.in_(['LIVE', 'SCHEDULED'])
            ).all()
            
            result = []
            for match in matches:
                match_dict = match.to_dict()
                
                # Get associated prediction
                prediction = Prediction.query.filter_by(match_id=match.id).first()
                if prediction:
                    match_dict['prediction'] = prediction.to_dict()
                
                result.append(match_dict)
            
            return result
        except Exception as e:
            logger.error(f"Error fetching live matches: {str(e)}")
            return []
