from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from os import getenv
from ai_backend import AIParser
from pypdf import PdfReader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import BinaryIO, List, AnyStr, Dict, Union
from multiprocessing.pool import Pool

load_dotenv()

class OutputResponse(BaseModel):
    compliant: AnyStr  # Max score is 100%
    name: AnyStr
    mobile: List[AnyStr]
    email: List[AnyStr]
    companies_worked_for: List[AnyStr]
    experience_total: int
    experience_relevant: int
    major_tech_stack: List[AnyStr]
    certifications: List[AnyStr]
    domains_experience: List[AnyStr]


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

ai_parser = AIParser(
    api_key=getenv("API_KEY"),
)

parse_proxy = ai_parser.parse

def pdf_to_text(file: BinaryIO):
    return "".join([ x.extract_text('layout') for x in PdfReader(file).pages ])

def job_to_text(file: BinaryIO):
    return file.read().decode("utf-8", "ignore")

# /parse_pdf endpoint
# Accepts a POST request with a PDF file and a job description text
# parse the PDF/text and job description file/text and return the parsed data
@app.post("/parse_pdf")
async def parse_pdf(resume: UploadFile, job_description: UploadFile):
    if resume.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "Only PDF files are allowed"})

    resume_text = pdf_to_text(resume.file)
    job_description_text = job_to_text(job_description.file)

    return await parse_proxy(resume_text, job_description_text)

@app.post("/parse_text")
async def parse_text(resume: AnyStr, job_description: AnyStr):
    return await parse_proxy(resume, job_description)


@app.post("/parse_pdf/stream")
async def parse_pdf_and_stream_response(resume: UploadFile, job_description: UploadFile) -> StreamingResponse:
    if resume.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "Only PDF files are allowed"})

    resume_text = pdf_to_text(resume.file)
    job_description_text = job_to_text(job_description.file)

    def _yield():
        for res in ai_parser.parse_s(resume_text, job_description_text):
            yield res.text

    return StreamingResponse(content=_yield(), media_type="application/json")

@app.post("/parse_text/stream")
async def parse_text_and_stream_response(resume: AnyStr, job_description: AnyStr) -> StreamingResponse:
    def _yield():
        for res in ai_parser.parse_s(resume, job_description):
            yield res.text

    return StreamingResponse(content=_yield(), media_type="application/json")

