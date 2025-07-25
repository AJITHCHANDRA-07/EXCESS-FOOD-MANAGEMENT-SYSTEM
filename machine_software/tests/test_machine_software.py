"""
test_machine_software.py - Test script for the Exes Food Management System machine software

This script tests the integration of all machine software components.
"""

import os
import sys
import logging
import sqlite3
import unittest
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import machine software modules
from hardware_interface import HardwareInterface
from storage_manager import StorageManager
from api_client import APIClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_machine.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("TestMachine")

class TestMachineSoftware(unittest.TestCase):
    """Test cases for the machine software."""
    
    def setUp(self):
        """Set up test environment."""
        logger.info("Setting up test environment")
        
        # Create in-memory database for testing
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        
        # Create required tables
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_timestamp TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            storage_location TEXT NOT NULL,
            status TEXT NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS machine_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature REAL,
            door_status TEXT,
            available_space INTEGER,
            error_code TEXT,
            network_status TEXT
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            food_item_id INTEGER,
            quantity INTEGER,
            status TEXT NOT NULL
        )
        ''')
        
        self.conn.commit()
        
        # Initialize hardware interface
        self.hardware = HardwareInterface("TEST_MACHINE")
        
        # Initialize storage manager
        self.storage = StorageManager(self.conn, self.hardware)
        
        # Initialize API client (with mock URL)
        self.api = APIClient("TEST_MACHINE", "http://localhost:5000/api")
    
    def tearDown(self):
        """Clean up after tests."""
        logger.info("Cleaning up test environment")
        self.conn.close()
    
    def test_hardware_interface(self):
        """Test the hardware interface."""
        logger.info("Testing hardware interface")
        
        # Test door operations
        self.assertEqual(self.hardware.door.get_status().value, "CLOSED")
        self.assertTrue(self.hardware.door.open())
        self.assertEqual(self.hardware.door.get_status().value, "OPEN")
        self.assertTrue(self.hardware.door.close())
        self.assertEqual(self.hardware.door.get_status().value, "CLOSED")
        
        # Test compartment operations
        compartment_id = "A"
        self.assertTrue(self.hardware.add_items_to_compartment(compartment_id, 5))
        self.assertEqual(self.hardware.compartments[compartment_id].current_items, 5)
        self.assertTrue(self.hardware.remove_items_from_compartment(compartment_id, 2))
        self.assertEqual(self.hardware.compartments[compartment_id].current_items, 3)
        
        # Test sensor operations
        self.assertIsNotNone(self.hardware.sensors.get_temperature())
        self.assertIsNotNone(self.hardware.sensors.get_humidity())
        self.assertIsNotNone(self.hardware.sensors.get_power_status())
        
        # Test system status
        status = self.hardware.get_system_status()
        self.assertIn("door", status)
        self.assertIn("compartments", status)
        self.assertIn("temperature", status)
    
    def test_storage_manager(self):
        """Test the storage manager."""
        logger.info("Testing storage manager")
        
        # Test adding food items
        tomorrow = (datetime.now() + timedelta(days=1)).date().isoformat()
        success, item_id = self.storage.add_food_item(5, tomorrow, "A")
        self.assertTrue(success)
        self.assertIsInstance(item_id, int)
        
        # Test getting available food items
        items = self.storage.get_available_food_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["quantity"], 5)
        self.assertEqual(items[0]["expiry_date"], tomorrow)
        
        # Test collecting food items
        success, collected = self.storage.collect_food_items(limit=1)
        self.assertTrue(success)
        self.assertEqual(len(collected), 1)
        
        # Verify item was marked as collected
        items = self.storage.get_available_food_items()
        self.assertEqual(len(items), 0)
        
        # Test expired item handling
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        self.storage.add_food_item(3, yesterday, "B")
        
        # Verify expired item is found
        success, count = self.storage.remove_expired_items()
        self.assertTrue(success)
        self.assertEqual(count, 1)
        
        # Test storage status
        status = self.storage.get_storage_status()
        self.assertIn("available_items_count", status)
        self.assertIn("expired_items_count", status)
        self.assertIn("available_space", status)
    
    def test_integration(self):
        """Test integration between components."""
        logger.info("Testing component integration")
        
        # Add food items through storage manager
        next_week = (datetime.now() + timedelta(days=7)).date().isoformat()
        success, item_id = self.storage.add_food_item(10, next_week)
        self.assertTrue(success)
        
        # Verify hardware state was updated
        best_compartment = self.hardware.find_best_compartment_for_donation(10)
        self.assertEqual(self.hardware.compartments[best_compartment].current_items, 10)
        
        # Collect items
        success, collected = self.storage.collect_food_items()
        self.assertTrue(success)
        
        # Verify hardware state was updated again
        self.assertEqual(self.hardware.compartments[best_compartment].current_items, 0)
        
        # Test system status integration
        status = self.storage.get_storage_status()
        self.assertEqual(status["available_items_count"], 0)
        self.assertEqual(status["available_space"], 
                         sum(comp.max_capacity for comp in self.hardware.compartments.values()))


if __name__ == "__main__":
    unittest.main()
