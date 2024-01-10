import unittest
from helpers.document_helper import *
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter


class MyTestCase(unittest.TestCase):

    def test_get_texts_by_splitting_text(self):
        text = """
                AWS has significantly more services, and more features within those services, than any other cloud provider–from infrastructure technologies like compute, storage, and databases–to emerging technologies, such as machine learning and artificial intelligence, data lakes and analytics, and Internet of Things..
                AWS also has the deepest functionality within those services. For example, AWS offers the widest variety of databases that are purpose-built for different types of applications so you can choose the right tool for the job to get the best cost and performance.
               """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=5000,
            chunk_overlap=0,
            separators=["\n\n", "\n", " ", ""]
        )
        result = text_splitter.split_text(text)
        print(len(result))
        print(result)

    def test_get_texts_by_character_text_splitter(self):
        text = """
                AWS has significantly more services, and more features within those services
                than any other cloud provider–from infrastructure technologies like compute,
                storage, and databases–to emerging technologies, such as machine learning
            
                AWS also has the deepest functionality within those services.
                For example, AWS offers the widest variety of databases that 
                are purpose-built for different types of applications
               """

        text_splitter = CharacterTextSplitter(
            chunk_size=0,
            chunk_overlap=0,
            separator="\n\n",
        )
        result = text_splitter.split_text(text)

        print(f"Document count {len(result)}")
        print(*result, sep = "\n")



if __name__ == '__main__':
    unittest.main()
