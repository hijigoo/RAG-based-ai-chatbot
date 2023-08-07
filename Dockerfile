FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /code/requirements.txt
COPY ./bedrock-sdk/botocore-1.29.162-py3-none-any.whl /code/bedrock-sdk/botocore-1.29.162-py3-none-any.whl
COPY ./bedrock-sdk/boto3-1.26.162-py3-none-any.whl /code/bedrock-sdk/boto3-1.26.162-py3-none-any.whl

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install /code/bedrock-sdk/botocore-1.29.162-py3-none-any.whl
RUN pip install /code/bedrock-sdk/boto3-1.26.162-py3-none-any.whl
RUN pip install mangum

COPY ./app /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]