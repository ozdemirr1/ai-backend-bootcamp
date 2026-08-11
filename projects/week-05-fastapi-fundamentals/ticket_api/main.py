from fastapi import FastAPI

app = FastAPI(title="Week 05 FastAPI Fundamentals")


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tickets")
def list_tickets(
    status: str | None = None, limit: int = 10
) -> dict[str, str | int | None]:
    return {"status_filter": status, "limit": limit}


@app.get("/tickets/{ticket_id}")
def read_ticket(ticket_id: int) -> dict[str, int]:
    return {"ticket_id": ticket_id}
