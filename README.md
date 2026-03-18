# Patient Risk Predictor

Patient risk stratification with FHIR and synthetic data

## Features

- Api
Data - Feature Engineering
Data - Fhir Parser
Data - Synthetic Generator
Explainability - Shap Explainer
Models - Readmission
Models - Sepsis

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Key Dependencies:** pydantic,fastapi,uvicorn,anthropic,openai,numpy
- **Containerization:** Docker + Docker Compose

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)

### Installation

```bash
git clone https://github.com/MukundaKatta/patient-risk-predictor.git
cd patient-risk-predictor
pip install -r requirements.txt
```

### Running

```bash
uvicorn app.main:app --reload
```

### Docker

```bash
docker-compose up
```

## Project Structure

```
patient-risk-predictor/
├── src/           # Source code
├── tests/         # Test suite
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## License

MIT
