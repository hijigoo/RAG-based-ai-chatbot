from helpers import document_helper
from services import opensearch_service
from services import bedrock_service


def upload_pdf_as_vector(name: str, file_path: str, chunk_size: int, chunk_overlap: int):
    """PDF 경로 를 받아서 Vector 로 변경 후 Opensearch Vector Store 에 저장.
    name: PDF 이름.
    file_path: PDF 경로. PDF 는 다시 chunk size 로 나눠짐.
    chunk_size: 각 Text 를 나눌 최대 사이즈. Vector 로 변경될 크기.
    chunk_overlap: Chunk Size 로 나눌 때 겹치는 부분의 크기.
    """
    embeddings = bedrock_service.get_bedrock_embeddings()
    print("get embeddings")
    docs = document_helper.get_documents_by_splitting_pdf(file_path=file_path, chunk_size=chunk_size,
                                                          chunk_overlap=chunk_overlap)
    print("get docs")
    return opensearch_service.create_index_from_documents(index_name=name, embeddings=embeddings, documents=docs)


def upload_texts_as_vector(name: str, texts: list[str], chunk_size: int, chunk_overlap: int):
    """Text List 를 받아서 Vector 로 변경 후 Opensearch Vector Store 에 저장.
    name: Text 묶음의 이름.
    texts: Text 묶음. 각 Text 는 다시 chunk size 로 나눠짐.
    chunk_size: 각 Text 를 나눌 최대 사이즈. Vector 로 변경될 크기.
    chunk_overlap: Chunk Size 로 나눌 때 겹치는 부분의 크기.
    """
    embeddings = bedrock_service.get_bedrock_embeddings()
    docs = document_helper.get_documents_by_splitting_texts(texts=texts, chunk_size=chunk_size,
                                                            chunk_overlap=chunk_overlap)
    return opensearch_service.create_index_from_documents(index_name=name, embeddings=embeddings, documents=docs)


def delete_document_index(name: str):
    """Vector 로 변경 된 Opensearch Vector Store 에 저장.
    """
    return opensearch_service.delete_index(index_name=name)
