#!/usr/bin/env python3
"""
test_integration.py - Test script for machine-backend integration

This script tests the connectivity between the machine software and the backend server,
verifying that all endpoints are accessible and functioning correctly.
"""

import sys
import logging
import json
from datetime import datetime, timedelta
from api_client import APIClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("integration_test.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("IntegrationTest")

def test_machine_backend_integration():
    """Test the integration between machine software and backend server."""
    
    # Create a test machine ID - using integer ID to match backend schema
    machine_id = 9001  # Using a numeric ID instead of string
    
    # Initialize API client with the backend URL
    # In production, this would be the actual backend URL
    api_client = APIClient(machine_id, base_url="http://localhost:5000/api")
    
    # Test results dictionary
    test_results = {
        "registration": False,
        "authentication": False,
        "status_update": False,
        "donation": False,
        "collection": False,
        "expired_removal": False,
        "alert": False,
        "nearest_machines": False,
        "config": False
    }
    
    # Step 1: Test machine registration (must be done before authentication)
    logger.info("Testing machine registration...")
    location_data = {
        "latitude": 34.052235,
        "longitude": -118.243683,
        "address": "123 Test St, Integration City",
        "hours": "24/7"
    }
    reg_result = api_client.register_machine(location_data)
    test_results["registration"] = reg_result is not None
    logger.info(f"Registration test: {'PASSED' if test_results['registration'] else 'FAILED'}")
    
    if not test_results["registration"]:
        logger.error("Registration failed, aborting further tests")
        return test_results
    
    # Step 2: Test authentication (after registration)
    logger.info("Testing authentication...")
    auth_result = api_client.authenticate()
    test_results["authentication"] = auth_result
    logger.info(f"Authentication test: {'PASSED' if auth_result else 'FAILED'}")
    
    if not auth_result:
        logger.error("Authentication failed, aborting further tests")
        return test_results
    
    # Step 3: Test status update
    logger.info("Testing status update...")
    status_data = {
        "available_space": 75,
        "available_food_items": 12,
        "temperature": 4.5,
        "door_status": "closed",
        "error_code": None,
        "network_status": "online"
    }
    status_result = api_client.update_machine_status(status_data)
    test_results["status_update"] = status_result is not None
    logger.info(f"Status update test: {'PASSED' if test_results['status_update'] else 'FAILED'}")
    
    # Step 4: Test donation reporting
    logger.info("Testing donation reporting...")
    tomorrow = datetime.now() + timedelta(days=1)
    donation_data = {
        "quantity": 3,
        "expiry_date": tomorrow.strftime("%Y-%m-%d"),
        "storage_location": "COMPARTMENT_A"
    }
    donation_result = api_client.report_donation(donation_data)
    test_results["donation"] = donation_result is not None
    logger.info(f"Donation test: {'PASSED' if test_results['donation'] else 'FAILED'}")
    
    # Step 5: Test collection reporting
    logger.info("Testing collection reporting...")
    collection_data = {
        "food_item_ids": [1, 2],  # Assuming these IDs exist
        "quantity": 2
    }
    collection_result = api_client.report_collection(collection_data)
    test_results["collection"] = collection_result is not None
    logger.info(f"Collection test: {'PASSED' if test_results['collection'] else 'FAILED'}")
    
    # Step 6: Test expired food removal
    logger.info("Testing expired food removal...")
    removal_data = {
        "food_item_ids": [3, 4],  # Assuming these IDs exist
        "quantity": 2
    }
    removal_result = api_client.report_expired_removal(removal_data)
    test_results["expired_removal"] = removal_result is not None
    logger.info(f"Expired removal test: {'PASSED' if test_results['expired_removal'] else 'FAILED'}")
    
    # Step 7: Test alert reporting
    logger.info("Testing alert reporting...")
    alert_data = {
        "alert_type": "temperature_warning",
        "severity": "medium",
        "message": "Temperature slightly above normal range",
        "details": {"temperature": 6.2, "threshold": 5.0}
    }
    alert_result = api_client.report_alert(alert_data)
    test_results["alert"] = alert_result is not None
    logger.info(f"Alert test: {'PASSED' if test_results['alert'] else 'FAILED'}")
    
    # Step 8: Test nearest machines
    logger.info("Testing nearest machines query...")
    nearest_result = api_client.get_nearest_machines(34.052235, -118.243683, "donor")
    test_results["nearest_machines"] = nearest_result is not None
    logger.info(f"Nearest machines test: {'PASSED' if test_results['nearest_machines'] else 'FAILED'}")
    
    # Step 9: Test configuration
    logger.info("Testing machine configuration...")
    config_result = api_client.get_machine_config()
    test_results["config"] = config_result is not None
    logger.info(f"Configuration test: {'PASSED' if test_results['config'] else 'FAILED'}")
    
    # Calculate overall success
    passed_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests) * 100
    
    logger.info(f"Integration test completed: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
    
    return test_results

if __name__ == "__main__":
    logger.info("Starting machine-backend integration test")
    results = test_machine_backend_integration()
    
    # Print summary
    print("\n=== INTEGRATION TEST SUMMARY ===")
    for test, result in results.items():
        print(f"{test.replace('_', ' ').title()}: {'PASSED' if result else 'FAILED'}")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)
