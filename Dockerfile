FROM python:3
WORKDIR /usr/src/app
COPY . .


RUN  apt-get update && apt-get upgrade  -y 
RUN echo "*** *** *** *** *** *** *** *** *** ** ** ** ** * * ***************************************"
RUN python -m pip install beautifulsoup4
RUN python -m pip install lxml
RUN python -m pip install forex_python 
RUN python -m pip install discord.py
RUN python -m pip install requests
RUN python -m pip install tweepy
RUN python -m pip install datetime
RUN python -m pip install redis

CMD [ "python", "./bot.py" ]
