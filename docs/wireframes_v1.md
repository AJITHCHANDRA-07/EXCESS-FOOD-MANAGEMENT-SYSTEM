# Low-Fidelity Wireframes: Exes Food Management System

This document provides textual low-fidelity wireframes for key screens of the Exes Food Management System, based on the `ui_ux_design_document.md`.

**Legend:**
*   `[Text Label]` : Represents a text label or static text.
*   `{Button: Text}` : Represents a clickable button.
*   `{Input: Placeholder}` : Represents an input field.
*   `{Link: Text}` : Represents a hyperlink.
*   `(Image/Icon: Description)` : Represents an image or icon.
*   `--- Screen Separator ---` : Separates different screens.

## 1. Machine Interface Wireframes

### 1.1. Main Screen / Idle State

```
+------------------------------------+
| (Image: System Logo/Name)          |
| [Exes Food Management System]      |
|                                    |
| [Donate Food. Receive Food.        |
|  Help Your Community.]             |
|                                    |
| {Button: Donate Food}              |
| {Button: Receive Food}             |
|                                    |
| [Status: Accepting Donations]      |
| {Link: Volunteer Access}           |
+------------------------------------+
```

--- Screen Separator ---

### 1.2. Donor Flow - Screen 1: Instructions & Pre-check (After tapping "Donate Food")

```
+------------------------------------+
| [Thank you for donating!]          |
| [Please ensure food is unopened    |
|  and not past its expiry date.]    |
|                                    |
| (System checking space...)         |
|                                    |
| IF NO SPACE:                       |
|   [Sorry, this machine is full.    |
|    Please check website for        |
|    nearest available machine.]     |
|   (QR Code: Website Link)          |
|   {Button: Back to Main}           |
|                                    |
| IF SPACE AVAILABLE:                |
|   (Proceeds to Donor Screen 2)     |
+------------------------------------+
```

--- Screen Separator ---

### 1.3. Donor Flow - Screen 2: Input Food Details

```
+------------------------------------+
| [Enter Food Details]               |
|                                    |
| [Food Expiry Date (YYYY-MM-DD):]   |
| {Input: Date Picker/Numeric}       |
|                                    |
| [Quantity (items/packets):]        |
| {Input: Numeric +/- or Keypad}     |
|                                    |
| {Button: Cancel} {Button: Next}    |
+------------------------------------+
```

--- Screen Separator ---

### 1.4. Donor Flow - Screen 3: Dispense Cover & Deposit

```
+------------------------------------+
| [Prepare Your Donation]            |
|                                    |
| [Please take a packing cover       |
|  from the dispenser below.]        |
|                                    |
| [Place your item(s) in the deposit |
|  slot when it opens.]              |
|                                    |
| (Animation: Slot opening/timer)    |
+------------------------------------+
```

--- Screen Separator ---

### 1.5. Donor Flow - Screen 4: Confirmation

```
+------------------------------------+
| (Icon: Success Checkmark)          |
| [Thank you!]                       |
| [Your donation has been received.] |
|                                    |
| {Button: Finish}                   |
+------------------------------------+
```

--- Screen Separator ---

### 1.6. Receiver Flow - Screen 1: Availability & Dispensing (After tapping "Receive Food")

```
+------------------------------------+
| (System checking availability...)  |
|                                    |
| IF NO FOOD:                        |
|   [Sorry, no food is currently     |
|    available at this machine.      |
|    Please check website for        |
|    nearest machine with food.]     |
|   (QR Code: Website Link)          |
|   {Button: Back to Main}           |
|                                    |
| IF FOOD AVAILABLE:                 |
|   [Dispensing 2 items...]          |
|   [Please collect your items       |
|    from the slot below.]           |
+------------------------------------+
```

--- Screen Separator ---

### 1.7. Receiver Flow - Screen 2: Confirmation

```
+------------------------------------+
| (Icon: Success Checkmark)          |
| [Items Dispensed!]                 |
| [We hope this helps!]              |
|                                    |
| {Button: Finish}                   |
+------------------------------------+
```

--- Screen Separator ---

### 1.8. Volunteer Flow - Screen 1: Login (After tapping "Volunteer Access")

```
+------------------------------------+
| [Volunteer Access]                 |
|                                    |
| [Enter PIN Code:]                  |
| {Input: PIN Pad}                   |
|                                    |
| OR                                 |
| [Scan Volunteer Badge]             |
| (Area for badge scan)              |
|                                    |
| {Button: Cancel} {Button: Login}   |
+------------------------------------+
```

--- Screen Separator ---

### 1.9. Volunteer Flow - Screen 2: Volunteer Dashboard

```
+------------------------------------+
| [Welcome, Volunteer Name!]         |
|                                    |
| {Button: View/Remove Expired Food} |
| {Button: Machine Status Report}    |
|                                    |
| {Button: Logout}                   |
+------------------------------------+
```

--- Screen Separator ---

### 1.10. Volunteer Flow - Screen 3: View Expired Food

```
+------------------------------------+
| [Expired Food Items - Machine X]   |
|                                    |
| [Item ID | Expiry | Donated On]    |
| [--------------------------------] |
| [12345   | 2025-05-10 | 2025-05-01] {Checkbox} |
| [12346   | 2025-05-12 | 2025-05-03] {Checkbox} |
| ...                                |
|                                    |
| [Please identify and remove items. |
|  Check boxes for removed items.]   |
| {Button: Back} {Button: Confirm Removal} |
+------------------------------------+
```

## 2. Web Application Wireframes

### 2.1. Public - Machine Locator Page

```
+--------------------------------------------------------------------+
| Header: [Logo] {Link: Home} {Link: Find Machine} {Link: About} ... |
+--------------------------------------------------------------------+
| [Find a Food Machine]                                              |
|                                                                    |
| {Toggle Button: I want to DONATE} {Toggle Button: I want to RECEIVE FOOD} |
| {Input: Search Location (Address/Zip)} {Button: Search}            |
|                                                                    |
| +----------------------------------------------------------------+ |
| | (Interactive Map Area)                                         | |
| | - Marker 1 (Machine A - Green for Donate, Blue for Receive)    | |
| | - Marker 2 (Machine B)                                         | |
| +----------------------------------------------------------------+ |
|                                                                    |
| IF Marker Clicked:                                                 |
|   [Machine A Details]                                              |
|   [Address: 123 Main St]                                           |
|   [Hours: 24/7]                                                    |
|   [Status: Accepting Donations: High Capacity / Food Available: Good Stock] |
+--------------------------------------------------------------------+
```

--- Screen Separator ---

### 2.2. Admin Portal - Dashboard

```
+--------------------------------------------------------------------+
| Header: [Logo] [Admin Portal] {Link: Dashboard} {Link: Machines} ... {Link: Logout} |
+--------------------------------------------------------------------+
| [Admin Dashboard]                                                  |
|                                                                    |
| +----------------------+  +----------------------+  +----------------------+ |
| | [Total Machines]     |  | [Active Machines]    |  | [Donations Today]    | |
| | [Value: 50]          |  | [Value: 48]          |  | [Value: 120 items]   | |
| +----------------------+  +----------------------+  +----------------------+ |
|                                                                    |
| +----------------------+  +----------------------+  +----------------------+ |
| | [Dispensed Today]    |  | [Volunteer Activity] |  | [Expired Items Alert]| |
| | [Value: 80 items]    |  | [Value: 5 active]    |  | [Value: 3 machines]  | |
| +----------------------+  +----------------------+  +----------------------+ |
|                                                                    |
| [Recent Alerts/Notifications Area]                                 |
| - Machine X offline                                                |
| - Low stock region Y                                               |
+--------------------------------------------------------------------+
```

--- Screen Separator ---

### 2.3. Admin Portal - Machine Management Page

```
+--------------------------------------------------------------------+
| Header: [Logo] [Admin Portal] ... {Link: Machines} ... {Link: Logout} |
+--------------------------------------------------------------------+
| [Machine Management] {Button: + Add New Machine}                   |
|                                                                    |
| [Filter Options: Status, Location] {Input: Search by ID/Address}   |
|                                                                    |
| +------------------------------------------------------------------+ |
| | ID | Location    | Status | Storage | Last Heartbeat | Actions  | |
| |----|-------------|--------|---------|----------------|----------| |
| | 01 | 123 Main St | Active | 75/100  | 2 mins ago     | {Edit} {View} | |
| | 02 | 456 Oak Ave | Maint. | 0/50    | 1 hour ago     | {Edit} {View} | |
| | ...| ...         | ...    | ...     | ...            | ...      | |
| +------------------------------------------------------------------+ |
| [Pagination Controls]                                              |
+--------------------------------------------------------------------+
```

--- Screen Separator ---

### 2.4. Volunteer Portal - Dashboard

```
+--------------------------------------------------------------------+
| Header: [Logo] [Volunteer Portal] {Link: Dashboard} ... {Link: Logout} |
+--------------------------------------------------------------------+
| [Welcome, Volunteer Name!]                                         |
|                                                                    |
| [Machines Requiring Attention (Expired Food):]                     |
| - Machine A (5 items) {Link: View Details}                         |
| - Machine C (2 items) {Link: View Details}                         |
|                                                                    |
| [My Assigned Machines (if applicable):]                            |
| - Machine A {Link: View Status}                                    |
|                                                                    |
| {Button: View All Expired Food Reports}                            |
+--------------------------------------------------------------------+
```

This provides a basic structural outline for the key screens. Visual design, specific iconography, and detailed component states would be developed in high-fidelity mockups.
