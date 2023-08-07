from services import opensearch_service
from services import bedrock_service


def get_vector_store_retrieval(index_name: str, k: int):
    embeddings = bedrock_service.get_bedrock_embeddings()
    osv_client = opensearch_service.get_opensearch_vector_client(index_name=index_name, embeddings=embeddings)
    return osv_client.as_retriever(
        search_type="similarity", search_kwargs={"k": k}
    )


def retrieve_indices(name: str):
    indices = opensearch_service.get_index_list(index_name=name)
    return [index for index in indices]


def retrieve_relative_documents(index_name: str, query: str, number: int):
    embeddings = bedrock_service.get_bedrock_embeddings()
    return opensearch_service.get_most_similar_docs_by_query(index_name=index_name, embeddings=embeddings,
                                                             query=query,
                                                             k=number)
