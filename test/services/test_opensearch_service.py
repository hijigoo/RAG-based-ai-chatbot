import unittest
from services.opensearch_service import *
from services.bedrock_service import *
from helpers.document_helper import *


class MyTestCase(unittest.TestCase):

    def test_opensearch_check_if_index_exists(self):
        check_if_index_exists(index_name='doc-index-name')

    def test_create_index_from_documents(self):
        # Given
        texts = get_sample_texts()

        # When
        documents = get_sample_documents(texts=texts)
        embeddings = get_bedrock_embeddings()
        create_index_from_documents('doc-index-name', embeddings=embeddings, documents=documents)

        # Then

        # Clean
        delete_index(index_name='doc-index-name')

    def test_delete_index(self):
        # Given
        create_index(index_name='doc-index-name')

        # When
        delete_index(index_name='doc-index-name')

    def test_get_index_list(self):
        # Given
        create_index(index_name='doc-index-name1')
        create_index(index_name='doc-index-name2')

        # When
        indices = get_index_list(index_name='doc-*')
        for index in indices:
            print(index)

        # Clean
        delete_index(index_name='doc-index-name1')
        delete_index(index_name='doc-index-name2')

    def test_get_most_similar_docs_by_query(self):
        # Given
        embeddings = get_bedrock_embeddings()
        texts = get_sample_texts()
        documents = get_sample_documents(texts=texts)
        create_index_from_documents('doc-index-name', embeddings=embeddings, documents=documents)

        # When
        query = "what is security"
        docs = get_most_similar_docs_by_query('doc-index-name', embeddings=embeddings, query=query, k=1)
        print(docs)

        # Then

        # Clean
        delete_index(index_name='doc-index-name')


if __name__ == '__main__':
    unittest.main()
