from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    HTTPException,
    Query,
    Response,
    status,
)
from starlette.types import Lifespan

from ticket_api.dependencies import get_ticket_service
from ticket_api.lifespan import database_lifespan
from ticket_api.models import (
    Ticket,
    TicketPriority,
    TicketStatus,
)
from ticket_api.schemas import (
    TicketCreateRequest,
    TicketResponse,
    TicketUpdateRequest,
)
from ticket_api.schemas import TicketStatus as TicketStatusValue
from ticket_api.services import (
    DuplicateTicketError,
    TicketNotFoundError,
    TicketService,
)

router = APIRouter()


TicketServiceDependency = Annotated[
    TicketService,
    Depends(get_ticket_service),
]


def _to_ticket_response(ticket: Ticket) -> TicketResponse:
    return TicketResponse(
        ticket_id=ticket.ticket_id,
        title=ticket.title,
        priority=ticket.priority.value,
        status=ticket.status.value,
    )


@router.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/tickets", response_model=list[TicketResponse])
def list_tickets(
    service: TicketServiceDependency,
    status: TicketStatusValue | None = None,
    limit: Annotated[
        int,
        Query(ge=1, le=100),
    ] = 10,
) -> list[TicketResponse]:
    tickets = service.list_tickets()

    if status is not None:
        tickets = [ticket for ticket in tickets if ticket.status.value == status]

    limited_tickets = tickets[:limit]

    return [_to_ticket_response(ticket) for ticket in limited_tickets]


@router.post(
    "/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED
)
def create_ticket(
    ticket_data: TicketCreateRequest,
    service: TicketServiceDependency,
) -> TicketResponse:
    try:
        ticket = service.create_ticket(
            title=ticket_data.title,
            priority=TicketPriority(ticket_data.priority),
        )
    except DuplicateTicketError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return _to_ticket_response(ticket)


@router.post("/tickets/preview")
def preview_ticket(ticket: TicketCreateRequest) -> dict[str, str]:
    return {
        "title": ticket.title,
        "priority": ticket.priority,
    }


@router.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse,
)
def read_ticket(
    ticket_id: int,
    service: TicketServiceDependency,
) -> TicketResponse:
    try:
        ticket = service.get_ticket(ticket_id)
    except TicketNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc

    return _to_ticket_response(ticket)


@router.patch(
    "/tickets/{ticket_id}",
    response_model=TicketResponse,
)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdateRequest,
    service: TicketServiceDependency,
) -> TicketResponse:
    try:
        ticket = service.update_ticket(
            ticket_id,
            title=ticket_data.title,
            priority=(
                TicketPriority(ticket_data.priority)
                if ticket_data.priority is not None
                else None
            ),
            status=(
                TicketStatus(ticket_data.status)
                if ticket_data.status is not None
                else None
            ),
        )
    except TicketNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return _to_ticket_response(ticket)


@router.delete(
    "/tickets/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_ticket(
    ticket_id: int,
    service: TicketServiceDependency,
) -> Response:
    try:
        service.delete_ticket(ticket_id)
    except TicketNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


def create_app(
    *,
    lifespan_handler: Lifespan[FastAPI] | None = database_lifespan,
) -> FastAPI:
    application = FastAPI(title="Month 02 Ticket API", lifespan=lifespan_handler)
    application.include_router(router)
    return application


app = create_app()
