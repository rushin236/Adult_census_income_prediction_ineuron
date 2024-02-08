FROM python:3.9

# Copy application code and set working directory
COPY . /app
WORKDIR /app

# # Install Python dependencies
RUN pip install -r requirements.txt
RUN python main.py

# # Expose port and specify application entry point
EXPOSE 3000
CMD ["python", "app.py"]

