FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Create a folder for the application
RUN mkdir -p /app/src

# Copy the rest of the application files into the working directory
COPY . /app/src

# Set the working directory to the application folder
WORKDIR /app/src

# Expose the port your FastAPI app is running on
EXPOSE 8000

# Start the FastAPI and Telegram bot applications
CMD uvicorn main:app --host 0.0.0.0 --port 8000 & python telegram_bot.py