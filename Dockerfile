FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

ENV PYTHONPATH=/app:$PYTHONPATH

# Copy the requirements file into the container
COPY src/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src .

# Command to run the app
CMD ["watchmedo", "auto-restart", "--patterns=*.py", "--recursive", "--", "python", "main.py"]

