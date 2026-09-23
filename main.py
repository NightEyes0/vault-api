from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import uvicorn
import sqlite3

app = FastAPI()

api_key_header = APIKeyHeader(name="X-Vault-Token")

def verify_token(api_key: str = Security(api_key_header)):
    if api_key != "supersecret123":
        raise HTTPException(status_code=403, detail="Access Denied: Invalid Token")
    return api_key

def init_db():
    conn = sqlite3.connect("vault.db")
    conn.execute("CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, title TEXT, content TEXT)")
    conn.commit()
    conn.close()

init_db() 

class SecretItem(BaseModel):
    title: str
    content: str

@app.get("/")
def read_root():
    return {"message": "Secure Vault API is running!"}

#Locked down POST with Depends(verify_token)
@app.post("/secrets/")
def create_secret(item: SecretItem, token: str = Depends(verify_token)):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO secrets (title, content) VALUES (?, ?)", (item.title, item.content))
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return {"status": "success", "id": inserted_id, "title": item.title}

@app.get("/secrets/")
def get_secrets(token: str = Depends(verify_token)):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM secrets")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "content": row[2]} for row in rows]

# Delete endpoint with a Path Parameter and Security
@app.delete("/secrets/{secret_id}")
def delete_secret(secret_id: int, token: str = Depends(verify_token)):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM secrets WHERE id = ?", (secret_id,))
    conn.commit()
    deleted_count = cursor.rowcount # Checks if a row was actually deleted
    conn.close()
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Secret not found")
    return {"status": "success", "message": f"Secret {secret_id} permanently deleted"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)