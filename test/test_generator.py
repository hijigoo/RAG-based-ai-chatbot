import unittest
from generator import *
from helpers.document_helper import get_sample_texts, get_sample_documents
from services.bedrock_service import get_bedrock_embeddings
from services.opensearch_service import *


class MyTestCase(unittest.TestCase):

    def test_generate_answer(self):
        result = generate_answer('what is security?')
        print(result)

    def test_generate_answer_with_retrieval(self):
        # Given
        embeddings = get_bedrock_embeddings()
        texts = get_sample_texts()
        documents = get_sample_documents(texts=texts)
        create_index_from_documents('doc-index-uploader', embeddings=embeddings, documents=documents)

        # When
        result = generate_answer_with_retrieval(
            index_name='doc-index-uploader',
            question='what is operational excellence?',
            k=1)
        print(result[0].get("outputText"))

        # Clean
        delete_index(index_name='doc-index-uploader')

    def test_generate_answer_with_retrieval_by_chain(self):
        # Given
        embeddings = get_bedrock_embeddings()
        texts = get_sample_texts()
        documents = get_sample_documents(texts=texts)
        create_index_from_documents('doc-index-operation', embeddings=embeddings, documents=documents)

        # When
        result = generate_answer_with_retrieval_by_chain(index_name='doc-index-operation',
                                                         question='what is security?',
                                                         k=3)
        print(result)
        print(result['source_documents'][0].page_content)
        print(result['result'])

        # Clean
        delete_index(index_name='doc-index-operation')


if __name__ == '__main__':
    unittest.main()
