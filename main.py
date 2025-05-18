from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Flower API on Railway is working!"}
