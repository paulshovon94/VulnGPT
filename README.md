# VulnGPT

A web-based vulnerability analysis interface combining Shodan data with ChatGPT-powered insights.

## Quick Setup

### 1. Environment Setup

Create and activate the conda environment:
```bash
conda create -n vulngpt python=3.10
conda activate vulngpt
```

### 2. Installation

Clone the repository and install dependencies:
```bash
git clone <repository-url>
cd vulngpt
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the project root:
```env
SHODAN_API_KEY=your_shodan_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 4. Running the Application

Start the application:
```bash
uvicorn main:app --reload
```

The interface will be available at `http://localhost:8000`

## Project Structure
```
vulngpt/
├── static/
│   ├── css/
│   │   └── style.css      # Interface styling
│   └── js/
│       └── main.js        # Frontend logic
├── templates/
│   └── index.html         # Main interface
├── main.py               # FastAPI application
├── requirements.txt      # Project dependencies
└── .env                 # Environment variables
```

## Requirements

The following packages are required (included in requirements.txt):
- fastapi
- uvicorn
- jinja2
- python-multipart
- python-dotenv
- shodan
- openai

## Troubleshooting

1. If you encounter environment issues:
```bash
conda deactivate
conda remove -n vulngpt --all
```
Then repeat the setup steps.

2. If the application fails to start, ensure:
- All dependencies are installed
- Environment variables are set correctly
- Port 8000 is not in use

## Support

For issues and support, please open a GitHub issue or contact the maintainers. 