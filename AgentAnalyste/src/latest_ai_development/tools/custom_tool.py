from crewai_tools import BaseTool
from pypdf import PdfReader
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    
class EmailSenderTool(BaseTool):
    name: str = "Email Sender"
    description: str = (
        "Sends an email to the customer with the provided content."
    )

    def _run(self, to_email: str, subject: str, body: str) -> str:
        sender_email = "xujohan40@gmail.com"
        sender_password = "wekm lqgw vtxd untj"
        smtp_server = "smtp.gmail.com"  
        smtp_port = 587  # 587 ou 465

        try:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = to_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP(smtp_server, smtp_port)

            status_code, response = server.ehlo()
            print(f"[*] Echoing the server: {status_code} {response}")

            status_code, response = server.starttls()
            print(f"[*] Starting TLS connection: {status_code} {response}")

            status_code, response = server.login(sender_email, sender_password)
            print(f"[*] Logging in: {status_code} {response}")

            server.sendmail(sender_email, to_email, msg.as_string())
            server.close()

            return f"Email sent successfully to {to_email}."

        except Exception as e:
            return f"Failed to send email: {str(e)}"