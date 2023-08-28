# RAG-based-ai-chatbot
[Amazon Bedrock](https://aws.amazon.com/bedrock/) 으로 RAG(retrieval augmented generation) Chatbot을 제작한 프로젝트입니다. 본 프로젝트를 이용해서 사용자는 LLM 모델을 사용해서 질문에 대한 응답을 생성할 수 있습니다. 또한 참고할 문서를 업로드 하고, 응답 생성시 참고하여 문서의 도메인 특화된 응답을 얻을 수 있습니다.  

## Cloud Architecture
<img width="787" alt="cloud-architecture-02" src="https://github.com/hijigoo/RAG-based-ai-chatbot/assets/1788481/f33fa6c6-48e7-409a-b745-ce6364e33bd6">

Amazon Bedrock을 이용해서 응답을 생성하고, [Amazon OpenSearch](https://docs.aws.amazon.com/opensearch-service/index.html)를 이용해서 문서와 임베딩 벡터 값을 저장합니다. Frontend 와 Backend가 포함된 본 애플리케이션은 [Amazon ECS](https://aws.amazon.com/ko/ecs/)에 배포되어 운영됩니다.

## Application Architecture
애플리케이션을 구성하고 있는 아키텍처에 대해 살펴보도록 하겠습니다.
## UseCase
<img width="262" alt="usecase-01" src="https://github.com/hijigoo/RAG-based-ai-chatbot/assets/1788481/2fc41ea0-c573-497c-a08e-7bf9a65dd79e">

- Store Document: 응답 생성시 참고할 문서를 업로드합니다.
- Delete Document: 업로드한 문서를 삭제합니다.
- Get Answer: LLM 과 업로드한 문서를 참고하여 응답을 생성합니다.

## Overview Diagram
<img width="427" alt="app-architecture-overview" src="https://github.com/hijigoo/RAG-based-ai-chatbot/assets/1788481/31a89bc6-bbd4-44e0-afb6-34d6a4b63c2e">

- Chatbot Interface: 사용자와 상호작용 할 수 있는 Chatbot 형태의 인터페이스를 제공합니다.
- Generator: Prompt 를 생성해서 LLM 으로 부터 응답 생성을 요청합니다.
- Retriever: Prompt 생성에 팔요한 사용자의 질문과 가장 관련이 있는 문서를 검색합니다.
- Knowledge Source: 문서를 임베딩 벡터와 함께 저장합니다.
- LLM(Large Language Model): 응답을 생성합니다.

## Module Diagram
<img width="726" alt="app-architecture-diagram" src="https://github.com/hijigoo/RAG-based-ai-chatbot/assets/1788481/cbed519c-9380-4887-808f-275635700948">

## Sequence Diagram
### Store Documents 
참고할 문서를 Chunk 단위로 나누고 Embedding Vector 로 변환하여 원본과 함께 저장합니다.

<kbd> 
<img style="border: 1px;" width="947" alt="app-architecture-sequence-01" src="https://github.com/hijigoo/RAG-based-ai-chatbot/assets/1788481/589dfe14-56d1-4efa-b079-c481c2bee165">
</kbd>

### Delete Document
저장된 문서와 Embedding Vector 를 제거합니다.

<kbd> 
<img  style="border: 1px;" width="735" alt="app-architecture-sequence-02" src="https://github.com/hijigoo/RAG-based-ai-chatbot/assets/1788481/6c9ce6d4-6b8b-44d3-9326-6b3315e3491d">
</kbd>


### Get Answer
질문과 연관된 문서를 찾아서 Prompt 를 만들어서 응답을 생성하는데 사용합니다.

<kbd> 
<img  style="border: 1px;" width="994" alt="app-architecture-sequence-03" src="https://github.com/hijigoo/RAG-based-ai-chatbot/assets/1788481/3aad96ec-cd25-474d-8580-3589e2694194">
</kbd>

## References
- https://github.com/kyopark2014/simple-chatbot-using-LLM-based-on-amazon-bedrock
- https://github.com/aws-samples/amazon-bedrock-workshop
- https://aws.amazon.com/ko/blogs/big-data/amazon-opensearch-services-vector-database-capabilities-explained/
