from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import uvicorn
import sqlite3
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet   #  encryption engine

load_dotenv()

#Initialize the cipher suite using the hidden key
cipher = Fernet(os.getenv("VAULT_ENCRYPTION_KEY"))

app = FastAPI()

api_key_header = APIKeyHeader(name="X-Vault-Token")

def verify_token(api_key: str = Security(api_key_header)):
    if api_key != os.getenv("VAULT_API_KEY"):
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

@app.post("/secrets/")
def create_secret(item: SecretItem, token: str = Depends(verify_token)):
    # NEW: Encrypt the text into unreadable bytes, then convert to a storable string
    encrypted_content = cipher.encrypt(item.content.encode()).decode()
    
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    #Insert the encrypted_content instead of the raw content
    cursor.execute("INSERT INTO secrets (title, content) VALUES (?, ?)", (item.title, encrypted_content))
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
    
    #Decrypt the content back into readable text before returning it to the user
    return [
        {
            "id": row[0], 
            "title": row[1], 
            "content": cipher.decrypt(row[2].encode()).decode()
        } for row in rows
    ]

@app.delete("/secrets/{secret_id}")
def delete_secret(secret_id: int, token: str = Depends(verify_token)):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM secrets WHERE id = ?", (secret_id,))
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Secret not found")
    return {"status": "success", "message": f"Secret {secret_id} permanently deleted"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)