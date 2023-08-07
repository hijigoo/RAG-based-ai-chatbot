import json
import retriever
from services import bedrock_service, opensearch_service
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def _get_prompt_template():
    prompt_template = """Human: Use the following pieces of context to provide a concise answer to the question at 
    the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {question}
        Assistant:"""
    # prompt_template = """Answer based on context:\n\n{context}\n\n{question}"""
    return PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )


def generate_answer(question: str):
    return bedrock_service.get_predict_from_bedrock_model(model_id='amazon.titan-tg1-large',
                                                          question=question)


def generate_answer_with_retrieval(index_name: str, question: str, k: int):
    docs = retriever.retrieve_relative_documents(index_name=index_name, query=question, number=k)
    context = " ".join([doc.page_content for doc in docs])
    prompt_data = f"""Human: Use the following pieces of context to provide a concise answer to the question at the 
    end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    {context}

    Question: {question}
    Assistant:"""

    parameters = {
        "maxTokenCount": 512,
        "stopSequences": [],
        "temperature": 0,
        "topP": 0.9
    }
    response = bedrock_service.get_predict_from_bedrock_client(model_id="amazon.titan-tg1-large",
                                                               prompt=prompt_data,
                                                               parameters=parameters)

    response_body = json.loads(response.get("body").read())
    return response_body.get("results")


def generate_answer_with_retrieval_by_chain(index_name: str, question: str, k: int):
    llm = bedrock_service.get_bedrock_model('amazon.titan-tg1-large')
    prompt = _get_prompt_template()
    vector_store_retrieval = retriever.get_vector_store_retrieval(index_name=index_name, k=k)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        # retriever=vector_store_retriever,
        retriever=vector_store_retrieval,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    result = qa({"query": question})
    return result
