
# 🤖 Revio InsightAI
### Explainable AI-Powered Customer Review Intelligence

**A prototype enhancement concept for Cynbit's Revio platform.**

Revio InsightAI is a Python-based customer review intelligence application that analyzes customer feedback, detects multiple complaint categories, identifies potentially urgent reviews, and generates human-reviewed response suggestions.

It combines machine learning, rule-based explainability, data visualization, and persistent storage in one interactive application.

---

## 🚀 Key Features

- **Sentiment Analysis:** Classifies reviews as Positive, Negative, or Neutral using TF-IDF and Logistic Regression.
- **Multi-Issue Classification:** Detects Delivery, Product Quality, Customer Support, Payment & Refund, Pricing, and Other.
- **Priority Detection:** Assigns High, Medium, or Low priority using customer ratings, sentiment, and urgency indicators.
- **Explainable Results:** Displays reasons behind priority decisions.
- **Suggested Responses:** Generates template-based response drafts for human review.
- **Interactive Dashboard:** Displays sentiment distribution, complaint categories, and review metrics.
- **CSV Upload:** Supports batch review analysis.
- **Review History:** Stores analyzed reviews using SQLite.
- **Model Evaluation:** Reports accuracy, precision, recall, F1-score, and a confusion matrix.
- **Automated Testing:** Includes Pytest tests for core functionality.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Streamlit | Web application |
| Scikit-learn | Machine learning |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Plotly | Interactive visualizations |
| SQLite | Database |
| Pytest | Automated testing |

## 🧠 System Architecture

```text
Customer Reviews
       |
       v
Text Preprocessing
       |
       v
TF-IDF Feature Extraction
       |
       v
Logistic Regression
       |
       v
Sentiment Prediction
       |
       +----------------------+
       |                      |
       v                      v
Issue Classification    Priority Detection
       |                      |
       +----------+-----------+
                  |
                  v
        Explainable Analysis
                  |
                  v
       Suggested Response Draft
                  |
                  v
          Streamlit Dashboard
                  |
                  v
           SQLite History
```

## 📂 Project Structure

```text
CynbitAIReviewAssistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── sample_reviews.csv
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── sentiment.py
│   ├── classification.py
│   ├── priority.py
│   ├── response_generator.py
│   └── database.py
│
├── tests/
│   ├── __init__.py
│   └── test_analysis.py
│
└── reports/
    ├── ai_opportunity_report.md
    └── technical_approach.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd CynbitAIReviewAssistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows Git Bash:**

```bash
source venv/Scripts/activate
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

## 📊 Model Evaluation

The current prototype was evaluated using a stratified held-out test set.

| Evaluation Metric | Result |
|---|---:|
| Synthetic dataset | 60 reviews |
| Test samples | 15 |
| Test accuracy | 73.3% |
| Automated tests | 7 passed |

The dashboard also displays precision, recall, F1-score, and the confusion matrix.

**Evaluation disclaimer:** The dataset is synthetic and sentiment labels are derived from customer ratings. The evaluation is preliminary and does not represent independently validated real-world performance.

## 🧪 Run Automated Tests

Execute:

```bash
python -m pytest -v
```

Current result:

```text
7 passed in 2.78s
```

## 📄 Project Reports

Detailed documentation is available in the `reports/` directory:

- `ai_opportunity_report.md` — Business opportunity and proposed solution.
- `technical_approach.md` — Architecture, technology, implementation, evaluation, and limitations.

## 🔮 Future Enhancements

- Evaluation using larger, independently labeled real-world datasets.
- Transformer-based sentiment analysis.
- Multilingual review analysis.
- LLM-based response drafting with human approval.
- Recurring complaint and trend detection.
- Secure integration with review management platforms.
- Authentication and production deployment.

## ⚠️ Current Limitations

This is a proof of concept, not a production-ready integration.

- No live connection to Cynbit's Revio platform.
- Sentiment training uses synthetic demonstration data.
- Issue classification uses keyword matching.
- Priority detection uses predefined rules.
- Suggested responses are template-based, not generated by an integrated LLM.
- Human approval is required before any response is sent.

## 👩‍💻 Author

**Shrutiarya Biswal**

B.Tech — Computer Science & Technology

GitHub: https://github.com/shrutiaryabiswal-eng

## 🎯 Assessment Context

Developed as an AI/ML Engineer Intern assessment project to explore an explainable AI opportunity for customer review intelligence.

**Concept:** Revio InsightAI — Explainable Review Intelligence and Smart Escalation.
