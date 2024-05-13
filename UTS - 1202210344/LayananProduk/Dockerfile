# base image
FROM python:3.9-slim

# create working dir
WORKDIR /app

# copy all files
COPY . /app

# install dependencies
RUN pip install -r requirement.txt

EXPOSE 5001

CMD ["python", "app.py"]