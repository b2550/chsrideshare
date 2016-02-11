FROM python:3.5.1-alpine

RUN pip install -r requirements.txt

ENV APP_DEBUG=False
ENV APP_TESTING=False
ENV APP_SECRET_KEY=None
ENV APP_GOOGLE_API_KEY=None
ENV APP_RECAPTCHA_PUBLIC_KEY=None
ENV APP_RECAPTCHA_PRIVATE_KEY=None
ENV APP_MAIL_SERVER=None
ENV APP_MAIL_PORT=None
ENV APP_MAIL_USERNAME=None
ENV APP_MAIL_PASSWORD=None

EXPOSE 8001

CMD [ "python", "./run.py" ]

# TODO: Switch some config to environment variables