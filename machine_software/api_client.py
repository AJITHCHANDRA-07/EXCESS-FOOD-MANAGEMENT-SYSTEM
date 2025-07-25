"""
api_client.py - API client for communicating with the central backend server

This module handles all communication between the machine and the central backend server.
"""

import logging
import requests
import json
import time
from datetime import datetime

logger = logging.getLogger("ExesMachine.APIClient")

class APIClient:
    """Client for communicating with the central backend server."""
    
    def __init__(self, machine_id, base_url="http://localhost:5000/api"):
        """Initialize the API client.
        
        Args:
            machine_id: Unique identifier for this machine
            base_url: Base URL for the backend API
        """
        self.machine_id = machine_id
        self.base_url = base_url
        self.logger = logging.getLogger(f"ExesMachine.APIClient.{machine_id}")
        self.auth_token = None
        self.offline_queue = []
        
        # Try to authenticate on initialization
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with the backend server."""
        self.logger.info(f"Authenticating machine {self.machine_id} with backend")
        
        try:
            response = requests.post(
                f"{self.base_url}/machine/auth",
                json={"machine_id": self.machine_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("token")
                self.logger.info("Authentication successful")
                return True
            else:
                self.logger.error(f"Authentication failed: {response.status_code} - {response.text}")
                return False
        except requests.RequestException as e:
            self.logger.error(f"Authentication request failed: {e}")
            return False
    
    def _get_headers(self):
        """Get the headers for API requests."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}" if self.auth_token else ""
        }
    
    def _handle_request(self, method, endpoint, data=None, retry=True):
        """Handle an API request with error handling and offline queueing.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint to call
            data: Data to send (for POST/PUT)
            retry: Whether to retry on failure
            
        Returns:
            Response data or None on failure
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self._get_headers())
            elif method == "POST":
                response = requests.post(url, headers=self._get_headers(), json=data)
            elif method == "PUT":
                response = requests.put(url, headers=self._get_headers(), json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self._get_headers())
            else:
                self.logger.error(f"Unsupported HTTP method: {method}")
                return None
            
            if response.status_code == 401 and retry:
                # Token might be expired, try to re-authenticate
                self.logger.warning("Authentication token expired, re-authenticating")
                if self.authenticate():
                    # Retry the request with the new token
                    return self._handle_request(method, endpoint, data, retry=False)
                else:
                    return None
            
            if response.status_code >= 200 and response.status_code < 300:
                return response.json() if response.content else None
            else:
                self.logger.error(f"API request failed: {response.status_code} - {response.text}")
                
                # Queue the request for later if it's a network error
                if response.status_code >= 500 or response.status_code == 0:
                    self._queue_offline_request(method, endpoint, data)
                
                return None
        except requests.RequestException as e:
            self.logger.error(f"API request error: {e}")
            self._queue_offline_request(method, endpoint, data)
            return None
    
    def _queue_offline_request(self, method, endpoint, data):
        """Queue a request for later when offline."""
        self.logger.info(f"Queueing offline request: {method} {endpoint}")
        self.offline_queue.append({
            "method": method,
            "endpoint": endpoint,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
    
    def process_offline_queue(self):
        """Process any queued offline requests."""
        if not self.offline_queue:
            return
        
        self.logger.info(f"Processing offline queue ({len(self.offline_queue)} items)")
        
        # Make a copy of the queue and clear it
        queue_copy = self.offline_queue.copy()
        self.offline_queue = []
        
        for request in queue_copy:
            self.logger.info(f"Processing queued request: {request['method']} {request['endpoint']}")
            result = self._handle_request(
                request["method"],
                request["endpoint"],
                request["data"],
                retry=True
            )
            
            if result is None:
                # If still failing, add back to the queue
                self.offline_queue.append(request)
    
    # Machine registration and status
    
    def register_machine(self, location_data):
        """Register this machine with the backend server."""
        self.logger.info(f"Registering machine {self.machine_id}")
        
        data = {
            "machine_id": self.machine_id,
            "location_lat": location_data.get("latitude"),
            "location_lon": location_data.get("longitude"),
            "address_description": location_data.get("address"),
            "operational_hours": location_data.get("hours", "24/7")
        }
        
        return self._handle_request("POST", "machine/register", data)
    
    def update_machine_status(self, status_data):
        """Update the machine status on the backend server."""
        self.logger.info("Updating machine status")
        
        data = {
            "machine_id": self.machine_id,
            "timestamp": datetime.now().isoformat(),
            "available_space": status_data.get("available_space"),
            "available_food_items": status_data.get("available_food_items"),
            "temperature": status_data.get("temperature"),
            "door_status": status_data.get("door_status"),
            "error_code": status_data.get("error_code"),
            "network_status": status_data.get("network_status")
        }
        
        return self._handle_request("POST", "machine/status", data)
    
    # Food item management
    
    def sync_food_items(self, items):
        """Sync food items with the backend server."""
        self.logger.info(f"Syncing {len(items)} food items with backend")
        
        data = {
            "machine_id": self.machine_id,
            "items": items
        }
        
        return self._handle_request("POST", "food/sync", data)
    
    def report_donation(self, donation_data):
        """Report a new donation to the backend server."""
        self.logger.info("Reporting new donation")
        
        data = {
            "machine_id": self.machine_id,
            "timestamp": datetime.now().isoformat(),
            "quantity": donation_data.get("quantity"),
            "expiry_date": donation_data.get("expiry_date"),
            "storage_location": donation_data.get("storage_location")
        }
        
        return self._handle_request("POST", "food/donate", data)
    
    def report_collection(self, collection_data):
        """Report a food collection to the backend server."""
        self.logger.info("Reporting food collection")
        
        data = {
            "machine_id": self.machine_id,
            "timestamp": datetime.now().isoformat(),
            "food_item_ids": collection_data.get("food_item_ids"),
            "quantity": collection_data.get("quantity")
        }
        
        return self._handle_request("POST", "food/collect", data)
    
    # Maintenance and alerts
    
    def report_expired_removal(self, removal_data):
        """Report removal of expired items to the backend server."""
        self.logger.info("Reporting expired item removal")
        
        data = {
            "machine_id": self.machine_id,
            "timestamp": datetime.now().isoformat(),
            "food_item_ids": removal_data.get("food_item_ids"),
            "quantity": removal_data.get("quantity")
        }
        
        return self._handle_request("POST", "maintenance/expired", data)
    
    def report_alert(self, alert_data):
        """Report an alert to the backend server."""
        self.logger.info(f"Reporting alert: {alert_data.get('alert_type')}")
        
        data = {
            "machine_id": self.machine_id,
            "timestamp": datetime.now().isoformat(),
            "alert_type": alert_data.get("alert_type"),
            "severity": alert_data.get("severity"),
            "message": alert_data.get("message"),
            "details": alert_data.get("details")
        }
        
        return self._handle_request("POST", "maintenance/alert", data)
    
    # Location services
    
    def get_nearest_machines(self, latitude, longitude, filter_type=None):
        """Get the nearest machines to a location.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            filter_type: Optional filter ('donor' for machines with space, 'receiver' for machines with food)
            
        Returns:
            List of nearby machines or None on failure
        """
        self.logger.info(f"Getting nearest machines to ({latitude}, {longitude})")
        
        endpoint = f"location/nearest?lat={latitude}&lon={longitude}"
        if filter_type:
            endpoint += f"&filter={filter_type}"
        
        return self._handle_request("GET", endpoint)
    
    # Configuration
    
    def get_machine_config(self):
        """Get the machine configuration from the backend server."""
        self.logger.info("Getting machine configuration")
        
        return self._handle_request("GET", f"machine/config/{self.machine_id}")
    
    def update_machine_config(self, config_data):
        """Update the machine configuration on the backend server."""
        self.logger.info("Updating machine configuration")
        
        data = {
            "machine_id": self.machine_id,
            "config": config_data
        }
        
        return self._handle_request("PUT", "machine/config", data)
