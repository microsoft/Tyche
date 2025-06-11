import os
import requests
from semantic_kernel.functions import kernel_function

class EmailPlugin:
    """
    Plugin to send an email by calling a Logic App HTTP request trigger.
    The endpoint is read from the EMAIL_ENDPOINT environment variable.
    """
    def __init__(self):
        self.endpoint = os.getenv("EMAIL_ENDPOINT")
        if not self.endpoint:
            raise ValueError("EMAIL_ENDPOINT environment variable is not set.")

    @kernel_function(
        description="Send an email using the Logic App HTTP request trigger.",
        name="send_email",
    )
    def send_email(self, email_subject: str, email_body: str) -> str:
        """
        Sends an email by posting to the Logic App endpoint.
        Args:
            email_subject (str): Email subject
            email_body (str): Email body
        Returns:
            str: Status message
        """
        # Improve readability: replace double newlines with single, ensure paragraphs, and strip excess whitespace
        formatted_body = email_body.strip().replace('\n\n', '\n').replace('\n', '\n\n')
        payload = {
            "email_subject": email_subject,
            "email_body": formatted_body
        }
        response = requests.post(self.endpoint, json=payload)
        response.raise_for_status()
        return "Email sent successfully" if response.status_code == 200 else f"Failed to send email: {response.status_code}"
