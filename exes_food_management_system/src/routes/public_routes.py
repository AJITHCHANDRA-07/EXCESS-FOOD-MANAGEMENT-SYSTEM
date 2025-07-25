# Public API Routes (for website locator, etc.)

from flask import Blueprint, request, jsonify
from ..models.models import db, Machine, FoodItem
import datetime

public_bp = Blueprint("public_bp", __name__, url_prefix="/api/public")

@public_bp.route("/machines_for_donors", methods=["GET"])
def get_machines_for_donors():
    # Find machines that are active and have available storage space
    machines = Machine.query.filter(
        Machine.status == "active",
        Machine.current_storage_level < Machine.storage_capacity_max
    ).all()

    if not machines:
        return jsonify({"message": "No machines currently have available space for donations."}), 404

    result = [
        {
            "id": machine.id,
            "location_lat": machine.location_lat,
            "location_lon": machine.location_lon,
            "address_description": machine.address_description,
            "available_space": machine.storage_capacity_max - machine.current_storage_level,
            "operational_hours": machine.operational_hours
        } for machine in machines
    ]
    return jsonify(result), 200

@public_bp.route("/machines_for_receivers", methods=["GET"])
def get_machines_for_receivers():
    # Find machines that are active and have available, non-expired food
    today = datetime.date.today()
    
    # Subquery to count available food items per machine
    available_food_subquery = db.session.query(
        FoodItem.machine_id,
        db.func.count(FoodItem.id).label("available_items_count")
    ).filter(
        FoodItem.is_dispensed == False,
        FoodItem.is_expired_removed == False,
        FoodItem.expiry_date >= today
    ).group_by(FoodItem.machine_id).subquery()

    machines = db.session.query(Machine).join(
        available_food_subquery, Machine.id == available_food_subquery.c.machine_id
    ).filter(Machine.status == "active").all()

    if not machines:
        return jsonify({"message": "No machines currently have food available for dispensing."}), 404

    result = []
    for machine in machines:
        # Re-fetch the count for this specific machine to be sure (or use the subquery result directly if possible with alias)
        food_count = FoodItem.query.filter(
            FoodItem.machine_id == machine.id,
            FoodItem.is_dispensed == False,
            FoodItem.is_expired_removed == False,
            FoodItem.expiry_date >= today
        ).count()

        if food_count > 0:
            result.append({
                "id": machine.id,
                "location_lat": machine.location_lat,
                "location_lon": machine.location_lon,
                "address_description": machine.address_description,
                "available_food_items": food_count,
                "operational_hours": machine.operational_hours
            })

    if not result:
         return jsonify({"message": "No machines currently have food available for dispensing."}), 404

    return jsonify(result), 200

