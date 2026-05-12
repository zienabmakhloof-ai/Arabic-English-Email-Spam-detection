from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import uuid
from services.prediction_service import predict_url, predict_text, extract_url
from services.data_service import load_emails, save_to_excel, LINKS_FILE, EMAILS_FILE
import pandas as pd
router = APIRouter()

@router.get("/api/junk_emails")
async def get_junk_emails(request: Request):
    try:
        user_id = request.cookies.get("user_id")
        if not user_id:
            return JSONResponse(content={"emails": []})
        
        emails = load_emails(user_id)
        return JSONResponse(content={"emails": emails})
        
    except Exception as e:
        print(f"Server error in get_junk_emails: {str(e)}")
        return JSONResponse(
            content={"error": "Internal server error"},
            status_code=500
        )


@router.post("/delete_email")
async def delete_email(request: Request):
    try:
        user_id = request.cookies.get("user_id")
        if not user_id:
            return JSONResponse(
                content={"error": "User ID not found"},
                status_code=400
            )

        data = await request.json()
        timestamp = data.get("timestamp")
        
        if not timestamp:
            return JSONResponse(
                content={"error": "Timestamp is required"},
                status_code=400
            )

        if not EMAILS_FILE.exists():
            return JSONResponse(
                content={"error": "Emails file not found"},
                status_code=404
            )

        
        df = pd.read_excel(EMAILS_FILE)
       
        df = df[~((df['timestamp'] == timestamp) & (df['user_id'] == user_id))]
        
        df.to_excel(EMAILS_FILE, index=False)
        
        return JSONResponse(content={"status": "success"})
        
    except Exception as e:
        print(f"Error in delete_email: {str(e)}")
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )

@router.post("/predict")
async def predict(request: Request):
    data = await request.json()
    text = data.get("text", "")
    save_to_junk = data.get("save_to_junk", False)
    
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    user_id = request.cookies.get("user_id")
    if not user_id:
        user_id = str(uuid.uuid4())

    # استخراج الروابط والنص بدون روابط
    urls, text_without_links = extract_url(text)
    # print("from predict")
    # تنبؤ النص
    text_result = predict_text(text_without_links)
    # print("from predict text_result", text_result)
    # تنبؤ الروابط إذا وجدت
    url_results = []
    if urls:
        url_results = predict_url(urls)
        url_final_result = "Malicious" if "Malicious" in url_results else "Not Malicious"
    else:
        url_final_result = "No URLs found"

    # النتيجة النهائية
    final_result = "Malicious" if text_result == "Malicious" or url_final_result == "Malicious" else "Not Malicious"
    print("final_result", final_result)

    # الحفظ إذا طلب
    if save_to_junk:
        save_to_excel(EMAILS_FILE, {
            "Email": text,
            "Text_Result": text_result,
            "URL_Result": url_final_result,
            "Final_Result": final_result
        }, user_id)

        if urls:
            for url, result in zip(urls, url_results if isinstance(url_results, list) else [url_results]):
                save_to_excel(LINKS_FILE, {
                    "URL": url,
                    "URL_Result": result,
                }, user_id)

    response = JSONResponse(content={
        "Text result": text_result.get("result") if isinstance(text_result, dict) else text_result,
        "URL result": url_final_result,
        "Final result": final_result
    })
    
    response.set_cookie(key="user_id", value=user_id, max_age=60*60*24*30)
    return response

@router.post("/set_language")
async def set_language(request: Request):
    data = await request.json()
    lang = data.get("lang", "en")
    response = JSONResponse(content={"status": "success"})
    response.set_cookie(key="lang", value=lang, max_age=60*60*24*30)
    return response