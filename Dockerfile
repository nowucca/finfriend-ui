# Use the official Python 3.12.5 image as the base
FROM python:3.12.5-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies (Streamlit and any others listed in requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 8502 for the Streamlit app
EXPOSE 8502

# Command to run the Streamlit app on port 8502
CMD ["streamlit", "run", "🏠_FinFriend.py", "--server.port=8502", "--server.headless=true"]
