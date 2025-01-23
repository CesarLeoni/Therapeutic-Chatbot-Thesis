FROM python:3.9

# Install FFmpeg command-line tool required for Whisper
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory inside the container
WORKDIR /app

# Set the Python path environment variable
ENV PYTHONPATH=/app:$PYTHONPATH

# Copy the requirements file into the container
COPY src/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src .

# Preload the Whisper model by running the command
# This ensures that Whisper is loaded and cached during the build
#RUN python3 -c "import whisper; model = whisper.load_model('base')"

# Command to run the app with watchmedo for live code updates
CMD ["watchmedo", "auto-restart", "--patterns=*.py", "--recursive", "--", "python", "main.py"]
