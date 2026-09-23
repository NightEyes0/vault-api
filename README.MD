# Secure Vault API 🛡️

A RESTful backend API built with Python and FastAPI, to securely store, retrieve, and delete sensitive text data using a persistent SQLite relational database.

## Enterprise Architecture
* **FastAPI Framework:** High-performance  web routing and automatic OpenAPI (Swagger) documentation generation.
* **Relational Database (SQLite):** Persistent data storage using SQL `INSERT`, `SELECT`, and `DELETE` operations.
* **Data Validation:** Strict payload validation and serialization using Pydantic `BaseModel`.
* **Security & Authentication:** Global endpoint protection using injected API Key Header dependencies (`X-Vault-Token`) to reject unauthorized HTTP requests (403 Forbidden).

## API Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/` | Health check for the server | No |
| `POST` | `/secrets/` | Creates a new secret in the vault | Yes |
| `GET` | `/secrets/` | Retrieves all stored secrets | Yes |
| `DELETE` | `/secrets/{id}` | Permanently destroys a specific secret | Yes |

## Local Development
Start the Uvicorn ASGI server:
python main.py