FROM python:3.11.2
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
# Install ffmpeg using apt
RUN apt update && apt install -y ffmpeg
CMD ["python", "bot.py"]
