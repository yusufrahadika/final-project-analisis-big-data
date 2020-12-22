FROM jupyter/pyspark-notebook

COPY . /app

WORKDIR /app
CMD jupyter lab --ip='*' --NotebookApp.token='' --NotebookApp.password=''
