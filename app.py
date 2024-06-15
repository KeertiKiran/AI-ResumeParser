from fastapi import FastAPI, UploadFile
from os import getenv
from ai_backend import AIParser
from pypdf import PdfReader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, AnyStr, Dict

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
    history_file="history/history.json"
)


# /parse_pdf endpoint
# Accepts a POST request with a PDF file and a job description text
@app.post("/parse_pdf", response_class=JSONResponse, response_model=OutputResponse)
async def parse_pdf(resume: UploadFile, jd_text: UploadFile):
    if resume.content_type != "application/pdf":
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid file type for resume. Please upload a PDF file."}
        )

    if jd_text.content_type != "text/plain":
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid file type for jd_text. Please upload a text file."}
        )

    jd_text = jd_text.file.read().decode("utf-8", "ignore")

    resume_text = str().join(
        [
            page.extract_text(extraction_mode="layout")
            for page in PdfReader(resume.file).pages
        ]
    )

    response = await ai_parser.parse(resume_text, jd_text)
    return JSONResponse(
        status_code=200,
        content=response
    )


@app.post("/parse_text", response_class=JSONResponse, response_model=OutputResponse)
async def parse_text(resume_text: str, jd_text: str):
    response = await ai_parser.parse(resume_text, jd_text)
    return JSONResponse(
        status_code=200,
        content=response
    )


@app.post("/parse_pdfs", response_class=JSONResponse, response_model=Dict[str, OutputResponse])
async def parse_pdfs(resumes: list[UploadFile], jd_text: UploadFile):
    resume_texts = [
        str().join(
            [
                page.extract_text(extraction_mode="layout")
                for page in PdfReader(resume.file).pages
            ]
        )
        for resume in resumes
    ]

    jd_text = jd_text.file.read().decode("utf-8", "ignore")

    responses = [
        await ai_parser.parse(resume_text, jd_text)
        for resume_text in resume_texts
    ]

    # Map the filenames to the responses
    result = {
        resume.filename: response
        for resume, response in zip(resumes, responses)
    }

    return JSONResponse(
        status_code=200,
        content=result
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=getenv("SERVER_HOST", "localhost"),
        port=int(getenv("SERVER_PORT", 8000))
    )
