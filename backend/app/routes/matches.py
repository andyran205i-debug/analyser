from flask import Blueprint, jsonify
from app.services import DataService
from app import db
from app.models import Match

bp = Blueprint('matches', __name__, url_prefix='/matches')
data_service = DataService()

@bp.route('/live', methods=['GET'])
def get_live_matches():
    """Get all live matches with predictions."""
    try:
        matches = data_service.get_live_matches_with_predictions()
        return jsonify({
            'status': 'success',
            'data': matches
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/sync', methods=['POST'])
def sync_matches():
    """Manually trigger sync of live matches."""
    try:
        success = data_service.sync_live_matches()
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Matches synced successfully'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to sync matches'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """Get a specific match with its details."""
    try:
        match = Match.query.get(match_id)
        if not match:
            return jsonify({
                'status': 'error',
                'message': 'Match not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': match.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
