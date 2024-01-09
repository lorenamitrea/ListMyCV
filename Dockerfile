FROM python:3.12.1-slim-bookworm
WORKDIR /code
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
WORKDIR /code/scrappy
EXPOSE 8000
CMD ["/code/run.sh"]