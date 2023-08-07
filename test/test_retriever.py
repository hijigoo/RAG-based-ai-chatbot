import unittest
from retriever import *
from uploader import *
from helpers.document_helper import *


class MyTestCase(unittest.TestCase):
    def test_retrieve_relative_documents(self):
        # Given
        texts = get_sample_texts()
        upload_texts_as_vector(name='doc-index-uploader', texts=texts, chunk_size=1000, chunk_overlap=0)

        # When
        docs = retrieve_relative_documents(name='doc-index-uploader', query='what is pillar', number=2)

        # Then
        print(docs)

        # Clean
        delete_document_index('doc-index-uploader')


if __name__ == '__main__':
    unittest.main()
