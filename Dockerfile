FROM python:2-onbuild
RUN python ./db_create.py
RUN python ./db_migrate.py

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
ENV APP_BADCONFIG=True

CMD [ "python", "./run.py" ]

# TODO: Switch some config to environment variables