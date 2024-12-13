from crewai_tools import BaseTool
from pypdf import PdfReader


class PDFReaderTool(BaseTool):
    name: str = "PDF Reader"
    description: str = (
        "Reads the content of a PDF file and returns the text"
    )

    def _run(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

