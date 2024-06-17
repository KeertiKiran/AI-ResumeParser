from fastapi import FastAPI, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, HTMLResponse
from os import getenv
from ai_backend import AIParser
from pypdf import PdfReader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import BinaryIO, List, AnyStr, Dict, Union
from converter import convert_docx_to_pdf_in_memory
import sentry_sdk


sentry_sdk.init(
    dsn="https://3204939d18ce8486a4ac2d7d2f928e84@o1303859.ingest.us.sentry.io/4507441298866176",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


load_dotenv()
templates = Jinja2Templates(directory="website")



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

# Template renderer

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
async def parse_pdf(resume: UploadFile, job_description: str):
    # Check if the file is a PDF or a DOCX/DOC file
    if resume.content_type != "application/pdf" and resume.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document" and resume.content_type != "application/msword":
        return JSONResponse(status_code=400, content={"error": "Only PDF/DOCX files are allowed"})

    # If the file is a DOCX/DOC file, convert it to PDF
    if resume.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or resume.content_type != "application/msword":
        resume_ = convert_docx_to_pdf_in_memory(resume.file)
    else:
        resume_ = resume.file
    
    resume_text = pdf_to_text(resume_)

    return await parse_proxy(resume_text, job_description)


@app.get("/")
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.j2", context={"request": request})
    
@app.get("/upload")
async def upload(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("upload.j2", context={"request": request})