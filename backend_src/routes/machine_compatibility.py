"""
Machine Compatibility API Routes

This module provides compatibility endpoints for the machine software to connect with the backend.
It adapts the machine client's expected endpoints to the actual backend implementation.
"""

from flask import Blueprint, request, jsonify
from models.models import db, Machine, FoodItem
import datetime
import secrets
import jwt
from functools import wraps

# Create blueprint with the prefix expected by machine client
machine_compat_bp = Blueprint("machine_compat_bp", __name__, url_prefix="/api")

# Secret key for JWT token generation
JWT_SECRET = secrets.token_hex(32)  # In production, this should be in environment variables

# Dictionary to store machine tokens
machine_tokens = {}

# Token verification decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            machine_id = data['machine_id']
            
            # Verify machine exists
            machine = Machine.query.get(machine_id)
            if not machine:
                return jsonify({'error': 'Invalid machine'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
            
        return f(machine_id, *args, **kwargs)
    
    return decorated

# Machine authentication endpoint
@machine_compat_bp.route("/machine/auth", methods=["POST"])
def machine_auth():
    """Authenticate a machine and provide a JWT token."""
    data = request.get_json()
    
    if not data or 'machine_id' not in data:
        return jsonify({'error': 'Machine ID is required'}), 400
    
    machine_id = data['machine_id']
    
    # Check if machine exists in database
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({'error': 'Machine not found'}), 404
    
    # Generate JWT token
    token = jwt.encode(
        {
            'machine_id': machine_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        },
        JWT_SECRET,
        algorithm="HS256"
    )
    
    # Store token
    machine_tokens[machine_id] = token
    
    return jsonify({'token': token}), 200

# Machine registration endpoint
@machine_compat_bp.route("/machine/register", methods=["POST"])
def register_machine():
    """Register a new machine or update existing machine information."""
    data = request.get_json()
    
    if not data or 'machine_id' not in data:
        return jsonify({'error': 'Machine ID is required'}), 400
    
    machine_id = data['machine_id']
    
    # Check if machine already exists
    machine = Machine.query.get(machine_id)
    
    if machine:
        # Update existing machine
        if 'location_lat' in data:
            machine.location_lat = data['location_lat']
        if 'location_lon' in data:
            machine.location_lon = data['location_lon']
        if 'address_description' in data:
            machine.address_description = data['address_description']
        if 'operational_hours' in data:
            machine.operational_hours = data['operational_hours']
        
        db.session.commit()
        return jsonify({'message': 'Machine updated successfully'}), 200
    else:
        # Create new machine
        new_machine = Machine(
            id=machine_id,
            location_lat=data.get('location_lat', 0),
            location_lon=data.get('location_lon', 0),
            address_description=data.get('address_description', ''),
            status='active',
            storage_capacity_max=100,  # Default value
            current_storage_level=0,
            operational_hours=data.get('operational_hours', '24/7')
        )
        
        db.session.add(new_machine)
        db.session.commit()
        return jsonify({'message': 'Machine registered successfully'}), 201

# Machine status update endpoint
@machine_compat_bp.route("/machine/status", methods=["POST"])
@token_required
def update_status(machine_id):
    """Update machine status information."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({'error': 'Machine not found'}), 404
    
    # Update machine status
    if 'available_space' in data:
        machine.current_storage_level = data['available_space']
    
    if 'error_code' in data and data['error_code']:
        machine.status = 'maintenance'
    else:
        machine.status = 'active'
    
    machine.last_heartbeat = datetime.datetime.utcnow()
    
    db.session.commit()
    return jsonify({'message': 'Machine status updated successfully'}), 200

# Food donation endpoint
@machine_compat_bp.route("/food/donate", methods=["POST"])
@token_required
def donate_food(machine_id):
    """Report a new food donation."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({'error': 'Machine not found'}), 404
    
    if machine.status != 'active':
        return jsonify({'error': 'Machine not active'}), 403
    
    if machine.current_storage_level >= machine.storage_capacity_max:
        return jsonify({'error': 'Machine storage is full'}), 403
    
    # Process donation
    try:
        expiry_date = datetime.datetime.strptime(data.get('expiry_date', ''), "%Y-%m-%d").date()
        quantity = int(data.get('quantity', 1))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid expiry date or quantity'}), 400
    
    if expiry_date < datetime.date.today():
        return jsonify({'error': 'Cannot donate expired food'}), 400
    
    # Add food items
    for _ in range(quantity):
        if machine.current_storage_level < machine.storage_capacity_max:
            new_food_item = FoodItem(
                machine_id=machine_id,
                expiry_date=expiry_date,
                quantity=1  # Assuming 1 item per entry for easier tracking
            )
            db.session.add(new_food_item)
            machine.current_storage_level += 1
        else:
            db.session.rollback()
            return jsonify({'error': 'Machine became full during donation process'}), 507
    
    db.session.commit()
    return jsonify({
        'message': 'Donation reported successfully',
        'new_storage_level': machine.current_storage_level
    }), 200

# Food collection endpoint
@machine_compat_bp.route("/food/collect", methods=["POST"])
@token_required
def collect_food(machine_id):
    """Report a food collection."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({'error': 'Machine not found'}), 404
    
    if machine.status != 'active':
        return jsonify({'error': 'Machine not active'}), 403
    
    # Find food items to dispense
    quantity = int(data.get('quantity', 1))
    dispensed_items = []
    
    for _ in range(quantity):
        # Find the soonest-to-expire, non-dispensed, non-expired food item
        food_to_dispense = FoodItem.query.filter(
            FoodItem.machine_id == machine_id,
            FoodItem.is_dispensed == False,
            FoodItem.is_expired_removed == False,
            FoodItem.expiry_date >= datetime.date.today()
        ).order_by(FoodItem.expiry_date.asc()).first()
        
        if not food_to_dispense:
            break
        
        food_to_dispense.is_dispensed = True
        food_to_dispense.dispensed_at = datetime.datetime.utcnow()
        machine.current_storage_level -= food_to_dispense.quantity
        dispensed_items.append(food_to_dispense.id)
    
    if not dispensed_items:
        return jsonify({'error': 'No suitable food available for dispensing'}), 404
    
    if machine.current_storage_level < 0:
        machine.current_storage_level = 0  # Safety check
    
    db.session.commit()
    return jsonify({
        'message': 'Food collected successfully',
        'items_dispensed': dispensed_items,
        'new_storage_level': machine.current_storage_level
    }), 200

# Food sync endpoint
@machine_compat_bp.route("/food/sync", methods=["POST"])
@token_required
def sync_food(machine_id):
    """Sync food items between machine and backend."""
    data = request.get_json()
    
    if not data or 'items' not in data:
        return jsonify({'error': 'No items provided'}), 400
    
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({'error': 'Machine not found'}), 404
    
    items = data['items']
    synced_items = []
    
    # Process each item
    for item in items:
        item_id = item.get('id')
        
        # Check if item exists
        food_item = FoodItem.query.get(item_id) if item_id else None
        
        if food_item:
            # Update existing item
            if 'is_dispensed' in item:
                food_item.is_dispensed = item['is_dispensed']
            if 'is_expired_removed' in item:
                food_item.is_expired_removed = item['is_expired_removed']
            synced_items.append(food_item.id)
        else:
            # Create new item
            try:
                expiry_date = datetime.datetime.strptime(item.get('expiry_date', ''), "%Y-%m-%d").date()
            except ValueError:
                continue
                
            new_food_item = FoodItem(
                machine_id=machine_id,
                expiry_date=expiry_date,
                quantity=item.get('quantity', 1),
                is_dispensed=item.get('is_dispensed', False),
                is_expired_removed=item.get('is_expired_removed', False)
            )
            db.session.add(new_food_item)
            synced_items.append('new')
    
    # Update machine storage level
    active_items = FoodItem.query.filter(
        FoodItem.machine_id == machine_id,
        FoodItem.is_dispensed == False,
        FoodItem.is_expired_removed == False
    ).count()
    
    machine.current_storage_level = active_items
    db.session.commit()
    
    return jsonify({
        'message': 'Food items synced successfully',
        'synced_items': len(synced_items),
        'current_storage_level': machine.current_storage_level
    }), 200

# Expired food removal endpoint
@machine_compat_bp.route("/maintenance/expired", methods=["POST"])
@token_required
def remove_expired(machine_id):
    """Report removal of expired food items."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({'error': 'Machine not found'}), 404
    
    food_item_ids = data.get('food_item_ids', [])
    removed_count = 0
    
    # Mark items as expired and removed
    for item_id in food_item_ids:
        food_item = FoodItem.query.get(item_id)
        if food_item and food_item.machine_id == machine_id:
            food_item.is_expired_removed = True
            removed_count += 1
    
    # Update machine storage level
    active_items = FoodItem.query.filter(
        FoodItem.machine_id == machine_id,
        FoodItem.is_dispensed == False,
        FoodItem.is_expired_removed == False
    ).count()
    
    machine.current_storage_level = active_items
    db.session.commit()
    
    return jsonify({
        'message': 'Expired items removed successfully',
        'removed_count': removed_count,
        'current_storage_level': machine.current_storage_level
    }), 200

# Alert reporting endpoint
@machine_compat_bp.route("/maintenance/alert", methods=["POST"])
@token_required
def report_alert(machine_id):
    """Report a machine alert or issue."""
    data = request.get_json()
    
    if not data or 'alert_type' not in data:
        return jsonify({'error': 'Alert type is required'}), 400
    
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({'error': 'Machine not found'}), 404
    
    # In a real implementation, we would store this alert in a dedicated alerts table
    # For now, we'll just update the machine status if it's a critical alert
    
    severity = data.get('severity', 'info')
    if severity in ['critical', 'high']:
        machine.status = 'maintenance'
        db.session.commit()
    
    return jsonify({
        'message': 'Alert reported successfully',
        'alert_type': data.get('alert_type'),
        'severity': severity
    }), 200

# Nearest machines endpoint
@machine_compat_bp.route("/location/nearest", methods=["GET"])
def get_nearest_machines():
    """Get nearest machines to a location."""
    try:
        lat = float(request.args.get('lat', 0))
        lon = float(request.args.get('lon', 0))
    except ValueError:
        return jsonify({'error': 'Invalid coordinates'}), 400
    
    filter_type = request.args.get('filter')
    
    # Get all active machines
    machines = Machine.query.filter(Machine.status == 'active').all()
    
    # Calculate distances and filter
    machine_data = []
    for machine in machines:
        # In a real implementation, we would use a proper distance calculation
        # For now, we'll use a simple approximation
        distance = ((machine.location_lat - lat) ** 2 + (machine.location_lon - lon) ** 2) ** 0.5
        
        # Count available food items
        available_food = FoodItem.query.filter(
            FoodItem.machine_id == machine.id,
            FoodItem.is_dispensed == False,
            FoodItem.is_expired_removed == False,
            FoodItem.expiry_date >= datetime.date.today()
        ).count()
        
        # Calculate available space
        available_space = machine.storage_capacity_max - machine.current_storage_level
        
        # Apply filter
        if filter_type == 'donor' and available_space <= 0:
            continue
        if filter_type == 'receiver' and available_food <= 0:
            continue
        
        machine_data.append({
            'id': machine.id,
            'location_lat': machine.location_lat,
            'location_lon': machine.location_lon,
            'address_description': machine.address_description,
            'distance': distance,
            'available_space': available_space,
            'available_food': available_food,
            'operational_hours': machine.operational_hours
        })
    
    # Sort by distance
    machine_data.sort(key=lambda x: x['distance'])
    
    return jsonify(machine_data), 200

# Machine configuration endpoints
# Fixed: Removed the machine_id parameter from the route since it's already provided by the token_required decorator
@machine_compat_bp.route("/machine/config", methods=["GET"])
@token_required
def get_config(machine_id):
    """Get machine configuration."""
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({'error': 'Machine not found'}), 404
    
    # In a real implementation, we would have a dedicated configuration table
    # For now, we'll return some basic configuration
    
    config = {
        'max_donation_quantity': 10,
        'max_collection_quantity': 2,
        'min_expiry_days': 1,
        'maintenance_schedule': 'weekly',
        'ui_theme': 'default',
        'operational_hours': machine.operational_hours
    }
    
    return jsonify(config), 200

@machine_compat_bp.route("/machine/config", methods=["PUT"])
@token_required
def update_config(machine_id):
    """Update machine configuration."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({'error': 'Machine not found'}), 404
    
    # In a real implementation, we would update a dedicated configuration table
    # For now, we'll just update the operational hours
    
    if 'operational_hours' in data:
        machine.operational_hours = data['operational_hours']
        db.session.commit()
    
    return jsonify({'message': 'Configuration updated successfully'}), 200
