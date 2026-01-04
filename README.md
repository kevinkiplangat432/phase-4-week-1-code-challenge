# Superheroes API
A Flask REST API for tracking superheroes and their superpowers. This API allows you to manage superheroes, their powers, and associations between them with full CRUD operations, validation, and error handling.

## Features
##### Hero Management
    Track superheroes with their secret and public identities

##### Power Management 
    Manage superpowers with detailed descriptions

##### Hero-Power Associations 
    Link heroes to powers with customizable strength levels

##### Full CRUD Operations 
    Create, read, update, and delete functionality

##### Data Validation
    Comprehensive validation for all inputs

##### Error Handling 
    Proper HTTP status codes and error messages

##### RESTful Design 
    Clean, predictable API endpoints

## Tech Stack
Backend: Python, Flask

Database: SQLite (with SQLAlchemy ORM)

Serialization: JSON

Validation: SQLAlchemy validators

CORS: Flask-CORS for cross-origin requests

Prerequisites
Python 3.8 or higher

pip (Python package manager)

Git (for version control)

## Installation & Setup
1. Clone the Repository
bash
git clone https://github.com/kevinkiplangat432/phase-4-week-1-code-challenge.git

cd superheroes-api
2. Create Virtual Environment
bash
### Create virtual environment
pipenv install

### Activate virtual environment
pipenv shell

3. Install Dependencies
bash
pip install -r requirements.txt

4. Initialize Database
bash
### Seed the database with initial data
python seed.py

5. Run the Application
bash
### Development server
python run.py

### The API will be available at: http://localhost:5555

Endpoint
1. GET /
Returns API welcome message and available endpoints.

Response:

json
{
  "message": "Welcome to Superheroes API",
  "endpoints": {
    "GET /heroes": "List all heroes",
    "GET /heroes/<id>": "Get hero details with powers",
    "GET /powers": "List all powers",
    "GET /powers/<id>": "Get power details",
    "PATCH /powers/<id>": "Update power description",
    "POST /hero_powers": "Create hero-power association"
  }
}
2. GET /heroes
Returns a list of all heroes.

Response:

json
[
  {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel"
  },
  {
    "id": 2,
    "name": "Doreen Green",
    "super_name": "Squirrel Girl"
  },
  ...
]
3. GET /heroes/<id>
Returns details of a specific hero including their powers.

Parameters:

id (integer): Hero ID

Success Response (200):

json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "hero_powers": [
    {
      "hero_id": 1,
      "id": 1,
      "power": {
        "description": "gives the wielder super-human strengths",
        "id": 1,
        "name": "super strength"
      },
      "power_id": 1,
      "strength": "Strong"
    }
  ]
}
Error Response (404):

json
{
  "error": "Hero not found"
}
4. GET /powers
Returns a list of all powers.

Response:

json
[
  {
    "description": "gives the wielder super-human strengths",
    "id": 1,
    "name": "super strength"
  },
  {
    "description": "gives the wielder the ability to fly through the skies at supersonic speed",
    "id": 2,
    "name": "flight"
  },
  ...
]
5. GET /powers/<id>
Returns details of a specific power.

Parameters:

id (integer): Power ID

Success Response (200):

json
{
  "description": "gives the wielder super-human strengths",
  "id": 1,
  "name": "super strength"
}
Error Response (404):

json
{
  "error": "Power not found"
}
6. PATCH /powers/<id>
Updates the description of a specific power.

Parameters:

id (integer): Power ID

Request Body:

json
{
  "description": "Updated description with at least 20 characters"
}
Success Response (200):

json
{
  "description": "Updated description with at least 20 characters",
  "id": 1,
  "name": "super strength"
}
Error Responses:

404 - Power not found:

json
{
  "error": "Power not found"
}
400 - Validation error:

json
{
  "errors": ["Description must be at least 20 characters long"]
}
7. POST /hero_powers
Creates a new association between a hero and a power.

Request Body:

json
{
  "strength": "Average",
  "power_id": 1,
  "hero_id": 3
}
Success Response (201):

json
{
  "id": 11,
  "hero_id": 3,
  "power_id": 1,
  "strength": "Average",
  "hero": {
    "id": 3,
    "name": "Gwen Stacy",
    "super_name": "Spider-Gwen"
  },
  "power": {
    "description": "gives the wielder super-human strengths",
    "id": 1,
    "name": "super strength"
  }
}
Error Responses:

400 - Validation error:

json
{
  "errors": ["Strength must be one of: Strong, Weak, Average"]
}
404 - Hero/Power not found:

json
{
  "errors": ["Hero not found"]
}
Data Models
Hero
python
{
  "id": Integer (Primary Key),
  "name": String (Required),
  "super_name": String (Required)
}
Power
python
{
  "id": Integer (Primary Key),
  "name": String (Required),
  "description": String (Required, Minimum 20 characters)
}
HeroPower
python
{
  "id": Integer (Primary Key),
  "strength": String (Required, Must be: 'Strong', 'Weak', or 'Average'),
  "hero_id": Integer (Foreign Key to Hero, Cascade Delete),
  "power_id": Integer (Foreign Key to Power, Cascade Delete)
}
Validation Rules
Power Model
description: Must be present and at least 20 characters long

HeroPower Model
strength: Must be one of: 'Strong', 'Weak', 'Average'

Testing the API
Using cURL
bash
### Get all heroes
curl http://localhost:5555/heroes

### Get hero with ID 1
curl http://localhost:5555/heroes/1

### Get all powers
curl http://localhost:5555/powers

### Update power description
curl -X PATCH http://localhost:5555/powers/1 \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated description with more than 20 characters"}'

### Create hero-power association
curl -X POST http://localhost:5555/hero_powers \
  -H "Content-Type: application/json" \
  -d '{"strength": "Average", "power_id": 1, "hero_id": 3}'
Using Postman
Import the provided Postman collection: challenge-2-superheroes.postman_collection.json

Set the base URL to http://localhost:5555

Test all endpoints

Automated Testing
Run the test script:

bash
python test_api.py

Database Operations
Seeding the Database
bash
python seed.py
This creates:

10 heroes

4 powers

Random associations between heroes and powers

Resetting the Database
bash
### Delete the database file
rm superheroes.db

### Recreate and seed
python seed.py
Development
Adding New Features
Create a new branch: git checkout -b feature-name

Make your changes

Test thoroughly

Commit changes: git commit -m "Description of changes"

Push to branch: git push origin feature-name

Create a Pull Request

Running Tests
bash
### Run the test suite
python -m pytest tests/
## Code Style used and suggested for use in future.
Follow PEP 8 guidelines

Use meaningful variable names

Add docstrings for functions and classes

Keep functions focused and single-purpose

## Deployment
Local Deployment
Follow installation steps above

Run: python run.py

Access at: http://localhost:5555

Production Deployment (Example with Gunicorn)
bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
Environment Variables
Create a .env file in the root directory:

env
DATABASE_URL=sqlite:///superheroes.db
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
Troubleshooting
Common Issues
"No such table" error

bash
### Delete and recreate the database
rm superheroes.db
python seed.py
Port already in use

python
### In run.py, change the port
app.run(debug=True, port=5000)  # or any other available port
Import errors

bash
### Make sure you're in the correct directory
cd superheroes-api

### Ensure virtual environment is activated
source venv/bin/activate

### Check if dependencies are installed
pip list | grep Flask
Database connection issues

bash
### Check if database file exists
ls -la superheroes.db

### Check file permissions
chmod 644 superheroes.db
Debug Mode
To enable debug mode, set FLASK_ENV=development in your .env file or run:

bash
FLASK_ENV=development python run.py
API Examples
Example Workflow
Get all heroes:

bash
curl http://localhost:5555/heroes
View a specific hero's powers:

bash
curl http://localhost:5555/heroes/1
Update a power's description:

bash
curl -X PATCH http://localhost:5555/powers/1 \
  -H "Content-Type: application/json" \
  -d '{"description": "Enhanced description with more than twenty characters for validation"}'
Assign a new power to a hero:

bash
curl -X POST http://localhost:5555/hero_powers \
  -H "Content-Type: application/json" \
  -d '{"strength": "Strong", "power_id": 2, "hero_id": 5}'
Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a Pull Request

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Flask documentation and community

SQLAlchemy ORM

All contributors and testers

Support
For support, please:

Check the troubleshooting section above

Review the API documentation

Create an issue in the GitHub repository

Contact
Project Maintainer: [Your Name]
Email: [your.email@example.com]
GitHub: https://github.com/YOUR_USERNAME