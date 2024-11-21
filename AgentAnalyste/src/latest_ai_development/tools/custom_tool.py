from crewai_tools import BaseTool
from pypdf import PdfReader

class PDFReaderTool(BaseTool):
    name: str = "PDF Reader"
    description: str = (
        "Reads the content of a PDF file and returns the text"
    )

    def _run(self, pdf_path: str) -> str:
        reader= PdfReader(pdf_path)
        text=""
        for page in reader.pages:
            text+= page.extract_text()
        return text

 
class PDFSearchTool(BaseTool):
    name: str = "PDF Search Tool"
    description: str = (
        "Searches for a keyword in a PDF file and returns the page number"
    )

    def _run(self, solution_path: str, keyword: str) -> int:
        reader= PdfReader(solution_path)
        for i, page in enumerate(reader.pages):
            text= page.extract_text()
            if keyword in text:
                return i+1
        return -1