from flask import Blueprint
from app.routes import matches, predictions, health

api_bp = Blueprint('api', __name__)

# Register routes
api_bp.register_blueprint(matches.bp)
api_bp.register_blueprint(predictions.bp)
api_bp.register_blueprint(health.bp)
