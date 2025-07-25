# Machine API Routes

from flask import Blueprint, request, jsonify
from ..models.models import db, Machine, FoodItem
import datetime

machine_bp = Blueprint("machine_bp", __name__, url_prefix="/api/machines")

@machine_bp.route("/", methods=["POST"])
def create_machine():
    data = request.get_json()
    if not all(k in data for k in ["location_lat", "location_lon", "storage_capacity_max"]):
        return jsonify({"error": "Missing required fields: location_lat, location_lon, storage_capacity_max"}), 400
    
    new_machine = Machine(
        location_lat=data["location_lat"],
        location_lon=data["location_lon"],
        address_description=data.get("address_description"),
        status=data.get("status", "active"),
        storage_capacity_max=data["storage_capacity_max"],
        current_storage_level=data.get("current_storage_level", 0),
        operational_hours=data.get("operational_hours")
    )
    db.session.add(new_machine)
    db.session.commit()
    return jsonify({"message": "Machine created successfully", "machine_id": new_machine.id}), 201

@machine_bp.route("/<int:machine_id>", methods=["GET"])
def get_machine(machine_id):
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({"error": "Machine not found"}), 404
    
    food_items_data = [
        {
            "id": item.id, 
            "expiry_date": item.expiry_date.isoformat(), 
            "donated_at": item.donated_at.isoformat(),
            "is_dispensed": item.is_dispensed
        } 
        for item in machine.food_items if not item.is_dispensed and not item.is_expired_removed and item.expiry_date >= datetime.date.today()
    ]

    return jsonify({
        "id": machine.id,
        "location_lat": machine.location_lat,
        "location_lon": machine.location_lon,
        "address_description": machine.address_description,
        "status": machine.status,
        "storage_capacity_max": machine.storage_capacity_max,
        "current_storage_level": machine.current_storage_level,
        "available_food_count": len(food_items_data),
        "operational_hours": machine.operational_hours,
        "last_heartbeat": machine.last_heartbeat.isoformat() if machine.last_heartbeat else None
    }), 200

@machine_bp.route("/<int:machine_id>/status", methods=["PUT"])
def update_machine_status(machine_id):
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({"error": "Machine not found"}), 404
    data = request.get_json()
    if "status" in data:
        machine.status = data["status"]
    if "current_storage_level" in data:
        machine.current_storage_level = data["current_storage_level"]
    machine.last_heartbeat = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify({"message": "Machine status updated"}), 200

@machine_bp.route("/<int:machine_id>/heartbeat", methods=["POST"])
def machine_heartbeat(machine_id):
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({"error": "Machine not found"}), 404
    machine.last_heartbeat = datetime.datetime.utcnow()
    # Potentially update storage level from machine report
    data = request.get_json()
    if data and "current_storage_level" in data:
        machine.current_storage_level = data["current_storage_level"]
    db.session.commit()
    return jsonify({"message": "Heartbeat received"}), 200

# Endpoint for machine to report a donation (internal, called by machine hardware)
@machine_bp.route("/<int:machine_id>/report_donation", methods=["POST"])
def report_donation(machine_id):
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({"error": "Machine not found"}), 404
    if machine.status != "active":
        return jsonify({"error": "Machine not active or in maintenance"}), 403
    if machine.current_storage_level >= machine.storage_capacity_max:
        return jsonify({"error": "Machine storage is full"}), 403

    data = request.get_json()
    if not data or "expiry_date" not in data or "quantity" not in data:
        return jsonify({"error": "Missing expiry_date or quantity"}), 400
    
    try:
        expiry_date = datetime.datetime.strptime(data["expiry_date"], "%Y-%m-%d").date()
        quantity = int(data["quantity"])
    except ValueError:
        return jsonify({"error": "Invalid date format (YYYY-MM-DD) or quantity"}), 400

    if expiry_date < datetime.date.today():
        return jsonify({"error": "Cannot donate expired food"}), 400

    for _ in range(quantity):
        if machine.current_storage_level < machine.storage_capacity_max:
            new_food_item = FoodItem(
                machine_id=machine_id,
                expiry_date=expiry_date,
                quantity=1 # Assuming 1 item per entry for easier tracking
            )
            db.session.add(new_food_item)
            machine.current_storage_level += 1
        else:
            db.session.rollback() # Rollback if partial donation leads to overflow
            return jsonify({"error": "Machine became full during donation process"}), 507 # Insufficient Storage
    
    db.session.commit()
    return jsonify({"message": "Donation reported successfully", "new_storage_level": machine.current_storage_level}), 200

# Endpoint for machine to report food dispensing (internal, called by machine hardware)
@machine_bp.route("/<int:machine_id>/dispense_food", methods=["POST"])
def dispense_food(machine_id):
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({"error": "Machine not found"}), 404
    if machine.status != "active":
        return jsonify({"error": "Machine not active or in maintenance"}), 403

    # Find the soonest-to-expire, non-dispensed, non-expired food item
    food_to_dispense = FoodItem.query.filter(
        FoodItem.machine_id == machine_id,
        FoodItem.is_dispensed == False,
        FoodItem.is_expired_removed == False,
        FoodItem.expiry_date >= datetime.date.today()
    ).order_by(FoodItem.expiry_date.asc()).first()

    if not food_to_dispense:
        return jsonify({"error": "No suitable food available for dispensing"}), 404

    food_to_dispense.is_dispensed = True
    food_to_dispense.dispensed_at = datetime.datetime.utcnow()
    machine.current_storage_level -= food_to_dispense.quantity # Should be 1 if we stick to 1 item per entry
    if machine.current_storage_level < 0: machine.current_storage_level = 0 # Safety check
    
    db.session.commit()
    return jsonify({"message": "Food dispensed successfully", "item_id": food_to_dispense.id, "new_storage_level": machine.current_storage_level}), 200

