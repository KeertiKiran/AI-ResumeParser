FROM python:3.12
LABEL authors="Advik"
LABEL description="This is a custom image for the ResumeParser API"

# Set the working directory in the container
WORKDIR /app

# Copy files to the working directory
COPY . .

# Install any dependencies
RUN pip install -r requirements.txt

EXPOSE 2000

CMD [ "gunicorn", "app:app"]
