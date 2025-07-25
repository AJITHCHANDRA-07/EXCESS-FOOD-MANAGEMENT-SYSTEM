# Exes Food Management System - Project Checklist

## I. Physical Machine Features

- [ ] **Machine Placement:** Strategically located in various accessible areas.
- [ ] **Food Storage:** Secure and appropriate storage for donated food items.
- [ ] **Server Connectivity:** Each machine maintains a persistent connection to a central server for real-time data synchronization.

### A. Donor Interaction Module (Anonymous)

- [ ] **Anonymous Food Donation Process:**
    - [ ] Allow donor to input food quantity.
    - [ ] Allow donor to input food expiry date.
    - [ ] System provides food packing covers/containers.
    - [ ] Machine physically accepts and stores the donated food.
- [ ] **Storage Full Logic:**
    - [ ] If machine storage is full, display or direct the donor to the next nearest available machine location.

### B. Receiver Interaction Module

- [ ] **Food Dispensing Process:**
    - [ ] Dispense a standard quantity of food (e.g., 2 packets) to a receiver.
- [ ] **Food Unavailability/Expiry Logic:**
    - [ ] If food is not available in the machine, display or direct the receiver to the next nearest machine location.
    - [ ] If available food is found to be expired (cross-check with volunteer module), prevent dispensing and direct the receiver to the next nearest machine location.

### C. Volunteer Interaction Module

- [ ] **Expired Food Management:**
    - [ ] Interface for volunteers to view details of expired food items within a specific machine.
    - [ ] Mechanism for volunteers to confirm removal of expired food from the machine.

## II. Server-Side System

- [ ] **Machine Network Management:** Manage and monitor all connected food bank machines.
- [ ] **Data Synchronization:** Real-time updates between machines and the central server (inventory, status, etc.).
- [ ] **Location Services:** Maintain and provide information on machine locations and their current status (e.g., storage capacity, food availability).
- [ ] **API Development:** Develop APIs for communication with machines and the website.

## III. Website Application

- [ ] **General Website Features:**
    - [ ] User registration and login for Admin and Volunteer roles (Donors interact anonymously).
    - [ ] Information about the initiative, how to donate, how to receive, and how to volunteer.
    - [ ] Map displaying machine locations: for donors (shows available storage space), for receivers (shows food availability), and general status/hours.

### A. Admin Page/Dashboard

- [ ] **System Overview:** View overall system status (number of machines, total donations, total food dispensed, volunteer activity).
- [ ] **Machine Management:** Add, remove, or update machine details and locations.
- [ ] **User Management:** Manage donor, receiver, and volunteer accounts.
- [ ] **Inventory Monitoring:** Track food inventory across all machines.
- [ ] **Reporting & Analytics:** Generate reports on food donation, dispensation, expiry rates, etc.

### B. Donor Page/Portal

- [ ] **Donation History:** View past donations.
- [ ] **Machine Locator:** Find nearby machines and check their current capacity for donations.
- [ ] **Pledge Donations (Optional):** Allow donors to indicate upcoming donations.

### C. Receiver Page/Portal

- [ ] **Machine Locator:** Find nearby machines and check food availability.
- [ ] **Request History (Optional):** View past food collections.

### D. Volunteer Page/Portal

- [ ] **Machine Assignment:** View assigned machines or select machines to service.
- [ ] **Expired Food Alerts:** Receive notifications or view a list of machines with expired food requiring collection.
- [ ] **Collection Log:** Record details of expired food collected.

## IV. System Architecture & Technology

- [ ] **Database Design:** Design a schema to store information about users, machines, food items, donations, dispensations, and volunteer activities.
- [ ] **Backend Development:** Choose an appropriate backend framework (e.g., Flask, given the need for server-side logic and database interaction).
- [ ] **Frontend Development:** Develop a responsive and user-friendly interface for the website.
- [ ] **Machine Software:** Develop or specify software for the physical machines to handle interactions and server communication.
- [ ] **Security:** Implement security measures for data protection and user authentication.

## V. Project Management & Documentation

- [ ] **Detailed Requirements Document:** Further refine and document all functional and non-functional requirements.
- [ ] **System Design Document:** Create detailed design specifications for hardware and software components.
- [ ] **Testing Plan:** Develop a comprehensive plan for unit, integration, system, and user acceptance testing.
- [ ] **Deployment Plan:** Outline the strategy for deploying the machines and the web application.



## VI. Phase 2: Machine Software and Frontend Development

### A. Machine-Side Software Development

- [ ] **Define Detailed Machine UI/UX Requirements:**
    - [ ] Specify screen flows for donor interactions (food input, expiry, confirmation).
    - [ ] Specify screen flows for receiver interactions (food request, dispensing).
    - [ ] Specify screen flows for volunteer interactions (login, view expired food, confirm removal).
    - [ ] Design intuitive touchscreen layouts and visual elements.
- [ ] **Develop Machine Application Logic:**
    - [ ] Implement donor interaction module (interfacing with hardware for input, cover dispensing, food intake).
    - [ ] Implement receiver interaction module (interfacing with hardware for dispensing).
    - [ ] Implement volunteer interaction module (secure access, display data, confirm actions).
- [ ] **Integrate Machine Software with Backend APIs:**
    - [ ] Implement API calls for reporting donations.
    - [ ] Implement API calls for confirming food dispensing.
    - [ ] Implement API calls for fetching machine status and inventory (for volunteer view).
    - [ ] Implement API calls for volunteer actions (e.g., confirming removal of expired food).
    - [ ] Implement API calls for heartbeat and status reporting.
    - [ ] Handle API error responses gracefully.
- [ ] **Simulate/Test Machine Hardware Interactions:** (If actual hardware is not yet available)
    - [ ] Create stubs or simulators for sensors and actuators.
- [ ] **Unit & Integration Testing for Machine Software.**

### B. Website Frontend Development

- [ ] **Define Detailed Website UI/UX Requirements:**
    - [ ] Design mockups/wireframes for Admin portal dashboards and management pages.
    - [ ] Design mockups/wireframes for Volunteer portal (assigned machines, alerts, task logging).
    - [ ] Design mockups/wireframes for Public pages (machine locator map with donor/receiver views, informational content).
    - [ ] Ensure responsive design for all pages.
- [ ] **Setup Frontend Development Environment:**
    - [ ] Choose frontend framework (e.g., React, Vue, or Flask templates as per proposal).
    - [ ] Set up project structure, build tools, and dependencies.
- [ ] **Develop Core Frontend Components:**
    - [ ] Implement user authentication components (for Admin, Volunteer login).
    - [ ] Implement navigation, layout, and common UI elements.
    - [ ] Implement mapping component for machine locator.
- [ ] **Develop Admin Portal Frontend:**
    - [ ] Implement dashboard for system overview.
    - [ ] Implement machine management interface (CRUD operations, status view).
    - [ ] Implement user management interface (Admin/Volunteer accounts).
    - [ ] Implement inventory oversight views.
    - [ ] Implement reporting interface.
    - [ ] Integrate with backend Admin APIs.
- [ ] **Develop Volunteer Portal Frontend:**
    - [ ] Implement dashboard for volunteer tasks and alerts.
    - [ ] Implement interface to view assigned machine status and expired food.
    - [ ] Implement interface to log actions (e.g., confirming food removal, if not solely done at machine).
    - [ ] Integrate with backend Volunteer APIs.
- [ ] **Develop Public Website Pages:**
    - [ ] Implement machine locator map with filters for donors (available space) and receivers (food availability).
    - [ ] Implement informational pages (About, How to Use, FAQ).
    - [ ] Integrate with backend Public APIs for machine data.
- [ ] **Unit & Integration Testing for Website Frontend.**

### C. System-Wide Integration and Testing

- [ ] **End-to-End Testing:**
    - [ ] Test full flow: Donor uses machine -> Data updates on server -> Admin/Volunteer sees updates on website.
    - [ ] Test full flow: Receiver uses machine -> Data updates on server -> Admin sees updates.
    - [ ] Test full flow: Volunteer uses machine/website to manage expired food -> Data updates correctly.
- [ ] **User Acceptance Testing (UAT) - Phase 2:**
    - [ ] Prepare UAT scenarios for machine software.
    - [ ] Prepare UAT scenarios for website frontend.
    - [ ] Conduct UAT with the user/stakeholders.
- [ ] **Refinement and Bug Fixing based on UAT Feedback.**

### D. Phase 2 Deliverables and Documentation

- [ ] **Updated Source Code:** Including machine software and website frontend.
- [ ] **Deployment Plan (Initial Draft):** For machines and web application.
- [ ] **Updated Project Documentation:** Reflecting Phase 2 development.

