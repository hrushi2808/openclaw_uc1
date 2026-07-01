from mcp.server.fastmcp import FastMCP
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mcp = FastMCP("EmailServer")

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """Send a follow-up email to a meeting participant"""
    sender   = "hrushikesh2808@gmail.com"
    password = "eljzipqkjvgzrpag"

    try:
        msg = MIMEMultipart()
        msg["From"]    = sender
        msg["To"]      = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, to, msg.as_string())

        print(f"EMAIL SENT | To: {to} | Subject: {subject}")    
        return f"Email successfully sent to {to}"

    except Exception as e:
        print(f"EMAIL FAILED | {str(e)}")
        return f"Failed to send email: {str(e)}"
    


if __name__ == "__main__":
    mcp.run(transport="stdio")