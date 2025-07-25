# UI/UX Design Document: Exes Food Management System

## 1. Introduction

This document outlines the User Interface (UI) and User Experience (UX) design considerations for the Exes Food Management System. It covers both the physical machine interface and the web application. The goal is to create intuitive, accessible, and efficient interfaces for all user types (donors, receivers, volunteers, and administrators).

## 2. General Design Principles

*   **Simplicity:** Interfaces should be clean, uncluttered, and easy to understand, especially for donors and receivers who may be in a hurry or less tech-savvy.
*   **Clarity:** Information and instructions should be clear, concise, and unambiguous. Use universally understood icons where appropriate.
*   **Efficiency:** Users should be able to complete their tasks with minimal steps and effort.
*   **Accessibility:** Design with accessibility in mind (e.g., sufficient contrast, legible fonts, considerations for users with disabilities where feasible for a physical kiosk).
*   **Consistency:** Maintain a consistent design language (colors, typography, layout) across the machine interface and web application where appropriate.
*   **Feedback:** Provide clear feedback to users for their actions (e.g., confirmation messages, progress indicators).
*   **Anonymity (Donor/Receiver):** The design must reinforce the anonymity of donors and receivers at the machine and on public-facing website features.

## 3. Machine Interface (Touchscreen)

The machine interface will be a touchscreen designed for public use. It needs to be robust and easy to navigate.

### 3.1. Visual Style & Branding (Placeholder - Awaiting User Input)

*   **Color Scheme:** To be determined. Suggestion: Calm, trustworthy colors (e.g., greens, blues) with clear accent colors for calls to action.
*   **Typography:** Clear, legible sans-serif fonts suitable for screen display.
*   **Iconography:** Simple, universally recognizable icons.

### 3.2. Main Screen / Idle State

*   **Content:**
    *   Clear branding (Exes Food Management System logo/name).
    *   Brief statement of purpose (e.g., "Donate Food. Receive Food. Help Your Community.").
    *   Two primary buttons: "Donate Food" and "Receive Food".
    *   Smaller button/link for "Volunteer Access" (less prominent, possibly requiring a specific gesture or code to activate if not a physical button).
    *   Indication of machine status (e.g., "Accepting Donations", "Food Available", "Temporarily Out of Service").

### 3.3. Donor Interaction Flow

1.  **Tap "Donate Food" on Main Screen.**
2.  **Screen 1: Instructions & Pre-check**
    *   Message: "Thank you for donating! Please ensure food is unopened and not past its expiry date."
    *   System automatically checks if there is space. 
        *   If NO space: Message "Sorry, this machine is currently full. Please check the website for the nearest machine with available space." (Display QR code to website or nearest machine info if possible).
        *   If YES space: Proceed.
3.  **Screen 2: Input Food Details**
    *   Prompt: "Enter Food Expiry Date (YYYY-MM-DD)" (Large, easy-to-use date picker or numeric input).
    *   Prompt: "Enter Quantity (number of items/packets)" (Simple numeric input, e.g., +/- buttons or keypad).
    *   Button: "Next".
4.  **Screen 3: Dispense Packing Cover & Deposit Food**
    *   Message: "Please take a packing cover from the dispenser below."
    *   Message: "Place your item(s) in the deposit slot when it opens."
    *   (Machine dispenses cover, opens deposit slot).
    *   On-screen animation or timer indicating deposit window.
5.  **Screen 4: Confirmation**
    *   Message: "Thank you! Your donation has been received."
    *   (Deposit slot closes).
    *   Button: "Finish" (returns to Main Screen).

### 3.4. Receiver Interaction Flow

1.  **Tap "Receive Food" on Main Screen.**
2.  **Screen 1: Availability Check & Dispensing**
    *   System automatically checks for available, non-expired food.
        *   If NO food: Message "Sorry, no food is currently available at this machine. Please check the website for the nearest machine with food." (Display QR code to website or nearest machine info if possible).
        *   If YES food: Message "Dispensing food. Please collect your items from the slot below." (e.g., "Dispensing 2 items").
    *   (Machine dispenses food).
3.  **Screen 2: Confirmation**
    *   Message: "Items dispensed. We hope this helps!"
    *   Button: "Finish" (returns to Main Screen).

### 3.5. Volunteer Interaction Flow

1.  **Access Volunteer Mode (e.g., tap "Volunteer Access" or specific corner of screen, then enter PIN/scan badge).**
2.  **Screen 1: Volunteer Dashboard (Simplified)**
    *   Welcome message: "Welcome, Volunteer!"
    *   Option 1: "View/Remove Expired Food".
    *   Option 2: "Machine Status Report" (basic diagnostics, if applicable).
    *   Button: "Logout".
3.  **Screen 2: View Expired Food (If Option 1 selected)**
    *   List of expired food items: Item ID (internal), Expiry Date, Date Donated.
    *   Instruction: "Please identify and remove the following items."
    *   Button next to each item or a general button: "Confirm Removal of Selected Items".
4.  **Screen 3: Confirm Removal**
    *   Message: "Items marked as removed. Thank you for your service!"
    *   Button: "Back to Volunteer Menu" or "Logout".

## 4. Web Application UI/UX

The web application will have distinct sections for Public users, Volunteers, and Administrators.

### 4.1. Visual Style & Branding (Placeholder - Awaiting User Input)

*   **Color Scheme:** Consistent with machine interface, but adapted for web. Professional and clean.
*   **Typography:** Web-safe, highly legible sans-serif fonts.
*   **Layout:** Responsive design (desktop, tablet, mobile).
*   **Iconography:** Consistent with machine where applicable, standard web icons.

### 4.2. Public Pages

*   **Homepage:**
    *   Hero section: Mission statement, call to action (Find a Machine).
    *   Brief explanation of how it works (for donors, for receivers).
    *   Impact statistics (e.g., total food donated/received - if desired).
    *   Navigation: Home, Find a Machine, About Us, How to Help (Volunteer Info), FAQ.
*   **Find a Machine (Machine Locator):**
    *   Interactive map (e.g., Leaflet, OpenStreetMap, Google Maps).
    *   Markers for each machine.
    *   Filter/Toggle: 
        *   "I want to DONATE" (shows machines with available storage space, color-coded or icon indicator).
        *   "I want to RECEIVE FOOD" (shows machines with available food, color-coded or icon indicator).
    *   Clicking a marker shows: Machine Address, Operational Hours, Status (e.g., "Accepting Donations: High Capacity", "Food Available: Good Stock", "Temporarily Out of Service").
    *   Search bar for location (address, zip code).
*   **About Us:** Information about the organization/initiative.
*   **How to Help:** Information for potential volunteers, link to volunteer registration/login.
*   **FAQ:** Common questions for donors, receivers, volunteers.

### 4.3. Volunteer Portal

*   **Login Page:** Secure login for registered volunteers.
*   **Dashboard:**
    *   Welcome message.
    *   Overview: Assigned machines (if applicable), machines needing attention (expired food alerts).
    *   Quick links: View Expired Food List, Log Activity.
*   **Machines with Expired Food Page:**
    *   List of machines with expired items (Machine ID, Address, Number of expired items).
    *   Link to view details for each machine.
*   **Machine Detail Page (for Volunteers):**
    *   Specific machine inventory, highlighting expired items.
    *   Ability to confirm removal of items (if not done at machine, or as a secondary confirmation).
*   **Activity Log (Optional):** View past actions.
*   **Profile Management:** Update contact info, availability.

### 4.4. Admin Portal

*   **Login Page:** Secure login for administrators.
*   **Dashboard:**
    *   System overview: Total machines, active machines, total donations (count/volume), total food dispensed, volunteer activity summary, food expiry rates/trends.
    *   Key alerts (e.g., machines offline, critically low stock in an area).
*   **Machine Management Page:**
    *   Table/List of all machines: ID, Location, Status, Current Storage, Max Storage, Last Heartbeat.
    *   Actions: Add New Machine, Edit Machine Details (location, capacity, status), Remove Machine.
    *   View detailed inventory and history for each machine.
*   **User Management Page:**
    *   Tabs for Admins and Volunteers.
    *   List users: Username, Role, Date Registered.
    *   Actions: Add New Admin/Volunteer, Edit User (reset password, change role), Deactivate User.
*   **Inventory Oversight Page:**
    *   Consolidated view of inventory across all machines.
    *   Filters by food type (if implemented), expiry date range.
    *   Identify trends, potential shortages or overstock.
*   **Reporting Suite Page:**
    *   Generate reports: Donation trends, dispensation rates, volunteer hours/activity, food wastage, machine uptime.
    *   Export options (e.g., CSV, PDF).
*   **System Configuration Page (Optional):** Manage global settings.
*   **Content Management (Optional):** Edit content for public informational pages.

## 5. Next Steps

*   Gather user feedback on these initial UI/UX considerations.
*   Develop low-fidelity wireframes for key screens.
*   Iterate on wireframes based on feedback.
*   Develop high-fidelity mockups for selected screens.
*   Create a style guide.

