# Secure Vault API 

A RESTful backend API built with Python and FastAPI, designed to securely store,retriev and delete sensitive text data using an encrypted SQLite relational database.

## Enterprise Architecture (V2.0)
* **FastAPI Framework:** High-performance asynchronos web routing and automatic OpenAPI (Swagger) documentation generation.
* **Data-at-Rest Encryption:** Integrates `cryptography` to ensure all database payloads are cryptographically scrambled before being written to disk, protecting against physical data exfiltration.
* **Secrets Management:** Implements `python-dotenv` to isolate environmental configurations and API keys away from source code.
* **Security & Authentication:** Global endpoint protection using injected API Key Header dependencies (`X-Vault-Token`) to reject unauthorized HTTP requests (403 Forbidden).
* **Data Validation:** Strict payload validation and serialization using Pydantic `BaseModel`.

## API Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/` | Health check for the server | No |
| `POST` | `/secrets/` | Creates a new encrypted secret in the vault | Yes |
| `GET` | `/secrets/` | Retrieves and decrypts all stored secrets | Yes |
| `DELETE` | `/secrets/{id}` | Permanently destroys a specific secret | Yes |

## Local Development
1. Create a `.env` file in the root directory:
   ```text
   VAULT_API_KEY=your_secure_password
   VAULT_ENCRYPTION_KEY=your_32_byte_base64_fernet_key