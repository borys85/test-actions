from fastapi import FastAPI
from datetime import datetime, date

app = FastAPI(title="Time Server API")

@app.get("/")
def root():
    return {"message": "Добро пожаловать в Time Server API"}

@app.get("/time")
def get_time():
    """Возвращает текущее время UTC"""
    return {"current_time_utc": datetime.utcnow().isoformat()}

@app.get("/datetime")
def get_datetime():
    """Возвращает текущие дату и время локального сервера"""
    return {"datetime": datetime.now().isoformat()}

@app.get("/date")
def get_date():
    """Возвращает текущую дату"""
    return {"date": date.today().isoformat()}

@app.get("/health")
def health_check():
    """Эндпоинт для проверки работоспособности"""
    return {"status": "ok", "service": "time-server"}