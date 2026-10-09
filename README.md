# Project DigiStix

> A dynamic information and documentation system for a campus organization.

## About

**Project DigiStix** is a web-based information and documentation system designed to organize and present important information about a campus organization in one centralized application.

Instead of manually editing HTML files whenever organization information changes, DigiStix is being developed as a **dynamic system** where authorized users can manage information through the application.

The project is intended to make organization information easier to maintain, update, and access while keeping the system simple enough for students and organization personnel to use.

## Purpose

DigiStix aims to provide a centralized platform for managing and presenting organization information such as:

* Organization structure and members
* Officers and advisers
* Founding members
* Target plans
* Accomplishment reports
* Inventory and equipment records
* Organization activities
* Supporting documentation and information

The system is being developed as a campus-oriented project and is not intended to replace official university record-keeping systems.

## How It Works

The planned system follows a traditional web application architecture:

```text
User
 │
 ▼
HTML / CSS / JavaScript
 │
 ▼
Flask Application
 │
 ▼
SQLAlchemy
 │
 ▼
PostgreSQL Database
```

The frontend is responsible for displaying information and interacting with users, while Flask handles the application logic and SQLAlchemy communicates with the PostgreSQL database.

## Technology Stack

| Technology       | Purpose                      |
| ---------------- | ---------------------------- |
| HTML5            | Page structure               |
| CSS3             | Styling and layout           |
| JavaScript       | Frontend interactions        |
| Python           | Backend programming          |
| Flask            | Web application framework    |
| Flask-SQLAlchemy | Database integration         |
| Flask-Login      | User authentication          |
| PostgreSQL       | Relational database          |
| Psycopg 3        | PostgreSQL database driver   |
| python-dotenv    | Environment configuration    |
| Git              | Version control              |
| GitHub           | Repository and collaboration |

## Project Structure

```text
Project-DigiStix/
│
├── app/
│   ├── models/
│   │   ├── user.py
│   │   ├── officer.py
│   │   ├── adviser.py
│   │   ├── founding_member.py
│   │   ├── target_plan.py
│   │   ├── accomplishment.py
│   │   ├── inventory.py
│   │   └── activity.py
│   │
│   ├── routes/
│   │   ├── public.py
│   │   ├── auth.py
│   │   └── admin.py
│   │
│   ├── templates/
│   └── static/
│
├── migrations/
├── tests/
├── instance/
│
├── config.py
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Authentication

DigiStix is planned to include authentication for authorized personnel.

Public users will be able to view organization information, while authorized users will be able to manage information through the administrative side of the system.

Sensitive configuration such as database credentials and secret keys should be stored in environment variables and must not be committed to the repository.

## Development

The project is currently being developed using:

* Python
* Flask
* PostgreSQL
* SQLAlchemy
* Git
* Termux for mobile development
* Desktop environments for additional development and testing

The repository is designed so that the project can be cloned to another computer and continued by other members of the development team.

### Running the Project

Clone the repository:

```bash
git clone https://github.com/chessTica542319/Project-DigiStix.git
cd Project-DigiStix
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables, then run:

```bash
python run.py
```

## Project Status

**Current stage:** Initial project foundation

The current foundation includes:

* Flask application structure
* PostgreSQL database setup
* SQLAlchemy integration
* Psycopg PostgreSQL driver
* Flask-Login dependency
* Environment configuration
* Git repository setup

Additional database models, routes, authentication functionality, administrative pages, and organization features will be developed progressively.

## Development

Project DigiStix is developed as a collaborative academic project.

### Author

**Sam Ruda**

### School

**Iloilo State University of Fisheries ,Science and Technology**

### Repository

GitHub: **[github.com/chessTica542319](https://github.com/chessTica542319)**

## License

This project is developed for academic and educational purposes.

