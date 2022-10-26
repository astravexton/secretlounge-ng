FROM python:alpine

WORKDIR /usr/src/app

COPY . ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt config.yaml.example Dockerfile README.md

CMD ["./secretlounge-ng"]
