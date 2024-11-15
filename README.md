# Email Analysis API - ClearBoundaries

Empowering workplaces with AI-driven harassment detection and prevention. ClearBoundaries is a **SaaS** API designed to help organizations analyze email communications for tone, sentiment, and potential harassment, using advanced natural language processing and AI techniques.

## Core Technology: **Gemini AI Model**

The ClearBoundaries API integrates the **Gemini** AI model to:
- Analyze the tone and sentiment of emails.
- Detect harmful, inappropriate, or offensive language.
- Provide actionable feedback to improve workplace communication.

## Features
- **Gemini-Powered Analysis:** Uses the Gemini AI model to provide insights into email content.
- Analyzes emails for tone, sentiment, and potential harassment.
- Provides JSON responses with actionable feedback and suggestions for improving email tone.
- Dockerized for easy deployment.
- Designed as a **SaaS** solution for scalable and flexible integration into various applications.
- **Empowers workplaces:** Aims to make workplace communications respectful and professional, reducing instances of harassment.

## Setup

### 1. Clone the Repository
To get started, clone the repository to your local machine:

```bash
gh repo clone justinDevel/ClearBoundaries-Gemini-AI-driven-Harassment-Detection
cd email-analysis-api
```

### 2. Configure the `example.env` File
In the root of the project rename example.env to .env, then edit the `.env` file to have your api key environment variable:

```bash
GEMINI_API_KEY="your-gemini-api-key"  # Replace with your actual Gemini API key
GEMINI_API_MODEL_NAME="gemini-1.5-flash-latest"  # Specify the desired Gemini model version or keep the default
```

- **GEMINI_API_KEY**: Enter your personal API key from Gemini, which will authenticate requests to the Gemini AI service.
- **GEMINI_API_MODEL_NAME**: Define the model version you want to use (e.g., `gemini-1.5-flash-latest`). You can choose the appropriate model based on your use case.


Replace `"your-gemini-api-key"` with your actual Gemini API key.

### 3. Install Dependencies
Install the necessary dependencies listed in the `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Run the API Locally
To run the FastAPI server locally, use `uvicorn`:

```bash
uvicorn app.main:app --reload
```

This will start the development server, and you can access the API at `http://127.0.0.1:8000`.

### 5. API Documentation
Once the API is running, you can explore the available endpoints using the auto-generated Swagger UI at `http://127.0.0.1:8000/docs`.

### 6. Analyze an Email

To analyze an email using the API, you can use the following sample request. This request will assess the tone, sentiment, and potential instances of harassment within the provided message.

#### Sample Request

```json
{
   "messages": [
      {
         "subject": "Immediate Performance Concerns",
         "body": "I don’t know how many times I have to tell you this, but your work is way below acceptable standards. It’s honestly baffling how you’ve made it this far without getting fired. Every task you take on seems to turn into a disaster, and I’m getting tired of cleaning up your messes. You’re dragging the team down, and I’m seriously questioning why we even keep you on board. This is your last chance to prove you’re not a complete waste of time, or I’ll personally see to it that you’re replaced by someone competent. We don’t have room for someone who can’t handle basic responsibilities.",
         "sender": "manager@example.com",
         "recipient": "employee@example.com",
         "created_at": "2024-11-13T11:00:00Z",
         "modified_at": "2024-11-13T11:15:00Z",
         "email_thread_id": "thread56789",
         "language": "English"
      }
   ],
   "data": {
      "context": "workplace communication analysis"
   }
}
```

#### Explanation of Fields
- **`messages`**: A list of message objects to be analyzed. Each object should include:
  - **`subject`**: Subject line of the email.
  - **`body`**: Content of the email message.
  - **`sender`**: Email address of the sender.
  - **`recipient`**: Email address of the recipient.
  - **`created_at`**: Timestamp of when the message was created.
  - **`modified_at`**: Timestamp of the last modification.
  - **`email_thread_id`**: Unique identifier for the email thread.
  - **`language`**: Language of the message (e.g., "English").

- **`data`**: Additional context for analysis:
  - **`context`**: Specifies the analysis setting, such as `"workplace communication analysis"`.

#### Response
The API will return a detailed analysis including:
- Tone and sentiment of the message
- Flagged phrases with suggestions for improvement
- A harassment report indicating any identified concerns for further HR action

This sample request demonstrates a workplace scenario, but the API can be customized for other contexts with relevant configurations in `data.context`.

## Notes
- The API is designed as a **SaaS** solution, meaning it is scalable, flexible, and accessible via HTTP requests from any application needing email analysis.
- **ClearBoundaries** aims to empower workplaces by providing a tool that fosters respectful and professional communication, reducing instances of harassment and making the work environment safer and more supportive for everyone.

---

