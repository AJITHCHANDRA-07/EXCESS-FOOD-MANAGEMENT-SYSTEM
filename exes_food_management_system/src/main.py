# Main application entry point
import os
import sys

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
# Updated model imports
from src.models.models import db, Machine, FoodItem, User, Volunteer, Admin

# Import blueprints
from src.routes.machine_routes import machine_bp
from src.routes.volunteer_routes import volunteer_bp
from src.routes.public_routes import public_bp
# Import the new machine compatibility blueprint
from src.routes.machine_compatibility import machine_compat_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_very_strong_default_secret_key_for_dev')

# Database Configuration - Using SQLite for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exes_food.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register blueprints
app.register_blueprint(machine_bp, url_prefix='/api/machines')
app.register_blueprint(volunteer_bp, url_prefix='/api/volunteer')
app.register_blueprint(public_bp, url_prefix='/api/public')
# Register the new machine compatibility blueprint
app.register_blueprint(machine_compat_bp)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            # Basic API root message if no index.html
            return jsonify({"message": "Welcome to the Exes Food Management System API. Frontend not yet implemented."}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create database tables if they don't exist
    app.run(host='0.0.0.0', port=5000, debug=True)
