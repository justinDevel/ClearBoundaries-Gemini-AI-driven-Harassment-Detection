import logging
import os
from pathlib import Path
import aiofiles
import asyncio


logger = logging.getLogger(__name__)



script_dir = Path(__file__).resolve().parent
logger.info(f"Script directory: {script_dir}")

file_path = script_dir.parent / "templates" / "harassment.md"
logger.info(f"File path: {file_path}")

async def load_prompt_template(file_path: Path) -> str:
    """
    Asynchronously loads the prompt template from a markdown file.

    Args:
        file_path (Path): The path to the markdown file.

    Returns:
        str: The content of the file if it exists, otherwise None.
    """
    if not file_path.exists():
        logger.warning(f"Error: The file '{file_path}' does not exist.")
        return None
    
    try:
        logger.info(f"Script directory: {script_dir}")
        logger.info(f"File path: {file_path}")
        async with aiofiles.open(file_path, 'r') as file:
            prompt_template = await file.read()
        return prompt_template
    except IOError as e:
        logger.error(f"Error reading the file '{file_path}': {e}")
        return None
    



async def create_prompt(
    subject: str,
    body: str,
    sender: str,
    recipient: str,
    created_at: str,
    modified_at: str,
    email_thread_id: str,
    language: str,
    context: str,
    flagged_phrases: list = [],
    tone: str = "",
    sentiment: str = "",
    revised_email: str = "",
    # report: dict = None
) -> str:
    """
    Creates a prompt by loading a template and filling it with dynamic values for harassment prevention in workplace communication.
    
    Args:
        subject (str): Subject of the email.
        body (str): Body of the email.
        sender (str): Sender's email address.
        recipient (str): Recipient's email address.
        created_at (str): Timestamp of when the email was created.
        modified_at (str): Timestamp of when the email was last modified.
        email_thread_id (str): Identifier for the email thread.
        language (str): Language of the email.
        context (str): Context of the email (e.g., workplace, personal, etc.).
        is_harassment (bool): Whether the email is flagged as harassment.
        flagged_phrases (list, optional): List of flagged phrases in the email.
        tone (str, optional): The tone of the email (e.g., formal, casual).
        sentiment (str, optional): The sentiment of the email (e.g., positive, neutral).
        revised_email (str, optional): Revised email content after modifications.
        report (dict, optional): Report containing AI analysis results and recommendations.

    Returns:
        str: The generated prompt formatted with dynamic values.
    """

    # logger.log(f"report :: {report}")
    # Initialize report if None
    # if report is None:
    #     report = {
    #         "ai_analysis_is_harassment": False,
    #         "is_harassment": False,
    #         "harassment_type": "",
    #         "recommendations": []
    #     }

    # Load the harassment prevention prompt template (this should be from an external source like a file)
    template = await load_prompt_template(file_path)

    if not template:
        logger.warning("Prompt template loading failed. Returning default template.")

        # Default template with dynamic placeholders for harassment prevention
        default_template = (
            "Subject: {subject}\n"
            "Body: {body}\n"
            "Sender: {sender}\n"
            "Recipient: {recipient}\n"
            "Created At: {created_at}\n"
            "Modified At: {modified_at}\n"
            "Email Thread ID: {email_thread_id}\n"
            "Language: {language}\n"
            "Analyze the email for any harmful, inappropriate, or offensive language and provide suggestions for rephrasing if necessary."
        )

        # Format and return the default template
        return default_template.format(
            subject=subject,
            body=body,
            sender=sender,
            recipient=recipient,
            created_at=created_at,
            modified_at=modified_at,
            email_thread_id=email_thread_id,
            language=language,
        )
        # logger.info(f"formatted_prompt {formatted_prompt}")
    try:
       
        # Fill placeholders with dynamic values from the loaded template
        formatted_prompt = template.format(
            subject=subject,
            body=body,
            sender=sender,
            recipient=recipient,
            created_at=created_at,
            modified_at=modified_at,
            email_thread_id=email_thread_id,
            language=language,
        )
        logger.info("Prompt created successfully.")
        logger.info(f"formatted_prompt {formatted_prompt}")
        return formatted_prompt
    except KeyError as e:
        logger.error(f"Error formatting prompt: Missing placeholder for {e}")
        return template  # Return the unformatted template as a fallback