from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Добро пожаловать в Time Server API"}

@app.get("/time")
def get_time():
    return {"current_time_utc": datetime.utcnow().isoformat()}

@app.get("/datetime")
def get_datetime():
    return {"datetime": datetime.now().isoformat()}

@app.get("/date")
def get_date():
    return {"date": datetime.now().date().isoformat()}