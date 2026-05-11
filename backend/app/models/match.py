from app import db
from datetime import datetime

class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, unique=True, nullable=False)
    
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    
    league = db.Column(db.String(150), nullable=False)
    season = db.Column(db.Integer)
    
    match_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20))  # 'SCHEDULED', 'LIVE', 'FINISHED', 'POSTPONED'
    
    home_goals = db.Column(db.Integer)
    away_goals = db.Column(db.Integer)
    
    home_corners = db.Column(db.Integer)
    away_corners = db.Column(db.Integer)
    
    home_cards = db.Column(db.Integer)
    away_cards = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    predictions = db.relationship('Prediction', backref='match', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'api_id': self.api_id,
            'home_team_id': self.home_team_id,
            'away_team_id': self.away_team_id,
            'league': self.league,
            'match_date': self.match_date.isoformat(),
            'status': self.status,
            'home_goals': self.home_goals,
            'away_goals': self.away_goals,
            'home_corners': self.home_corners,
            'away_corners': self.away_corners,
            'home_cards': self.home_cards,
            'away_cards': self.away_cards
        }
