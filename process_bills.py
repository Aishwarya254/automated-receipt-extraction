import shutil
import os
import re
import csv
from collections import defaultdict
from google.cloud import vision

RAW_FOLDER = "raw_images"
PROCESSED_FOLDER = "processed_images"
OUTPUT_FILE = "bills_output_clean_final1.csv"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
client = vision.ImageAnnotatorClient()


# ===============================
# OCR
# ===============================
def extract_text(path):
    with open(path, "rb") as img:
        content = img.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.text_annotations:
        return response.text_annotations[0].description

    return ""


# ===============================
# DATE EXTRACTION
# ===============================
from datetime import datetime

def extract_date(text):
    text = text.replace("|", " ").replace(",", " ")
    text = re.sub(r"\s+", " ", text)

    patterns = [
        r"\b\d{1,2}/\d{1,2}/\d{4}\b",      # 02/22/2026
        r"\b\d{1,2}/\d{1,2}/\d{2}\b",      # 02/22/26
        r"\b\d{4}-\d{2}-\d{2}\b",          # 2026-02-22
        r"\b\d{1,2}-\d{1,2}-\d{4}\b",      # 02-22-2026
        r"\b\d{1,2}-\d{1,2}-\d{2}\b",      # 02-22-26
        r"\b(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|SEPT|OCT|NOV|DEC)[A-Z]*\s+\d{1,2}\s+\d{4}\b",
        r"\b\d{1,2}\s+(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|SEPT|OCT|NOV|DEC)[A-Z]*\s+\d{4}\b",
        r"\b(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|SEPT|OCT|NOV|DEC)[A-Z]*/\d{1,2}/\d{4}\b",
    ]

    found = []

    for pattern in patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            found.append(m.group())

    # try parsing into standard YYYY-MM-DD
    for raw in found:
        raw_clean = raw.strip()

        for fmt in [
            "%m/%d/%Y",
            "%m/%d/%y",
            "%Y-%m-%d",
            "%m-%d-%Y",
            "%m-%d-%y",
            "%b %d %Y",
            "%B %d %Y",
            "%d %b %Y",
            "%d %B %Y",
            "%b/%d/%Y",
            "%B/%d/%Y",
        ]:
            try:
                dt = datetime.strptime(raw_clean.title(), fmt)
                return dt.strftime("%Y-%m-%d")
            except:
                pass

    return ""

# ===============================
# CARD DETECTION
# ===============================
def extract_card_last4(text):

    lines = [l.strip().upper() for l in text.split("\n") if l.strip()]

    card_keywords = [
        "VISA",
        "MASTERCARD",
        "CARD",
        "DEBIT",
        "CREDIT",
        "REFERENCE#"
    ]

    for line in lines:

        # Look for card keywords
        if any(k in line for k in card_keywords):

            # Extract last 4 digits
            match = re.search(r"\d{4}", line)

            if match:
                return match.group()

        # Handle masked numbers like XXXXX7144
        match = re.search(r"[X\*]{4,}\d{4}", line)
        if match:
            return match.group()[-4:]

    return "cash"
# ===============================
# STORE DETECTION
# ===============================
def detect_store(lines):

    for line in lines[:10]:

        clean = line.strip()

        # skip lines that look like dates
        if re.search(r"\d{1,2}/\d{1,2}/\d{2,4}", clean):
            continue

        # skip lines that look like money
        if re.search(r"\d+\.\d{2}", clean):
            continue

        if len(clean) > 3:
            return clean

    return "UNKNOWN"


# ===============================
# TOTAL EXTRACTION (ROBUST)
# ===============================
def extract_total_from_text(text):

    lines = [l.strip().upper() for l in text.split("\n") if l.strip()]

    money_pattern = r"\d[\d,]*\.\d{2}"

    amounts = []
    keyword_amounts = []

    for i, line in enumerate(lines):

        # normalize commas
        clean_line = line.replace(",", "")

        matches = re.findall(money_pattern, clean_line)

        for m in matches:
            value = float(m)

            if value > 0 and value < 20000:
                amounts.append(value)

                if any(k in line for k in ["TOTAL", "AMOUNT", "BALANCE", "DUE"]):
                    keyword_amounts.append(value)

    # Prefer amounts near TOTAL
    if keyword_amounts:
        return max(keyword_amounts)

    # Otherwise fallback to largest realistic value
    if amounts:
        return max(amounts)

    return ""


# ===============================
# GROUP FILES
# bill1 stays single
# RD1A, RD1B -> RD1
# ===============================
def group_files(files):

    groups = defaultdict(list)

    for f in files:

        name, _ = os.path.splitext(f)
        name_upper = name.upper()

        rd_match = re.match(r"(RD\d+)[A-Z]$", name_upper)

        if rd_match:
            base = rd_match.group(1)
        else:
            base = name

        groups[base].append(f)

    return groups


# ===============================
# MAIN
# ===============================
def main():

    files = sorted(
    [f for f in os.listdir(RAW_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))],
    key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0
)

    grouped = group_files(files)

    results = []
    #bill_no = 1

    for base, file_list in grouped.items():

        store = ""
        bill_date = ""
        totals = []

        for file in sorted(file_list):

            path = os.path.join(RAW_FOLDER, file)

            text = extract_text(path)

            card_last4 = extract_card_last4(text)

            lines = text.split("\n")

            if not store:
                store = detect_store(lines)

            if not bill_date:
                bill_date = extract_date(text)

            total = extract_total_from_text(text)

            if total:
                totals.append(total)
            # Move processed image
            destination = os.path.join(PROCESSED_FOLDER, file)
            shutil.move(path, destination)

        if totals:
            final_total = max(totals)
        else:
            final_total = ""

        if not store:
          store = "UNKNOWN"

        bill_number_match = re.search(r"\d+", base)

        if bill_number_match:
          bill_number = int(bill_number_match.group())
        else:
          bill_number = base
        results.append([
          bill_number,
          base,
          store,
          bill_date,
          final_total,
          len(file_list),
          card_last4
        ])

        print(f"[OK] Bill {bill_number}: {store} | {bill_date or '(no date)'} | Total={final_total} | Files={len(file_list)}")

        #bill_no += 1


    results.sort(key=lambda x: int(x[0]) if str(x[0]).isdigit() else 9999)
    with open(OUTPUT_FILE, "w", newline="") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(["Serial_No", "Bill_File", "Store_Name", "Invoice_Date", "Total","Image Count","Card used"])

        writer.writerows(results)


    print(f"\nDone. Wrote {len(results)} rows → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()