# Project DigiStix

> A dynamic information and documentation system for a campus organization.

## About

**Project DigiStix** is a web-based information and documentation system designed to organize and present important information about a campus organization through a centralized application.

Instead of manually editing HTML files whenever organization information changes, DigiStix uses a dynamic web application where authorized personnel can manage information through administrative pages.

The project aims to make organization information easier to maintain, update, and access while keeping the system practical for students and organization personnel.

## Purpose

DigiStix aims to provide a centralized platform for managing and presenting:

* Organization structure and members
* Officers and advisers
* Founding members
* Target plans
* Accomplishment reports
* Inventory and equipment records
* Organization activities
* Supporting documents and attachments

The system is being developed as a campus-oriented academic project and is not intended to replace official university record-keeping systems.

## Features

### Public Information

* View published organization activities.
* Access available activity information and supporting attachments.
* Browse information presented through the public-facing website.

### Authentication and Access Control

* User authentication through Flask-Login.
* Restricted access to staff and administrative functionality.
* Separation between public-facing pages and authorized management pages.

### Activity Management

* Create and edit organization activities.
* Publish and unpublish activities.
* Upload and manage activity attachments.
* Remove activities and their associated attachment records.
* Sanitize activity descriptions before displaying submitted HTML content.

### Configuration and Security

* Environment-based application secret configuration.
* Local upload storage excluded from Git.
* Attachment validation and access restrictions.
* Automated tests for authentication and staff access controls.

*Note: Features should be considered implemented only to the extent verified in the current application. Additional organization modules may still be under development.*

## How It Works

The application follows a traditional web architecture:

```text
User
 │
 ▼
HTML / CSS / JavaScript
 │
 ▼
Flask Application
 │
 ├── Authentication and Access Control
 ├── Public Routes
 └── Administrative Routes
 │
 ▼
SQLAlchemy ORM
 │
 ▼
PostgreSQL Database
```

Flask handles request processing and application logic. SQLAlchemy provides database integration, while PostgreSQL stores relational application data.

Activity attachment files are stored in the configured local upload directory.

## Technology Stack

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| HTML5            | Page structure            |
| CSS3             | Styling and layout        |
| JavaScript       | Frontend interactions     |
| Python           | Backend programming       |
| Flask            | Web application framework |
| Flask-SQLAlchemy | Database integration      |
| Flask-Login      | User authentication       |
| PostgreSQL       | Relational database       |
| Psycopg 3        | PostgreSQL driver         |
| python-dotenv    | Environment configuration |
| Bleach           | HTML sanitization         |
| pytest           | Automated testing         |
| Git              | Version control           |
| GitHub           | Repository hosting        |

## Project Structure

```text
Project-DigiStix/
├── app/
│   ├── models/
│   ├── routes/
│   │   ├── public.py
│   │   ├── auth.py
│   │   └── admin.py
│   ├── templates/
│   │   └── admin/
│   ├── static/
│   └── content.py
├── migrations/
├── tests/
├── instance/
│   └── uploads/
├── config.py
├── run.py
├── requirements.txt
├── .env                 # Local configuration; do not commit
├── .gitignore
└── README.md
```

This is a simplified overview. The exact contents of each directory may change as development continues.

## Requirements

Before running DigiStix, prepare:

* Python
* PostgreSQL
* A configured database
* Git
* The dependencies listed in `requirements.txt`

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/chessTica542319/Project-DigiStix.git
cd Project-DigiStix
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows, activate the environment using:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file in the project root. Configure the values required by `config.py`, including:

```dotenv
SECRET_KEY=replace_with_a_secure_random_secret
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/database_name
```

Replace the database connection details with your own PostgreSQL configuration. Use a securely generated secret for `SECRET_KEY`; do not use the example text as the actual secret.

Keep `.env` private and never commit real credentials or secret keys.

### 5. Prepare the database

Ensure PostgreSQL is running and the configured database exists. Apply the project's database migrations if required by the current setup.

### 6. Run the application

```bash
python run.py
```

The application's startup behavior and listening address depend on the configuration in the project.

## Testing

Run the automated test suite:

```bash
python -m pytest -q
```

Check Python files for compilation errors:

```bash
python -m compileall -q app tests
```

The test suite should be rerun after changes to authentication, access control, activity management, or other application features.

## Development

DigiStix is developed as a collaborative academic project using Python, Flask, PostgreSQL, and Git.

Development and testing have included Termux on Android and desktop environments.

## Project Status

**Current stage: Core application development**

The current implementation includes the Flask application foundation, database integration, authentication and staff access controls, and activity-management functionality with attachment handling.

Further work may include expanding the remaining organization modules, improving validation and usability, conducting additional security tests, and preparing the application for deployment.

## Author

**Sam Ruda**

### School

Iloilo State University of Fisheries and Science and Technology

### Repository

[github.com/chessTica542319/Project-DigiStix](https://github.com/chessTica542319/Project-DigiStix)

## License

This project is developed for academic and educational purposes. No specific open-source license is declared in this README.

