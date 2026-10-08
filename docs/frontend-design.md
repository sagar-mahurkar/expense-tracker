# Frontend Design

## 1. Technology

- Vue 3
- TypeScript
- Vite

## 2. Frontend Structure

frontend/
└── src/
    ├── assets/
    ├── components/
    ├── layouts/
    ├── pages/
    ├── router/
    ├── services/
    ├── stores/
    ├── types/
    ├── App.vue
    ├── main.ts
    └── style.css

### Responsibilities

- `components/` — Reusable UI components.
- `layouts/` — Application-level layouts.
- `pages/` — Route-level views.
- `router/` — Vue Router configuration.
- `services/` — HTTP/API communication.
- `stores/` — Application and authentication state.
- `types/` — TypeScript types.
- `assets/` — Static assets.

## 3. Architecture Principles

- Keep the frontend clean and maintainable.
- Keep MVP scope strict.
- Avoid unnecessary abstractions and over-engineering.
- Foundational decisions should allow future growth without requiring a rewrite.
- Add abstractions only when they are actually needed.

## 4. Dependencies

- Vue Router for routing.
- Pinia for application and authentication state.
- Axios for API communication.
- Bootstrap for standard UI components and responsive layout.

## 5. Development Tooling

- Use Vue - Official for Vue 3 + TypeScript language support in VS Code.
- Do not use Vetur alongside Vue - Official.
- Do not add custom Vue module declarations to work around editor diagnostics when standard Vue tooling is correctly configured.

## 6. Application Layout

Protected application pages use a shared `AppLayout.vue`.

The application layout provides:

- Application navigation.
- Links to Dashboard, Transactions, and Categories.
- Logged-in user identity.
- Logout action.
- Shared page container through `RouterView`.

Login and registration pages do not use the application layout.

The navbar uses a light Bootstrap style with a subtle bottom border.

## 7. Implemented MVP UI

### Authentication

- Login page.
- Registration page.
- Bootstrap-based forms.
- API integration deferred to Phase 12.

### Dashboard

- Dashboard heading and description.
- Balance summary.
- Income summary.
- Expense summary.
- Recent transactions section.

### Transactions

- Transaction table.
- Add Transaction modal.
- Transaction form containing:
  - Type
  - Amount
  - Category
  - Description
  - Transaction date
- Search by description.
- Type filter.
- Date filter.
- Clear filters action.
- Pagination UI.
- Edit and Delete actions.
- API integration deferred to Phase 12.

### Categories

- Category table.
- Add Category modal.
- Category creation form.
- Delete action.
- API integration deferred to Phase 12.

## 8. MVP UI Scope

The frontend currently focuses on the core MVP workflow.

The following are intentionally deferred:

- API integration.
- Authentication state integration.
- Real user information.
- Functional logout.
- Advanced dashboard visualizations.
- Additional profile functionality.
- Additional UI abstractions.

These will only be added when required by the remaining implementation phases.

## 9. Current Status

Phase 10 — Frontend Setup: Complete.

Phase 11 — Frontend UI: UI implementation complete.

Implemented:

- Bootstrap UI foundation.
- Authentication pages.
- Dashboard UI.
- Transactions UI.
- Categories UI.
- Shared application layout.
- Navigation between application pages.
- Responsive Bootstrap-based layouts.

API integration and authentication state integration are planned for Phase 12.
