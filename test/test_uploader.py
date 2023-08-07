import unittest
from uploader import *
from helpers.document_helper import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_upload_pdf_as_vector(self):
        # Given
        file_path = './../app/samples/wellarchitected-operational-excellence-pillar-introduction.pdf'

        # When
        upload_pdf_as_vector(name='doc-index-pdf', file_path=file_path, chunk_size=1000, chunk_overlap=100)

        # Clean
        # delete_vectors(name='doc-index-pdf')

    def test_upload_texts_as_vector(self):
        # Given
        texts = get_sample_texts()

        # When
        upload_texts_as_vector(name='doc-index-uploader', texts=texts, chunk_size=1000, chunk_overlap=100)

        # Clean
        delete_document_index(name='doc-index-uploader')


if __name__ == '__main__':
    unittest.main()
