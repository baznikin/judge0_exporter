FROM python:3.10

WORKDIR /code
ENV PYTHONPATH '/code/'

ADD code/pip-requirements.txt /code/pip-requirements.txt
RUN pip install -r /code/pip-requirements.txt

ADD code /code

CMD ["python" , "/code/collector.py"]
