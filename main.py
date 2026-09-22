from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import sqlite3

app = FastAPI()

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
def create_secret(item: SecretItem):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO secrets (title, content) VALUES (?, ?)", (item.title, item.content))
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return {"status": "success", "id": inserted_id, "title": item.title}

#  Retrieve data from the database
@app.get("/secrets/")
def get_secrets():
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM secrets")
    rows = cursor.fetchall()
    conn.close()
    # Convert raw SQL data into a clean list of dictionaries
    return [{"id": row[0], "title": row[1], "content": row[2]} for row in rows]

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)