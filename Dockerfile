FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN apk add gcc libffi-dev musl-dev openssl-dev make
RUN pip install flask slackclient requests azure
EXPOSE 9090
CMD [ "python", "./azure_slackbot_blob.py" ]
