from paddleocr import PaddleOCR

image_path = "raw_images/bill5.jpeg"

print("Running PaddleOCR...")

ocr = PaddleOCR(lang="en", use_textline_orientation=True)

result = ocr.ocr(image_path)   # <-- NO cls argument here

print("\n===== OCR OUTPUT =====\n")

for page in result:
    for line in page:
        text = line[1][0]
        confidence = line[1][1]
        print(f"{confidence:.2f} | {text}")