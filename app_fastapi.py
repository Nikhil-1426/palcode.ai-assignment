from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import io
from PIL import Image

app = FastAPI()

model = YOLO('best.pt')

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    results = model(image, conf=0.25)

    detections = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            label = model.names[int(box.cls[0])]
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            bbox = [x1, y1, x2 - x1, y2 - y1]
            detections.append({
                "label": label,
                "confidence": round(confidence, 2),
                "bbox": [round(coord, 1) for coord in bbox]
            })

    return JSONResponse(content={"detections": detections})
