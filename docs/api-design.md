# API Design

## 1. Overview

The Expense Tracker backend follows a layered, feature-based architecture.

The primary request flow is:

Request → Route → Schema/Validation → Service → Repository → SQLAlchemy → PostgreSQL

The architecture is designed to remain consistent with the layered architecture used in the Railway Reservation System while adapting the implementation to Flask, Python, and SQLAlchemy.

---

## 2. Architecture

The backend is organized by feature/module.

```text
app/
├── modules/
│   ├── auth/
│   ├── users/
│   ├── categories/
│   └── transactions/
└── models/
```

Each feature module contains the layers required by that feature.

```text
Feature Module
├── route.py
├── schema.py
├── service.py
└── repository.py
```

Not every module must contain every layer immediately. Files are added when the corresponding functionality is required.

---

## 3. Layer Responsibilities

### 3.1 Route

`route.py` is the HTTP/controller layer.

Responsibilities:

- Define Flask routes.
- Receive HTTP requests.
- Extract request data.
- Invoke validation.
- Call the appropriate service method.
- Return HTTP responses.
- Handle HTTP-specific concerns.

Routes should not contain business logic or direct database queries.

### 3.2 Schema

`schema.py` contains request and response schemas.

Responsibilities:

- Validate incoming request data.
- Define expected request structure.
- Validate data types and constraints.
- Define response structures where required.

Validation should happen before business logic is executed.

### 3.3 Service

`service.py` contains business logic.

Responsibilities:

- Implement application/business rules.
- Coordinate multiple repository operations when required.
- Enforce business-level rules.
- Transform data between application layers.
- Coordinate transactions where required.

The service layer should not depend on Flask request/response objects.

The service layer should not directly perform database queries.

For transactions, the service layer must enforce business rules that cannot be represented by the current database constraints.

For example:

- A transaction's `type` must match the selected category's `type`.
- A transaction category must belong to the authenticated user.

### 3.4 Repository

`repository.py` contains database-access logic.

Responsibilities:

- Query database records.
- Create, update, and delete records.
- Execute SQLAlchemy queries.
- Handle persistence-related operations.
- Use SQLAlchemy to interact with PostgreSQL.

Repositories should not contain business rules.

### 3.5 Model

Models are defined under:

```text
app/models/
```

Responsibilities:

- Represent database tables.
- Define columns and data types.
- Define relationships.
- Define database-level constraints.
- Map Python objects to PostgreSQL records.

Models should not contain HTTP or application-flow logic.

---

## 4. Request Flow

A typical API request follows this flow:

```text
Client
  ↓
Flask Route
  ↓
Request Validation
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

The response follows the reverse direction:

```text
PostgreSQL
  ↓
SQLAlchemy
  ↓
Repository
  ↓
Service
  ↓
Route
  ↓
JSON Response
  ↓
Client
```

---

## 5. Response Format

API responses should use JSON.

Successful responses should provide the requested resource or operation result.

Example:

```json
{
  "data": {
    "id": "uuid",
    "name": "Food",
    "type": "expense"
  }
}
```

Error responses should provide a consistent structure.

Example:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data"
  }
}
```

The exact response structure may be extended as the API develops, but consistency across endpoints is required.

---

## 6. Error Handling

Application errors should be handled centrally rather than implementing duplicated error-handling logic in every route.

The API should distinguish between:

- Validation errors
- Authentication errors
- Authorization errors
- Resource-not-found errors
- Business-rule errors
- Database errors
- Unexpected internal errors

Routes should return appropriate HTTP status codes.

---

## 7. Authentication and Authorization

Authentication will use JWT.

The authentication flow is:

```text
Login
  ↓
Validate credentials
  ↓
Generate JWT
  ↓
Client stores token
  ↓
Client sends Authorization header
  ↓
Authentication middleware/decorator
  ↓
Protected route
```

Protected endpoints require a valid JWT.

Authorization rules, where required, should be enforced separately from authentication.

The current MVP does not require an administrative role.

---

## 8. Validation

Request validation occurs at the API boundary before the service layer.

Validation includes:

- Required fields
- Data types
- String lengths
- Valid transaction types
- Positive transaction amounts
- Valid dates
- UUID formats
- Request-specific constraints

Database constraints remain important even when API validation exists.

API validation protects the application boundary, while database constraints protect data integrity.

---

## 9. Database Access Rules

The following rules apply:

1. Routes must not directly query the database.
2. Services must not directly query the database.
3. Repository classes/functions handle database access.
4. SQLAlchemy models represent database entities.
5. Business rules belong in services.
6. Database integrity constraints belong in the database/model definition.
7. Transactions involving multiple related database operations should be coordinated by the service layer.

---

## 10. Module Organization

The initial feature modules are:

```text
app/modules/
├── auth/
├── users/
├── categories/
└── transactions/
```

### Auth

Responsible for:

- Registration
- Login
- JWT generation
- Authentication-related operations

### Users

Responsible for:

- User profile operations
- User-specific functionality

### Categories

Responsible for:

- Category creation
- Category retrieval
- Category update
- Category deletion

### Transactions

Responsible for:

- Income/expense creation
- Transaction retrieval
- Transaction update
- Transaction deletion
- Transaction filtering/search
- Transaction-related operations

---

## 11. Naming Conventions

Python naming conventions are used throughout the backend.

- Files: `snake_case`
- Variables: `snake_case`
- Functions: `snake_case`
- Classes: `PascalCase`
- Database tables: `snake_case`
- Database columns: `snake_case`

Examples:

```text
transaction.py
transaction_service.py
find_transactions()
Transaction
transaction_date
```

---

## 12. API Versioning

The initial MVP will use a single API version:

```text
/api/v1/
```

Examples:

```text
/api/v1/auth/login
/api/v1/categories
/api/v1/transactions
```

Versioning allows future API changes without immediately breaking existing clients.

---

## 13. Design Principles

The backend follows these principles:

- Separation of concerns
- Feature-based organization
- Layered architecture
- Single responsibility
- Centralized error handling
- Validation at the API boundary
- Business logic in services
- Database access through repositories
- Database integrity enforced through constraints
- Consistent request and response conventions
- Avoid unnecessary abstractions
- Prefer simple implementations suitable for the MVP

## 14. Authentication and Security

### 14.1 Password Hashing

Passwords must never be stored in plaintext.

The application will use Werkzeug's password hashing utilities to hash passwords before storing them in the database.

```text
Plaintext Password
        ↓
Password Hashing
        ↓
password_hash
        ↓
PostgreSQL
```

During login, the provided password will be verified against the stored password hash.

The application will never return `password_hash` in API responses.

---

### 14.2 JWT Authentication

Authentication will use Flask-JWT-Extended.

After successful login, the server generates a JWT containing the authenticated user's identity.

The JWT identity will be the user's UUID.

Example payload:

```json
{
  "sub": "<user-uuid>"
}
```

The JWT must not contain:

- Passwords
- Password hashes
- Unnecessary sensitive user information

---

### 14.3 JWT Secret

The JWT signing secret will be provided through an environment variable:

```env
JWT_SECRET_KEY=<secret>
```

The secret must:

- Not be hard-coded in source code.
- Not be committed to Git.
- Be stored in the local `.env` file during development.
- Be provided through secure environment configuration in deployment environments.

#### JWT Expiration

Access JWTs will expire after 1 hour.

The expiration limits the lifetime of a stolen access token and requires the user to authenticate again after the token expires.

The expiration will be configured through the application configuration rather than hard-coded in authentication logic.

---

### 14.4 Registration Flow

The registration flow is:

```text
Client
  ↓
POST /api/v1/auth/register
  ↓
Request Validation
  ↓
Auth Service
  ↓
Check Email Uniqueness
  ↓
Hash Password
  ↓
Create User
  ↓
PostgreSQL
  ↓
Return Safe User Response
```

The registration response must not expose the stored password hash.

---

### 14.5 Login Flow

The login flow is:

```text
Client
  ↓
POST /api/v1/auth/login
  ↓
Request Validation
  ↓
Auth Service
  ↓
Find User by Email
  ↓
Verify Password
  ↓
Generate JWT
  ↓
Return Authentication Response
```

The authentication response will contain the JWT and safe user information required by the client.

---

### 14.6 Protected Endpoints

Protected endpoints require a valid JWT in the `Authorization` header.

Expected format:

```text
Authorization: Bearer <JWT>
```

The authentication middleware will:

1. Extract the JWT.
2. Verify the JWT signature and validity.
3. Extract the authenticated user's identity.
4. Make the authenticated user identity available to the protected request.

Protected endpoints must not trust a client-supplied `user_id` to determine the authenticated user.

---

### 14.7 Authentication Errors

Authentication failures will use the standardized API error format.

Examples:

```text
Missing JWT         → 401 UNAUTHORIZED
Invalid JWT         → 401 UNAUTHORIZED
Expired JWT         → 401 UNAUTHORIZED
Invalid credentials → 401 UNAUTHORIZED
```

Example response:

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

---

### 14.8 User Isolation

Authenticated user identity must be derived from the verified JWT.

User-owned resources must always be accessed using the authenticated user's identity.

For example:

```text
JWT
 ↓
Authenticated User ID
 ↓
Service
 ↓
Repository
 ↓
Query using authenticated user ID
```

Client-provided user identifiers must not be trusted for authorization or ownership checks.

This ensures that one user cannot access or modify another user's categories or transactions.

---

### 14.9 Security Principles

The authentication implementation follows these principles:

- Never store plaintext passwords.
- Never return password hashes.
- Keep JWT secrets outside source control.
- Keep JWT payloads minimal.
- Require JWT authentication for protected endpoints.
- Derive resource ownership from the authenticated identity.
- Return consistent authentication errors.
- Keep authentication logic in the authentication layer rather than embedding it in individual business operations.

## 15. Registration Behavior

### Registration Endpoint

The registration endpoint is:

`POST /api/v1/auth/register`

### Registration Inputs

The request contains:

- `name`
- `email`
- `password`

Request validation is performed using the `RegisterRequest` schema.

### Registration Processing

The registration process follows these steps:

1. Validate the request data.
2. Search for an existing user using the provided email.
3. If the email is already registered, raise a `ValidationError`.
4. Hash the plaintext password.
5. Create the user through the repository.
6. Commit the database transaction.
7. Return the safe user information.

### Duplicate Email Handling

Email addresses must be unique.

If the email is already registered, the API returns:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is already registered"
  }
}
```

HTTP status: `400 Bad Request`.

### Registration Result

A successful registration returns:

- `id`
- `name`
- `email`
- `created_at`

The response must not contain `password` or `password_hash`.

### Registration Transaction

The service layer owns the database transaction.

- The repository adds and flushes the new user.
- The service commits the transaction after successful user creation.
- If an unexpected error occurs, the service rolls back the transaction.

### Registration Layer Interaction

```text
Route
  ↓
Request Validation
  ↓
Auth Service
  ├── Check email uniqueness
  ├── Hash password
  ├── Create user
  └── Commit transaction
  ↓
User Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

The route layer handles HTTP concerns, while the service layer handles registration business logic.

---

## 16. Login Behavior

### Login Endpoint

The login endpoint is:

`POST /api/v1/auth/login`

### Login Inputs

The request contains:

- `email`
- `password`

Request validation is performed using the `LoginRequest` schema.

### Login Processing

The login process follows these steps:

1. Validate the request data.
2. Search for a user using the provided email.
3. If the user does not exist, raise an `UnauthorizedError`.
4. Verify the supplied password against the stored password hash.
5. If the password is incorrect, raise an `UnauthorizedError`.
6. Generate an access JWT using the authenticated user's UUID as the token identity.
7. Return the access token and safe user information.

### Failed Authentication

Both a non-existent email and an incorrect password return the same response:

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid email or password"
  }
}
```

HTTP status: `401 Unauthorized`.

This prevents the API from revealing whether a particular email address is registered.

### Login Result

A successful login returns:

```json
{
  "data": {
    "access_token": "<JWT>",
    "user": {
      "id": "<UUID>",
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

HTTP status: `200 OK`.

The response must not contain the user's password or password hash.

### Login Transaction

Login does not modify persistent user data, so no database transaction commit is required.

### Login Layer Interaction

```text
Route
  ↓
Request Validation
  ↓
Auth Service
  ├── Find user by email
  ├── Verify password
  └── Generate JWT
  ↓
User Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

The route layer handles HTTP concerns, while the service layer handles login business logic and JWT generation.
