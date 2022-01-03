FROM python:3.7-stretch

RUN apt-get install libjpeg-dev zlib1g-dev -y

RUN pip install --upgrade pip

WORKDIR /app 
COPY . /app  
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install convertdate
RUN pip3 install lunarcalendar
RUN pip3 install holidays
RUN pip3 install tqdm
RUN pip3 install pystan==2.19.1.1
RUN pip3 install fbprophet
RUN pip3 install -r requirements.txt 

CMD ["python3", "autotrade.py"]