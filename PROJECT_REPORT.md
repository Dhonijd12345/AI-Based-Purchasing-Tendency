# AI-Based Purchasing Tendency

## Project Report

**Author:** Nikile Eines Dhoni J
**Degree:** B.Tech – Artificial Intelligence and Data Science
**Institution:** Mohamed Sathak Engineering College
**Project Version:** v1.0.0
**Domain:** Artificial Intelligence / Machine Learning / Retail Intelligence

---

# 1. Executive Summary

**AI-Based Purchasing Tendency** is an AI-driven retail intelligence project designed to analyze customer purchasing behavior and derive useful insights from transactional patterns.

The project explores the combination of **Graph Neural Networks (GNNs)** and the **SASRec sequential recommendation architecture** to model relationships and purchasing sequences.

The system focuses on customer behavior analysis, purchasing-community discovery, location-wise demand analysis, and personalized product recommendation.

---

# 2. Introduction

Retail platforms generate large amounts of customer and transaction data.

Understanding this data can help organizations identify:

* Customer purchasing patterns.
* Product relationships.
* Customer communities.
* Regional demand.
* Personalized product preferences.

Traditional statistical approaches can provide useful summaries, but complex relationships and sequential behavior require more advanced machine-learning approaches.

This project therefore explores an AI-based approach combining graph learning and sequential recommendation.

---

# 3. Problem Statement

Traditional purchasing analysis may rely on:

* Product frequency.
* Sales totals.
* Customer counts.
* Basic statistical summaries.

These approaches may not fully capture:

* Customer-product relationships.
* Sequential purchasing behavior.
* Similar purchasing communities.
* Geographic demand patterns.
* Personalized customer preferences.

The project addresses this challenge by exploring relationship-aware and sequence-aware AI techniques.

---

# 4. Project Objectives

The main objectives are:

1. Analyze customer purchasing behavior.
2. Model relationships between customers and products.
3. Discover purchasing communities.
4. Analyze purchasing patterns across locations.
5. Model sequential product interactions.
6. Support personalized product recommendations.
7. Demonstrate the application of modern AI techniques to retail intelligence.

---

# 5. Proposed Solution

The project uses two complementary approaches.

## 5.1 Graph Neural Networks

Purchasing interactions can be represented as relationships between connected entities.

Example:

```text
Customer
   │
   │ Purchases
   ▼
Product
```

Multiple relationships can form a larger graph containing customers, products, and purchasing interactions.

GNN-based learning can then be used to learn structural patterns from the graph.

---

## 5.2 SASRec

SASRec stands for **Self-Attentive Sequential Recommendation**.

It models sequences of customer-item interactions.

Example:

```text
Product A
    ↓
Product C
    ↓
Product B
    ↓
Product D
```

The sequence provides information about purchasing behavior and can support next-item recommendation tasks.

---

# 6. System Architecture

```text
                 ┌───────────────────────┐
                 │    Purchasing Data    │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ Data Preprocessing    │
                 └───────────┬───────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
                 ▼                       ▼
       ┌─────────────────┐     ┌─────────────────┐
       │      GNN        │     │     SASRec      │
       │ Graph Learning  │     │   Transformer   │
       └────────┬────────┘     └────────┬────────┘
                │                       │
                └───────────┬───────────┘
                            │
                            ▼
                 ┌───────────────────────┐
                 │ Retail Intelligence  │
                 └───────────┬───────────┘
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
       Customer          Demand          Product
       Communities      Analysis       Recommendations
```

---

# 7. Methodology

The overall methodology can be summarized as:

```text
Purchasing Data
      ↓
Data Cleaning
      ↓
Feature Preparation
      ↓
Customer/Product Relationships
      ↓
Graph Construction
      ↓
GNN Learning
      ↓
Purchase Sequence Construction
      ↓
SASRec Modeling
      ↓
Pattern Analysis
      ↓
Retail Intelligence
```

---

# 8. Major Components

## 8.1 Data Processing

The purchasing data is prepared for analysis and model development.

Typical activities include:

* Data loading
* Data cleaning
* Feature preparation
* Transaction organization
* Customer/product relationship preparation
* Purchase sequence construction

---

## 8.2 Graph-Based Learning

The graph component represents relationships between entities.

It is intended to support:

* Relationship learning
* Community discovery
* Structural purchasing analysis

---

## 8.3 Sequential Recommendation

The sequential component models customer-item interaction sequences.

It is intended to support:

* Purchase sequence analysis
* Next-item prediction
* Personalized recommendation

---

## 8.4 Retail Intelligence

The combined AI approach can support:

* Customer behavior analysis
* Purchasing community discovery
* Location-wise demand analysis
* Product recommendation
* Data-driven retail planning

---

# 9. Technology Stack

| Technology                   | Purpose                    |
| ---------------------------- | -------------------------- |
| Python                       | Core development           |
| Pandas                       | Data processing            |
| NumPy                        | Numerical computation      |
| Scikit-learn                 | Machine-learning utilities |
| Graph Neural Networks        | Relationship learning      |
| SASRec                       | Sequential recommendation  |
| Transformer / Self-Attention | Sequence modeling          |
| Matplotlib                   | Data visualization         |

The project dependency configuration should remain synchronized with the actual implementation.

---

# 10. Project Structure

```text
AI-Based-Purchasing-Tendency/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── PROJECT_REPORT.md
│
└── purchasing tendancy/
    │
    ├── app.py
    ├── requirements.txt
    ├── run_project.ps1
    ├── data/
    ├── models/
    ├── scripts/
    ├── scratch/
    ├── templates/
    ├── utils/
    └── static/
        └── img/
            └── categories/
```

---

# 11. Installation

Clone the repository:

```bash
git clone https://github.com/Dhonijd12345/AI-Based-Purchasing-Tendency.git
```

Navigate into the repository:

```bash
cd AI-Based-Purchasing-Tendency
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 12. Running the Project

The project contains an `app.py` application entry point and a PowerShell project runner.

On Windows:

```powershell
.\run_project.ps1
```

Alternatively:

```bash
python app.py
```

Use the execution method supported by the current project implementation.

---

# 13. Expected Intelligence

The project is intended to provide insights related to:

### Customer Behavior

Identify meaningful purchasing patterns.

### Purchasing Communities

Discover groups of customers with similar purchasing behavior.

### Location-Wise Demand

Analyze purchasing patterns across locations.

### Personalized Recommendations

Use sequential purchasing patterns to support relevant product recommendations.

---

# 14. Potential Applications

The project concept can be applied to:

* E-commerce recommendation systems
* Retail analytics
* Inventory planning
* Demand planning
* Personalized marketing
* Customer segmentation
* Regional sales analysis
* Customer behavior intelligence

---

# 15. Evaluation

For future production-level evaluation, appropriate metrics may include:

* Precision
* Recall
* F1-score
* Hit Rate
* NDCG
* Mean Reciprocal Rank (MRR)

Only metrics that are actually implemented and measured should be reported as project results.

---

# 16. Data Privacy and Security

If real customer or transaction data is used:

* Personally identifiable information should be removed or anonymized.
* Private datasets should not be uploaded to public repositories.
* Confidential business information should not be exposed.
* API keys and credentials must never be committed.
* Public or synthetic datasets should be preferred for demonstrations.

---

# 17. Limitations

Potential limitations include:

* Recommendation quality depends on available purchasing history.
* Sparse customer-item interactions may reduce recommendation quality.
* Model performance depends on data quality.
* Large graph datasets may require additional computational resources.
* Sequential recommendation requires meaningful interaction histories.
* Real-world deployment requires additional evaluation and monitoring.

---

# 18. Future Enhancements

Potential improvements include:

* Real-time recommendation inference.
* Advanced customer segmentation.
* Improved demand forecasting.
* Explainable recommendations.
* Interactive analytics dashboard.
* Model comparison and benchmarking.
* REST API integration.
* Cloud deployment.
* Automated model retraining.
* MLOps pipeline integration.
* Real-time retail intelligence.

---

# 19. Learning Outcomes

This project provided practical exposure to:

* Artificial Intelligence
* Machine Learning
* Deep Learning
* Graph Neural Networks
* Transformer architectures
* Recommendation systems
* Sequential modeling
* Retail analytics
* Customer behavior analysis
* Data preprocessing
* Python development

---

# 20. Conclusion

**AI-Based Purchasing Tendency** demonstrates how modern Artificial Intelligence techniques can be applied to a real-world retail intelligence problem.

By combining graph-based relationship learning with sequential recommendation modeling, the project explores a richer understanding of customer purchasing behavior.

The project provides a foundation for future development in recommendation systems, demand analysis, customer intelligence, and AI-driven retail decision support.

---

# 21. Author

## Nikile Eines Dhoni J

**B.Tech – Artificial Intelligence and Data Science**

GitHub:

https://github.com/Dhonijd12345

LinkedIn:

https://www.linkedin.com/in/dhoni-j-7b73b92a2

---

# 22. License

This project is released under the MIT License.

See the `LICENSE` file for complete details.

---

<div align="center">

### 🛒 AI-Based Purchasing Tendency

**Artificial Intelligence • Machine Learning • Graph Learning • Recommendation Systems • Retail Intelligence**

⭐ If you find this project useful, consider starring the repository.

**© 2026 Nikile Eines Dhoni J**

</div>
