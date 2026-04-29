# Stroke Risk Analytics System

A clinical decision support tool built to explore stroke risk patterns across 172,000 simulated patient records. Built with pure Python and a Flask web interface — no pandas or numpy — to demonstrate low-level data engineering alongside clinical insight.

**Live dashboard:** run locally via `python3 gui.py` → `http://localhost:5000`

---

## The Problem

Stroke is one of the leading causes of death and disability in the UK. Early identification of at-risk patients — particularly those with compounding risk factors like hypertension, heart disease, and lifestyle behaviours — can meaningfully support clinical intervention. This project explores what patterns emerge when those risk factors are analysed together across a large patient dataset.

---

## Key Findings

Analysis of 172,000 patient records revealed several clinically relevant patterns:

- **Hypertension is a significant stroke predictor.** Of 25,823 hypertensive patients, 9.8% (2,522) went on to have a stroke — nearly 1 in 10.
- **Heart disease compounds risk substantially.** Of 17,248 patients with heart disease, 10.1% (1,737) experienced a stroke — a higher rate than hypertension alone.
- **Smoking combined with hypertension affects older patients most.** Among smokers with hypertension who had a stroke, the mean age was 54.68, median 55, but mode 73 — indicating a concentration of cases in older age groups.
- **Heart disease stroke patients show elevated glucose.** Those with heart disease who had a stroke had a mean glucose level of 183.53 mg/dL, well above the dataset mean of 184.93 — consistent with known diabetes-stroke comorbidity.
- **Dietary habits showed no protective effect across groups.** Mixed, non-vegetarian, and vegetarian patients all showed a stroke rate of exactly 10%, suggesting diet alone is not a differentiating factor in this dataset.
- **Urban and rural patients showed near-identical stroke ages.** Urban stroke patients had a mean age of 54.19 vs 53.92 for rural — a negligible difference, suggesting geography is not a meaningful risk differentiator here.
- **Sleep hours were not a distinguishing factor.** Stroke patients averaged 7.51 hours of sleep vs 7.50 for non-stroke patients — effectively identical across 172,000 records.
- **The patient population is middle-aged on average.** Mean age 54.01, range 18–90, with a standard deviation of 21.08 — a broadly distributed cohort.
- **BMI averages in the overweight range.** Mean BMI of 30.01 (borderline obese), with 75% of patients at or below 40.1 — indicating a population with meaningful cardiovascular risk load.

---

## Dataset

- **Records:** 172,000 simulated patient records
- **Features:** 20 clinical and lifestyle variables including age, BMI, glucose level, smoking status, hypertension, heart disease, dietary habits, sleep hours, residence type, and stroke occurrence
- **Source:** Synthetic dataset — not real patient data. The `data.csv` file is excluded from this repository (see `.gitignore`) in line with data governance best practice.

To replicate: generate a synthetic dataset with the above features, or contact the author for dataset structure details.

---

## System Architecture

```
stroke-risk-analytics/
├── dataset_module.py    # Custom CSV parser — no pandas/numpy
├── query_module.py      # 11 analytical query functions
├── ui_module.py         # Terminal interface
├── gui.py               # Flask web application
├── main.ipynb           # Jupyter notebook entry point
├── static/              # CSS, JS, Chart.js assets
└── templates/           # HTML dashboard template
```

**Key technical decision:** The entire data pipeline is built without pandas or numpy, using only Python standard library. This was a deliberate engineering choice to demonstrate understanding of data structures, custom parsing, and statistical computation from first principles.

---

## Analyses Available

| # | Analysis | Output |
|---|----------|--------|
| 1 | Smokers + hypertension → stroke | Mean/median/mode age |
| 2 | Heart disease + stroke | Age and glucose statistics |
| 3 | Gender × hypertension × stroke | Age breakdown by gender group |
| 4 | Smoking status vs stroke | Age comparison across smoking categories |
| 5 | Urban vs rural stroke | Geographic age comparison |
| 6 | Dietary habits + stroke | Distribution across diet types |
| 7 | Hypertension → stroke patients | Full patient records |
| 8 | Hypertension + stroke overview | Stroke rate with doughnut chart |
| 9 | Heart disease + stroke overview | Stroke rate with doughnut chart |
| 10 | Descriptive stats | Any of: age, BMI, glucose, sleep hours |
| 11 | Sleep hours comparison | Stroke vs non-stroke averages |

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Yvannaesseba/stroke-risk-analytics.git
cd stroke-risk-analytics

# Install dependencies
pip3 install flask jupyter

# Add your data.csv to the project folder (see Dataset section)

# Run the Flask dashboard
python3 gui.py

# Open in browser
http://localhost:5000
```

---

## Technologies

- **Python 3** — core language, no high-level data libraries
- **Flask** — web framework and REST API
- **Chart.js** — interactive bar and doughnut charts
- **Jupyter Notebook** — exploratory analysis and terminal interface
- **HTML/CSS/JavaScript** — custom dashboard UI

---

## Limitations & Next Steps

This is an exploratory analysis on synthetic data. Real-world clinical application would require:
- Validated, real patient data with appropriate governance approvals
- Multivariate modelling to control for confounding variables
- Predictive modelling (logistic regression, decision trees) rather than descriptive statistics only
- Integration with electronic health record systems

Next development steps: add predictive risk scoring, incorporate SHAP-based feature importance, and extend the dashboard with patient-level risk profiling.

---

## Author

**Emmanuelle Yvanna Esseba Ayangma**  
MSc Big Data Analytics  — Sheffield Hallam University  
[LinkedIn](https://www.linkedin.com/in/e-esseba) | [GitHub](https://github.com/Yvannaesseba) | [Portfolio](https://yvannaesseba.github.io)
