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
git clone <your-repo-url>
cd email-analysis-api
```

### 2. Configure the `.env` File
In the root of the project, edit the `.env` file to have your api key environment variables:

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


## Notes
- The API is designed as a **SaaS** solution, meaning it is scalable, flexible, and accessible via HTTP requests from any application needing email analysis.
- **ClearBoundaries** aims to empower workplaces by providing a tool that fosters respectful and professional communication, reducing instances of harassment and making the work environment safer and more supportive for everyone.

---

