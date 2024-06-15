FROM python:3.12
LABEL authors="Advik"
LABEL description="This is a custom image for the ResumeParser API"

# Set environment variables
ENV API_KEY="AIzaSyDUhsbslsK7JC23JbmVzAZyRsuyUWoL4EA"

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY src/ .
COPY history .
COPY requirements.txt .
COPY gunicorn.conf.py .

# Install any dependencies
RUN pip install -r requirements.txt

EXPOSE 2000

CMD [ "gunicorn", "app:app"]

