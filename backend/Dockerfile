FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "rasa run actions --port 5055 & rasa run -m models/core-20250624-001111-red-yard.tar.gz --enable-api --port $PORT --cors '*' --endpoints endpoints.yml"]
