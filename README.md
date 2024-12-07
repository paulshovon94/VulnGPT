# VulnGPT

A web-based vulnerability analysis interface combining Shodan data with ChatGPT-powered insights, featuring performance evaluation and visualization capabilities.

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

### 5. Running Performance Evaluations

The project includes two types of performance evaluations:

#### Single-Query Performance
Run the basic performance evaluation:
```bash
python evaluation.py
```
This will measure response times for individual components and save results in `evaluation_results/`.

#### Load Testing
Run the concurrent users simulation:
```bash
python load_evaluation.py
```
This simulates multiple concurrent users and saves results in `load_test_results/`.

### 6. Visualizing Results

Generate visualizations for the evaluation results:

#### Basic Performance Visualization
```bash
python visualization.py
```
Creates plots showing component-wise performance metrics.

#### Load Test Visualization
```bash
python load_visualization.py
```
Creates plots showing system performance under load.

## Project Structure
```
vulngpt/
├── static/
│   ├── css/
│   │   └── style.css        # Interface styling
│   └── js/
│       └── main.js          # Frontend logic
├── templates/
│   └── index.html           # Main interface
├── services/
│   ├── chatgpt.py          # ChatGPT integration
│   ├── shodan.py           # Shodan API integration
│   └── vulnSolution.py     # Security solution generation
├── evaluation_results/      # Performance evaluation results
├── load_test_results/      # Load testing results
├── main.py                 # FastAPI application
├── evaluation.py           # Performance evaluation
├── visualization.py        # Results visualization
├── load_evaluation.py      # Load testing
├── load_visualization.py   # Load test visualization
├── requirements.txt        # Project dependencies
└── .env                   # Environment variables
```

## Requirements

Key dependencies (included in requirements.txt):
- FastAPI and related packages
- Shodan API client
- OpenAI API client
- Data analysis: pandas, numpy
- Visualization: matplotlib, seaborn
- Other utilities: python-dotenv, httpx

## Performance Metrics

The system has been evaluated for:
- Component-wise response times
- Concurrent user handling
- System scalability
- Success rates under load

Visualization capabilities include:
- Response time distributions
- Component breakdown analysis
- Success rate analysis
- Performance metrics under load

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

3. For visualization issues:
- Ensure matplotlib and seaborn are properly installed
- Check write permissions in results directories
- Verify that evaluation results exist before visualization

## Support

For issues and support:
- Open a GitHub issue
- Contact the maintainers
- Check the documentation for common solutions

## License

[Your License Information]

## Author

Shovon Paul
  