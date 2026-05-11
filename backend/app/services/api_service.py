import requests
from app.config import Config
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class APIService:
    """Service for handling external API calls to football data providers."""
    
    def __init__(self):
        self.api_football_key = Config.API_FOOTBALL_KEY
        self.football_data_key = Config.FOOTBALL_DATA_KEY
        self.api_football_url = 'https://api-football-v3.p.rapidapi.com'
        self.football_data_url = 'https://api.football-data.org/v4'
    
    # API-FOOTBALL Methods
    def get_live_matches_api_football(self) -> Optional[Dict]:
        """Fetch live matches from API-FOOTBALL."""
        headers = {
            'x-rapidapi-key': self.api_football_key,
            'x-rapidapi-host': 'api-football-v3.p.rapidapi.com'
        }
        
        try:
            response = requests.get(
                f'{self.api_football_url}/fixtures',
                params={'live': 'all'},
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API-FOOTBALL error: {str(e)}")
            return None
    
    def get_match_predictions_api_football(self, fixture_id: int) -> Optional[Dict]:
        """Fetch predictions for a specific match from API-FOOTBALL."""
        headers = {
            'x-rapidapi-key': self.api_football_key,
            'x-rapidapi-host': 'api-football-v3.p.rapidapi.com'
        }
        
        try:
            response = requests.get(
                f'{self.api_football_url}/predictions',
                params={'fixture': fixture_id},
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API-FOOTBALL predictions error: {str(e)}")
            return None
    
    def get_match_statistics_api_football(self, fixture_id: int) -> Optional[Dict]:
        """Fetch statistics for a specific match from API-FOOTBALL."""
        headers = {
            'x-rapidapi-key': self.api_football_key,
            'x-rapidapi-host': 'api-football-v3.p.rapidapi.com'
        }
        
        try:
            response = requests.get(
                f'{self.api_football_url}/fixtures/statistics',
                params={'fixture': fixture_id},
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API-FOOTBALL statistics error: {str(e)}")
            return None
    
    # football-data.org Methods
    def get_live_matches_football_data(self) -> Optional[Dict]:
        """Fetch live matches from football-data.org."""
        headers = {'X-Auth-Token': self.football_data_key}
        
        try:
            response = requests.get(
                f'{self.football_data_url}/matches',
                params={'status': 'LIVE'},
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"football-data.org error: {str(e)}")
            return None
    
    def get_match_details_football_data(self, match_id: int) -> Optional[Dict]:
        """Fetch detailed information for a match from football-data.org."""
        headers = {'X-Auth-Token': self.football_data_key}
        
        try:
            response = requests.get(
                f'{self.football_data_url}/matches/{match_id}',
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"football-data.org match details error: {str(e)}")
            return None
