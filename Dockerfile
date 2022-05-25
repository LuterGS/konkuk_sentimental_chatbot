FROM python:3.8

# set folder
RUN mkdir -p /app
COPY . /app
WORKDIR /app

# install package
RUN pip install -r requirements.txt

# set fastAPI and run
CMD ["python", "main.py"]