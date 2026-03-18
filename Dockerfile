FROM python:3.11
WORKDIR /veritybot

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 8080

# Copy config.ini
COPY config.ini ./config.ini


# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["python", "src/main.py", "--verbose"]
