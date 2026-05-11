from flask import Blueprint, jsonify, request
from app.services import PredictionService
from app import db
from app.models import Prediction, Match

bp = Blueprint('predictions', __name__, url_prefix='/predictions')
prediction_service = PredictionService()

@bp.route('/match/<int:match_id>', methods=['GET'])
def get_match_prediction(match_id):
    """Get prediction for a specific match."""
    try:
        prediction = Prediction.query.filter_by(match_id=match_id).first()
        
        if not prediction:
            return jsonify({
                'status': 'error',
                'message': 'Prediction not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': prediction.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/generate/<int:match_id>', methods=['POST'])
def generate_prediction(match_id):
    """Generate prediction for a specific match."""
    try:
        match = Match.query.get(match_id)
        if not match:
            return jsonify({
                'status': 'error',
                'message': 'Match not found'
            }), 404
        
        # Get features from request or use defaults
        data = request.get_json() or {}
        features = {
            'home_team_strength': data.get('home_team_strength', 0.7),
            'away_team_strength': data.get('away_team_strength', 0.65),
            'home_form': data.get('home_form', 0.6),
            'away_form': data.get('away_form', 0.55),
            'head_to_head': data.get('head_to_head', 0.5),
            'home_possession': data.get('home_possession', 0.55),
            'away_possession': data.get('away_possession', 0.45)
        }
        
        # Generate predictions
        outcome, confidence = prediction_service.predict_match_outcome(features)
        goals = prediction_service.predict_goals(features)
        corners = prediction_service.predict_corners(features)
        cards = prediction_service.predict_cards(features)
        
        # Store prediction in database
        prediction = Prediction.query.filter_by(match_id=match_id).first()
        if not prediction:
            prediction = Prediction(match_id=match_id)
        
        prediction.outcome_prediction = outcome
        prediction.outcome_confidence = confidence
        prediction.total_goals_prediction = goals['total']
        prediction.over_under_2_5 = goals['over_under_2_5']
        prediction.home_goals_prediction = goals['home']
        prediction.away_goals_prediction = goals['away']
        prediction.total_corners_prediction = corners['total']
        prediction.over_under_corners_8_5 = corners['over_under_8_5']
        prediction.total_cards_prediction = cards['total']
        
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'data': prediction.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
