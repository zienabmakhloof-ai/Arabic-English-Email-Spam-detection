# Mail Pawns

AI-powered spam, phishing, and malicious link detection system with Arabic and English language support.

---

## Overview

Mail Pawns is an intelligent email and message analysis platform designed to detect:

- Spam messages
- Phishing attempts
- Malicious URLs
- Suspicious email content

The system combines Natural Language Processing (NLP) models with URL analysis techniques to provide a complete security analysis workflow.

It supports both Arabic and English content and exposes prediction services through a REST API built with FastAPI.

---

# Features

- Arabic and English message analysis
- Spam and phishing detection
- Malicious URL detection
- Automatic language detection
- REST API using FastAPI
- HTML frontend templates included
- Stores suspicious emails for review
- AI-powered text classification
- URL extraction and analysis
- Excel-based data storage

---

# Project Architecture

```text
Mail-Pawns/
│
├── app/
│   ├── data/               # Excel files and datasets
│   ├── models/             # AI model loading and management
│   ├── routes/             # API routes/endpoints
│   ├── services/           # Prediction and business logic
│   ├── templates/          # HTML frontend pages
│   │   ├── static/             # CSS / JS / assets
│   ├── utils/              # URL Utils
│   └── main.py             # FastAPI application entry 
│   └── config.py           # System Configration 
│
├── requirements.txt
├── colab_run.ipynb
├── EmailSpam_ar.ipynb      # Training model for arabic email
├── EmailSpam_en.ipynb      # Training model for english email
├── url_detection.ipynb     # Training model for url detection
├── README.md
└── .env

```

---

# Technologies Used

## Backend

- Python
- FastAPI
- Uvicorn

## Machine Learning & NLP

- TensorFlow
- PyTorch
- Hugging Face Transformers
- AraBERT
- Logistic Regression

## Frontend

- HTML
- CSS
- JavaScript

## Storage

- Excel files (.xlsx)

---

# AI Models

## 1. Text Classification Models

The project uses different NLP models depending on the detected language:

### Arabic Detection

- AraBERT-based classifier
- Detects phishing and spam content in Arabic text

### English Detection

- Spam detection model for English emails/messages

---

## 2. URL Classification Model

The system analyzes extracted URLs using machine learning techniques to determine whether a link is:

- Safe
- Suspicious
- Malicious

The URL detector is based on Logistic Regression and URL feature extraction.

---

# Workflow

The `/predict` endpoint follows this pipeline:

1. Receive email/message content
2. Detect message language
3. Extract URLs from text
4. Analyze message content using NLP models
5. Analyze extracted URLs
6. Combine prediction results
7. Return final classification

Possible results:

- Malicious
- Not Malicious

---

# API Endpoints

## Predict Endpoint

```http
POST /predict
```

### Request Example

```json
{
  "text": "Your account has been suspended. Click here to verify your identity."
}
```

### Response Example

```json
{
  "text_prediction": "Spam",
  "url_prediction": "Malicious",
  "final_prediction": "Malicious"
}
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/zienabmakhloof-ai/Arabic-English-Email-Spam-detection.git
```

---

## 2. Running the Project

```bash
open colab and uplaod colab_run.ipynb

run the cells then open the generate links (ngrok)
```


---


# Frontend Pages

The project includes ready-to-use frontend templates for:

- Homepage
- About Us page
- Email analysis interface
- Junk emails page
- Prediction results

---

# Data Storage

Suspicious emails and analyzed links are stored in Excel files:

- `emails.xlsx`
- `links.xlsx`

Stored information includes:

- Original message
- Text prediction
- URL prediction
- Final classification
- Extracted URLs

---

# Results
[Results/image1.png]
[Results/image2.png]


# Security Notes

Before deploying the project publicly:

- Remove hardcoded API keys and tokens
- Move secrets to environment variables
- Use a secure database instead of Excel files
- Add authentication and authorization
- Enable request validation and rate limiting

---

# Future Improvements

- Database integration (PostgreSQL / MongoDB)
- User authentication system
- Admin dashboard
- Real-time email scanning
- Browser extension support
- Docker deployment
- CI/CD integration
- Improved phishing detection accuracy

---

# Example Use Cases

- Email spam filtering
- Phishing detection systems
- Secure messaging platforms
- Cybersecurity research projects
- AI-based email security solutions

---

# Contributors

Developed by Zienab Makhloof.

---

# Contact

For questions, suggestions, or collaboration opportunities:

- GitHub: https://github.com/zienabmakhloof-ai
- Email: zienabmakhloof0@gmail.com
