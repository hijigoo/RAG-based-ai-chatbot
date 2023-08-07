import logging

from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def get_texts_by_splitting_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        # separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)


def get_documents_by_splitting_texts(texts: list[str], chunk_size: int = 1000, chunk_overlap: int = 100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        # separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.create_documents(texts)


def get_documents_by_splitting_document(docs: list[Document], chunk_size: int = 1000, chunk_overlap: int = 100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        # separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(docs)


def get_documents_by_splitting_pdf(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 100):
    documents = PyPDFLoader(file_path=file_path).load()
    print("load documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        # separators=["\n\n", "\n", " ", ""]
    )
    print("text_splitter")

    return text_splitter.split_documents(documents)


def get_documents_by_splitting_pdf_from_dir(dir_path: str, chunk_size: int = 1000, chunk_overlap: int = 100):
    documents = PyPDFDirectoryLoader(path=dir_path).load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        # separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)


def get_sample_texts():
    return [
        'The operational excellence pillar focuses on running and monitoring systems, and continually improving '
        'processes and procedures. Key topics include automating changes, responding to events, and defining '
        'standards to manage daily operations.',

        'The security pillar focuses on protecting information and systems. Key topics include confidentiality and '
        'integrity of data, managing user permissions, and establishing controls to detect security events.',

        'The reliability pillar focuses on workloads performing their intended functions and how to recover quickly '
        'from failure to meet demands. Key topics include distributed system design, recovery planning, and adapting '
        'to changing requirements.',

        'The performance efficiency pillar focuses on structured and streamlined allocation of IT and computing '
        'resources. Key topics include selecting resource types and sizes optimized for workload requirements, '
        'monitoring performance, and maintaining efficiency as business needs evolve.',

        'The cost optimization pillar focuses on avoiding unnecessary costs. Key topics include understanding '
        'spending over time and controlling fund allocation, selecting resources of the right type and quantity, '
        'and scaling to meet business needs without overspending.',

        'The sustainability pillar focuses on minimizing the environmental impacts of running cloud workloads. Key '
        'topics include a shared responsibility model for sustainability, understanding impact, and maximizing '
        'utilization to minimize required resources and reduce downstream impacts.'
    ]


def get_sample_documents(texts: list[str]):
    return [
        Document(
            page_content=t
        ) for t in texts
    ]
