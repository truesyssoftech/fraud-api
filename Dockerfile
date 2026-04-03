# ---------- BASE IMAGE ----------
FROM python:3.10-slim

# ---------- ENV ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- WORKDIR ----------
WORKDIR /app

# ---------- SYSTEM DEPENDENCIES ----------
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---------- COPY REQUIREMENTS ----------
COPY requirements.txt .

# ---------- INSTALL DEPENDENCIES ----------
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---------- COPY PROJECT ----------
COPY . .

# ---------- CREATE MODEL DIRECTORY ----------
RUN mkdir -p model

# ---------- TRAIN MODEL INSIDE CONTAINER ----------
RUN python train_model.py

# ---------- VERIFY MODEL (DEBUG) ----------
RUN echo "=== MODEL FILES ===" && ls -lh model/

# ---------- EXPOSE PORT ----------
EXPOSE 8080

# ---------- START APP ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]