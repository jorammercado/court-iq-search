# Search Bar Microservice

This repository contains the Flask-based microservice that powers the natural language search functionality for the Court-IQ platform — a basketball analytics and sports betting application. Initially conceived as a prototype for more advanced AI predictions and question-answering, the service was scaled down due to hardware limitations (e.g., insufficient resources to fine-tune or run large models). It now performs fast fuzzy matching on a pre-defined set of Q&A pairs to deliver relevant responses.

The service is deployed independently on **Render**, where it responds to search requests passed through the primary [court-iq-server](https://github.com/jorammercado/court-iq-server).

## Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Functionality](#functionality)
- [Reference GitHub Repos](#reference-github-repos)
- [Example](#example)
- [Tech Stack](#tech-stack)
- [Limitations](#limitations)
- [Installation](#installation)
- [License](#license)
- [Contact](#contact)

## Overview
The search system uses a JSON-based Q&A dataset and returns the closest matching answer to a user's query using the **FuzzyWuzzy** string-matching library. Search queries are routed from the Court-IQ frontend to this microservice through the main backend server:

**Frontend → `court-iq-server` → `court-iq-search` (this microservice)**

The backend acts as a bridge, forwarding user input to this microservice and returning the response.

## Architecture
- **Deployed on**: [Render](https://render.com)
- **Data Storage**: A local JSON file (`allConvertedData.json`) stored on the Render instance
- **Service Communication**: This service does not interface directly with a database or external APIs. It communicates exclusively via HTTP POST requests from the main backend.

## Functionality
- Accepts a `POST` request with a user question in the body (`/ask` route)
- Uses fuzzy string matching to compare the user’s query to a large predefined dataset of questions
- Returns the answer for the closest-matching question, provided the similarity score exceeds a defined threshold
- If no sufficiently similar question is found, returns a fallback message

## Reference GitHub Repos
- [court-iq](https://github.com/jorammercado/court-iq)
- [court-iq-server](https://github.com/jorammercado/court-iq-server)

## Example
**Input (Frontend):**
```json
{
  "question": "How tall is LeBron James?"
}
```

**Closest match (from dataset):**
> "How tall or what is the height of LeBron James?"

**Response:**
```json
{
  "answer": "LeBron James is 6 feet 9 inches."
}
```

If no sufficiently close match is found:
```json
{
  "answer": "I'm not sure how to answer that. Can you please ask another question or rephrase your question?"
}
```

## Tech Stack
- **Language**: Python 3.9.6
- **Framework**: Flask
- **Dependencies**:
  - `fuzzywuzzy`: for fuzzy string matching
  - `gunicorn`: for production-ready deployment
  - `transformers` and `torch`: included from early GPT-based experimentation (currently unused but left for potential future use)

## Limitations
- Answers are limited to static data in `allConvertedData.json`.
- As of yet, no real-time data pipeline updates or external API querying have been implemented.
- Does not understand new or unseen questions that aren't closely phrased to existing entries.
- The dataset is currently outdated and was originally intended for prototyping.
- On deployment (Render), the service may require a short wake-up period if inactive. 

## Installation

1. Fork the repository from [github.com/jorammercado/court-iq-search](https://github.com/jorammercado/court-iq-search).

2. Clone the repository:
```bash
git clone https://github.com/your-username/court-iq-search.git
```

3. Navigate to the project directory:
```bash
cd court-iq-search
```

4. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Run the application:
```bash
python flask_app.py
```

7. Test locally using a tool like Postman or `curl`:
```bash
curl -X POST http://localhost:5001/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "Where was Jae\'Sean Tate born?"}'
```

## License
This project is licensed under the MIT License. See [LICENSE](https://opensource.org/license/mit) file for details.

## Contact
**Joram Mercado**  
[GitHub](https://github.com/jorammercado) | [LinkedIn](https://www.linkedin.com/in/jorammercado)