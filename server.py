from fastapi import FastAPI, HTTPException, UploadFile, File
from database import create_collection, delete_and_insert_all_promotions, get_promotion, health_check, delete_all_promotions, bulk_insert_promotion
import csv
import io
import json
import uvicorn

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

app_config = config['app']
app_host = app_config['host']
app_port = app_config['port']

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await create_collection("promotions")

@app.get("/")
async def read_root():
    return {"message": "Hello, Verve Group!"}

@app.get("/health")
async def health():
    return await health_check()

@app.get("/promotions/{promotion_id}")
async def read_promotion(promotion_id: str):
    try:
        promotion = await get_promotion(promotion_id)
        return {
            "id": str(promotion['id']),
            "price": float(promotion['price']),
            "expiration_date": promotion['expiration_date']
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Promotion {promotion_id} not Found")

@app.post("/add-promotions/")
async def add_promotions_file(file: UploadFile = File(...)):
    content = await file.read()
    csv_reader = csv.DictReader(io.StringIO(content.decode("utf-8")), fieldnames=["id", "price", "expiration_date"])
    promotions = []
    for row in csv_reader:
        promotions.append({
            "id": row['id'],
            "price": float(row['price']),
            "expiration_date": row['expiration_date']
        })
    try:
        await delete_and_insert_all_promotions(promotions)
        return {"status": "success", "message": "Promotions added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed in adding promotions, Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host=app_host, port=app_port)
