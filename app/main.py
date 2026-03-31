from fastapi import FastAPI

app = FastAPI(title="Dot Campus Discussion API")


@app.get("/")
def root():
    return {"message": "Dot Campus Discussion API is running"}
