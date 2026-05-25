# Step 1: Start with a Python environment
FROM python:3.11-slim

# Step 2: Create a folder inside the container for our code
WORKDIR /app

# Step 3: Copy our requirements file and install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Step 4: Copy all our application files into the container
COPY . .

# Step 5: Run the application when the container starts
CMD ["python", "app.py"]

