# 🌱 WasteWise AI

<p align="center"><strong>AI-powered cafeteria waste intelligence for smarter preparation and sustainable operations.</strong></p>

<p align="center">
<a href="https://wastewise-ai-o.streamlit.app/"><img src="https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Live Demo"></a>
<a href="https://github.com/Ani2828/WasteWise-AI"><img src="https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white" alt="GitHub Repository"></a>
<img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
<img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
</p>

<p align="center"><a href="https://wastewise-ai-o.streamlit.app/"><strong>🚀 Open the Live Demo</strong></a></p>

---

## 📌 Overview

**WasteWise AI** is an interactive AI-assisted decision-support application for cafeteria and institutional food-service operations.

It combines a supervised machine-learning regression model, operational decision logic, scenario simulation, and a zero-shot computer-vision scanner to help users move from cafeteria conditions to practical waste-reduction actions.

### Core workflow

**Predict → Assess → Optimize → Observe → Act**

### Questions the system helps answer

- How much food waste is expected under the current operating conditions?
- What is the current waste-risk level?
- How should meal preparation be adjusted?
- How does a different attendance or preparation plan affect expected waste?
- What food-waste category is visually dominant in an uploaded image?

---

## ✨ Features

| Feature | What it does |
|---|---|
| 📈 **Waste Prediction** | Predicts expected food waste in kilograms from cafeteria operating conditions. |
| 🚦 **Risk Assessment** | Classifies the predicted waste level into an operational risk category. |
| 🍽️ **Meal Optimization** | Evaluates candidate preparation quantities and identifies a lower-waste preparation plan. |
| 🔄 **What-If Simulation** | Lets users test alternative attendance and preparation scenarios. |
| 📷 **AI Waste Scanner** | Uses zero-shot CLIP image classification to estimate the dominant visible waste category. |
| 📊 **Interactive Analytics** | Provides Plotly-based comparisons, impact indicators, and waste intelligence views. |
| 🎨 **Appearance Studio** | Supports customizable themes, backgrounds, accent colors, text colors, and wallpaper. |
| 🧭 **Decision Flow** | Visualizes the Predict → Assess → Optimize → Observe → Act workflow. |

---

## 🧠 AI & Machine Learning

### Waste prediction model

The core model is a supervised regression model trained on cafeteria operational data.

#### Test-set evaluation

| Metric | Result |
|---|---:|
| **MAE** | **1.522 kg** |
| **RMSE** | **1.947 kg** |
| **R²** | **0.882** |

The trained model is persisted at `models/waste_prediction_model.pkl`.

> **Important:** the current training dataset is generated/simulated cafeteria data. These metrics describe performance on the project's test split and should not be interpreted as production performance on real cafeteria operations.

### Meal preparation optimization

The optimization layer evaluates a range of meal-preparation quantities for the current scenario and compares the predicted waste for each candidate.

The workflow is:

1. Calculate a minimum preparation quantity slightly above expected attendance.
2. Evaluate candidate preparation quantities up to the current preparation level.
3. Predict waste for each candidate.
4. Select the candidate with the lowest predicted waste.
5. Report the current plan, optimized plan, predicted waste, and reduction.

### Computer vision waste scanner

The scanner uses:

- **OpenAI CLIP ViT-B/32**
- **Hugging Face Transformers**
- **Zero-shot image classification**

Candidate categories include Rice-Based Food, Vegetables, Bread & Bakery, Fruits, Meat & Protein, Desserts, Mixed Food, and Other.

> **Scanner limitation:** CLIP produces model confidence scores for candidate visual categories. It does **not** measure physical weight, volume, or exact percentage composition of the waste.

---

## 🏗️ Architecture

```text
                         ┌────────────────────────┐
                         │      Streamlit UI      │
                         │         app.py         │
                         └────────────┬───────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
                ▼                     ▼                     ▼
       ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
       │ Waste Prediction│    │  Optimization  │    │  Waste Scanner │
       │     Engine      │    │     Engine     │    │  CLIP ViT-B/32│
       └───────┬────────┘    └───────┬────────┘    └───────┬────────┘
               │                     │                     │
               └─────────────────────┼─────────────────────┘
                                     ▼
                         ┌────────────────────────┐
                         │   AI-assisted Output   │
                         │ Risk • Actions • Impact│
                         │ Simulation • Categories│
                         └────────────────────────┘
```

---

## 📁 Project Structure

```text
WasteWise-AI/
│
├── app.py
├── backend/
│   ├── prediction_engine.py
│   ├── simulator.py
│   ├── waste_scanner.py
│   ├── test_engine.py
│   ├── test_optimizer.py
│   └── test_simulator.py
├── data/
│   └── cafeteria_waste.csv
├── models/
│   └── waste_prediction_model.pkl
├── training/
│   ├── generate_dataset.py
│   └── train_model.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

### Module responsibilities

- **`app.py`** — Streamlit dashboard and user interaction layer.
- **`backend/prediction_engine.py`** — prediction, risk assessment, recommendations, and optimization.
- **`backend/simulator.py`** — what-if scenario calculations.
- **`backend/waste_scanner.py`** — CLIP-based visual classification.
- **`training/generate_dataset.py`** — cafeteria dataset generation.
- **`training/train_model.py`** — model training and persistence.
- **`backend/test_*.py`** — backend validation scripts.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python |
| **Web Application** | Streamlit |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn |
| **Model Persistence** | Joblib |
| **Visualization** | Plotly |
| **Computer Vision** | Hugging Face Transformers + OpenAI CLIP |
| **Deep Learning Runtime** | PyTorch + Torchvision |
| **Image Processing** | Pillow |

---

## 🚀 Run Locally

### Prerequisites

- Python 3.12
- Git
- Internet access for downloading the CLIP model the first time the scanner is used

### 1. Clone

```bash
git clone https://github.com/Ani2828/WasteWise-AI.git
cd WasteWise-AI
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run

```bash
streamlit run app.py
```

---

## ☁️ Deployment

WasteWise AI is deployed with **Streamlit Community Cloud**.

- Repository: `Ani2828/WasteWise-AI`
- Branch: `main`
- Entrypoint: `app.py`

### Live application

**🚀 [Launch WasteWise AI](https://wastewise-ai-o.streamlit.app/)**

---

## 🧪 Testing

The repository includes backend test scripts for the decision logic:

```bash
python backend/test_engine.py
python backend/test_optimizer.py
python backend/test_simulator.py
```

---

## 🎯 Intended Use

WasteWise AI is designed for:

- College and university cafeterias
- Corporate cafeterias
- Institutional kitchens
- Food-service operations
- Sustainability and food-waste reduction programs

It is an **AI-assisted decision-support tool** rather than an autonomous food-production controller.

---

## ⚠️ Limitations

1. **Data realism** — the current cafeteria dataset is generated/simulated rather than collected from a production cafeteria environment.
2. **Generalization** — model performance can change when real-world data distributions differ from the training data.
3. **Vision classification** — the scanner is a zero-shot classifier, not a dedicated food-waste detection or segmentation model.
4. **Optimization assumptions** — recommendations use predicted waste and a small safety buffer above expected attendance; real deployments should validate recommendations against actual demand, food-safety requirements, and service constraints.

---

## 🔮 Future Improvements

- Connect to live cafeteria attendance and POS systems.
- Add weekly and monthly time-series forecasting.
- Train a domain-specific vision model on real food-waste images.
- Add object detection and segmentation for mixed waste.
- Add database-backed multi-cafeteria analytics.
- Add downloadable sustainability reports.
- Add automated high-risk waste alerts.
- Track long-term waste-reduction KPIs.

---

## 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/your-feature
git add .
git commit -m "feat: describe your change"
git push origin feature/your-feature
```

Then open a pull request describing the change and how it was tested.

---

## 🔐 Security

Do not commit API keys, credentials, local environment files, model caches, or other secrets.

The repository's `.gitignore` covers common Python artifacts, virtual environments, environment files, IDE files, caches, logs, and temporary files.

---

## 📄 License

Licensed under the **MIT License**. See [LICENSE](LICENSE) for the complete license text.

---

## 🌱 Project Summary

WasteWise AI brings together **predictive analytics, operational optimization, scenario simulation, and computer vision** in a single cafeteria sustainability workflow.

**Predict less waste. Plan smarter. Operate sustainably.**

