# --- Base Stage ---
# Use a specific, lightweight Python version for reproducibility
FROM python:3.10-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# --- Builder Stage ---
# This stage is for installing dependencies
FROM base AS builder

# Install build dependencies if any (e.g., for compiling certain Python packages)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Final Stage ---
# This is the final, lean image
FROM base AS final

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy the application code
COPY . .

# Command to run the application
CMD ["python", "bot.py"]