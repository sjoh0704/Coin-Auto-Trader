FROM python:3.7-slim 
WORKDIR /app 
COPY . /app  
RUN pip install -r requirements.txt 
CMD ["python3", "autotrade.py"]