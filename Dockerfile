FROM python:3.11
WORKDIR /veritybot

# Install system dependencies for tkinter
USER root
RUN apt-get update && \
    apt-get install -y python3-tk libffi-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy config.ini to container
COPY config.ini ./

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 8080

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["python", "src/main.py", "--verbose"]
