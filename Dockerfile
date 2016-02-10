FROM python:2-onbuild
RUN ./db_create.py
RUN ./db_migrate.py
CMD [ "python", "./run.py" ]