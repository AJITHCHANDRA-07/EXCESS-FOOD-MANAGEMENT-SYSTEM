# Exes Food Management System - Startup Guide

This comprehensive guide provides step-by-step instructions for starting and operating both the machine software and website components of the Exes Food Management System.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Starting the Backend API Server](#starting-the-backend-api-server)
3. [Starting the Website Frontend](#starting-the-website-frontend)
4. [Starting the Machine Software](#starting-the-machine-software)
5. [Accessing the System](#accessing-the-system)
6. [Troubleshooting](#troubleshooting)
7. [Shutdown Procedures](#shutdown-procedures)

## System Requirements

### Backend API Server
- Python 3.11 or higher
- MySQL database (optional, SQLite is used by default)
- Required Python packages (installed via requirements.txt)

### Website Frontend
- Node.js 16.0 or higher
- npm or pnpm package manager

### Machine Software
- Python 3.11 or higher
- Tkinter (usually included with Python)
- SQLite (usually included with Python)

## Starting the Backend API Server

1. **Extract the backend code**
   ```
   unzip exes_food_management_system_code.zip -d exes_backend
   ```

2. **Navigate to the project directory**
   ```
   cd exes_backend
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

5. **Start the backend server**
   ```
   cd src
   python main.py
   ```

6. **Verify the server is running**
   - The console should display a message indicating the server is running
   - By default, the server runs on http://localhost:5000
   - You can test it by opening http://localhost:5000/api/status in your browser

## Starting the Website Frontend

1. **Extract the frontend code**
   ```
   unzip exes_frontend_complete.zip -d exes_frontend
   ```

2. **Navigate to the project directory**
   ```
   cd exes_frontend
   ```

3. **Install dependencies**
   - Using npm:
     ```
     npm install
     ```
   - Using pnpm:
     ```
     pnpm install
     ```

4. **Start the development server**
   - Using npm:
     ```
     npm run dev
     ```
   - Using pnpm:
     ```
     pnpm run dev
     ```

5. **Verify the frontend is running**
   - The console should display a message indicating the server is running
   - By default, the website is accessible at http://localhost:5173
   - Open this URL in your browser to access the website

## Starting the Machine Software

1. **Extract the machine software**
   ```
   unzip machine_software_package.zip -d machine_software
   ```

2. **Navigate to the project directory**
   ```
   cd machine_software
   ```

3. **Start the machine software**
   ```
   python main.py
   ```

4. **Verify the machine software is running**
   - A graphical user interface should appear
   - The main screen should show options for donors and receivers
   - The console may display log messages indicating the software is running

## Accessing the System

### Website Access

1. **Public Access (Donors and Receivers)**
   - Open http://localhost:5173 in a web browser
   - The homepage provides options for donors and receivers
   - Use the machine locator to find nearby machines

2. **Admin Access**
   - Navigate to http://localhost:5173/admin/login
   - Login with the demo credentials:
     - Email: admin@example.com
     - Password: admin123
   - After login, you'll be redirected to the admin dashboard

3. **Volunteer Access**
   - Navigate to http://localhost:5173/volunteer/login
   - Login with the demo credentials:
     - Email: volunteer@example.com
     - Password: volunteer123
   - After login, you'll be redirected to the volunteer portal

### Machine Software Access

The machine software simulates the physical machines and provides interfaces for:

1. **Donors**
   - Click "I want to DONATE food" on the main screen
   - Follow the prompts to enter food quantity and expiry date
   - The system will simulate the donation process

2. **Receivers**
   - Click "I want to RECEIVE food" on the main screen
   - Follow the prompts to collect available food
   - The system will simulate the food collection process

3. **Administrators**
   - Click "Admin / Maintenance" at the bottom of the screen
   - Enter PIN: 1234
   - Access the admin dashboard for machine maintenance

## Troubleshooting

### Backend API Issues

1. **Server won't start**
   - Verify Python version: `python --version`
   - Check for port conflicts: Another service might be using port 5000
   - Verify all dependencies are installed: `pip install -r requirements.txt`

2. **Database errors**
   - Check database configuration in src/main.py
   - Ensure database file is not corrupted
   - For MySQL, verify connection parameters

### Website Frontend Issues

1. **Development server won't start**
   - Verify Node.js version: `node --version`
   - Check for port conflicts: Another service might be using port 5173
   - Verify all dependencies are installed: `npm install` or `pnpm install`

2. **Import errors**
   - If you see import path errors, check the path in the error message
   - Correct the import paths as needed (e.g., change "./ui/use-toast" to "../hooks/use-toast")

3. **API connection errors**
   - Verify the backend API server is running
   - Check the API URL in src/context/ApiContext.tsx
   - Verify network connectivity between frontend and backend

### Machine Software Issues

1. **Software won't start**
   - Verify Python version: `python --version`
   - Check that Tkinter is installed: `python -m tkinter`
   - Verify all dependencies are installed

2. **Hardware simulation errors**
   - Check the console for error messages
   - Verify the database file is not corrupted
   - Restart the application

## Shutdown Procedures

### Backend API Server

1. **Graceful shutdown**
   - Press Ctrl+C in the terminal where the server is running
   - Wait for the server to complete any pending operations

2. **Force shutdown (if needed)**
   - On Windows: Press Ctrl+C or close the terminal
   - On macOS/Linux: Press Ctrl+C or run `pkill -f "python main.py"`

### Website Frontend

1. **Development server shutdown**
   - Press Ctrl+C in the terminal where the server is running
   - Wait for the server to complete the shutdown process

### Machine Software

1. **Graceful shutdown**
   - Click the close button (X) on the application window
   - Or press Ctrl+C in the terminal if running from command line

## Production Deployment (Optional)

For production deployment, additional steps are required:

### Backend API

1. **Build for production**
   - Configure production database settings
   - Set up environment variables for security
   - Consider using Gunicorn or uWSGI for production serving

2. **Deploy to server**
   - Transfer files to production server
   - Set up reverse proxy (Nginx or Apache)
   - Configure SSL for secure connections

### Website Frontend

1. **Build for production**
   - Using npm:
     ```
     npm run build
     ```
   - Using pnpm:
     ```
     pnpm run build
     ```

2. **Deploy to server**
   - Transfer the contents of the dist/ directory to your web server
   - Configure the server to serve the static files
   - Set up SSL for secure connections

### Machine Software

1. **Package for distribution**
   - Consider using PyInstaller to create standalone executables
   - Create installation packages for target operating systems
   - Configure for production hardware interfaces

---

For additional support or questions, please refer to the project documentation or contact the system administrator.
