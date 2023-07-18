from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def render_home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login():
    # authentication logic
    return RedirectResponse(url="/dashboard")