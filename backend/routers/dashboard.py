from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from config.database import SessionLocal
from model import ticket, user
from model.user import User
from app.auth import get_db, get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Dashboard route
@router.get("/", response_class=HTMLResponse)
def dashboard(
    request: Request,
    show_all: bool = False,
    group_id: int = None,
    status_id: int = None,
    date_opened: str = None,
    assigned_user_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    # Retrieve tickets based on the show_all parameter
    if show_all:
        tickets = db.query(ticket).all()
    else:
        tickets = db.query(ticket).filter(ticket.creator == current_user.id).all()

    # Apply filters if provided
    filtered_tickets = apply_filters(
        tickets,
        group_id=group_id,
        status_id=status_id,
        date_opened=date_opened,
        assigned_user_id=assigned_user_id
    )

    # Render the dashboard template with the tickets
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "tickets": tickets,
            "filtered_tickets": filtered_tickets,
            "current_user": current_user,
            "show_all": show_all,
            "group_id": group_id,
            "status_id": status_id,
            "date_opened": date_opened,
            "assigned_user_id": assigned_user_id
        }
    )

def apply_filters(tickets, group_id=None, status_id=None, date_opened=None, assigned_user_id=None):
    filtered_tickets = tickets

    # Apply filters if provided
    if group_id is not None:
        filtered_tickets = filtered_tickets.filter(ticket.group_id == group_id)
    if status_id is not None:
        filtered_tickets = filtered_tickets.filter(ticket.status_id == status_id)
    if date_opened is not None:
        filtered_tickets = filtered_tickets.filter(ticket.date_opened == date_opened)
    if assigned_user_id is not None:
        filtered_tickets = filtered_tickets.filter(ticket.assigned_user_id == assigned_user_id)

    return filtered_tickets
