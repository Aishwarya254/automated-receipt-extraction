# AI-Powered Receipt OCR & Expense Analytics Pipeline
Built as part of a Data Analyst technical project demonstrating automation, data processing, and analytics.
## Overview

This project automates the extraction of structured expense data from receipt images using OCR and Python automation. It transforms unstructured receipt images into a clean dataset that can be used for business analytics and financial tracking.

---

## Business Problem

Restaurants and small businesses receive daily receipts for inventory and operational expenses. These are often stored as images, making manual tracking inefficient, time-consuming, and error-prone.

---

## Solution

This pipeline automates the entire workflow:

- Extracts text from receipt images using OCR
- Identifies key fields like store name, invoice date, total amount, and payment method
- Cleans and structures the data
- Generates a dataset ready for analytics

---
## Why This Matters

This system reduces manual effort in expense tracking and enables businesses to make data-driven decisions based on structured financial data.

---

## Architecture

```
Receipt Images
      ↓
Scheduled Automation (n8n)
      ↓
Flask API Trigger
      ↓
Python OCR Processing
      ↓
Data Cleaning & Transformation
      ↓
Structured Expense Dataset
      ↓
Analytics Dashboard
```

---

## Key Features

- Automated OCR extraction from images
- Python-based ETL pipeline
- Scheduled workflow using n8n
- Card vs Cash detection
- Automatic file handling (processed vs raw)
- Clean dataset generation for analysis

---

## Tech Stack

- Python (Pandas, Regex)
- Flask API
- Google Vision OCR
- n8n (Workflow Automation)
- Excel / Tableau (for analytics)

---

## Sample Output

The pipeline generates a structured dataset:

| Store Name | Date | Total | Card Used |
|-----------|------|------|----------|
| SUBZI MANDI | 2026-03-06 | 126.0 | Cash |


```
sample_output/bills_output_clean_final.csv
```

---

## Business Insights (Potential)

- Daily expense tracking
- Vendor-wise spend analysis
- Cash vs Card usage trends
- High expense categories
- Monthly spend patterns

---

## Future Improvements

- Cloud deployment (AWS/GCP)
- WhatsApp API integration
- Real-time processing
- Dashboard UI for business users
- Database storage (PostgreSQL)

---

## Author

Aishwarya Arul  
MS Business Analytics | Data Analyst | AI + Automation Enthusiast