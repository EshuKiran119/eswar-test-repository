FROM mcr.microsoft.com/playwright/python:v1.51.0-noble
WORKDIR /sample
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "pytest", "-q", "--browser", "chromium"]
