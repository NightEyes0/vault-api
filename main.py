from fastapi import FastAPI
from pydantic import BaseModel # NEW: Helps us define data structures
import uvicorn

app = FastAPI()

# define "Secret" should look like
class SecretItem(BaseModel):
    title: str
    content: str

@app.get("/")
def read_root():
    return {"message": "Secure Vault API is running!"}

# A POST route catches incoming data
@app.post("/secrets/")
def create_secret(item: SecretItem):
    return {"status": "success", "received_title": item.title}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)