"""
storage_manager.py - Storage management module for the Exes Food Management System machine

This module handles the management of food items in the machine's storage compartments.
"""

import logging
import sqlite3
from datetime import datetime, date

logger = logging.getLogger("ExesMachine.StorageManager")

class StorageManager:
    """Manages the storage of food items in the machine."""
    
    def __init__(self, db_connection, hardware_interface):
        """Initialize the storage manager.
        
        Args:
            db_connection: SQLite database connection
            hardware_interface: Hardware interface for controlling compartments
        """
        self.conn = db_connection
        self.cursor = self.conn.cursor()
        self.hardware = hardware_interface
        self.logger = logging.getLogger("ExesMachine.StorageManager")
        
        # Ensure the database is properly set up
        self._ensure_tables_exist()
    
    def _ensure_tables_exist(self):
        """Ensure that all required tables exist in the database."""
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
        self.conn.commit()
    
    def add_food_item(self, quantity, expiry_date, storage_location=None):
        """Add a new food item to storage.
        
        Args:
            quantity: Number of items
            expiry_date: Expiry date in ISO format (YYYY-MM-DD)
            storage_location: Optional compartment ID, will be determined if not provided
            
        Returns:
            Tuple of (success, item_id or error_message)
        """
        self.logger.info(f"Adding food item: quantity={quantity}, expiry={expiry_date}")
        
        # Determine storage location if not provided
        if not storage_location:
            storage_location = self._determine_best_storage_location(quantity)
            if not storage_location:
                return (False, "No suitable storage location available")
        
        try:
            # Update the hardware simulation
            if not self.hardware.add_items_to_compartment(storage_location, quantity):
                return (False, f"Hardware error: Could not add items to compartment {storage_location}")
            
            # Add to database
            self.cursor.execute('''
            INSERT INTO food_items (entry_timestamp, expiry_date, quantity, storage_location, status)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                expiry_date,
                quantity,
                storage_location,
                "AVAILABLE"
            ))
            self.conn.commit()
            
            item_id = self.cursor.lastrowid
            self.logger.info(f"Food item added successfully: id={item_id}")
            return (True, item_id)
        except Exception as e:
            self.logger.error(f"Error adding food item: {e}")
            return (False, str(e))
    
    def _determine_best_storage_location(self, quantity):
        """Determine the best storage location for a new food item.
        
        Args:
            quantity: Number of items to store
            
        Returns:
            Compartment ID or None if no suitable location
        """
        return self.hardware.find_best_compartment_for_donation(quantity)
    
    def get_available_food_items(self, limit=None):
        """Get available food items, sorted by expiry date (oldest first).
        
        Args:
            limit: Optional limit on number of items to return
            
        Returns:
            List of food items
        """
        try:
            query = '''
            SELECT id, entry_timestamp, expiry_date, quantity, storage_location
            FROM food_items
            WHERE status = 'AVAILABLE'
            ORDER BY expiry_date ASC
            '''
            
            if limit:
                query += f" LIMIT {limit}"
            
            self.cursor.execute(query)
            items = self.cursor.fetchall()
            
            # Convert to list of dictionaries
            result = []
            for item in items:
                result.append({
                    "id": item[0],
                    "entry_timestamp": item[1],
                    "expiry_date": item[2],
                    "quantity": item[3],
                    "storage_location": item[4]
                })
            
            return result
        except Exception as e:
            self.logger.error(f"Error getting available food items: {e}")
            return []
    
    def collect_food_items(self, limit=2):
        """Collect food items for a receiver (oldest items first).
        
        Args:
            limit: Maximum number of items to collect
            
        Returns:
            Tuple of (success, list of collected items or error message)
        """
        self.logger.info(f"Collecting up to {limit} food items")
        
        try:
            # Get the oldest available items
            items = self.get_available_food_items(limit=limit)
            
            if not items:
                return (False, "No food items available")
            
            collected_items = []
            compartments_to_open = set()
            
            # Mark items as collected and track compartments to open
            for item in items:
                self.cursor.execute('''
                UPDATE food_items SET status = 'COLLECTED' WHERE id = ?
                ''', (item["id"],))
                
                # Track which compartment needs to be opened
                compartments_to_open.add(item["storage_location"])
                
                # Update hardware simulation
                self.hardware.remove_items_from_compartment(
                    item["storage_location"], 
                    item["quantity"]
                )
                
                collected_items.append(item)
            
            self.conn.commit()
            
            # Open compartments (in a real system, this would happen one by one)
            for compartment in compartments_to_open:
                self.hardware.open_compartment(compartment)
                # In a real system, we would wait for confirmation before closing
                self.hardware.close_compartment(compartment)
            
            self.logger.info(f"Successfully collected {len(collected_items)} food items")
            return (True, collected_items)
        except Exception as e:
            self.logger.error(f"Error collecting food items: {e}")
            return (False, str(e))
    
    def remove_expired_items(self):
        """Remove expired food items.
        
        Returns:
            Tuple of (success, count of removed items or error message)
        """
        self.logger.info("Removing expired food items")
        
        try:
            today = date.today().isoformat()
            
            # Find expired items
            self.cursor.execute('''
            SELECT id, quantity, storage_location FROM food_items
            WHERE status = 'AVAILABLE' AND expiry_date < ?
            ''', (today,))
            
            expired_items = self.cursor.fetchall()
            
            if not expired_items:
                return (True, 0)
            
            # Update status and hardware
            for item_id, quantity, storage_location in expired_items:
                self.cursor.execute('''
                UPDATE food_items SET status = 'EXPIRED_REMOVED' WHERE id = ?
                ''', (item_id,))
                
                # Update hardware simulation
                self.hardware.remove_items_from_compartment(storage_location, quantity)
            
            self.conn.commit()
            
            count = len(expired_items)
            self.logger.info(f"Removed {count} expired food items")
            return (True, count)
        except Exception as e:
            self.logger.error(f"Error removing expired items: {e}")
            return (False, str(e))
    
    def get_storage_status(self):
        """Get the current storage status.
        
        Returns:
            Dictionary with storage status information
        """
        try:
            # Count available items
            self.cursor.execute('''
            SELECT COUNT(*), SUM(quantity) FROM food_items WHERE status = 'AVAILABLE'
            ''')
            count_row = self.cursor.fetchone()
            available_items_count = count_row[0] or 0
            available_items_quantity = count_row[1] or 0
            
            # Count expired items
            today = date.today().isoformat()
            self.cursor.execute('''
            SELECT COUNT(*) FROM food_items 
            WHERE status = 'AVAILABLE' AND expiry_date < ?
            ''', (today,))
            expired_count = self.cursor.fetchone()[0] or 0
            
            # Get hardware status
            hardware_status = self.hardware.get_system_status()
            available_space = self.hardware.get_available_space()
            
            return {
                "available_items_count": available_items_count,
                "available_items_quantity": available_items_quantity,
                "expired_items_count": expired_count,
                "available_space": available_space,
                "compartments": hardware_status["compartments"],
                "temperature": hardware_status["temperature"]
            }
        except Exception as e:
            self.logger.error(f"Error getting storage status: {e}")
            return {
                "error": str(e)
            }
