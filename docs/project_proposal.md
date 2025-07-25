# Proposal: Exes Food Management System - Features and Architecture

## 1. Introduction

This document outlines the proposed features and system architecture for the Exes Food Management System. It is based on the initial requirements provided by the user and insights gathered from researching existing food bank and pantry management solutions. The goal is to create a robust, user-friendly, and efficient system to facilitate food donation and distribution through a network of automated machines and a central web platform.

## 2. Proposed Features

The features are categorized by system component:

### 2.1. Physical Machine Features

Each machine will be an IoT-enabled device with the following functionalities:

*   **Donor Interaction:**
    *   **Intuitive Touchscreen Interface:** For guiding donors through the process.
    *   **Food Detail Input:** Allow donors to specify the type of food (e.g., perishable, non-perishable - though initial request focused on quantity and expiry), quantity, and mandatory expiry date.
    *   **Automated Food Packing Cover Dispenser:** Provides standardized packaging.
    *   **Secure Food Intake Mechanism:** A compartment for depositing food, which then moves to internal storage.
    *   **Real-time Storage Capacity Check:** Before accepting donations.
    *   **Nearest Machine Redirection (Donor):** If the current machine is full, the interface will display the location and availability of the nearest alternative machine.
    *   **Donation Confirmation:** On-screen confirmation. No e-receipt or identity capture to maintain anonymity.

*   **Receiver Interaction:**
    *   **Simple Touchscreen Interface:** For requesting food.
    *   **Standardized Food Dispensing:** Dispense a pre-defined quantity (e.g., 2 packets) of available, non-expired food.
    *   **Food Availability Check:** Real-time check of available, non-expired food.
    *   **Nearest Machine Redirection (Receiver):** If food is unavailable or all available food is expired, the interface will display the location and availability of the nearest alternative machine.
    *   **Anonymity for Receivers:** No personal identification required at the machine for receiving food, as per the initial concept.

*   **Volunteer Interaction (at the machine):**
    *   **Secure Access:** Volunteers log in via a secure method (e.g., PIN, NFC card, or app-based authentication).
    *   **Expired Food Identification:** The machine interface will clearly list food items that are expired or nearing expiry (based on server data).
    *   **Guided Removal Process:** Interface to guide volunteers in removing specific expired items.
    *   **Confirmation of Removal:** Volunteers confirm removal, and the system updates inventory accordingly.

*   **General Machine Operations:**
    *   **Persistent Server Connectivity:** Via Wi-Fi or cellular network for real-time data sync.
    *   **Internal Climate Control:** (If applicable, depending on food types stored) to maintain food safety.
    *   **Tamper Detection & Alerts:** For security.
    *   **Remote Diagnostics & Status Monitoring:** For administrators.
    *   **Software Update Capability:** Over-the-air updates for machine software.

### 2.2. Server-Side System Features

The central server will be the backbone of the system:

*   **Machine Network Management:**
    *   Register, monitor, and manage all connected machines.
    *   Track machine status (online/offline, storage levels, errors, temperature if applicable).
*   **Inventory Management (Centralized):**
    *   Real-time tracking of food inventory (type, quantity, expiry dates) across all machines.
    *   Algorithm to flag expired or soon-to-expire food for volunteer attention.
*   **User Management (for Website Users):**
    *   Secure registration and authentication for Admins and Volunteers. Donors will interact anonymously and will not require registration.
*   **Location Services & Routing:**
    *   Maintain a database of machine locations.
    *   Algorithm to determine the "next nearest machine" based on availability and location.
*   **API Endpoints:**
    *   Secure APIs for communication with physical machines (reporting donations, dispensing food, updating status, volunteer actions).
    *   Secure APIs for the website (user authentication, data retrieval for dashboards, machine locations, etc.).
*   **Reporting & Analytics Engine:**
    *   Collect data on donations, dispensations, food wastage (expired items), machine uptime, volunteer activity.
    *   Generate reports for administrators.
*   **Notification System:**
    *   Alerts for admins (e.g., machine offline, critical errors).
    *   Alerts for volunteers (e.g., expired food in assigned machines).
*   **Database Management:** Secure and scalable database to store all system data.

### 2.3. Website Application Features

The website will serve as the primary interface for management, information, and coordination.

*   **General Website Features:**
    *   **Responsive Design:** Accessible on desktop and mobile devices.
    *   **Informational Pages:** About the initiative, how it works, impact stories (optional).
    *   **Machine Locator Map:** Publicly accessible map showing all machine locations. For donors, it will indicate machines with available storage space. For receivers, it will indicate machines with food currently available. It will also show operational hours and general status (e.g., temporarily out of service).

*   **Admin Portal:**
    *   **Dashboard:** Overview of system health, key metrics (total donations, food dispensed, active machines, volunteer activity, food expiry rates).
    *   **Machine Management:** Add/edit/remove machines, update locations, view detailed status and inventory of each machine, remotely trigger maintenance modes.
    *   **User Management:** Manage admin, donor (if registered), and volunteer accounts (approve registrations, assign roles, reset passwords).
    *   **Inventory Oversight:** View consolidated inventory across all machines, identify trends in food types and expiry.
    *   **Volunteer Coordination:** Assign machines to volunteers, track volunteer activity and performance.
    *   **Content Management:** Update informational pages on the website.
    *   **Reporting Suite:** Generate and download detailed reports on various aspects of the system.
    *   **System Configuration:** Set system-wide parameters (e.g., standard food packet quantity).

*   **Donor Portal (Optional, if donors register):**
    *   **Profile Management:** Manage personal information.
    *   **Donation History:** Track their past donations made via machines (if linked to their account).
    *   **Find a Machine:** Enhanced machine locator with filters.
    *   **Pledge Donations (Future Scope):** Indicate intent to donate specific items.

*   **Receiver Information Page (Public):**
    *   **Machine Locator:** Easy-to-use map to find nearest machines with food availability.
    *   **How to Use:** Simple instructions on using the machines.
    *   **FAQ:** Answers to common questions for receivers.

*   **Volunteer Portal:**
    *   **Profile Management:** Manage personal information and availability.
    *   **Dashboard:** View assigned machines, summary of tasks (e.g., expired food alerts).
    *   **Machine Status & Inventory:** View detailed status and inventory (especially expiry dates) of assigned machines.
    *   **Expired Food Alerts:** Receive notifications for machines requiring attention for expired food removal.
    *   **Task Management:** Accept tasks, log collection of expired food (confirmation can also be at the machine).
    *   **Communication Hub:** Receive messages from admins.

## 3. Proposed System Architecture

A three-tier architecture is proposed:

### 3.1. Tier 1: Physical Machines (IoT Devices)

*   **Hardware:** Each machine will consist of:
    *   Microcontroller/Single-Board Computer (e.g., Raspberry Pi, Arduino with network capabilities) for processing and control.
    *   Touchscreen display for user interaction.
    *   Sensors for detecting food deposits, storage levels, door status, internal temperature (optional).
    *   Actuators for dispensing packing covers and food items.
    *   Network interface (Wi-Fi/Ethernet/Cellular) for server communication.
    *   Secure storage for food.
    *   Optional: Barcode/QR code scanner (for future enhancements like tracking specific donated items).
*   **Software:**
    *   Embedded Linux or RTOS.
    *   Application software (e.g., Python, C++) to manage UI, hardware interactions, and communication with the server via secure APIs (HTTPS/MQTT).
    *   Local caching mechanism for essential data in case of temporary network loss (e.g., machine location, basic operational logic).

### 3.2. Tier 2: Server-Side Application (Backend)

*   **Technology Stack:**
    *   **Web Framework:** Flask (Python-based) is recommended due to its flexibility, scalability, and suitability for API development and database interaction, aligning with the knowledge module guidance.
    *   **Database:** A relational database like PostgreSQL or MySQL for structured data (users, machines, inventory, logs). PostgreSQL is often favored for its robustness and advanced features.
    *   **API Design:** RESTful APIs for communication between machines and the server, and between the website frontend and the server.
    *   **Authentication:** Token-based authentication (e.g., JWT) for securing API endpoints.
*   **Deployment:**
    *   Cloud-based hosting (e.g., AWS, Google Cloud, Azure) for scalability, reliability, and manageability.
    *   Containerization (e.g., Docker) and orchestration (e.g., Kubernetes) for easier deployment and scaling.
*   **Key Modules:** (as described in Server-Side System Features)
    *   Machine Communication Interface
    *   Inventory Management Logic
    *   User Authentication & Authorization
    *   API Gateway
    *   Reporting Service
    *   Notification Service

### 3.3. Tier 3: Website Application (Frontend)

*   **Technology Stack:**
    *   **Option 1 (Integrated with Flask):** Use Flask with templating engines (e.g., Jinja2) to serve HTML, CSS, and JavaScript. Suitable for sites where interactivity is moderate.
    *   **Option 2 (Decoupled Frontend):** Use a modern JavaScript framework like React, Vue, or Angular for a more dynamic and interactive user experience. This would communicate with the Flask backend via APIs. Given the complexity of different user portals and dashboards, a decoupled frontend might offer better maintainability and user experience in the long run. The knowledge module mentions `create_react_app` for static/frontend applications, but React can also be used for dynamic frontends consuming APIs.
    *   **Styling:** CSS frameworks like Bootstrap or Tailwind CSS for responsive design.
    *   **Mapping:** Integration with a mapping service (e.g., Leaflet, Google Maps API, OpenStreetMap) for the machine locator.
*   **Key Components:** (as described in Website Application Features)
    *   Public Informational Pages
    *   Admin Portal SPA (Single Page Application)
    *   Donor Portal SPA (if implemented)
    *   Volunteer Portal SPA
    *   Machine Locator Component

### 3.4. Data Flow Example (Food Donation)

1.  **Donor** approaches machine, selects "Donate Food".
2.  **Machine UI** prompts for quantity and expiry date.
3.  **Donor** inputs details.
4.  **Machine** sends a pre-check request to the **Server API** (Is there space? Is this a valid request?).
5.  **Server** validates, checks machine capacity, responds to **Machine**.
6.  If OK, **Machine** dispenses packing cover, opens intake.
7.  **Donor** deposits food.
8.  **Machine** confirms deposit (e.g., weight sensor, compartment sensor), sends donation details (food type (if captured), quantity, expiry, timestamp, machine ID) to **Server API**.
9.  **Server** updates central inventory, logs the donation.
10. **Machine UI** shows confirmation to donor.
11. **Admin/Volunteer Portals** on the website can now reflect the updated inventory for that machine.

## 4. Next Steps

This proposal provides a comprehensive overview of the envisioned system. The next step is to validate these features and architectural choices with the user, gather feedback, and refine the plan accordingly. Following user approval, detailed design and development phases can commence.

