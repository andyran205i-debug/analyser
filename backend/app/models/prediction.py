from app import db
from datetime import datetime

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    
    # Match Outcome Prediction
    outcome_prediction = db.Column(db.String(10))  # 'HOME', 'DRAW', 'AWAY'
    outcome_confidence = db.Column(db.Float)
    
    # Goal Prediction
    total_goals_prediction = db.Column(db.Float)
    over_under_2_5 = db.Column(db.String(10))  # 'OVER', 'UNDER'
    home_goals_prediction = db.Column(db.Float)
    away_goals_prediction = db.Column(db.Float)
    
    # Corner Prediction
    total_corners_prediction = db.Column(db.Float)
    over_under_corners_8_5 = db.Column(db.String(10))
    
    # Card Prediction
    total_cards_prediction = db.Column(db.Float)
    
    # Confidence & Accuracy
    model_version = db.Column(db.String(50))
    accuracy_score = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'match_id': self.match_id,
            'outcome': {
                'prediction': self.outcome_prediction,
                'confidence': self.outcome_confidence
            },
            'goals': {
                'total': self.total_goals_prediction,
                'over_under_2_5': self.over_under_2_5,
                'home': self.home_goals_prediction,
                'away': self.away_goals_prediction
            },
            'corners': {
                'total': self.total_corners_prediction,
                'over_under_8_5': self.over_under_corners_8_5
            },
            'cards': {
                'total': self.total_cards_prediction
            },
            'model_version': self.model_version,
            'accuracy': self.accuracy_score
        }
