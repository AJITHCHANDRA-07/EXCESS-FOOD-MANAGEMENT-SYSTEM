#!/usr/bin/env python3
# main.py - Main entry point for the Exes Food Management System machine software

import os
import sys
import logging
import sqlite3
import tkinter as tk
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("machine.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("ExesMachine")

class ExesFoodMachine:
    """Main class for the Exes Food Management System machine software."""
    
    def __init__(self, machine_id="MACHINE001"):
        """Initialize the machine software with the given machine ID."""
        self.machine_id = machine_id
        self.logger = logging.getLogger(f"ExesMachine.{machine_id}")
        self.logger.info(f"Initializing machine {machine_id}")
        
        # Initialize database
        self.init_database()
        
        # Initialize UI
        self.init_ui()
        
    def init_database(self):
        """Initialize the SQLite database for local storage."""
        self.logger.info("Initializing local database")
        try:
            db_path = os.path.join(os.path.dirname(__file__), "machine_data.db")
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            
            # Create tables if they don't exist
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
            self.logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Database initialization error: {e}")
            raise
    
    def init_ui(self):
        """Initialize the Tkinter UI."""
        self.logger.info("Initializing user interface")
        self.root = tk.Tk()
        self.root.title(f"Exes Food Machine - {self.machine_id}")
        self.root.geometry("800x600")  # Set window size for touchscreen
        
        # Configure full screen for actual deployment
        # self.root.attributes('-fullscreen', True)
        
        # Create a frame for the main content
        self.main_frame = tk.Frame(self.root, bg="#50C878")  # Using the green from our style guide
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create welcome screen
        self.show_welcome_screen()
    
    def show_welcome_screen(self):
        """Display the welcome screen with options for donors and receivers."""
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add title
        title_label = tk.Label(
            self.main_frame, 
            text="Welcome to Exes Food Management System",
            font=("Montserrat", 24, "bold"),
            bg="#50C878",
            fg="white"
        )
        title_label.pack(pady=(50, 30))
        
        # Add subtitle
        subtitle_label = tk.Label(
            self.main_frame, 
            text="Please select an option:",
            font=("Open Sans", 18),
            bg="#50C878",
            fg="white"
        )
        subtitle_label.pack(pady=(0, 50))
        
        # Create a frame for buttons
        button_frame = tk.Frame(self.main_frame, bg="#50C878")
        button_frame.pack()
        
        # Donor button
        donor_button = tk.Button(
            button_frame,
            text="I want to DONATE food",
            font=("Open Sans", 16, "bold"),
            bg="#F8D147",  # Yellow from our style guide
            fg="#4A4A4A",
            padx=20,
            pady=15,
            borderwidth=0,
            command=self.show_donor_screen
        )
        donor_button.pack(pady=10, ipadx=10)
        
        # Receiver button
        receiver_button = tk.Button(
            button_frame,
            text="I want to RECEIVE food",
            font=("Open Sans", 16, "bold"),
            bg="#F8D147",  # Yellow from our style guide
            fg="#4A4A4A",
            padx=20,
            pady=15,
            borderwidth=0,
            command=self.show_receiver_screen
        )
        receiver_button.pack(pady=10, ipadx=10)
        
        # Admin button (smaller and less prominent)
        admin_button = tk.Button(
            self.main_frame,
            text="Admin / Maintenance",
            font=("Open Sans", 12),
            bg="#50C878",
            fg="white",
            borderwidth=0,
            command=self.show_admin_login
        )
        admin_button.pack(side=tk.BOTTOM, pady=20)
    
    def show_donor_screen(self):
        """Display the donor input screen."""
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add title
        title_label = tk.Label(
            self.main_frame, 
            text="Donate Food",
            font=("Montserrat", 24, "bold"),
            bg="#50C878",
            fg="white"
        )
        title_label.pack(pady=(50, 30))
        
        # Create a frame for the form
        form_frame = tk.Frame(self.main_frame, bg="#50C878")
        form_frame.pack(pady=20)
        
        # Quantity selection
        quantity_label = tk.Label(
            form_frame,
            text="Estimated Quantity (number of items):",
            font=("Open Sans", 14),
            bg="#50C878",
            fg="white"
        )
        quantity_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        quantity_var = tk.StringVar(value="1")
        quantity_options = ["1", "2", "3", "4", "5", "6+"]
        
        quantity_menu = tk.OptionMenu(form_frame, quantity_var, *quantity_options)
        quantity_menu.config(font=("Open Sans", 14), bg="white", width=10)
        quantity_menu.grid(row=0, column=1, sticky="w", padx=20, pady=(0, 10))
        
        # Expiry date selection
        expiry_label = tk.Label(
            form_frame,
            text="Expiry Date:",
            font=("Open Sans", 14),
            bg="#50C878",
            fg="white"
        )
        expiry_label.grid(row=1, column=0, sticky="w", pady=(10, 10))
        
        # Simple date selection for prototype
        # In a real implementation, use a date picker widget
        expiry_frame = tk.Frame(form_frame, bg="#50C878")
        expiry_frame.grid(row=1, column=1, sticky="w", padx=20, pady=(10, 10))
        
        # Get today's date for default values
        today = datetime.now()
        
        # Day
        day_var = tk.StringVar(value=str(today.day))
        day_options = [str(i) for i in range(1, 32)]
        day_menu = tk.OptionMenu(expiry_frame, day_var, *day_options)
        day_menu.config(font=("Open Sans", 14), bg="white", width=3)
        day_menu.pack(side=tk.LEFT, padx=(0, 5))
        
        # Month
        month_var = tk.StringVar(value=str(today.month))
        month_options = [str(i) for i in range(1, 13)]
        month_menu = tk.OptionMenu(expiry_frame, month_var, *month_options)
        month_menu.config(font=("Open Sans", 14), bg="white", width=3)
        month_menu.pack(side=tk.LEFT, padx=5)
        
        # Year
        year_var = tk.StringVar(value=str(today.year))
        year_options = [str(today.year + i) for i in range(3)]  # Current year and next 2 years
        year_menu = tk.OptionMenu(expiry_frame, year_var, *year_options)
        year_menu.config(font=("Open Sans", 14), bg="white", width=5)
        year_menu.pack(side=tk.LEFT, padx=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.main_frame, bg="#50C878")
        buttons_frame.pack(pady=40)
        
        # Back button
        back_button = tk.Button(
            buttons_frame,
            text="Back",
            font=("Open Sans", 14),
            bg="#4A4A4A",
            fg="white",
            padx=15,
            pady=10,
            command=self.show_welcome_screen
        )
        back_button.pack(side=tk.LEFT, padx=10)
        
        # Continue button
        def on_continue():
            # In a real implementation, validate inputs and proceed
            # For now, just show the confirmation screen
            quantity = quantity_var.get()
            expiry_date = f"{year_var.get()}-{month_var.get().zfill(2)}-{day_var.get().zfill(2)}"
            self.show_donor_confirmation(quantity, expiry_date)
        
        continue_button = tk.Button(
            buttons_frame,
            text="Continue",
            font=("Open Sans", 14, "bold"),
            bg="#F8D147",  # Yellow from our style guide
            fg="#4A4A4A",
            padx=15,
            pady=10,
            command=on_continue
        )
        continue_button.pack(side=tk.LEFT, padx=10)
    
    def show_donor_confirmation(self, quantity, expiry_date):
        """Display the donation confirmation screen."""
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add title
        title_label = tk.Label(
            self.main_frame, 
            text="Confirm Donation",
            font=("Montserrat", 24, "bold"),
            bg="#50C878",
            fg="white"
        )
        title_label.pack(pady=(50, 30))
        
        # Create a frame for the confirmation details
        confirm_frame = tk.Frame(self.main_frame, bg="#50C878")
        confirm_frame.pack(pady=20)
        
        # Display donation details
        details_text = f"You are donating {quantity} item(s) with expiry date: {expiry_date}"
        details_label = tk.Label(
            confirm_frame,
            text=details_text,
            font=("Open Sans", 16),
            bg="#50C878",
            fg="white",
            wraplength=600
        )
        details_label.pack(pady=10)
        
        # Instructions
        instructions_label = tk.Label(
            confirm_frame,
            text="Please place your food items in the donation compartment when it opens.",
            font=("Open Sans", 14),
            bg="#50C878",
            fg="white",
            wraplength=600
        )
        instructions_label.pack(pady=20)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.main_frame, bg="#50C878")
        buttons_frame.pack(pady=40)
        
        # Back button
        back_button = tk.Button(
            buttons_frame,
            text="Back",
            font=("Open Sans", 14),
            bg="#4A4A4A",
            fg="white",
            padx=15,
            pady=10,
            command=self.show_donor_screen
        )
        back_button.pack(side=tk.LEFT, padx=10)
        
        # Confirm button
        def on_confirm():
            # In a real implementation:
            # 1. Open the donation compartment
            # 2. Record the donation in the database
            # 3. Sync with the backend when possible
            
            # For now, simulate adding to database
            try:
                self.cursor.execute('''
                INSERT INTO food_items (entry_timestamp, expiry_date, quantity, storage_location, status)
                VALUES (?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    expiry_date,
                    int(quantity.replace("+", "")),  # Simple conversion, handle "6+" case better in real implementation
                    "COMPARTMENT_A",  # In real implementation, determine optimal location
                    "AVAILABLE"
                ))
                
                # Record the transaction
                self.cursor.execute('''
                INSERT INTO transactions (timestamp, transaction_type, quantity, status)
                VALUES (?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    "DONATION",
                    int(quantity.replace("+", "")),
                    "COMPLETED"
                ))
                
                self.conn.commit()
                self.logger.info(f"Donation recorded: {quantity} items, expiry: {expiry_date}")
                
                # Show thank you screen
                self.show_donor_thank_you()
            except Exception as e:
                self.logger.error(f"Error recording donation: {e}")
                # In a real implementation, handle this error appropriately
                # For now, still show thank you screen
                self.show_donor_thank_you()
        
        confirm_button = tk.Button(
            buttons_frame,
            text="Confirm & Open Compartment",
            font=("Open Sans", 14, "bold"),
            bg="#F8D147",  # Yellow from our style guide
            fg="#4A4A4A",
            padx=15,
            pady=10,
            command=on_confirm
        )
        confirm_button.pack(side=tk.LEFT, padx=10)
    
    def show_donor_thank_you(self):
        """Display the thank you screen after donation."""
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add title
        title_label = tk.Label(
            self.main_frame, 
            text="Thank You!",
            font=("Montserrat", 32, "bold"),
            bg="#50C878",
            fg="white"
        )
        title_label.pack(pady=(100, 30))
        
        # Thank you message
        message_label = tk.Label(
            self.main_frame,
            text="Your donation has been received and will help someone in need.",
            font=("Open Sans", 18),
            bg="#50C878",
            fg="white",
            wraplength=600
        )
        message_label.pack(pady=20)
        
        # Auto-return to welcome screen after 5 seconds
        self.root.after(5000, self.show_welcome_screen)
        
        # Or return now button
        return_button = tk.Button(
            self.main_frame,
            text="Return to Main Menu",
            font=("Open Sans", 14),
            bg="#F8D147",
            fg="#4A4A4A",
            padx=15,
            pady=10,
            command=self.show_welcome_screen
        )
        return_button.pack(pady=40)
    
    def show_receiver_screen(self):
        """Display the receiver screen."""
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add title
        title_label = tk.Label(
            self.main_frame, 
            text="Receive Food",
            font=("Montserrat", 24, "bold"),
            bg="#50C878",
            fg="white"
        )
        title_label.pack(pady=(50, 30))
        
        # Check if food is available
        try:
            self.cursor.execute('''
            SELECT COUNT(*) FROM food_items WHERE status = 'AVAILABLE'
            ''')
            available_count = self.cursor.fetchone()[0]
            
            if available_count > 0:
                # Food is available
                available_label = tk.Label(
                    self.main_frame,
                    text=f"There are {available_count} food items available.",
                    font=("Open Sans", 16),
                    bg="#50C878",
                    fg="white"
                )
                available_label.pack(pady=20)
                
                instructions_label = tk.Label(
                    self.main_frame,
                    text="You can receive up to 2 food items. Press 'Continue' to proceed.",
                    font=("Open Sans", 14),
                    bg="#50C878",
                    fg="white",
                    wraplength=600
                )
                instructions_label.pack(pady=10)
                
                # Buttons frame
                buttons_frame = tk.Frame(self.main_frame, bg="#50C878")
                buttons_frame.pack(pady=40)
                
                # Back button
                back_button = tk.Button(
                    buttons_frame,
                    text="Back",
                    font=("Open Sans", 14),
                    bg="#4A4A4A",
                    fg="white",
                    padx=15,
                    pady=10,
                    command=self.show_welcome_screen
                )
                back_button.pack(side=tk.LEFT, padx=10)
                
                # Continue button
                continue_button = tk.Button(
                    buttons_frame,
                    text="Continue",
                    font=("Open Sans", 14, "bold"),
                    bg="#F8D147",  # Yellow from our style guide
                    fg="#4A4A4A",
                    padx=15,
                    pady=10,
                    command=self.show_receiver_confirmation
                )
                continue_button.pack(side=tk.LEFT, padx=10)
            else:
                # No food available
                no_food_label = tk.Label(
                    self.main_frame,
                    text="Sorry, there are no food items available at this time.",
                    font=("Open Sans", 16),
                    bg="#50C878",
                    fg="white",
                    wraplength=600
                )
                no_food_label.pack(pady=20)
                
                # Show nearest machine with food
                nearest_label = tk.Label(
                    self.main_frame,
                    text="The nearest machine with available food is at: 456 Oak Ave, LA",
                    font=("Open Sans", 14),
                    bg="#50C878",
                    fg="white",
                    wraplength=600
                )
                nearest_label.pack(pady=10)
                
                # Return button
                return_button = tk.Button(
                    self.main_frame,
                    text="Return to Main Menu",
                    font=("Open Sans", 14),
                    bg="#F8D147",
                    fg="#4A4A4A",
                    padx=15,
                    pady=10,
                    command=self.show_welcome_screen
                )
                return_button.pack(pady=40)
        except Exception as e:
            self.logger.error(f"Error checking food availability: {e}")
            # Handle error gracefully
            error_label = tk.Label(
                self.main_frame,
                text="Sorry, we encountered an error. Please try again later.",
                font=("Open Sans", 16),
                bg="#50C878",
                fg="white",
                wraplength=600
            )
            error_label.pack(pady=20)
            
            # Return button
            return_button = tk.Button(
                self.main_frame,
                text="Return to Main Menu",
                font=("Open Sans", 14),
                bg="#F8D147",
                fg="#4A4A4A",
                padx=15,
                pady=10,
                command=self.show_welcome_screen
            )
            return_button.pack(pady=40)
    
    def show_receiver_confirmation(self):
        """Display the food collection confirmation screen."""
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add title
        title_label = tk.Label(
            self.main_frame, 
            text="Collect Your Food",
            font=("Montserrat", 24, "bold"),
            bg="#50C878",
            fg="white"
        )
        title_label.pack(pady=(50, 30))
        
        # Get the oldest available food items (up to 2)
        try:
            self.cursor.execute('''
            SELECT id, entry_timestamp, expiry_date FROM food_items 
            WHERE status = 'AVAILABLE' 
            ORDER BY expiry_date ASC
            LIMIT 2
            ''')
            items = self.cursor.fetchall()
            
            if items:
                # Display instructions
                instructions_label = tk.Label(
                    self.main_frame,
                    text="The compartment will open. Please take your food items.",
                    font=("Open Sans", 16),
                    bg="#50C878",
                    fg="white",
                    wraplength=600
                )
                instructions_label.pack(pady=20)
                
                # In a real implementation, show which compartment is opening
                compartment_label = tk.Label(
                    self.main_frame,
                    text="Compartment A is opening...",
                    font=("Open Sans", 14, "bold"),
                    bg="#50C878",
                    fg="white"
                )
                compartment_label.pack(pady=10)
                
                # Buttons frame
                buttons_frame = tk.Frame(self.main_frame, bg="#50C878")
                buttons_frame.pack(pady=40)
                
                # Confirm collection button
                def on_confirm_collection():
                    # Update the status of the collected items
                    for item_id, _, _ in items:
                        self.cursor.execute('''
                        UPDATE food_items SET status = 'COLLECTED' WHERE id = ?
                        ''', (item_id,))
                        
                        # Record the transaction
                        self.cursor.execute('''
                        INSERT INTO transactions (timestamp, transaction_type, food_item_id, status)
                        VALUES (?, ?, ?, ?)
                        ''', (
                            datetime.now().isoformat(),
                            "COLLECTION",
                            item_id,
                            "COMPLETED"
                        ))
                    
                    self.conn.commit()
                    self.logger.info(f"Food items collected: {[item[0] for item in items]}")
                    
                    # Show thank you screen
                    self.show_receiver_thank_you()
                
                confirm_button = tk.Button(
                    buttons_frame,
                    text="I've Collected My Food",
                    font=("Open Sans", 14, "bold"),
                    bg="#F8D147",  # Yellow from our style guide
                    fg="#4A4A4A",
                    padx=15,
                    pady=10,
                    command=on_confirm_collection
                )
                confirm_button.pack()
            else:
                # This shouldn't happen if we checked availability earlier, but handle it just in case
                error_label = tk.Label(
                    self.main_frame,
                    text="Sorry, there are no food items available at this time.",
                    font=("Open Sans", 16),
                    bg="#50C878",
                    fg="white",
                    wraplength=600
                )
                error_label.pack(pady=20)
                
                # Return button
                return_button = tk.Button(
                    self.main_frame,
                    text="Return to Main Menu",
                    font=("Open Sans", 14),
                    bg="#F8D147",
                    fg="#4A4A4A",
                    padx=15,
                    pady=10,
                    command=self.show_welcome_screen
                )
                return_button.pack(pady=40)
        except Exception as e:
            self.logger.error(f"Error preparing food collection: {e}")
            # Handle error gracefully
            error_label = tk.Label(
                self.main_frame,
                text="Sorry, we encountered an error. Please try again later.",
                font=("Open Sans", 16),
                bg="#50C878",
                fg="white",
                wraplength=600
            )
            error_label.pack(pady=20)
            
            # Return button
            return_button = tk.Button(
                self.main_frame,
                text="Return to Main Menu",
                font=("Open Sans", 14),
                bg="#F8D147",
                fg="#4A4A4A",
                padx=15,
                pady=10,
                command=self.show_welcome_screen
            )
            return_button.pack(pady=40)
    
    def show_receiver_thank_you(self):
        """Display the thank you screen after food collection."""
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add title
        title_label = tk.Label(
            self.main_frame, 
            text="Thank You!",
            font=("Montserrat", 32, "bold"),
            bg="#50C878",
            fg="white"
        )
        title_label.pack(pady=(100, 30))
        
        # Thank you message
        message_label = tk.Label(
            self.main_frame,
            text="We hope you enjoy your food. Please visit again!",
            font=("Open Sans", 18),
            bg="#50C878",
            fg="white",
            wraplength=600
        )
        message_label.pack(pady=20)
        
        # Auto-return to welcome screen after 5 seconds
        self.root.after(5000, self.show_welcome_screen)
        
        # Or return now button
        return_button = tk.Button(
            self.main_frame,
            text="Return to Main Menu",
            font=("Open Sans", 14),
            bg="#F8D147",
            fg="#4A4A4A",
            padx=15,
            pady=10,
            command=self.show_welcome_screen
        )
        return_button.pack(pady=40)
    
    def show_admin_login(self):
        """Display the admin login screen."""
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add title
        title_label = tk.Label(
            self.main_frame, 
            text="Admin Login",
            font=("Montserrat", 24, "bold"),
            bg="#50C878",
            fg="white"
        )
        title_label.pack(pady=(50, 30))
        
        # Create a frame for the login form
        login_frame = tk.Frame(self.main_frame, bg="#50C878")
        login_frame.pack(pady=20)
        
        # PIN entry
        pin_label = tk.Label(
            login_frame,
            text="Enter PIN:",
            font=("Open Sans", 14),
            bg="#50C878",
            fg="white"
        )
        pin_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        pin_var = tk.StringVar()
        pin_entry = tk.Entry(
            login_frame,
            textvariable=pin_var,
            font=("Open Sans", 14),
            show="*",  # Hide PIN with asterisks
            width=10
        )
        pin_entry.grid(row=0, column=1, sticky="w", padx=20, pady=(0, 10))
        
        # Error message (hidden initially)
        error_var = tk.StringVar()
        error_label = tk.Label(
            login_frame,
            textvariable=error_var,
            font=("Open Sans", 12),
            bg="#50C878",
            fg="red"
        )
        error_label.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.main_frame, bg="#50C878")
        buttons_frame.pack(pady=40)
        
        # Back button
        back_button = tk.Button(
            buttons_frame,
            text="Back",
            font=("Open Sans", 14),
            bg="#4A4A4A",
            fg="white",
            padx=15,
            pady=10,
            command=self.show_welcome_screen
        )
        back_button.pack(side=tk.LEFT, padx=10)
        
        # Login button
        def on_login():
            # In a real implementation, validate PIN against stored value
            # For this prototype, use a simple hardcoded PIN: 1234
            if pin_var.get() == "1234":
                self.show_admin_dashboard()
            else:
                error_var.set("Invalid PIN. Please try again.")
        
        login_button = tk.Button(
            buttons_frame,
            text="Login",
            font=("Open Sans", 14, "bold"),
            bg="#F8D147",  # Yellow from our style guide
            fg="#4A4A4A",
            padx=15,
            pady=10,
            command=on_login
        )
        login_button.pack(side=tk.LEFT, padx=10)
    
    def show_admin_dashboard(self):
        """Display the admin dashboard."""
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add title
        title_label = tk.Label(
            self.main_frame, 
            text="Admin Dashboard",
            font=("Montserrat", 24, "bold"),
            bg="#50C878",
            fg="white"
        )
        title_label.pack(pady=(30, 20))
        
        # Create a frame for the dashboard content
        dashboard_frame = tk.Frame(self.main_frame, bg="#50C878")
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Machine status section
        status_frame = tk.LabelFrame(
            dashboard_frame,
            text="Machine Status",
            font=("Open Sans", 14, "bold"),
            bg="#50C878",
            fg="white"
        )
        status_frame.pack(fill=tk.X, pady=10)
        
        # Get machine status
        try:
            # Count available items
            self.cursor.execute('''
            SELECT COUNT(*) FROM food_items WHERE status = 'AVAILABLE'
            ''')
            available_count = self.cursor.fetchone()[0]
            
            # Count expired items
            today = datetime.now().date().isoformat()
            self.cursor.execute('''
            SELECT COUNT(*) FROM food_items 
            WHERE status = 'AVAILABLE' AND expiry_date < ?
            ''', (today,))
            expired_count = self.cursor.fetchone()[0]
            
            # Calculate available space (simplified)
            available_space = 100 - (available_count * 5)  # Assume each item takes 5% of space
            if available_space < 0:
                available_space = 0
            
            # Display status
            status_info = f"Available Items: {available_count}\n"
            status_info += f"Expired Items: {expired_count}\n"
            status_info += f"Available Space: {available_space}%\n"
            status_info += f"Door Status: Closed\n"  # Simulated
            status_info += f"Temperature: 4.2°C\n"  # Simulated
            status_info += f"Network Status: Connected"  # Simulated
            
            status_label = tk.Label(
                status_frame,
                text=status_info,
                font=("Open Sans", 12),
                bg="#50C878",
                fg="white",
                justify=tk.LEFT
            )
            status_label.pack(padx=20, pady=10, anchor="w")
        except Exception as e:
            self.logger.error(f"Error getting machine status: {e}")
            status_label = tk.Label(
                status_frame,
                text="Error retrieving machine status.",
                font=("Open Sans", 12),
                bg="#50C878",
                fg="white"
            )
            status_label.pack(padx=20, pady=10)
        
        # Actions section
        actions_frame = tk.LabelFrame(
            dashboard_frame,
            text="Actions",
            font=("Open Sans", 14, "bold"),
            bg="#50C878",
            fg="white"
        )
        actions_frame.pack(fill=tk.X, pady=10)
        
        # Action buttons
        actions_buttons_frame = tk.Frame(actions_frame, bg="#50C878")
        actions_buttons_frame.pack(padx=20, pady=10)
        
        # Remove expired items button
        def on_remove_expired():
            try:
                today = datetime.now().date().isoformat()
                self.cursor.execute('''
                UPDATE food_items 
                SET status = 'EXPIRED_REMOVED' 
                WHERE status = 'AVAILABLE' AND expiry_date < ?
                ''', (today,))
                
                # Record the maintenance action
                self.cursor.execute('''
                INSERT INTO transactions (timestamp, transaction_type, status)
                VALUES (?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    "EXPIRED_REMOVAL",
                    "COMPLETED"
                ))
                
                self.conn.commit()
                self.logger.info("Expired items marked as removed")
                
                # Refresh the dashboard
                self.show_admin_dashboard()
            except Exception as e:
                self.logger.error(f"Error removing expired items: {e}")
                # Handle error
        
        remove_expired_button = tk.Button(
            actions_buttons_frame,
            text="Remove Expired Items",
            font=("Open Sans", 12),
            bg="#F8D147",
            fg="#4A4A4A",
            padx=10,
            pady=5,
            command=on_remove_expired
        )
        remove_expired_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Test door button
        def on_test_door():
            # In a real implementation, this would control the physical door
            self.logger.info("Door test initiated")
            # Simulate door operation
            # Show a message
            tk.messagebox.showinfo("Door Test", "Door operation simulated successfully.")
        
        test_door_button = tk.Button(
            actions_buttons_frame,
            text="Test Door",
            font=("Open Sans", 12),
            bg="#F8D147",
            fg="#4A4A4A",
            padx=10,
            pady=5,
            command=on_test_door
        )
        test_door_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Sync with server button
        def on_sync():
            # In a real implementation, this would sync with the central server
            self.logger.info("Server sync initiated")
            # Simulate sync
            # Show a message
            tk.messagebox.showinfo("Sync", "Sync with server completed successfully.")
        
        sync_button = tk.Button(
            actions_buttons_frame,
            text="Sync with Server",
            font=("Open Sans", 12),
            bg="#F8D147",
            fg="#4A4A4A",
            padx=10,
            pady=5,
            command=on_sync
        )
        sync_button.grid(row=1, column=0, padx=5, pady=5)
        
        # View logs button
        def on_view_logs():
            # In a real implementation, show a detailed log viewer
            # For now, just show a simple message
            tk.messagebox.showinfo("Logs", "Log viewer would be shown here.")
        
        logs_button = tk.Button(
            actions_buttons_frame,
            text="View Logs",
            font=("Open Sans", 12),
            bg="#F8D147",
            fg="#4A4A4A",
            padx=10,
            pady=5,
            command=on_view_logs
        )
        logs_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Return to main menu button
        exit_button = tk.Button(
            self.main_frame,
            text="Exit Admin Mode",
            font=("Open Sans", 14),
            bg="#4A4A4A",
            fg="white",
            padx=15,
            pady=10,
            command=self.show_welcome_screen
        )
        exit_button.pack(side=tk.BOTTOM, pady=20)
    
    def run(self):
        """Run the main application loop."""
        self.logger.info("Starting application main loop")
        self.root.mainloop()
    
    def cleanup(self):
        """Clean up resources before exiting."""
        self.logger.info("Cleaning up resources")
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()


if __name__ == "__main__":
    try:
        # Create and run the machine application
        app = ExesFoodMachine()
        app.run()
    except Exception as e:
        logging.error(f"Unhandled exception: {e}", exc_info=True)
    finally:
        # Ensure cleanup happens even if there's an exception
        if 'app' in locals():
            app.cleanup()
