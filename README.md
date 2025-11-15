# AI-Powered Kitchen Supply Replacement Engine  
[![CI - PR to Main](https://github.com/JY1Z/Junction-Hacakathon-Project-Backend/actions/workflows/ci-main.yml/badge.svg)](https://github.com/JY1Z/Junction-Hacakathon-Project-Backend/actions/workflows/ci-main.yml)
[![CD - Deploy to Render](https://github.com/JY1Z/Junction-Hacakathon-Project-Backend/actions/workflows/cd-main.yml/badge.svg)](https://github.com/JY1Z/Junction-Hacakathon-Project-Backend/actions/workflows/cd-main.yml)

A backend service that analyzes restaurant delivery orders, detects unavailable items, and uses an LLM (Gemini) to recommend replacements.

# Install dependencies
## Runtime
```
pip install -r requirements.txt
```
## Development (optional)
```
pip install -r requirements-dev.txt
```
# Start the App
```
uvicorn app.main:app --reload
```
API is available at:
```
http://127.0.0.1:8000
```

# API Documentation
Swagger UI: https://junction2025.onrender.com/docs

