from models.prediction_models import logistic_model, model, tokenizer, model_en, tokenizer_en
from utils.url_utils import extract_features
import tensorflow as tf
import torch
import openai
import json
from langdetect import detect
from config import settings
import pandas as pd

openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = settings.openrouter_api_key

def predict_url(url):
    if isinstance(url, list):
        results = []
        for u in url:
            features = extract_features(u)
            features_df = pd.DataFrame([features], columns=[
                'use_of_ip_address', 'abnormal_url', 'google_index', 'count-www', 'count@',
                'count_dir', 'count_embed_domian', 'short_url', 'count-https',
                'count-http', 'count%', 'count?', 'count-', 'count=', 'url_length',
                'hostname_length', 'sus_url', 'fd_length', 'tld_length', 'count-digits',
                'count-letters'
            ])
            prediction = logistic_model.predict(features_df)
            results.append("Malicious" if prediction[0] == 1 else "Not Malicious")
        return results
    else:
        features = extract_features(url)
        features_df = pd.DataFrame([features], columns=[
            'use_of_ip_address', 'abnormal_url', 'google_index', 'count-www', 'count@',
            'count_dir', 'count_embed_domian', 'short_url', 'count-https',
            'count-http', 'count%', 'count?', 'count-', 'count=', 'url_length',
            'hostname_length', 'sus_url', 'fd_length', 'tld_length', 'count-digits',
            'count-letters'
        ])
        prediction = logistic_model.predict(features_df)
        return "Malicious" if prediction[0] == 1 else "Not Malicious"

def predict_text(text):
    # print("hello from predict_text")
    urls, text_without_links = extract_url(text)
    # print("text_without_links", text_without_links)
    
    lang = detect(text_without_links)
        
    if lang == "ar":
            # print("hello from arabic")
            inputs = tokenizer(text_without_links, return_tensors="tf", padding=True, truncation=True, max_length=128)
            outputs = model(inputs['input_ids'])
            prediction = tf.argmax(outputs.logits, axis=1).numpy()[0]
            # print("prediction",prediction)
            if prediction == 1:
                return {"result": "Malicious"}
            else:
                return {"result": "Not Malicious"}

    elif lang == "en":
            # print("hello from english")
            inputs = tokenizer_en(text_without_links, return_tensors="pt", padding=True, truncation=True, max_length=512)
            with torch.no_grad():
                outputs = model_en(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=1)
                prediction = torch.argmax(probabilities, dim=1).item()
                # print("prediction",prediction)
                if prediction == 1:
                     return "Malicious"
                
                else: return "Not Malicious"
    else:
            return "This language is not supported."

def extract_url(text):
    prompt = f"""
    النص: {text}

    المطلوب:
    1. استخرج جميع الروابط في النص وأعدها كمصفوفة.
    2. أعد النص الأصلي بعد إزالة جميع الروابط.
    3. إذا لم توجد روابط، أعد None للروابط والنص الأصلي كما هو.

    الخرج يجب أن يكون بتنسيق JSON مثل:
    {{
        "links": ["رابط1", "رابط2"],
        "text_without_links": "النص بعد إزالة الروابط"
    }}
    """

    try:
        response = openai.ChatCompletion.create(
            model="meta-llama/llama-4-scout",
            messages=[
                {'role': 'system', 'content': 'أنت مستخرج روابط من النصوص. أعد الإجابة بتنسيق JSON فقط.'},
                {'role': 'user', 'content': prompt}
            ],
        )
        response_content = response.choices[0].message.content.strip()
        
        start_idx = response_content.find('{')
        end_idx = response_content.rfind('}') + 1
        json_str = response_content[start_idx:end_idx]
        
        response_json = json.loads(json_str)
        links = response_json.get("links", None)
        text_without_links = response_json.get("text_without_links", text)
        
        return links, text_without_links
    except Exception as e:
        print(f"Error extracting URLs: {str(e)}")
        return None, text