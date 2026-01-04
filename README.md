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

## Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Flask documentation and community

SQLAlchemy ORM

All contributors and testers

## Support
For support, please:

Check the troubleshooting section above

Review the API documentation

Create an issue in the GitHub repository

## Contact
Project Maintainer: Kevin kiplangat
Email: kiplangatkevin335@gmail.com
GitHub: https://github.com/kevinkiplangat432