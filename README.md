# Password Generator, Checker, and Currency Converter

This is a FastAPI-based web application providing three main functionalities:

1. **Password Generation**  
2. **Password Security Check**  
3. **Currency Conversion**

---

## Features

- **Password Generation**: Create secure passwords of customizable length, optionally including a specific word.
- **Password Security Check**: Evaluate the security of a given password based on length, character variety, and other criteria.
- **Currency Conversion**: Convert amounts between currencies using real-time exchange rates.

---

## How to Run the Application

### Prerequisites
- Python 3.9 or later installed on your system.
- A virtual environment (optional but recommended).
- Required Python libraries installed (`FastAPI`, `Jinja2`, `freecurrencyapi`, `python-dotenv`, and `uvicorn`).

### Steps to Set Up and Run

#### Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```
#### Set Up the Environment

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install the required libraries:

```bash
pip install fastapi jinja2 freecurrencyapi python-dotenv uvicorn
```
Create .env file:

Add the following to a .env file in the root directory:
```bash
CONVERSION_API=fca_live_YourAPIKeyHere
```

Run the Application
```bash
uvicorn main:app --reload
```
The app will be available at http://127.0.0.1:8000

###  Application Functionality
#### 1. Password Generation
This feature generates secure passwords with customizable length and an optional specific word.

Endpoints
- GET /generate-password: Displays the password generation form.
- POST /generate-password: Accepts form data to generate a password.


The form and results are rendered via index.html

#### 2. Password Security Check
Checks the security of a given password based on:

Minimum length of 12 characters.
Inclusion of uppercase, lowercase, digits, and special characters.
Avoiding common patterns or weak passwords.

Endpoints:
- GET /check-password: Displays the password security check form.
- POST /check-password: Evaluates the security of the provided password.


The form and results are rendered via checkPassword.html

#### 3. Currency Conversion
Converts an amount from one currency to another using live exchange rates.

Endpoints
- GET /get-conversion: Displays the currency conversion form.
- POST /get-conversion: Performs the conversion and displays the results.

The form and results are rendered via currency.html

## Dependencies
FastAPI: Web framework.
Jinja2: Templating engine.
freecurrencyapi: Currency conversion API.
python-dotenv: Environment variable management.
uvicorn: ASGI server.
```bash
pip install fastapi jinja2 freecurrencyapi python-dotenv uvicorn
```
**PS: I added apiKey for conversion in .env file.**

**Go to http://127.0.0.1:8000/docs Swagger UI**
