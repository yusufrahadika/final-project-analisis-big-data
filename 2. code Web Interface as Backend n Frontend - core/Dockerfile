# from python:3.7-slim-stretch
from python:3.8-slim

WORKDIR /root
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && apt-get install apt-transport-https ca-certificates wget dirmngr gnupg software-properties-common -y
RUN wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add -
RUN add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/
RUN apt-get update && apt-get install adoptopenjdk-8-hotspot -y
RUN wget https://downloads.apache.org/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz && tar xzf hadoop-3.3.0.tar.gz

# Hadoop Related Options
ENV JAVA_HOME=/usr/lib/jvm/adoptopenjdk-8-hotspot-amd64/
ENV HADOOP_HOME=/root/hadoop-3.3.0
ENV HADOOP_INSTALL=$HADOOP_HOME
ENV HADOOP_MAPRED_HOME=$HADOOP_HOME
ENV HADOOP_COMMON_HOME=$HADOOP_HOME
ENV HADOOP_HDFS_HOME=$HADOOP_HOME
ENV YARN_HOME=$HADOOP_HOME
ENV HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
ENV PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
ENV HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"

COPY . /app
WORKDIR /app/bigdatadigitalent

RUN pip install -q Django django-livereload-server sqlparse
CMD python manage.py livereload
CMD python manage.py runserver 0.0.0.0:8000
EXPOSE 8000
