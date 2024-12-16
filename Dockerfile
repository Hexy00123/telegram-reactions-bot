FROM python:3.12-slim

# Set the working directory
WORKDIR /bot

# Copy the current directory contents into the container at /bot
COPY ./requirements.txt /bot/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /bot
COPY ./src /bot/src

# Run app.py when the container launches
CMD ["python", "-m", "src"]