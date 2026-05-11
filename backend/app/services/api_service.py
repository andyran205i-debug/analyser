import requests
from app.config import Config
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class APIService:
    """Service for handling external API calls to API-FOOTBALL."""
    
    def __init__(self):
        self.api_football_key = Config.API_FOOTBALL_KEY
        self.api_football_url = 'https://api-football-v3.p.rapidapi.com'
        self.host = 'api-football-v3.p.rapidapi.com'
    
    def _get_headers(self) -> Dict[str, str]:
        """Get standard headers for API requests."""
        return {
            'x-rapidapi-key': self.api_football_key,
            'x-rapidapi-host': self.host
        }
    
    def is_api_key_valid(self) -> bool:
        """Check if API key is valid by making a simple request."""
        try:
            response = requests.get(
                f'{self.api_football_url}/status',
                headers=self._get_headers(),
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"API key validation error: {str(e)}")
            return False
    
    # ============================================
    # LIVE MATCHES
    # ============================================
    
    def get_live_matches(self) -> Optional[Dict]:
        """Fetch all currently live matches from API-FOOTBALL."""
        try:
            response = requests.get(
                f'{self.api_football_url}/fixtures',
                params={'live': 'all'},
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Live matches API error: {str(e)}")
            return None
    
    # ============================================
    # SCHEDULED MATCHES
    # ============================================
    
    def get_scheduled_matches(self, days_ahead: int = 7) -> Optional[Dict]:
        """Fetch scheduled matches for the next N days."""
        try:
            from_date = datetime.utcnow().strftime('%Y-%m-%d')
            to_date = (datetime.utcnow() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
            
            response = requests.get(
                f'{self.api_football_url}/fixtures',
                params={
                    'status': 'NS',  # Not Started
                    'from': from_date,
                    'to': to_date
                },
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Scheduled matches API error: {str(e)}")
            return None
    
    # ============================================
    # LEAGUE FIXTURES
    # ============================================
    
    def get_fixtures_by_league(self, league_id: int, season: int) -> Optional[Dict]:
        """Fetch all fixtures for a specific league and season."""
        try:
            response = requests.get(
                f'{self.api_football_url}/fixtures',
                params={
                    'league': league_id,
                    'season': season
                },
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"League fixtures API error: {str(e)}")
            return None
    
    # ============================================
    # MATCH DETAILS & STATISTICS
    # ============================================
    
    def get_match_predictions(self, fixture_id: int) -> Optional[Dict]:
        """Fetch AI predictions for a specific match from API-FOOTBALL."""
        try:
            response = requests.get(
                f'{self.api_football_url}/predictions',
                params={'fixture': fixture_id},
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Predictions API error: {str(e)}")
            return None
    
    def get_match_statistics(self, fixture_id: int) -> Optional[Dict]:
        """Fetch detailed statistics for a specific match."""
        try:
            response = requests.get(
                f'{self.api_football_url}/fixtures/statistics',
                params={'fixture': fixture_id},
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Statistics API error: {str(e)}")
            return None
    
    def get_match_events(self, fixture_id: int) -> Optional[Dict]:
        """Fetch all events (goals, cards, corners) for a match."""
        try:
            response = requests.get(
                f'{self.api_football_url}/fixtures/events',
                params={'fixture': fixture_id},
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Match events API error: {str(e)}")
            return None
    
    def get_match_lineups(self, fixture_id: int) -> Optional[Dict]:
        """Fetch team lineups for a match."""
        try:
            response = requests.get(
                f'{self.api_football_url}/fixtures/lineups',
                params={'fixture': fixture_id},
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Lineups API error: {str(e)}")
            return None
    
    def get_fixture_details(self, fixture_id: int) -> Optional[Dict]:
        """Fetch complete details for a specific fixture."""
        try:
            response = requests.get(
                f'{self.api_football_url}/fixtures',
                params={'id': fixture_id},
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Fixture details API error: {str(e)}")
            return None
    
    # ============================================
    # TEAM DATA
    # ============================================
    
    def get_team_info(self, team_id: int) -> Optional[Dict]:
        """Fetch detailed information about a team."""
        try:
            response = requests.get(
                f'{self.api_football_url}/teams',
                params={'id': team_id},
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Team info API error: {str(e)}")
            return None
    
    def get_team_form(self, team_id: int, last_n: int = 5) -> Optional[Dict]:
        """Fetch recent form data for a team (last N matches)."""
        try:
            response = requests.get(
                f'{self.api_football_url}/fixtures',
                params={
                    'team': team_id,
                    'last': last_n
                },
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Team form API error: {str(e)}")
            return None
    
    def get_team_statistics(self, team_id: int, season: int) -> Optional[Dict]:
        """Fetch statistics for a team in a specific season."""
        try:
            response = requests.get(
                f'{self.api_football_url}/teams/statistics',
                params={
                    'team': team_id,
                    'season': season
                },
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Team statistics API error: {str(e)}")
            return None
    
    # ============================================
    # HEAD-TO-HEAD
    # ============================================
    
    def get_head_to_head(self, home_team_id: int, away_team_id: int, last_n: int = 5) -> Optional[Dict]:
        """Fetch head-to-head history between two teams."""
        try:
            response = requests.get(
                f'{self.api_football_url}/fixtures/headtohead',
                params={
                    'h2h': f'{home_team_id}-{away_team_id}',
                    'last': last_n
                },
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"H2H API error: {str(e)}")
            return None
    
    # ============================================
    # LEAGUE DATA
    # ============================================
    
    def get_league_standings(self, league_id: int, season: int) -> Optional[Dict]:
        """Fetch league standings/table for a season."""
        try:
            response = requests.get(
                f'{self.api_football_url}/standings',
                params={
                    'league': league_id,
                    'season': season
                },
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"League standings API error: {str(e)}")
            return None
    
    def get_top_scorers(self, league_id: int, season: int) -> Optional[Dict]:
        """Fetch top scorers in a league."""
        try:
            response = requests.get(
                f'{self.api_football_url}/players/topscorers',
                params={
                    'league': league_id,
                    'season': season
                },
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Top scorers API error: {str(e)}")
            return None
    
    def get_top_assists(self, league_id: int, season: int) -> Optional[Dict]:
        """Fetch top assists providers in a league."""
        try:
            response = requests.get(
                f'{self.api_football_url}/players/topassists',
                params={
                    'league': league_id,
                    'season': season
                },
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Top assists API error: {str(e)}")
            return None
    
    # ============================================
    # PLAYER DATA
    # ============================================
    
    def get_player_info(self, player_id: int) -> Optional[Dict]:
        """Fetch detailed information about a player."""
        try:
            response = requests.get(
                f'{self.api_football_url}/players',
                params={'id': player_id},
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Player info API error: {str(e)}")
            return None
    
    def get_player_statistics(self, player_id: int, season: int) -> Optional[Dict]:
        """Fetch player statistics for a specific season."""
        try:
            response = requests.get(
                f'{self.api_football_url}/players/statistics',
                params={
                    'player': player_id,
                    'season': season
                },
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Player statistics API error: {str(e)}")
            return None
    
    # ============================================
    # ODDS & BETTING
    # ============================================
    
    def get_odds(self, fixture_id: int) -> Optional[Dict]:
        """Fetch betting odds for a match."""
        try:
            response = requests.get(
                f'{self.api_football_url}/odds',
                params={'fixture': fixture_id},
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Odds API error: {str(e)}")
            return None
    
    def get_betting_markets(self) -> Optional[Dict]:
        """Fetch available betting markets."""
        try:
            response = requests.get(
                f'{self.api_football_url}/odds/markets',
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Betting markets API error: {str(e)}")
            return None
