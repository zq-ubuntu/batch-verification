# 1. Start with a lightweight version of Python
FROM python:3.10-slim

# 2. Install underlying system dependencies needed by OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy the requirements file into the container
COPY requirements.txt .

# 5. Install the Python packages
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy your FastAPI script into the container
COPY main.py .

# 7. Expose the port the API will run on
EXPOSE 8000

# 8. The command to start the API when the container boots
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
