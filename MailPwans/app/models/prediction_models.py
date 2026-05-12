from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, AutoModelForSequenceClassification
import tensorflow as tf
import torch
import joblib
from config import settings

# Load models
logistic_model = joblib.load(f"{settings.model_path}logistic_regression_model.pkl")
model = TFAutoModelForSequenceClassification.from_pretrained(f"{settings.model_path}arabert_model")
tokenizer = AutoTokenizer.from_pretrained(f"{settings.model_path}arabert_tokenizer")
tokenizer_en = AutoTokenizer.from_pretrained(f"{settings.model_path}en_spam-detector")
model_en = AutoModelForSequenceClassification.from_pretrained(f"{settings.model_path}en_spam-detector")