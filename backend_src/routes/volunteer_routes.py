# Volunteer API Routes

from flask import Blueprint, request, jsonify
from models.models import db, Machine, FoodItem, User # Assuming Volunteer is a User with role 'volunteer'
import datetime
from werkzeug.security import generate_password_hash, check_password_hash # For potential future login

# A simple way to check if user is authenticated as volunteer - replace with proper auth (e.g., JWT)
# For now, we might pass a volunteer_id or assume authentication for simplicity of this initial build.
# This is a placeholder and NOT secure for production.
def is_volunteer(user_id):
    user = User.query.get(user_id)
    return user and user.role == "volunteer"

volunteer_bp = Blueprint("volunteer_bp", __name__, url_prefix="/api/volunteer")

@volunteer_bp.route("/machines_with_expired_food", methods=["GET"])
def get_machines_with_expired_food():
    # In a real app, this would be tied to an authenticated volunteer and potentially their assigned machines
    # For now, showing all machines with any expired food for simplicity
    today = datetime.date.today()
    machines_with_issues = db.session.query(Machine.id, Machine.address_description, db.func.count(FoodItem.id).label("expired_item_count")) \
        .join(FoodItem, Machine.id == FoodItem.machine_id) \
        .filter(FoodItem.expiry_date < today, FoodItem.is_dispensed == False, FoodItem.is_expired_removed == False) \
        .group_by(Machine.id, Machine.address_description) \
        .all()

    if not machines_with_issues:
        return jsonify({"message": "No machines currently have expired food items requiring attention."}), 200

    result = [
        {
            "machine_id": machine.id, 
            "address": machine.address_description, 
            "expired_item_count": machine.expired_item_count
        } for machine in machines_with_issues
    ]
    return jsonify(result), 200

@volunteer_bp.route("/machine/<int:machine_id>/expired_items", methods=["GET"])
def get_expired_items_in_machine(machine_id):
    # volunteer_user_id = request.headers.get("X-Volunteer-ID") # Example of getting volunteer ID, NOT SECURE
    # if not volunteer_user_id or not is_volunteer(int(volunteer_user_id)):
    #     return jsonify({"error": "Unauthorized or invalid volunteer ID"}), 401
        
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({"error": "Machine not found"}), 404

    today = datetime.date.today()
    expired_items = FoodItem.query.filter(
        FoodItem.machine_id == machine_id,
        FoodItem.expiry_date < today,
        FoodItem.is_dispensed == False,
        FoodItem.is_expired_removed == False
    ).all()

    if not expired_items:
        return jsonify({"message": "No expired items to remove in this machine."}), 200

    result = [
        {
            "food_item_id": item.id,
            "expiry_date": item.expiry_date.isoformat(),
            "donated_at": item.donated_at.isoformat()
        } for item in expired_items
    ]
    return jsonify(result), 200

@volunteer_bp.route("/food_item/<int:food_item_id>/mark_removed", methods=["POST"])
def mark_food_item_removed(food_item_id):
    volunteer_user_id = request.json.get("volunteer_id") # Example: volunteer ID from request body
    if not volunteer_user_id:
         return jsonify({"error": "Volunteer ID is required"}), 400
    
    volunteer = User.query.filter_by(id=volunteer_user_id, role="volunteer").first()
    if not volunteer:
        return jsonify({"error": "Unauthorized or invalid volunteer ID"}), 401

    food_item = FoodItem.query.get(food_item_id)
    if not food_item:
        return jsonify({"error": "Food item not found"}), 404
    
    if food_item.is_dispensed:
        return jsonify({"error": "Food item has already been dispensed"}), 400
    
    if food_item.is_expired_removed:
        return jsonify({"error": "Food item has already been marked as removed"}), 400
    
    # Optional: Check if food is actually expired, or allow removal of non-expired too by volunteers
    # today = datetime.date.today()
    # if food_item.expiry_date >= today:
    #     return jsonify({"error": "Food item is not yet expired"}), 400

    machine = Machine.query.get(food_item.machine_id)
    if not machine:
        # This should ideally not happen if data integrity is maintained
        return jsonify({"error": "Associated machine not found"}), 500

    food_item.is_expired_removed = True
    food_item.expired_removed_at = datetime.datetime.utcnow()
    food_item.expired_removed_by_volunteer_id = volunteer.id
    
    # Adjust machine's current storage level
    machine.current_storage_level -= food_item.quantity # Assuming quantity is 1 per item
    if machine.current_storage_level < 0:
        machine.current_storage_level = 0
        
    db.session.commit()
    return jsonify({"message": f"Food item {food_item_id} marked as removed by volunteer {volunteer.username}", "new_storage_level": machine.current_storage_level}), 200
