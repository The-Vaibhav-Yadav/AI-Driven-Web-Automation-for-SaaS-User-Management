# AI-Driven Web Automation for SaaS User Management

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Ollama](https://img.shields.io/badge/Ollama-Generative_AI-orange)

An intelligent automation framework leveraging large language models (Ollama/Gemini natively) to completely streamline and automate web interactions for SaaS user provisioning. This system negates manual interface parsing, directly interpreting DOM elements and mimicking user navigations autonomously.

## Table of Contents
- [Tech Stack & Architecture](#tech-stack--architecture)
- [Prerequisites](#prerequisites)
- [Installation & Local Setup](#installation--local-setup)
- [Usage & Running the App](#usage--running-the-app)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing Guidelines](#contributing-guidelines)
- [License and Contact](#license-and-contact)

## Tech Stack & Architecture

- **Primary Technologies**: Python, Selenium/Playwright (Web Automation limits), LLMs (Ollama / Google Gemini API).
- **Core Strategy**: The system fetches targeted DOM elements and routes complex traversal decisions through local or hosted LLMs mapping semantic intent.

**Architecture**: 
- `scraper.py`: Core execution script initializing the browser driver, parsing the DOM, and passing page variables directly into the LLM logic layer. The LLM dictates interactions (click, type, navigate) dynamically bypassing rigid string locators globally.

## Prerequisites
- **Python**: v3.10+
- **Drivers**: A compatible web driver locally configured natively mapping interactions.
- **External Accounts**: A Google Cloud account providing API bounds (`GOOGLE_API_KEY`) or an active `Ollama` daemon locally spanning requests.

## Installation & Local Setup

```bash
git clone https://github.com/The-Vaibhav-Yadav/AI-Driven-Web-Automation-for-SaaS-User-Management.git
cd AI-Driven-Web-Automation-for-SaaS-User-Management

# Use `uv` package manager optimally
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Environment Variables**:
Create a standard baseline configuration file:
```bash
cp .env.example .env
```
Inside `.env`, define the parameter:
`GOOGLE_API_KEY=your_gemini_api_key_here`

## Usage & Running the App

Once configured natively via your `.env`, initialize the automation wrapper seamlessly:
```bash
uv run python scraper.py
```
**Expected execution**:
A discrete browser window opens, navigates natively to the target SaaS dashboard, extrapolates fields using AI context inferences, and procedurally generates dummy user deployments continuously.

## Testing
To test the core LLM interpretations without triggering full browser instantiations:
```bash
uv run pytest tests/
```
**Note**: End-to-end (E2E) testing limits apply heavily given dynamic SaaS frontend modifications changing semantic DOM structures.

## Deployment
Typically triggered via serverless functions (AWS Lambda natively scaling limits) or executed via daily cronjobs locally provisioning internal structural testing user data.

## Contributing Guidelines
1. Pull standard branches locally.
2. Adhere formatting natively using `Black`.
3. Add robust try/catch bounds encapsulating network timeouts preventing driver crashes dynamically.

## License and Contact
**License**: MIT 
**Author**: Vaibhav Yadav (https://github.com/The-Vaibhav-Yadav)
