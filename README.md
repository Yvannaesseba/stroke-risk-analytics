# Stroke Risk Analytics System

A clinical decision support system for analyzing stroke risk factors using a dataset of 172,000 patient records. Built to help healthcare providers identify high-risk patients and prevent cardiovascular-related fatalities through data-driven insights.

## Project Overview

Cardiovascular disease is one of the leading causes of death in the UK. This system analyzes patient vital signs and lifestyle factors to help clinicians monitor and predict stroke risk, enabling early intervention and prevention of avoidable deaths.

**Dataset:** 172,000 simulated patient records with 20 clinical features  
**Purpose:** Clinical decision support for stroke risk assessment  
**Implementation:** Pure Python (no pandas/numpy) with Flask web interface

## Key Features

- Custom CSV parsing without high-level libraries (pandas, numpy)
- Handles 172,000+ patient records efficiently
- Clinical analytics: age demographics, risk correlations, lifestyle impact
- Interactive Flask web application with visual dashboard
- Export results to CSV format

## Technologies Used

- Python 3.x
- Flask (web framework)
- Jupyter Notebook
- HTML/CSS/JavaScript

## Quick Start
```bash
cat > README.md << 'ENDOFFILE'
# Stroke Risk Analytics System

A clinical decision support system for analyzing stroke risk factors using a dataset of 172,000 patient records. Built to help healthcare providers identify high-risk patients and prevent cardiovascular-related fatalities through data-driven insights.

## Project Overview

Cardiovascular disease is one of the leading causes of death in the UK. This system analyzes patient vital signs and lifestyle factors to help clinicians monitor and predict stroke risk, enabling early intervention and prevention of avoidable deaths.

**Dataset:** 172,000 simulated patient records with 20 clinical features  
**Purpose:** Clinical decision support for stroke risk assessment  
**Implementation:** Pure Python (no pandas/numpy) with Flask web interface

## Key Features

- Custom CSV parsing without high-level libraries (pandas, numpy)
- Handles 172,000+ patient records efficiently
- Clinical analytics: age demographics, risk correlations, lifestyle impact
- Interactive Flask web application with visual dashboard
- Export results to CSV format

## Technologies Used

- Python 3.x
- Flask (web framework)
- Jupyter Notebook
- HTML/CSS/JavaScript

## Quick Start
```bash
# Install dependencies
pip install flask jupyter

# Run Flask app
python gui.py

# Open browser to: http://localhost:5000
```

## Repository Structure
```
stroke-risk-analytics/
├── dataset_module.py       # Data loading
├── query_module.py         # Analytics functions
├── ui_module.py           # Text interface
├── gui.py                 # Flask web app
├── main.ipynb             # Jupyter notebook
├── static/                # CSS, JS, images
└── templates/             # HTML templates
```

## Contact

Emmanuelle Yvanna Esseba Ayangma  
[LinkedIn](https://www.linkedin.com/in/e-esseba) | [GitHub](https://github.com/Yvannaesseba)
