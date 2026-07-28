from fastapi import FastAPI, BackgroundTasks
from datetime import datetime, date
import httpx

app = FastAPI(title="Time Server API")

LOKI_URL = "http://loki:3100/loki/api/v1/push"
DEFAULT_LABELS = {"app": "time-server", "env": "dev"}

async def send_log_to_loki(message: str, level: str = "info", extra_labels: dict = None):
    """
    Отправляет лог в Loki через POST /loki/api/v1/push
    Формат: https://grafana.com/docs/loki/latest/reference/loki-http-api/#ingest-logs
    """
    labels = {**DEFAULT_LABELS, "level": level, **(extra_labels or {})}
    # Loki ожидает timestamp в наносекундах
    ts = str(int(datetime.utcnow().timestamp() * 1e9))
    
    payload = {
        "streams": [
            {
                "stream": labels,
                "values": [[ts, message]]
            }
        ]
    }
    
    try:
        async with httpx.AsyncClient() as client:
            await client.post(LOKI_URL, json=payload, timeout=5.0)
    except Exception as e:
        print(f"Loki error: {e}")

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
    return {"date": date.today().isoformat()}

@app.get("/health")
async def health_check(background_tasks: BackgroundTasks):
    # BackgroundTasks гарантирует выполнение асинхронной задачи
    background_tasks.add_task(send_log_to_loki, "Health check performed", level="debug")
    return {"status": "ok", "service": "time-server"}