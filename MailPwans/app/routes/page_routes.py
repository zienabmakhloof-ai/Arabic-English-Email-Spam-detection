from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
templates.env.globals['get_language'] = lambda req: req.cookies.get("lang", "en")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    lang = request.cookies.get("lang", "en")
    return templates.TemplateResponse("home_ar.html" if lang == "ar" else "home.html", {"request": request})

@router.get("/check", response_class=HTMLResponse)
async def check(request: Request):
    lang = request.cookies.get("lang", "en")
    return templates.TemplateResponse("check_ar.html" if lang == "ar" else "check.html", {"request": request})

@router.get("/junk", response_class=HTMLResponse)
async def junk_page(request: Request):
    lang = request.cookies.get("lang", "en")
    return templates.TemplateResponse("junk_ar.html" if lang == "ar" else "junk.html", {"request": request})
    
@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    lang = request.cookies.get("lang", "en")
    return templates.TemplateResponse("AboutUs_ar.html" if lang =="ar" else "AboutUs.html", {"request": request})
    
@router.get("/help", response_class=HTMLResponse)
async def help_page(request: Request):
    lang = request.cookies.get("lang", "en")
    return templates.TemplateResponse("Help_ar.html" if lang == "ar" else "Help.html", {"request": request})