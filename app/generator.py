import json
import retriever
from services import bedrock_service, opensearch_service
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def _get_prompt_template():
    prompt_template = """

Human: Use the following pieces of context to provide a concise answer to the question at 
the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}

Assistant:"""
    # prompt_template = """Answer based on context:\n\n{context}\n\n{question}"""
    return PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )


def generate_answer(question: str):
    return bedrock_service.get_predict_from_bedrock_model(model_id="anthropic.claude-v2:1",
                                                          question=question)


def generate_answer_with_retrieval(index_name: str, question: str, k: int):
    docs = retriever.retrieve_relative_documents(index_name=index_name, query=question, number=k)
    context = " ".join([doc.page_content for doc in docs])

    prompt = f"""

Human: 너는 친절하게 정보를 제공하는 인공지능 비서야.
사용자가 질문하면 <content> tag 안에 있는 내용과 너가 알고 있는 지식을 더해서 답변을 해줘야 해.
사용자의 질문은 <question> tag 안에 있어.

<content>
{context}
</content>

<question>
{question}
</question>

<content> tag 안에 질문과 관련된 내용이 없으면 '사용자의 질문에 대한 내용을 문서에서 찾을 수는 없지만 제가 알고 있는 내용은' 이라는 서두와 함께 답변해 줘
<content> tag 안에 질문과 관련된 내용이 있으면 '문서에서 찾은 내용을 참고해서 답변드리겠습니다' 라는 서두와 함께 답변해줘 
"tag 에 따르면" 이라는 서두는 제외하고 답변해줘.
답변은 모두 공손하게 해줘

답변은 250 토큰 이내로 해줘

Assistant:"""

    model_id = "anthropic.claude-v2:1"
    parameters = {
        "prompt": prompt,
        "max_tokens_to_sample": 1024,  # min:0, max:8,000, default:200
        "stop_sequences": ["\n\nHuman:"],
        "temperature": 0.8,  # min:0, max:1, default:0.5
        "top_p": 1,  # min:0, max:1, default:1
        "top_k": 250  # min:0, max:500, default:250
    }
    response = bedrock_service.get_predict_from_bedrock_client(model_id=model_id,
                                                               parameters=parameters)

    response_body = json.loads(response.get("body").read())
    return response_body.get("completion"), docs


def generate_answer_with_retrieval_by_chain(index_name: str, question: str, k: int):
    llm = bedrock_service.get_bedrock_model(model_id="anthropic.claude-v2:1")
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
