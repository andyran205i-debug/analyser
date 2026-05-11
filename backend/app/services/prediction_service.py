import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class PredictionService:
    """Service for generating match predictions using ML models."""
    
    def __init__(self):
        self.outcome_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.goals_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.corners_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.cards_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train_models(self, training_data: pd.DataFrame) -> bool:
        """Train all prediction models on historical data."""
        try:
            # Prepare features
            X = training_data[[
                'home_team_strength',
                'away_team_strength',
                'home_form',
                'away_form',
                'head_to_head',
                'home_possession',
                'away_possession'
            ]].fillna(0)
            
            X_scaled = self.scaler.fit_transform(X)
            
            # Train outcome model (Win/Draw/Loss)
            y_outcome = training_data['outcome']
            self.outcome_model.fit(X_scaled, y_outcome)
            
            # Train goals model
            y_goals = training_data['total_goals']
            self.goals_model.fit(X_scaled, y_goals)
            
            # Train corners model
            y_corners = training_data['total_corners']
            self.corners_model.fit(X_scaled, y_corners)
            
            # Train cards model
            y_cards = training_data['total_cards']
            self.cards_model.fit(X_scaled, y_cards)
            
            self.is_trained = True
            logger.info("Models trained successfully")
            return True
        except Exception as e:
            logger.error(f"Model training error: {str(e)}")
            return False
    
    def predict_match_outcome(self, features: Dict) -> Tuple[str, float]:
        """Predict match outcome (HOME, DRAW, AWAY) with confidence."""
        try:
            X = np.array([[
                features['home_team_strength'],
                features['away_team_strength'],
                features['home_form'],
                features['away_form'],
                features['head_to_head'],
                features['home_possession'],
                features['away_possession']
            ]])
            
            X_scaled = self.scaler.transform(X)
            
            prediction = self.outcome_model.predict(X_scaled)[0]
            probabilities = self.outcome_model.predict_proba(X_scaled)[0]
            confidence = float(np.max(probabilities))
            
            outcome_map = {0: 'AWAY', 1: 'DRAW', 2: 'HOME'}
            return outcome_map.get(prediction, 'UNKNOWN'), confidence
        except Exception as e:
            logger.error(f"Outcome prediction error: {str(e)}")
            return 'UNKNOWN', 0.0
    
    def predict_goals(self, features: Dict) -> Dict[str, float]:
        """Predict total goals and over/under odds."""
        try:
            X = np.array([[
                features['home_team_strength'],
                features['away_team_strength'],
                features['home_form'],
                features['away_form'],
                features['head_to_head'],
                features['home_possession'],
                features['away_possession']
            ]])
            
            X_scaled = self.scaler.transform(X)
            total_goals = float(self.goals_model.predict(X_scaled)[0])
            
            return {
                'total': max(0, total_goals),
                'over_under_2_5': 'OVER' if total_goals > 2.5 else 'UNDER',
                'home': max(0, total_goals * 0.4),  # Heuristic split
                'away': max(0, total_goals * 0.6)   # Heuristic split
            }
        except Exception as e:
            logger.error(f"Goals prediction error: {str(e)}")
            return {'total': 0, 'over_under_2_5': 'UNKNOWN', 'home': 0, 'away': 0}
    
    def predict_corners(self, features: Dict) -> Dict[str, float]:
        """Predict total corners."""
        try:
            X = np.array([[
                features['home_team_strength'],
                features['away_team_strength'],
                features['home_form'],
                features['away_form'],
                features['head_to_head'],
                features['home_possession'],
                features['away_possession']
            ]])
            
            X_scaled = self.scaler.transform(X)
            total_corners = float(self.corners_model.predict(X_scaled)[0])
            
            return {
                'total': max(0, total_corners),
                'over_under_8_5': 'OVER' if total_corners > 8.5 else 'UNDER'
            }
        except Exception as e:
            logger.error(f"Corners prediction error: {str(e)}")
            return {'total': 0, 'over_under_8_5': 'UNKNOWN'}
    
    def predict_cards(self, features: Dict) -> Dict[str, float]:
        """Predict total cards."""
        try:
            X = np.array([[
                features['home_team_strength'],
                features['away_team_strength'],
                features['home_form'],
                features['away_form'],
                features['head_to_head'],
                features['home_possession'],
                features['away_possession']
            ]])
            
            X_scaled = self.scaler.transform(X)
            total_cards = float(self.cards_model.predict(X_scaled)[0])
            
            return {'total': max(0, total_cards)}
        except Exception as e:
            logger.error(f"Cards prediction error: {str(e)}")
            return {'total': 0}
