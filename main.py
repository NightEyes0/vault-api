from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import sqlite3  #built-in SQL database engine

app = FastAPI()

# Create the database and 'secrets' table if they don't exist
def init_db():
    conn = sqlite3.connect("vault.db")
    conn.execute("CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, title TEXT, content TEXT)")
    conn.commit()
    conn.close()

init_db() # Run every time the server starts

class SecretItem(BaseModel):
    title: str
    content: str

@app.get("/")
def read_root():
    return {"message": "Secure Vault API is running!"}

@app.post("/secrets/")
def create_secret(item: SecretItem):
    return {"status": "success", "received_title": item.title}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)