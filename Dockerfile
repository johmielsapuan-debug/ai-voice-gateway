FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py ./
# Include the public folder at build time if it exists in the repo
COPY public ./public
ENV PORT=10000
EXPOSE 10000
CMD ["python", "server.py"]
