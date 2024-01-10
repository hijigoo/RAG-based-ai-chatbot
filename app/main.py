import os

import aiofiles
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import generator
import retriever
import uploader

app = FastAPI()

dir_path = os.path.dirname(os.path.realpath(__file__))
static_dir = os.path.join(dir_path, "ui/static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates = Jinja2Templates(directory="ui")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "id": id})


@app.get("/health")
async def root():
    return {"message": "Healthy"}


@app.get("/documents")
async def get_documents(request: Request):
    return retriever.retrieve_indices("doc-*")


@app.post("/documents/{document}")
async def upload_document(file: UploadFile, document: str, chunk: int, overlap: int):
    print(f"File Name: {file.filename}", flush=True)
    print(f"Document Name: {document}", flush=True)
    print(f"Chunk Size: {chunk}", flush=True)
    print(f"Chunk Overlap Size: {overlap}", flush=True)

    filepath = f"/tmp/{file.filename}"
    async with aiofiles.open(filepath, 'wb+') as out_file:
        content = file.file.read()  # async read
        await out_file.write(content)  # async write

    print(f"file {file.filename} saved at ${filepath}")
    uploader.upload_pdf_as_vector(name=document,
                                  file_path=filepath,
                                  chunk_size=chunk,
                                  chunk_overlap=overlap)
    return {"status": 200}


@app.delete("/documents/{document}")
async def delete_documents(document: str):
    return uploader.delete_document_index(document)


@app.get("/answer/{question}")
async def get_answer(question: str):
    # document 가 없거나, k 가 0인 경우
    result = {}
    answer = generator.generate_answer(question=question)
    result['query'] = question
    result['result'] = answer
    result['reference_documents'] = []
    return result


@app.get("/answer/{document}/{question}")
async def get_answer_with_document(document: str, question: str, k: int = 0):
    result = {}
    if k == 0:
        answer = generator.generate_answer(question=question)
        result['query'] = question
        result['result'] = answer
        result['reference_documents'] = []
    else:
        answer, docs = generator.generate_answer_with_retrieval(index_name=document, question=question, k=k)
        result['query'] = question
        result['result'] = answer
        result['source_documents'] = docs
        result['reference_documents'] = []
        for doc in result['source_documents']:
            result['reference_documents'].append({"content": doc.page_content, "metadata": doc.metadata})

        del result["source_documents"]
    return result


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

