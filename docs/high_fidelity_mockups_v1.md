# High-Fidelity Mockup Descriptions: Exes Food Management System

This document provides textual descriptions of high-fidelity mockups for key screens of the Exes Food Management System. These descriptions are based on the `ui_ux_design_document.md`, `wireframes_v1.md`, and `style_guide_v1.md`.

**Refer to `style_guide_v1.md` for specific color codes, font families, and icon styles.**

## 1. Machine Interface Mockups

**General Machine Interface Style:**
*   **Background:** `#F5F5F5` (Light Gray)
*   **Text:** Headings in Montserrat Bold, body/button text in Montserrat Semi-Bold or Open Sans Regular. Primary text color `#333333`.
*   **Buttons:** Large, touch-friendly with rounded corners (8px). Primary buttons use `#50C878` (Green) with white text. Secondary/cancel buttons might use `#F8D147` (Yellow) or an outline style.
*   **Overall:** Clean, spacious, with clear visual hierarchy.

### 1.1. Main Screen / Idle State (Conceptual Image: `/home/ubuntu/mockups/machine_main_screen.png`)

*   **Layout:** Centered content.
*   **Top:** System Logo (to be designed - placeholder: simple icon with text "Exes Food System"). Below it, the text "Exes Food Management System" in Montserrat Bold, `#333333`.
*   **Middle:** Tagline "Donate Food. Receive Food. Help Your Community." in Open Sans Regular, `#666666`.
*   **Action Buttons (Large, stacked vertically with spacing):**
    *   `{Button: Donate Food}`: Solid `#50C878` (Green) background, white text (Montserrat Semi-Bold, ~24px). Icon (e.g., hand holding box) to the left of text.
    *   `{Button: Receive Food}`: Solid `#50C878` (Green) background, white text (Montserrat Semi-Bold, ~24px). Icon (e.g., shopping bag) to the left of text.
*   **Bottom:**
    *   Status text: e.g., "Status: Accepting Donations" in Open Sans Regular, `#333333`.
    *   Volunteer Access: Smaller text link or subtle button "Volunteer Access" in `#666666` (Open Sans Regular).

--- Mockup Separator ---

### 1.2. Donor Flow - Screen 2: Input Food Details

*   **Header:** "Enter Food Details" (Montserrat Bold, `#333333`).
*   **Expiry Date Input:**
    *   Label: "Food Expiry Date (YYYY-MM-DD):" (Open Sans Regular, `#333333`).
    *   Input Field: Large, clear date picker interface. Background `#FFFFFF`, border `#DDDDDD`. Selected date in Montserrat Regular.
*   **Quantity Input:**
    *   Label: "Quantity (items/packets):" (Open Sans Regular, `#333333`).
    *   Input Field: Numeric input with large `+` and `-` buttons. Background `#FFFFFF`, border `#DDDDDD`. Number displayed in Montserrat Regular.
*   **Navigation Buttons (Bottom):**
    *   `{Button: Cancel}`: Outline style, border `#DDDDDD`, text `#666666`.
    *   `{Button: Next}`: Solid `#50C878` (Green) background, white text.

--- Mockup Separator ---

## 2. Web Application Mockups

**General Web Application Style:**
*   **Background:** Main content area `#F5F5F5` or `#FFFFFF` for cards/sections.
*   **Text:** Headings in Montserrat, body in Open Sans. Colors as per style guide.
*   **Navigation:** Main navigation bar likely a darker shade (e.g., `#FFFFFF` with shadow, or a muted primary color) with links in Montserrat or Open Sans.

### 2.1. Public - Machine Locator Page (Conceptual Image: `/home/ubuntu/mockups/web_machine_locator.png`)

*   **Header:** Logo on left. Navigation links ("Home", "Find Machine", "About Us", "Volunteer") in Open Sans Semi-Bold, `#333333`. Active link highlighted with `#50C878` underline.
*   **Page Title:** "Find a Food Machine" (Montserrat Bold, 32px, `#333333`).
*   **Controls Area (below title):**
    *   Toggle Buttons: `I want to DONATE` / `I want to RECEIVE FOOD`. Styled as segmented controls or distinct buttons. Active state uses `#50C878`.
    *   Search Input: `{Input: Search by Address or Zip Code...}`. White background, `#DDDDDD` border. Search icon inside or next to it.
    *   `{Button: Search}`: Primary color `#50C878`.
*   **Map Area:** Large interactive map (e.g., OpenStreetMap styled to match theme). Markers are custom icons (e.g., green pin for donate availability, yellow pin for receive availability).
*   **Marker Info Popup (on click):**
    *   Card style with white background, rounded corners, subtle shadow.
    *   Machine Address (Montserrat Semi-Bold).
    *   Operational Hours (Open Sans Regular).
    *   Status: e.g., "Accepting Donations: High Capacity" (Green text/icon) or "Food Available: 15 items" (Yellow text/icon).

--- Mockup Separator ---

### 2.2. Admin Portal - Dashboard (Conceptual Image: `/home/ubuntu/mockups/admin_dashboard.png`)

*   **Layout:** Two-column or three-column layout for metric cards. Main content area `#F5F5F5`.
*   **Header/Sidebar Navigation:** Admin portal branding. Navigation links (Dashboard, Machines, Users, Reports, etc.) in Montserrat. Active link highlighted.
*   **Page Title:** "Admin Dashboard" (Montserrat Bold, 32px, `#333333`).
*   **Metric Cards:**
    *   White background (`#FFFFFF`), rounded corners (8px), subtle shadow.
    *   Title (e.g., "Total Machines", "Active Machines") in Montserrat Semi-Bold, `#666666`.
    *   Value (e.g., "50", "48") in large Montserrat Bold, `#333333`.
    *   Small icon related to the metric (e.g., server icon for machines) in `#50C878` or `#F8D147`.
*   **Charts/Graphs (Placeholder):** Area for potential charts (e.g., donations over time) using theme colors.
*   **Recent Alerts/Notifications Area:** Card style. List of alerts with icons (e.g., warning icon in `#FFC107`, error icon in `#DC3545`).

--- Mockup Separator ---

### 2.3. Admin Portal - Machine Management Page

*   **Page Title:** "Machine Management" (Montserrat Bold, 32px, `#333333`).
*   **Action Button (Top Right):** `{Button: + Add New Machine}` (Primary color `#50C878`).
*   **Filters/Search Area:** Inputs for filtering by status, location. Search bar for ID/Address.
*   **Machine Table:**
    *   Header row with dark gray background (`#E0E0E0`) or bold text.
    *   Columns: ID, Location, Status (e.g., colored badges: Green for Active, Yellow for Maintenance, Red for Offline), Storage (e.g., 75/100), Last Heartbeat, Actions.
    *   Action buttons (`Edit`, `View`) styled as small icon buttons or text links.
    *   Alternating row colors (`#FFFFFF` and `#F9F9F9`) for readability.
*   **Pagination:** Standard pagination controls at the bottom.

These descriptions aim to provide a clearer picture of the visual design. Actual mockups would involve graphical tools to create these screens visually.
