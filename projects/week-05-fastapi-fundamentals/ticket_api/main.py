from fastapi import FastAPI

app = FastAPI(title="Week 05 FastAPI Fundamentals")


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}
