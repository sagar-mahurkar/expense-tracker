# Frontend Design

## 1. Technology

- Vue 3
- TypeScript
- Vite

## 2. Frontend Structure

```text
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
```

### Directory Responsibilities

| Directory | Responsibility |
| --- | --- |
| `components/` | Reusable UI components |
| `layouts/` | Application-level page layouts |
| `pages/` | Route-level views |
| `router/` | Vue Router configuration |
| `services/` | HTTP/API communication |
| `stores/` | Client-side application and authentication state |
| `types/` | Shared TypeScript types |
| `assets/` | Static frontend assets |

## 3. Architecture Principles

- Keep the frontend clean and maintainable.
- Keep the MVP scope strict.
- Avoid unnecessary abstractions and over-engineering.
- Make foundational decisions that allow the application to grow without requiring a rewrite.
- Introduce additional abstractions only when the application actually needs them.

## 4. Planned Dependencies

The frontend will use:

- Vue Router for routing and route protection.
- Pinia for application and authentication state.
- Axios for API communication.

These dependencies will be added only as they become part of the implementation.

## 5. Development Tooling

- Use **Vue - Official** for Vue 3 + TypeScript language support in VS Code.
- Do not use Vetur alongside Vue - Official.
- Do not add custom Vue module declarations to work around editor diagnostics when the standard Vue tooling is correctly configured.

## 6. Current Status

Frontend setup is in progress.

The default Vite demo components and assets have been removed. The application-specific frontend structure will be established next.
