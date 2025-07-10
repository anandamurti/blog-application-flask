
Built by https://www.blackbox.ai

---

# Blog Application

## Project Overview
This project is a web-based blog application built using Flask, a lightweight WSGI web application framework for Python. The application allows users to create and manage blogs, upload images, and maintains a structured database for storing blog-related data. 

The application uses SQLAlchemy for the ORM and Flask-Migrate for handling database migrations seamlessly. It also integrates Flask-Bcrypt for password hashing, making it secure for user authentication.

## Features
- User registration and authentication.
- CRUD operations for blog posts.
- Image uploads with size restrictions.
- User-friendly Markdown support for formatting blog content.
- Error handling for large uploads.
- Organized project structure using blueprints for modularity.

## Installation
To get started with the project, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the project directory:**
   ```bash
   cd <project-folder>
   ```

3. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables:**
   Make sure to set the following environment variables:
   - `SECRET_KEY`: A secret key for session management (can be a random string).
   - `DB_PASSWORD`: The password to access your MySQL database.

6. **Run migrations (if necessary):**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

7. **Start the application:**
   ```bash
   python app.py
   ```

The application will run on `http://127.0.0.1:5000`.

## Usage
- Visit `http://127.0.0.1:5000` in your browser to access the application.
- Use the provided interface to register, create, and manage blog posts.
- You can upload images (max size: 5MB) while creating blog posts.
  
## Dependencies
The project requires the following Python libraries as listed in `requirements.txt`:
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Markdown
- MarkupSafe

Ensure you have installed all dependencies by running `pip install -r requirements.txt`.

## Project Structure
```
/blog-application
├── app.py                  # Entry point for the application
├── app_init.py             # Application factory and initial setup
├── manage.py               # CLI commands for database migrations
├── settings.py             # Configuration settings for the application
├── tests.py                # Unit tests for the application
├── home/                   # Blueprint for homepage functionality
│   └── views.py            # Handler for homepage routes
├── author/                 # Blueprint for author related functionality
│   └── views.py            # Handler for author routes
└── static/                 # Static files (CSS, JavaScript, uploaded images)
    └── uploads/            # Directory for uploaded images
```

This project structure aids in maintaining a clear separation of concerns and enhances code organization, making it easier for developers to navigate and contribute.

--- 

For any further information or contribution guidelines, feel free to check the project's documentation or raise issues in the repository.