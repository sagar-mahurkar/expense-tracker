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
