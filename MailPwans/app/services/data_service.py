import pandas as pd
import os
import datetime
from pathlib import Path


DATA_DIR = Path("app/data")
DATA_DIR.mkdir(exist_ok=True)

LINKS_FILE = DATA_DIR / "links.xlsx"
EMAILS_FILE = DATA_DIR / "emails.xlsx"

def init_files():
    
    if not EMAILS_FILE.exists():
        pd.DataFrame(columns=["Email", "Text_Result", "URL_Result", "Final_Result", "timestamp", "user_id"]).to_excel(EMAILS_FILE, index=False)
    if not LINKS_FILE.exists():
        pd.DataFrame(columns=["URL", "URL_Result", "Timestamp", "user_id"]).to_excel(LINKS_FILE, index=False)

def save_to_excel(file_name, data, user_id):
    init_files()  # التأكد من وجود الملفات
    
    data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['user_id'] = user_id
    
    try:
        df = pd.read_excel(file_name)
    except FileNotFoundError:
        df = pd.DataFrame()
    
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(file_name, index=False)

def load_emails(user_id):
    try:
        if not EMAILS_FILE.exists():
            return []

        df = pd.read_excel(EMAILS_FILE, engine='openpyxl')
        df = df.fillna('N/A')
        
        if 'user_id' not in df.columns:
            return []

        df = df[df['user_id'] == user_id]
        
        if 'timestamp' in df.columns:
            df = df.sort_values(by='timestamp', ascending=False)
        
        return df.replace([pd.NA, float('nan')], 'N/A').to_dict(orient='records')
    except Exception as e:
        print(f"Error loading emails: {str(e)}")
        return []