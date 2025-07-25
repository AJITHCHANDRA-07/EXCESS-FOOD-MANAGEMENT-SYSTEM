# Database Models for Exes Food Management System

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Machine(db.Model):
    __tablename__ = "machines"
    id = db.Column(db.Integer, primary_key=True)
    location_lat = db.Column(db.Float, nullable=False)
    location_lon = db.Column(db.Float, nullable=False)
    address_description = db.Column(db.String(255), nullable=True) # e.g., "Corner of Main St and Park Ave"
    status = db.Column(db.String(50), nullable=False, default="active") # e.g., active, inactive, maintenance
    storage_capacity_max = db.Column(db.Integer, nullable=False, default=100) # Max units of food
    current_storage_level = db.Column(db.Integer, nullable=False, default=0) # Current units of food
    last_heartbeat = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    operational_hours = db.Column(db.String(100), nullable=True) # e.g., "24/7" or "9am-5pm Mon-Fri"

    food_items = db.relationship("FoodItem", backref="machine", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Machine {self.id} at ({self.location_lat}, {self.location_lon})>"

class FoodItem(db.Model):
    __tablename__ = "food_items"
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey("machines.id"), nullable=False)
    # food_type = db.Column(db.String(100), nullable=False) # e.g., canned goods, bread, fruit - decided against for now to keep simple
    quantity = db.Column(db.Integer, nullable=False, default=1) # Assuming 1 item = 1 packet/unit
    expiry_date = db.Column(db.Date, nullable=False)
    donated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_dispensed = db.Column(db.Boolean, default=False)
    dispensed_at = db.Column(db.DateTime, nullable=True)
    is_expired_removed = db.Column(db.Boolean, default=False)
    expired_removed_at = db.Column(db.DateTime, nullable=True)
    expired_removed_by_volunteer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return f"<FoodItem {self.id} in Machine {self.machine_id}, Expires: {self.expiry_date}>"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # Store hashed passwords
    role = db.Column(db.String(50), nullable=False) # "admin" or "volunteer"
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # For volunteers, link to food items they removed with explicit primaryjoin
    removed_food_items = db.relationship(
        "FoodItem",
        primaryjoin="User.id==FoodItem.expired_removed_by_volunteer_id",
        backref="removed_by_volunteer",
        lazy=True
    )

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

# Specific table for Volunteers if more fields are needed, inherits from User or links via one-to-one
class Volunteer(User):
    __tablename__ = "volunteers"
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    # Add volunteer-specific fields here if any, e.g., phone_number, assigned_machine_ids (could be a separate table for many-to-many)
    # For simplicity, keeping it tied to the User table with role="volunteer"

    __mapper_args__ = {
        "polymorphic_identity": "volunteer",
    }

# Specific table for Admins if more fields are needed
class Admin(User):
    __tablename__ = "admins"
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    # Add admin-specific fields here if any

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

# Donations are anonymous, so no specific Donor table linked to users.
# Donation events can be implicitly tracked via FoodItem creation if needed for analytics,
# but without linking to a specific donor user.

# Receiver interactions are also anonymous at the machine level.
# Dispensing events are tracked in FoodItem.is_dispensed and FoodItem.dispensed_at.
