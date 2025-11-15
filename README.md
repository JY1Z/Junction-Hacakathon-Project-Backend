# AI-Powered Kitchen Supply Replacement Engine  
[![CI - PR to Main](https://github.com/JY1Z/Junction-Hacakathon-Project-Backend/actions/workflows/ci-main.yml/badge.svg)](https://github.com/JY1Z/Junction-Hacakathon-Project-Backend/actions/workflows/ci-main.yml)
[![CD - Deploy to Render](https://github.com/JY1Z/Junction-Hacakathon-Project-Backend/actions/workflows/cd-main.yml/badge.svg)](https://github.com/JY1Z/Junction-Hacakathon-Project-Backend/actions/workflows/cd-main.yml)
  

**Live API Demo**: https://junction2025.onrender.com/docs
## Overview
This project was built in 48 hours during Junction 2025.    
This backend service analyzes restaurant delivery orders, detects unavailable items, matches them with similar in-stock products from the warehouse, and automatically generates replacement recommendations using Google Gemini.
Customers can then confirm or reject the suggested replacements.
- If the customer confirms, delivery receives the updated replacement list.
- If the customer rejects, the delivery proceeds without the missing items.
   
## Tech Stack
- FastAPI
- Pydantic
- Google Gemini API
- GitHub Actions CI/CD
- Dockerized Deployment
- Render Cloud Hosting
## Install dependencies
### Runtime
```
pip install -r requirements.txt
```
### Development (optional)
```
pip install -r requirements-dev.txt
```
## Run the App
```
uvicorn app.main:app --reload
```
Local API:
```
http://127.0.0.1:8000
```

## API Documentation
Swagger UI: https://junction2025.onrender.com/docs

## API Endpoints
### POST /delivery/order
#### Request
```
{
  "customer_id": 101,
  "items": [
    {
      "id": 1,
      "name": "Whole Milk",
      "quantity": 1,
      "status": "unavailable",
      "price": 3.5
    },
    {
      "id": 2,
      "name": "Some Milk Name",
      "quantity": 1,
      "status": "available",
      "price": 3.0
    },
    {
      "id": 3,
      "name": "Low-Fat Milk",
      "quantity": 1,
      "status": "available",
      "price": 3.0
    }
  ]
}
```
#### Response
```
{
  "order_id": 1,
  "recommendations": [
    {
      "original_product_id": 1,
      "recommended_ids": [
        3,
        4
      ],
      "reason": "Low-Fat Milk (ID 3) is the closest dairy alternative, suitable for most traditional Italian cooking applications, maintaining ingredient consistency and flavor profile. Oat Milk (ID 4) is a popular and versatile plant-based option, essential for catering to diverse customer dietary preferences and modern beverage offerings in a casual restaurant setting.",
      "replacement_message": "Replacing missing Whole Milk with Low-Fat Milk and Oat Milk."
    }
  ]
}
```
### POST /customer/order/{order_id}/decision
#### Request
```
{
  "action": "confirm",
  "decisions": [
    {
      "original_product_id": 1,
      "chosen_product_id": 3
    }
  ]
}
```
#### Response
```
{
  "order_id": 1,
  "action": "confirm",
  "decisions": [
    {
      "original_product_id": 1,
      "chosen_product_id": 3
    }
  ],
  "status": "confirmed",
  "message_to_delivery": "Customer confirmed replacements for order 1."
}
```