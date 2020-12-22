FROM jupyter/pyspark-notebook

COPY . /app

RUN pip install -q findspark

WORKDIR /app
CMD jupyter lab --ip='*' --NotebookApp.token='' --NotebookApp.password=''
