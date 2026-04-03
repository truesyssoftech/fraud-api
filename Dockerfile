# ---------- BASE IMAGE ----------
FROM python:3.10-slim

# ---------- ENV SETTINGS ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- WORKDIR ----------
WORKDIR /app

# ---------- INSTALL SYSTEM DEPENDENCIES ----------
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---------- COPY REQUIREMENTS FIRST (for caching) ----------
COPY requirements.txt .

# ---------- INSTALL PYTHON DEPENDENCIES ----------
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---------- COPY PROJECT FILES ----------
COPY app/ app/
COPY model/ model/
COPY train_model.py .
COPY .env .

# ---------- VERIFY MODEL EXISTS (DEBUG SAFETY) ----------
RUN ls -lh model/

# ---------- EXPOSE PORT ----------
EXPOSE 8080

# ---------- START APP ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]