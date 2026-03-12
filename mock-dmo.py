import requests
import json

# This script pretends to be your existing DMO software on the manufacturing floor

API_URL = "http://localhost:8000/verify-batch"
IMAGE_PATH = "sample-batch.jpg"  # The cropped neck image we made on Day 5
EXPECTED_BATCH = "599698"  # Change this to match your actual test image!

print(f"⚙️ DMO SYSTEM: Bottle detected on line. Expected batch is {EXPECTED_BATCH}.")
print(f"⚙️ DMO SYSTEM: Snapping photo and sending to QA Microservice...\n")

# Open the image and send the POST request
with open(IMAGE_PATH, "rb") as image_file:
    files = {"file": (IMAGE_PATH, image_file, "image/jpeg")}
    data = {"expected_batch": EXPECTED_BATCH}

    # This is the exact code your DMO will use to talk to the microservice
    response = requests.post(API_URL, files=files, data=data)

# Print the JSON response received from the microservice
print("--- DMO RECEIVED RESPONSE FROM MICROSERVICE ---")
formatted_json = json.dumps(response.json(), indent=4)
print(formatted_json)

# Simulate DMO logic based on the response
payload = response.json()
if payload.get("alert_required"):
    print(
        "\n🚨 DMO SYSTEM: MISMATCH DETECTED! STOPPING LINE 3 AND LOGGING NON-CONFORMANCE! 🚨"
    )
else:
    print("\n✅ DMO SYSTEM: Batch verified. Continuing production.")
