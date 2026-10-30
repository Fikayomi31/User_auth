# FastAPI Authentication API

A RESTful authentication and authorization API built with **FastAPI**, **Python**, **SQLAlchemy**, and **JWT (JSON Web Tokens)**.

This project demonstrates how to implement secure user registration, login, password hashing, token-based authentication, and role-based access control using asynchronous database operations.

## Project Overview

The goal of this project is to build an authentication system that allows users to create accounts, securely log in, and access protected resources based on their assigned roles.

The application uses JWT access tokens to authenticate users and role-based authorization to control access to restricted endpoints.

It uses SQLite for data persistence and asynchronous SQLAlchemy sessions for database operations.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| SQLAlchemy | Database ORM |
| SQLite | Relational database |
| Pydantic | Request validation and response schemas |
| JWT | Token-based authentication |
| Passlib / bcrypt | Password hashing and verification |
| OAuth2PasswordBearer | Bearer-token authentication dependency |
| Uvicorn | ASGI development server |

## Key Features

### 1. User Registration
- Register new users with a username, email, and password.
- Validate incoming data using Pydantic.
- Check for existing usernames and email addresses.
- Hash passwords before storing them in the database.
- Assign the default `USER` role to newly registered accounts.

### 2. User Login
- Authenticate users using their email and password.
- Verify submitted passwords against stored password hashes.
- Generate a JWT access token after successful authentication.
- Return the access token and token type to the client.

### 3. JWT Authentication
- Generate signed JWT access tokens.
- Store the user's ID in the token subject (`sub`).
- Decode and validate tokens when protected endpoints are accessed.
- Reject invalid tokens and requests from users who no longer exist.

### 4. Role-Based Access Control (RBAC)

The application supports two user roles:

| Role | Description |
|---|---|
| USER | Standard registered user with access to permitted user resources |
| ADMIN | Administrator with access to administrator-restricted resources |

Access to protected resources is controlled using reusable role-checking dependencies.

### 5. Asynchronous Database Operations
- SQLAlchemy asynchronous database sessions.
- SQLite database persistence.
- Database queries using asynchronous operations.
- Relational user data management.

### 6. API Documentation
FastAPI automatically generates interactive API documentation.

Available documentation interfaces:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Authentication Workflow

The authentication process follows these steps:

1. A user submits registration details.
2. The application validates the submitted information.
3. The password is hashed and stored in the database.
4. The user submits their email and password to log in.
5. The application verifies the credentials.
6. A JWT access token is generated and returned.
7. The client sends the token when accessing protected endpoints.
8. The application validates the token and retrieves the corresponding user.
9. Role-based permissions determine whether the user can access the requested resource.

## Project Structure

The project follows a modular application structure:

```text
User_auth/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── jwt.py
│   │   └── security.py
│   │
│   ├── model/
│   │   └── user.py
│   │
│   ├── routers/
│   │   └── auth.py
│   │
│   ├── schemas/
│   │   └── user_schema.py
│   │
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   └── core/
│
├── auth.db
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: This structure illustrates the main application components. Adjust it to match the actual files in your project.*

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

Navigate into the project directory:

```bash
cd User_auth
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root and configure the required application settings.

For example:

```env
JWT_SECRET_KEY=your-secure-secret-key
```

Use a strong, randomly generated secret key in a real deployment. Do not commit your `.env` file or expose your secret key publicly.

### 6. Start the application

```bash
uvicorn app.main:app --reload
```

The application should be available at:

```text
http://127.0.0.1:8000
```

## API Endpoints

The following table describes the authentication endpoints.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate a user and generate an access token |
| GET | `/api/auth/me` | Retrieve the currently authenticated user's information |

Protected endpoints require a valid JWT access token.

*Additional role-specific endpoints depend on the routes registered in the application.*

## Testing the API with Postman

The JSON-based login endpoint can be tested using Postman.

### User Registration

Send a POST request to:

```text
http://127.0.0.1:8000/api/auth/register
```

Example JSON body:

```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "yourpassword"
}
```

### User Login

Send a POST request to:

```text
http://127.0.0.1:8000/api/auth/login
```

Select:

`Body → raw → JSON`

Example:

```json
{
    "email": "test@example.com",
    "password": "yourpassword"
}
```

A successful login returns:

```json
{
    "access_token": "your-generated-jwt-token",
    "token_type": "bearer"
}
```

### Accessing Protected Endpoints

Copy the access token returned from login.

In Postman:

1. Open the protected endpoint.
2. Select the Authorization tab.
3. Choose Bearer Token.
4. Paste your access token.
5. Send the request.

The API will validate the token and identify the authenticated user.

## Swagger UI OAuth2 Authorization Note

During development, an integration issue was encountered between the JSON-based login endpoint and Swagger UI's automatic OAuth2 authorization flow.

The login endpoint uses a Pydantic `UserLogin` schema and expects JSON credentials containing:

- `email`
- `password`

However, Swagger UI's OAuth2 password-flow authorization mechanism expects form-encoded credentials containing:

- `username`
- `password`

Consequently, the login endpoint can successfully authenticate users and generate JWT access tokens when tested directly through Postman or Swagger's normal endpoint execution, while Swagger's automatic **Authorize** process can return:

`422 Unprocessable Entity`

This happens because the request format expected by the OAuth2 authorization flow differs from the JSON format accepted by the login endpoint.

**Important distinction:** This issue concerns the integration between the login request format and Swagger's automatic OAuth2 authorization process. It does not, by itself, indicate that JWT generation, password verification, or token validation is broken.

The current implementation retains the JSON-based login endpoint. Postman can be used to authenticate users and obtain access tokens, which can then be supplied as Bearer tokens when testing protected endpoints.

## HTTP Response Codes

| Status Code | Meaning |
|---|---|
| 200 OK | Request completed successfully |
| 201 Created | Resource successfully created |
| 401 Unauthorized | Missing, invalid, or expired authentication credentials |
| 403 Forbidden | Authenticated user does not have the required permission |
| 409 Conflict | Username or email already exists |
| 422 Unprocessable Entity | Request validation or input format error |
| 500 Internal Server Error | Unexpected server-side error |

## Security Considerations

This project implements several important authentication security practices:

- Passwords are hashed rather than stored as plain text.
- JWT tokens are signed using a secret key.
- Protected endpoints require authentication.
- Role-based permissions restrict access to sensitive resources.
- Invalid authentication attempts receive appropriate error responses.
- Environment variables are used for sensitive configuration.

For production deployment, additional considerations include token expiration and refresh strategies, HTTPS, secret-key management, rate limiting, and account deactivation.

## Learning Outcomes

Through this project, I gained practical experience with:

- Building REST APIs using FastAPI.
- Implementing asynchronous database operations with SQLAlchemy.
- Designing database models and Pydantic schemas.
- Password hashing and verification.
- JWT token generation and validation.
- OAuth2 bearer-token authentication.
- Dependency injection in FastAPI.
- Implementing role-based access control.
- Handling authentication and authorization errors.
- Testing API endpoints using Postman and Swagger UI.

## Future Improvements

Potential improvements include:

- Refresh token implementation.
- Password reset functionality.
- Email verification.
- Account activation and deactivation.
- More comprehensive automated tests.
- PostgreSQL database support.
- Deployment to a cloud hosting platform.

## Author
Fikayo Ogundijo

Backend development project built as part of a Python + FastAPI Backend Development Internship by Datheon