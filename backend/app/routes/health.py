from flask import Blueprint, jsonify

bp = Blueprint('health', __name__, url_prefix='/health')

@bp.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Football Prediction API'
    }), 200
