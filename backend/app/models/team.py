from app import db
from datetime import datetime

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(10))
    country = db.Column(db.String(100))
    logo_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'api_id': self.api_id,
            'name': self.name,
            'code': self.code,
            'country': self.country,
            'logo_url': self.logo_url
        }
