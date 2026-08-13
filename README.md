# 🛍️ AI-Based Purchasing Tendency

<div align="center">

# 🧠 AI-Based Purchasing Tendency

### AI-Powered Retail Intelligence & Customer Purchase Behavior Analysis

**An intelligent retail analytics platform that uses Graph Neural Networks (GNN) and SASRec Transformer models to analyze customer purchasing behavior, identify purchasing communities, predict location-wise demand, and generate personalized product recommendations.**

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge\&logo=python)
![Artificial Intelligence](https://img.shields.io/badge/AI-Retail%20Intelligence-purple?style=for-the-badge)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Enabled-orange?style=for-the-badge)
![Deep Learning](https://img.shields.io/badge/Deep%20Learning-GNN%20%7C%20SASRec-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Developed by Nikile Eines Dhoni J**
**B.Tech – Artificial Intelligence and Data Science**

</div>

---

## 📖 Table of Contents

* [📌 Project Overview](#-project-overview)
* [🎯 Objectives](#-objectives)
* [❓ Problem Statement](#-problem-statement)
* [💡 Proposed Solution](#-proposed-solution)
* [✨ Key Features](#-key-features)
* [🧠 AI & Machine Learning Approach](#-ai--machine-learning-approach)
* [🏗️ System Architecture](#️-system-architecture)
* [🔄 Project Workflow](#-project-workflow)
* [🛠️ Technology Stack](#️-technology-stack)
* [📂 Project Structure](#-project-structure)
* [⚙️ Installation](#️-installation)
* [▶️ Running the Project](#️-running-the-project)
* [📊 Project Capabilities](#-project-capabilities)
* [📈 Retail Intelligence](#-retail-intelligence)
* [📸 Screenshots](#-screenshots)
* [📑 Project Presentation](#-project-presentation)
* [🔮 Future Enhancements](#-future-enhancements)
* [📚 Learning Outcomes](#-learning-outcomes)
* [📌 Project Information](#-project-information)
* [👨‍💻 Author](#-author)
* [🙏 Acknowledgements](#-acknowledgements)
* [📄 License](#-license)

---

# 📌 Project Overview

**AI-Based Purchasing Tendency** is an AI-powered retail intelligence project designed to analyze customer purchasing behavior and transform transaction patterns into useful business insights.

The platform combines graph-based learning and sequential recommendation techniques to understand relationships between customers, products, purchasing behavior, and retail demand.

The project focuses on four major intelligence capabilities:

* 👥 Customer purchasing behavior analysis
* 🔗 Purchasing community identification
* 📍 Location-wise demand prediction
* 🎯 Personalized product recommendations

The repository implements a retail intelligence architecture using **Graph Neural Networks (GNN)** and **SASRec Transformer models**.

---

# 🎯 Objectives

The major objectives of this project are:

* Analyze historical customer purchasing behavior.
* Discover relationships between customers and products.
* Identify meaningful purchasing communities.
* Understand sequential purchasing patterns.
* Predict demand across different locations.
* Generate personalized product recommendations.
* Provide AI-assisted insights for smarter retail decision-making.
* Build a practical AI solution for retail analytics.

---

# ❓ Problem Statement

Modern retail systems generate large volumes of customer transaction data.

Traditional analytics approaches can identify basic sales patterns, but they may not fully capture:

* Relationships between customers and products.
* Repeated purchasing behavior.
* Sequential purchase patterns.
* Customer communities.
* Location-specific demand.
* Individual product preferences.

Therefore, an intelligent system is required to analyze these complex patterns and convert them into actionable retail intelligence.

---

# 💡 Proposed Solution

This project proposes an AI-driven retail intelligence platform that combines:

### 🕸️ Graph Neural Networks

Graph-based learning can represent relationships between entities such as customers, products, and purchasing interactions.

This allows the system to analyze structural relationships within purchasing data.

### 🤖 SASRec Transformer

SASRec is used to model sequential user-item interactions.

It focuses on the order and context of previous interactions to understand customer purchasing patterns and support personalized recommendation tasks.

### 📊 Retail Analytics

The resulting intelligence can be used to understand:

* Customer behavior
* Product relationships
* Purchasing communities
* Location-wise demand
* Personalized product preferences

---

# ✨ Key Features

### 👥 Customer Behavior Analysis

Analyze purchasing patterns to understand customer interaction with products.

### 🕸️ Purchasing Community Identification

Use graph-based relationships to identify groups of customers with similar purchasing behavior.

### 📍 Location-Wise Demand Prediction

Analyze purchasing behavior according to location to support demand-oriented retail decisions.

### 🎯 Personalized Recommendations

Use sequential purchasing behavior to generate product recommendation insights.

### 🔗 Relationship-Aware Analysis

Graph-based learning helps capture relationships between connected retail entities.

### 📈 Sequential Behavior Modeling

SASRec-based modeling helps understand the order and context of customer interactions.

### 🖥️ Interactive Application

The project includes an application interface through `app.py` together with templates and static resources.

---

# 🧠 AI & Machine Learning Approach

The project combines two important AI approaches.

## 1. Graph Neural Networks — GNN

Graph Neural Networks are suitable for problems where entities are connected through relationships.

For a retail scenario, a graph can represent relationships such as:

```text
Customer
   │
   ├──────── Purchases ────────► Product
   │
   ├──────── Interacts ────────► Category
   │
   └──────── Located In ───────► Location
```

The graph representation allows the model to learn from both:

* Individual entity information
* Relationships between connected entities

---

## 2. SASRec Transformer

Customer purchases can also be represented as sequences:

```text
Customer
   │
   ▼
Product A
   │
   ▼
Product B
   │
   ▼
Product C
   │
   ▼
Next Product Prediction
```

SASRec uses self-attention mechanisms to model sequential interactions and identify relevant purchasing patterns.

---

# 🏗️ System Architecture

```text
                    ┌───────────────────────┐
                    │   Retail Data Input   │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Data Processing     │
                    │ & Feature Preparation │
                    └───────────┬───────────┘
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
      ┌────────────────────┐        ┌────────────────────┐
      │   Graph Learning   │        │ Sequential Learning│
      │       (GNN)        │        │      (SASRec)      │
      └─────────┬──────────┘        └─────────┬──────────┘
                │                             │
                └──────────────┬──────────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │   Retail Intelligence   │
                 └────────────┬─────────────┘
                              │
            ┌─────────────────┼──────────────────┐
            │                 │                  │
            ▼                 ▼                  ▼
      Customer            Demand            Product
      Communities        Prediction       Recommendations
```

---

# 🔄 Project Workflow

```text
1. Collect / Load Retail Data
              │
              ▼
2. Data Preprocessing
              │
              ▼
3. Build Customer–Product Relationships
              │
              ▼
4. Graph Representation
              │
              ▼
5. GNN-Based Learning
              │
              ▼
6. Sequential Purchase Modeling
              │
              ▼
7. SASRec Transformer
              │
              ▼
8. Generate Retail Intelligence
              │
       ┌──────┼────────┐
       ▼      ▼        ▼
   Community Demand  Recommendation
   Analysis  Prediction   Insights
```

---

# 🛠️ Technology Stack

| Category                  | Technology                                  |
| ------------------------- | ------------------------------------------- |
| Programming Language      | Python                                      |
| Artificial Intelligence   | AI / Machine Learning                       |
| Graph Learning            | Graph Neural Networks (GNN)                 |
| Sequential Recommendation | SASRec Transformer                          |
| Deep Learning             | Neural Network / Transformer-based Learning |
| Application               | Python-based application                    |
| Frontend Resources        | HTML Templates / Static Assets              |
| Data                      | Retail / Purchasing Interaction Data        |

> The exact package versions and runtime dependencies are maintained in the project's `requirements.txt`.

---

# 📂 Project Structure

```text
AI-Based-Purchasing-Tendency/
│
├── purchasing tendancy/
│   │
│   ├── app.py
│   ├── requirements.txt
│   ├── run_project.ps1
│   ├── Purchasing Tendency - PPT.pdf
│   │
│   ├── data/
│   │   └── Project data files
│   │
│   ├── models/
│   │   └── AI / ML model files
│   │
│   ├── scripts/
│   │   └── Supporting project scripts
│   │
│   ├── scratch/
│   │   └── Development / experimentation files
│   │
│   ├── templates/
│   │   └── Application HTML templates
│   │
│   ├── utils/
│   │   └── Utility modules
│   │
│   └── static/
│       └── img/
│           └── categories/
│               └── Category images
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Dhonijd12345/AI-Based-Purchasing-Tendency.git
```

## 2. Navigate to the Project

```bash
cd AI-Based-Purchasing-Tendency
```

Then enter the application directory:

```bash
cd "purchasing tendancy"
```

## 3. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

The repository contains a `run_project.ps1` script for the project environment.

On Windows PowerShell:

```powershell
.\run_project.ps1
```

Alternatively, if the application entry point is configured for direct execution:

```bash
python app.py
```

> Use the execution method supported by the current project configuration and dependency setup.

---

# 📊 Project Capabilities

The project is designed around the following retail intelligence capabilities:

| Capability                     | AI Approach                      |
| ------------------------------ | -------------------------------- |
| Customer Behavior Analysis     | GNN / Sequential Modeling        |
| Purchasing Communities         | Graph Neural Networks            |
| Location-Wise Demand           | Retail Pattern Analysis          |
| Product Recommendation         | SASRec Sequential Recommendation |
| Customer–Product Relationships | Graph Representation             |
| Purchase Sequence Modeling     | SASRec Transformer               |

---

# 📈 Retail Intelligence

The platform can support retail decision-making by converting purchasing behavior into AI-driven insights.

### 👥 Customer Intelligence

Understand how customers interact with products and discover groups with related purchasing patterns.

### 📍 Demand Intelligence

Analyze purchasing patterns across locations to support demand-oriented planning.

### 🎯 Recommendation Intelligence

Use previous purchasing sequences to identify products that may be relevant to a customer's future interactions.

### 🔗 Relationship Intelligence

Use graph-based representations to capture connections between customers, products, and purchasing interactions.

---

# 📸 Screenshots

Add project screenshots inside an `assets/` or `screenshots/` directory and update the paths below.

### 🖥️ Application Dashboard

```text
screenshots/dashboard.png
```

Example Markdown:

```markdown
![Application Dashboard](screenshots/dashboard.png)
```

### 📊 Purchasing Analytics

```text
screenshots/analytics.png
```

```markdown
![Purchasing Analytics](screenshots/analytics.png)
```

### 🎯 Recommendation Results

```text
screenshots/recommendations.png
```

```markdown
![Recommendation Results](screenshots/recommendations.png)
```

### 📍 Location-Based Insights

```text
screenshots/location-demand.png
```

```markdown
![Location Demand](screenshots/location-demand.png)
```

> Replace these placeholder paths with the actual screenshot filenames available in your project.

---

# 📑 Project Presentation

The repository includes the project presentation:

```text
Purchasing Tendency - PPT.pdf
```

It can be used to understand the project's presentation, objectives, methodology, and overall concept.

---

# 🔮 Future Enhancements

Potential future improvements include:

* Real-time recommendation updates.
* Advanced customer segmentation.
* Larger-scale graph processing.
* Improved sequential recommendation models.
* Real-time demand forecasting.
* Explainable recommendation results.
* Interactive analytics dashboards.
* Model performance monitoring.
* Cloud deployment.
* REST API integration.
* Advanced visualization of customer-product graphs.
* Continuous model retraining with new purchase data.

---

# 📚 Learning Outcomes

This project provides practical experience in:

* Artificial Intelligence
* Machine Learning
* Deep Learning
* Graph Neural Networks
* Transformer Architecture
* Recommendation Systems
* Sequential Modeling
* Customer Behavior Analysis
* Retail Analytics
* Data Processing
* Python Application Development
* AI-Based Decision Support

---

# 📌 Project Information

| Information          | Details                      |
| -------------------- | ---------------------------- |
| Project Name         | AI-Based Purchasing Tendency |
| Domain               | Artificial Intelligence      |
| Sub-Domain           | Retail Intelligence          |
| Application Area     | Customer & Product Analytics |
| Primary AI Approach  | Graph Neural Networks        |
| Sequential Model     | SASRec Transformer           |
| Programming Language | Python                       |
| Project Type         | AI / ML Application          |
| Version              | v1.0.0                       |
| License              | MIT                          |

---

# 👨‍💻 Author

## Nikile Eines Dhoni J

**B.Tech – Artificial Intelligence and Data Science**

### 🔗 GitHub

https://github.com/Dhonijd12345

### 🔗 LinkedIn

https://www.linkedin.com/in/dhoni-j-7b73b92a2

---

# 🙏 Acknowledgements

I would like to acknowledge the technologies, frameworks, libraries, and learning resources that contributed to the development of this project.

Special appreciation for the AI and open-source communities that make research and practical experimentation in Artificial Intelligence, Graph Learning, and Recommendation Systems accessible to developers and students.

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for complete license information.

---

<div align="center">

## ⭐ Support the Project

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

### Built with Python, Artificial Intelligence & Machine Learning

**© 2026 Nikile Eines Dhoni J**

</div>
