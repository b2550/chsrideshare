FROM python:2-onbuild
RUN python ./db_create.py'
RUN python ./db_migrate.py
CMD [ "python", "./run.py" ]