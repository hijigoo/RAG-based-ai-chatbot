import boto3
import json

from langchain.llms.bedrock import Bedrock
from langchain.embeddings import BedrockEmbeddings

bedrock_region = "us-west-2"

def get_bedrock_client():
    return boto3.client(
        service_name='bedrock-runtime',
        region_name=bedrock_region,
        # aws_access_key_id=BEDROCK_ACCESS_KEY, # Task Role 을 이용 해서 접근
        # aws_secret_access_key=BEDROCK_SECRET_ACCESS_KEY # Task Role 을 이용 해서 접근
    )


def get_bedrock_model(model_id):
    bedrock_client = get_bedrock_client()
    return Bedrock(model_id=model_id, client=bedrock_client)


def get_bedrock_embeddings():
    bedrock_client = get_bedrock_client()
    return BedrockEmbeddings(client=bedrock_client)


def get_predict_from_bedrock_model(model_id: str, question: str):
    prompt_data = f"""

Human: 너는 친절하게 정보를 제공하는 인공지능 비서야.
사용자가 질문하면 너가 알고 있는 지식을 더해서 답변을 해줘야 해.
사용자의 질분은 <question> tag 안에 있어.

<question>
{question}
</question>

Assistant:"""
    llm = get_bedrock_model(model_id=model_id)
    return llm.predict(prompt_data)


def get_predict_from_bedrock_client(model_id: str, parameters: dict):
    bedrock_client = get_bedrock_client()
    accept = 'application/json'
    content_type = 'application/json'
    return bedrock_client.invoke_model(
        body=json.dumps(parameters),
        modelId=model_id, accept=accept, contentType=content_type
    )