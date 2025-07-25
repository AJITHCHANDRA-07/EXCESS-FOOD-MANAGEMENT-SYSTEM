"""
hardware_interface.py - Simulated hardware interface for the Exes Food Management System machine

This module provides simulated hardware interfaces for the machine components:
- Door control
- Storage compartments
- Sensors (temperature, weight, etc.)
- Display (already handled by Tkinter in main.py)
"""

import logging
import time
import random
from enum import Enum

logger = logging.getLogger("ExesMachine.Hardware")

class DoorStatus(Enum):
    CLOSED = "CLOSED"
    OPENING = "OPENING"
    OPEN = "OPEN"
    CLOSING = "CLOSING"
    ERROR = "ERROR"

class CompartmentStatus(Enum):
    EMPTY = "EMPTY"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FULL = "FULL"
    ERROR = "ERROR"

class HardwareInterface:
    """Main class for simulating hardware interactions."""
    
    def __init__(self, machine_id="MACHINE001"):
        """Initialize the hardware interface."""
        self.machine_id = machine_id
        self.logger = logging.getLogger(f"ExesMachine.Hardware.{machine_id}")
        self.logger.info(f"Initializing hardware interface for machine {machine_id}")
        
        # Initialize hardware components
        self.door = DoorController()
        self.compartments = {
            "A": StorageCompartment("A", max_capacity=20),
            "B": StorageCompartment("B", max_capacity=20),
            "C": StorageCompartment("C", max_capacity=20)
        }
        self.sensors = SensorSystem()
        
        # Simulate initial hardware check
        self._perform_hardware_check()
    
    def _perform_hardware_check(self):
        """Simulate a hardware check on startup."""
        self.logger.info("Performing hardware check...")
        
        # Check door
        door_status = self.door.get_status()
        self.logger.info(f"Door status: {door_status}")
        
        # Check compartments
        for comp_id, compartment in self.compartments.items():
            comp_status = compartment.get_status()
            self.logger.info(f"Compartment {comp_id} status: {comp_status}")
        
        # Check sensors
        temp = self.sensors.get_temperature()
        self.logger.info(f"Temperature: {temp}°C")
        
        self.logger.info("Hardware check completed")
    
    def get_system_status(self):
        """Get the overall system status."""
        return {
            "door": self.door.get_status().value,
            "compartments": {
                comp_id: compartment.get_status().value
                for comp_id, compartment in self.compartments.items()
            },
            "temperature": self.sensors.get_temperature(),
            "humidity": self.sensors.get_humidity(),
            "power": self.sensors.get_power_status()
        }
    
    def open_compartment(self, compartment_id):
        """Open a specific compartment."""
        if compartment_id not in self.compartments:
            self.logger.error(f"Invalid compartment ID: {compartment_id}")
            return False
        
        self.logger.info(f"Opening compartment {compartment_id}")
        
        # First open the main door
        if not self.door.open():
            self.logger.error("Failed to open main door")
            return False
        
        # Then simulate opening the specific compartment
        # In a real system, this might involve moving a mechanism to the right position
        time.sleep(1)  # Simulate the time it takes to open
        
        self.logger.info(f"Compartment {compartment_id} opened successfully")
        return True
    
    def close_compartment(self, compartment_id):
        """Close a specific compartment."""
        if compartment_id not in self.compartments:
            self.logger.error(f"Invalid compartment ID: {compartment_id}")
            return False
        
        self.logger.info(f"Closing compartment {compartment_id}")
        
        # Simulate closing the specific compartment
        time.sleep(1)  # Simulate the time it takes to close
        
        # Then close the main door
        if not self.door.close():
            self.logger.error("Failed to close main door")
            return False
        
        self.logger.info(f"Compartment {compartment_id} closed successfully")
        return True
    
    def add_items_to_compartment(self, compartment_id, quantity):
        """Add items to a compartment (simulated)."""
        if compartment_id not in self.compartments:
            self.logger.error(f"Invalid compartment ID: {compartment_id}")
            return False
        
        compartment = self.compartments[compartment_id]
        if compartment.add_items(quantity):
            self.logger.info(f"Added {quantity} items to compartment {compartment_id}")
            return True
        else:
            self.logger.error(f"Failed to add items to compartment {compartment_id}")
            return False
    
    def remove_items_from_compartment(self, compartment_id, quantity):
        """Remove items from a compartment (simulated)."""
        if compartment_id not in self.compartments:
            self.logger.error(f"Invalid compartment ID: {compartment_id}")
            return False
        
        compartment = self.compartments[compartment_id]
        if compartment.remove_items(quantity):
            self.logger.info(f"Removed {quantity} items from compartment {compartment_id}")
            return True
        else:
            self.logger.error(f"Failed to remove items from compartment {compartment_id}")
            return False
    
    def get_available_space(self):
        """Get the total available space across all compartments."""
        total_capacity = sum(comp.max_capacity for comp in self.compartments.values())
        current_items = sum(comp.current_items for comp in self.compartments.values())
        return total_capacity - current_items
    
    def find_best_compartment_for_donation(self, quantity):
        """Find the best compartment for a new donation."""
        best_compartment = None
        best_fit = float('inf')
        
        for comp_id, compartment in self.compartments.items():
            available = compartment.max_capacity - compartment.current_items
            if available >= quantity and available < best_fit:
                best_compartment = comp_id
                best_fit = available
        
        return best_compartment
    
    def find_compartments_with_items(self):
        """Find compartments that have items available."""
        return [
            comp_id for comp_id, compartment in self.compartments.items()
            if compartment.current_items > 0
        ]


class DoorController:
    """Simulates the main door of the machine."""
    
    def __init__(self):
        """Initialize the door controller."""
        self.logger = logging.getLogger("ExesMachine.Hardware.Door")
        self.status = DoorStatus.CLOSED
    
    def get_status(self):
        """Get the current door status."""
        return self.status
    
    def open(self):
        """Open the door."""
        self.logger.info("Opening door...")
        
        # Simulate door opening process
        if self.status != DoorStatus.CLOSED:
            self.logger.warning(f"Cannot open door: current status is {self.status}")
            return False
        
        # Simulate potential hardware failure (5% chance)
        if random.random() < 0.05:
            self.logger.error("Door failed to open")
            self.status = DoorStatus.ERROR
            return False
        
        # Simulate opening sequence
        self.status = DoorStatus.OPENING
        time.sleep(1.5)  # Simulate the time it takes to open
        self.status = DoorStatus.OPEN
        self.logger.info("Door opened successfully")
        return True
    
    def close(self):
        """Close the door."""
        self.logger.info("Closing door...")
        
        # Simulate door closing process
        if self.status != DoorStatus.OPEN:
            self.logger.warning(f"Cannot close door: current status is {self.status}")
            return False
        
        # Simulate potential hardware failure (5% chance)
        if random.random() < 0.05:
            self.logger.error("Door failed to close")
            self.status = DoorStatus.ERROR
            return False
        
        # Simulate closing sequence
        self.status = DoorStatus.CLOSING
        time.sleep(1.5)  # Simulate the time it takes to close
        self.status = DoorStatus.CLOSED
        self.logger.info("Door closed successfully")
        return True
    
    def reset(self):
        """Reset the door controller in case of error."""
        self.logger.info("Resetting door controller...")
        time.sleep(2)  # Simulate reset time
        self.status = DoorStatus.CLOSED
        self.logger.info("Door controller reset successfully")
        return True


class StorageCompartment:
    """Simulates a storage compartment in the machine."""
    
    def __init__(self, compartment_id, max_capacity=20):
        """Initialize the storage compartment."""
        self.compartment_id = compartment_id
        self.max_capacity = max_capacity
        self.current_items = 0
        self.logger = logging.getLogger(f"ExesMachine.Hardware.Compartment.{compartment_id}")
    
    def get_status(self):
        """Get the current compartment status."""
        if self.current_items == 0:
            return CompartmentStatus.EMPTY
        elif self.current_items < self.max_capacity:
            return CompartmentStatus.PARTIALLY_FILLED
        else:
            return CompartmentStatus.FULL
    
    def add_items(self, quantity):
        """Add items to the compartment."""
        if self.current_items + quantity > self.max_capacity:
            self.logger.warning(f"Cannot add {quantity} items: compartment would exceed capacity")
            return False
        
        self.current_items += quantity
        self.logger.info(f"Added {quantity} items to compartment {self.compartment_id}")
        return True
    
    def remove_items(self, quantity):
        """Remove items from the compartment."""
        if self.current_items < quantity:
            self.logger.warning(f"Cannot remove {quantity} items: compartment only has {self.current_items}")
            return False
        
        self.current_items -= quantity
        self.logger.info(f"Removed {quantity} items from compartment {self.compartment_id}")
        return True


class SensorSystem:
    """Simulates various sensors in the machine."""
    
    def __init__(self):
        """Initialize the sensor system."""
        self.logger = logging.getLogger("ExesMachine.Hardware.Sensors")
        self.temperature = 4.0  # Initial temperature in Celsius
        self.humidity = 40.0    # Initial humidity percentage
        self.power_status = "NORMAL"  # Initial power status
    
    def get_temperature(self):
        """Get the current temperature reading."""
        # Simulate slight temperature variations
        self.temperature += random.uniform(-0.2, 0.2)
        # Keep within realistic bounds
        self.temperature = max(2.0, min(8.0, self.temperature))
        return round(self.temperature, 1)
    
    def get_humidity(self):
        """Get the current humidity reading."""
        # Simulate slight humidity variations
        self.humidity += random.uniform(-1.0, 1.0)
        # Keep within realistic bounds
        self.humidity = max(30.0, min(60.0, self.humidity))
        return round(self.humidity, 1)
    
    def get_power_status(self):
        """Get the current power status."""
        # Occasionally simulate power fluctuations
        if random.random() < 0.02:
            self.power_status = "FLUCTUATING"
        else:
            self.power_status = "NORMAL"
        return self.power_status
    
    def get_weight(self, compartment_id):
        """Simulate weight sensor for a specific compartment."""
        # This would be a real weight reading in a physical machine
        # For simulation, we'll return a random weight based on compartment
        return random.uniform(0.5, 2.0) * (ord(compartment_id) - ord('A') + 1)
