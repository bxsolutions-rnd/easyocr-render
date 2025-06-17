from fastapi import FastAPI, File, UploadFile
import easyocr
import cv2
import numpy as np
import re
from fastapi.responses import JSONResponse

app = FastAPI()
reader = easyocr.Reader(['en'], gpu=False)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # OCR
    results = reader.readtext(gray, detail=0)
    result_string = " ".join(results)

    # Regex
    total_match = re.search(r'Subtotal\s+[:\-]?\s*\$?((\d{1,3}(,\d{3})*|\d+)(\.\d{1,2})?)', result_string, re.IGNORECASE)
    cash_match = re.search(r'Order No\.\s*[:\-]*\s*([A-Za-z0-9\-_.]+)', result_string, re.IGNORECASE)

    total_amount = total_match.group(1) if total_match else "Not Found"
    cash_paid = cash_match.group(1) if cash_match else "Not Found"

    return JSONResponse({
        "extracted_text": result_string,
        "total_amount": total_amount,
        "order_number": cash_paid
    })
