from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pyngrok import ngrok
import uvicorn
import nest_asyncio
import os
from routes import api_routes, page_routes 
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

app.include_router(page_routes.router)
app.include_router(api_routes.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Global error handler: {str(exc)}")
    print(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )




def run_in_colab():
    # تهيئة ngrok
    ngrok.set_auth_token("2uiGvxm5sa7oe5XApugiucpCPqH_84zg6Th5sLDhrsGXYF8zA")
    tunnel = ngrok.connect(7000)
    public_url = tunnel.public_url
    print(f"Public URL: {public_url}")
    
    # ضروري لتشغيل asyncio في بيئة notebook
    nest_asyncio.apply()
    
    # تشغيل الخادم
    uvicorn.run(app, host="0.0.0.0", port=7000)

if __name__ == "__main__":
    run_in_colab()