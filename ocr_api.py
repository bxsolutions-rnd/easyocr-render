from fastapi import FastAPI
import time

print("🚀 App is starting up... (this should appear only once!)")
time.sleep(1)  # Simulate model load delay
print("✅ App startup complete.")

app = FastAPI()

@app.get("/")
def read_root():
    print("📩 Received a request to /")  # This should appear every time
    return {"message": "App is alive!"}
