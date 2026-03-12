# 🔍 EasyOCR Batch Verification API

> A high-performance REST API built with FastAPI that processes batches of images using EasyOCR to verify if the extracted text matches expected baselines, alerting users to any mismatches.

## 🚀 Features

* **Automated Mismatch Alerts:** Instantly compares text found in sample pictures against your expected strings and flags discrepancies.
* **Batch Processing:** Send multiple images in a single payload for rapid verification.
* **FastAPI Powered:** Extremely fast, automatically documented (Swagger UI), and asynchronous API.
* **Fully Containerized:** Pre-configured Docker setup ensures it runs consistently across any environment without dependency headaches.
* **EasyOCR Integration:** Ready out-of-the-box with multi-language optical character recognition.

---

## 📸 See It In Action

<!-- REPLACE THE SRC LINKS WITH YOUR ACTUAL LOCAL SCREENSHOT PATHS -->

<p align="center">
  <img src="screenshots/img-01.jpg" alt="FastAPI Swagger UI showing the /verify endpoint" width="600"/>
  <br>
  <em>Interactive API documentation generated automatically by FastAPI.</em>
</p>

<p align="center">
  <img src="screenshots/img-02.jpg" alt="JSON Response" width="600"/>
  <br>
  <em>The verification engine catching a mismatch and triggering an alert.</em>
</p>

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** FastAPI
* **Server:** Uvicorn
* **OCR Engine:** EasyOCR
* **Deployment:** Docker

---

## ⚙️ Installation & Setup

You can run this project locally or within a Docker container. **Docker is highly recommended** to avoid messy OCR dependency conflicts (like PyTorch or OpenCV).

### Option 1: Running with Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/easyocr-batch-verifier.git](https://github.com/yourusername/easyocr-batch-verifier.git)
   cd easyocr-batch-verifier
