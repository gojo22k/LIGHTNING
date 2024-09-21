FROM python:3.11.2
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
# Install ffmpeg using apt
RUN apt-get update -qq && apt-get -y install ffmpeg
CMD ["python", "bot.py"]
