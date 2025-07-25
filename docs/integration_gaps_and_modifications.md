# Exes Food Management System - Integration Gaps and Required Modifications

## Overview
This document outlines the gaps identified between the machine software, backend API, and website frontend components of the Exes Food Management System. It also details the required modifications to establish proper integration between these components.

## 1. API Endpoint Mismatches

### Machine Software API Client vs Backend API Routes

| Machine Client Expected Endpoint | Backend Actual Endpoint | Status | Required Action |
|----------------------------------|-------------------------|--------|-----------------|
| `/machine/auth` | Not implemented | Missing | Add authentication endpoint for machines |
| `/machine/register` | `/api/machines/` (POST) | Mismatch | Update machine client or add redirect endpoint |
| `/machine/status` | `/api/machines/<id>/status` (PUT) | Mismatch | Update machine client or add redirect endpoint |
| `/food/sync` | Not implemented | Missing | Add food sync endpoint |
| `/food/donate` | `/api/machines/<id>/report_donation` | Mismatch | Update machine client or add redirect endpoint |
| `/food/collect` | `/api/machines/<id>/dispense_food` | Mismatch | Update machine client or add redirect endpoint |
| `/maintenance/expired` | Not implemented | Missing | Add expired food removal endpoint |
| `/maintenance/alert` | Not implemented | Missing | Add alert reporting endpoint |
| `/location/nearest` | Not implemented | Missing | Add nearest machine location endpoint |
| `/machine/config/<id>` | Not implemented | Missing | Add machine configuration endpoint |

## 2. Authentication Mechanism Gaps

1. **Machine Software Authentication**:
   - Machine client expects a token-based authentication via `/machine/auth`
   - Backend does not currently implement machine authentication
   - Required: Implement machine authentication endpoint and token validation

2. **Website Authentication**:
   - Website uses token-based authentication with localStorage
   - Tokens are included in Authorization header
   - Required: Ensure consistent authentication approach between machine and website

## 3. Data Structure Mismatches

1. **Machine Status Updates**:
   - Machine client sends: `machine_id`, `timestamp`, `available_space`, `available_food_items`, etc.
   - Backend expects: `status`, `current_storage_level` directly
   - Required: Adapt data structure or add transformation layer

2. **Food Item Reporting**:
   - Machine client reports donations with: `machine_id`, `timestamp`, `quantity`, `expiry_date`, `storage_location`
   - Backend expects: `expiry_date`, `quantity` with different parameter structure
   - Required: Harmonize parameter naming and structure

## 4. Frontend Integration Gaps

1. **Mock Data Usage**:
   - MachineLocator component currently uses hardcoded mock data
   - Required: Replace with actual API calls to backend

2. **Location Services**:
   - Machine client has location services for finding nearest machines
   - Backend lacks corresponding endpoint
   - Frontend has location calculation logic but no API integration
   - Required: Implement backend endpoint and connect frontend

## 5. Implementation Plan

### Backend Modifications

1. Create new route file for machine API compatibility layer:
   - Implement all missing endpoints
   - Create adapters for mismatched endpoints
   - Ensure proper authentication

2. Add machine authentication system:
   - Implement `/api/machine/auth` endpoint
   - Create token generation and validation

### Machine Software Modifications

1. Update API client configuration:
   - Adjust base URL to match backend
   - Update endpoint paths or use compatibility layer

2. Enhance error handling and offline capabilities:
   - Ensure robust handling of connection issues
   - Improve offline queue processing

### Frontend Modifications

1. Update MachineLocator component:
   - Replace mock data with actual API calls
   - Implement proper error handling and loading states

2. Enhance location services:
   - Connect to backend nearest machine endpoint
   - Improve user location handling

## 6. Testing Strategy

1. Unit Testing:
   - Test each modified endpoint individually
   - Verify data transformation and authentication

2. Integration Testing:
   - Test machine client to backend communication
   - Test website to backend communication

3. End-to-End Testing:
   - Verify complete flow from machine donation to website display
   - Test offline capabilities and synchronization
