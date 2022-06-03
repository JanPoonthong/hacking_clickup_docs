FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3 cron python3-pip

COPY hello-cron /etc/cron.d/hello-cron

COPY . /root

WORKDIR /root
RUN pip3 install -r requirements.txt

WORKDIR ./
RUN chmod 0744 /etc/cron.d/hello-cron
RUN crontab /etc/cron.d/hello-cron
RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
