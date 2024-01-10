import unittest
from services.bedrock_service import *


class MyTestCase(unittest.TestCase):

    def test_get_bedrock_model_info(self):
        bedrock_client = get_bedrock_client()
        model_info = bedrock_client.list_foundation_models()
        print('models: ', model_info)

    def test_get_bedrock_llm_response(self):
        model_id = "anthropic.claude-v2:1"
        llm = get_bedrock_model(model_id=model_id)
        prompt_data = f"""

Human: 너 이름이 뭐야

Assistant:"""
        response = llm(prompt_data)
        print(response)

    def test_get_bedrock_embeddings(self):
        get_bedrock_embeddings()


if __name__ == '__main__':
    unittest.main()
