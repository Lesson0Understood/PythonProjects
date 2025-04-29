# Pothole Reporting System

## Overview

This project is a web application built with Flask for reporting, viewing, and managing potholes. It allows users to see reported potholes on a list, view details, and visualize them on a map. Administrators have the ability to add, update, and delete pothole records through the web interface.

Additionally, a command-line interface (CLI) tool is included for direct database interaction (viewing and deleting potholes), and a utility script is provided for resizing images.

## Features

*   **Web Application (Flask):**
    *   User Registration and Login system.
    *   View a list of reported potholes.
    *   View detailed information for each pothole.
    *   Visualize pothole locations on a map.
    *   Role-based access control (Admin role required for management).
    *   Admin functions: Create, Update, and Delete pothole records.
*   **Command-Line Interface (CLI):**
    *   View all potholes from the database in a formatted table.
    *   Delete specific potholes by ID.
*   **Database:**
    *   Uses SQLite (`site.db`) to store user and pothole data via SQLAlchemy.
*   **Image Utility:**
    *   A script (`image_resizer.py`) to batch resize images, useful for preparing pothole images for the web.

## Technology Stack

*   **Backend:** Python, Flask
*   **Database ORM:** SQLAlchemy
*   **Authentication:** Flask-Login
*   **Authorization:** Flask-Principal
*   **Web Forms:** Flask-WTF
*   **Database:** SQLite
*   **CLI Enhancements:** `prettytable`, `termcolor`, `art`, `python-inquirer`
*   **Image Processing:** Pillow (PIL)
*   **Frontend:** HTML, CSS, JavaScript (rendered via Flask templates)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install Flask Flask-SQLAlchemy Flask-Login Flask-Principal Flask-WTF Pillow prettytable termcolor python-inquirer art SQLAlchemy
    ```

4.  **Database Location:** The web application (`main.py`) will automatically create the SQLite database file at `./instance/site.db`. Ensure the `database_viewer_pothole.py` script is placed correctly relative to this (the current script expects it one level up: `../instance/site.db`).

## Running the Application

1.  **Run the Web Application:**
    ```bash
    python main.py
    ```
    The application will be accessible at `http://localhost:5000` or `http://0.0.0.0:5000`.

    *   **Initial Admin User:** You can create a test admin user by navigating to `http://localhost:5000/test` in your browser once. This creates a user with email `islamcraft2007@gmail.com` and password `a`. Alternatively, register a regular user and manually update their `roles` column in the `user` table (e.g., using a DB browser) to include "Admin".

2.  **Run the CLI Tool:**
    *   Navigate to the directory containing `database_viewer_pothole.py`.
    ```bash
    python database_viewer_pothole.py
    ```
    Follow the interactive prompts to view or delete potholes.

3.  **Run the Image Resizer Utility (Optional):**
    *   Modify the `input_directory` and `output_directory` paths within `image_resizer.py`.
    *   Run the script:
    ```bash
    python image_resizer.py
    ```

## Project Components

*   `main.py`: The main Flask application file containing routes, database models, and application logic.
*   `forms.py`: Defines Flask-WTF forms for user input (Create/Update/Delete Potholes, Login/Register).
*   `database_viewer_pothole.py`: A CLI tool for viewing and deleting pothole data directly from the database.
*   `image_resizer.py`: A utility script to resize images using Pillow.
*   `helper_functions.py`: Contains helper/debug functions (e.g., `print_all_data`).
*   `templates/`: Directory containing HTML templates for the web application.
*   `static/`: Directory containing static files (CSS, JavaScript, Images).
*   `instance/site.db`: The SQLite database file (created automatically on first run of `main.py`).
