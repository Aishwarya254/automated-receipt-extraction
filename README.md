# AI-Powered Receipt Data Pipeline & Expense Analytics System

## Overview

This project automates the extraction of structured expense data from receipt images using OCR and Python. It converts unstructured receipt images into a clean dataset that can be used for financial tracking and analytics.

The system is designed to reduce manual data entry effort and improve operational efficiency for businesses such as restaurants and small enterprises.

---

## Problem Statement

Many businesses manually enter receipt data into spreadsheets, which is time-consuming and error-prone. This project automates that process by extracting key information directly from receipt images.

---

## Solution

The system:

- Extracts text from receipt images using Google Vision OCR
- Processes and structures the data using Python
- Automates execution using Flask API + Docker
- Generates a clean dataset ready for analysis

---

## Features

- OCR-based data extraction
- Automated pipeline execution
- Card vs Cash detection
- Multi-image receipt handling
- Duplicate processing prevention
- Analytics-ready dataset output

---

## Tech Stack

- Python (Pandas, Regex)
- Flask API
- Google Cloud Vision API (OCR)
- Docker (Containerization)
- Excel / Power Query (Analytics)

---

## Project Structure

```
receipt-automation-system/
│
├── process_bills.py
├── run_pipeline.py
├── Dockerfile
├── run.sh / run.bat
├── requirements.txt
│
├── raw_images/
├── processed_images/
│
└── bills_output_clean_final1.csv
```

---

## How to Run (For Users)

### Step 1: Install Docker
Download and install Docker Desktop:  
https://www.docker.com/products/docker-desktop  

---

### Step 2: Download Project
Download this repository as a ZIP and extract it.

---

### Step 3: Set Up Google Vision API (One-Time Setup)

1. Go to: https://console.cloud.google.com  
2. Create a new project  
3. Enable **Vision API**  
4. Go to **IAM & Admin → Service Accounts**  
5. Create a service account  
6. Generate a key → Download JSON file  
7. Rename the file to:

```
vision_key.json
```

8. Place it inside the project folder

---

### Step 4: Add Receipt Images

Place all receipt images inside:

```
raw_images/
```

---

### Step 5: Run the System

#### On Mac:
```
./run.sh
```

#### On Windows:
Double-click:
```
run.bat
```

---

### Step 6: Execute Pipeline

Open in browser:

```
http://localhost:5001/run-pipeline
```

---

### Step 7: Get Output

Processed data will be saved in:

```
bills_output_clean_final1.csv
```

Processed images will be moved to:

```
processed_images/
```

---

## Notes

- No Python setup required — everything runs via Docker  
- Each user must use their own Google Vision API key  
- Initial Google Cloud usage includes free credits  

---

## Business Impact

- Reduces manual data entry effort by ~70–80%  
- Improves accuracy of financial data  
- Enables faster reporting and analytics  
- Scalable for daily business operations  

---

## Future Improvements

- Cloud deployment (AWS / GCP)
- Web-based upload interface
- Real-time processing
- Dashboard for business insights

---

## Author

Aishwarya Arul  
MS Business Analytics  
