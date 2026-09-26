# 🌱 WasteWise AI

> **AI-powered cafeteria waste intelligence for smarter meal planning, waste reduction, and sustainable operations.**

WasteWise AI is a Streamlit-based decision-support application that helps cafeteria administrators **predict food waste, assess operational risk, optimize meal preparation, and analyze waste visually**.

It combines a trained machine-learning regression model with a zero-shot computer-vision scanner and an interactive sustainability dashboard.

## ✨ Highlights

- 📈 **Waste Prediction** — predicts expected food waste in kilograms from operational and contextual inputs.
- 🎯 **Risk Assessment** — classifies predicted waste into actionable risk levels.
- 🍽️ **Meal Preparation Optimization** — estimates a more suitable preparation quantity from predicted waste.
- 🔬 **What-If Simulation** — explore how changing attendance, preparation, or other conditions affects waste.
- 📷 **AI Waste Scanner** — uses CLIP zero-shot image classification to estimate the visual waste category.
- 📊 **Interactive Analytics** — Plotly-based comparisons, impact indicators, and waste intelligence views.
- 🎨 **Appearance Studio** — customizable themes, backgrounds, accent colors, and wallpaper.
- 🧭 **AI Decision Flow** — a clear Predict → Assess → Optimize → Observe → Act workflow.

## 🧠 AI / ML

### Waste prediction

The core prediction model is a supervised regression model trained on cafeteria operational data.

**Model evaluation:**

| Metric | Result |
|---|---:|
| MAE | **1.522 kg** |
| RMSE | **1.947 kg** |
| R² | **0.882** |

The trained model is stored at `models/waste_prediction_model.pkl`.

### Visual waste scanning

The scanner uses **OpenAI CLIP (ViT-B/32)** through Hugging Face Transformers for zero-shot image classification.

It estimates categories such as:

- Rice-based food
- Vegetables
- Bread & bakery
- Fruits
- Meat & protein
- Desserts
- Mixed food
- Other waste

> **Note:** The scanner provides model-based visual category scores. It does **not** measure the exact physical composition or weight percentage of waste.

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │   Streamlit UI       │
                    │      app.py          │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       Waste Prediction   Optimization     Waste Scanner
          Engine             Engine          CLIP / ViT
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │   AI Insights        │
                    │ Risk • Actions •     │
                    │ Impact • Simulation  │
                    └──────────────────────┘
```

## 📁 Project Structure

```text
WasteWise-AI/
├── app.py                         # Streamlit application
├── backend/
│   ├── prediction_engine.py       # Prediction, risk and optimization logic
│   ├── simulator.py               # What-if simulation
│   ├── waste_scanner.py           # CLIP-based image classification
│   └── test_*.py                  # Backend tests
├── data/
│   └── cafeteria_waste.csv        # Training dataset
├── models/
│   └── waste_prediction_model.pkl # Trained ML model
├── training/
│   ├── generate_dataset.py        # Dataset generation
│   └── train_model.py             # Model training
├── requirements.txt
└── .gitignore
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Data | Pandas, NumPy |
| ML | Scikit-learn |
| Visualization | Plotly |
| Computer Vision | Hugging Face Transformers + CLIP |
| Deep Learning | PyTorch + Torchvision |
| Model Persistence | Joblib |
| Language | Python |

## 🚀 Run Locally

### 1. Clone

```bash
git clone https://github.com/Ani2828/WasteWise-AI.git
cd WasteWise-AI
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the dashboard

```bash
streamlit run app.py
```

The application will open at the local Streamlit URL shown in the terminal.

## ☁️ Deployment

WasteWise AI is designed for deployment with **Streamlit Community Cloud**.

Deployment configuration:

- **Repository:** `Ani2828/WasteWise-AI`
- **Branch:** `main`
- **Main file:** `app.py`

After deployment, add the live application URL to this README under **Live Demo**.

## 📌 Use Case

WasteWise AI is designed for environments such as:

- College and university cafeterias
- Corporate cafeterias
- Institutional kitchens
- Food-service operations
- Sustainability programs

The system is intended to support operational decisions by turning historical waste and meal-preparation information into actionable insights.

## ⚠️ Limitations

- Prediction quality depends on the quality and representativeness of the training data.
- The current dataset is a generated/simulated cafeteria dataset rather than a production-scale real-world dataset.
- The visual scanner performs zero-shot image classification; it is not a dedicated waste-object detector or segmentation system.
- The deployed application may take longer to start the first time because the computer-vision model and its dependencies need to initialize.

## 🔮 Future Improvements

- Connect to live cafeteria/POS attendance data.
- Add time-series forecasting for weekly and monthly waste.
- Train the vision component on a domain-specific food-waste dataset.
- Add object detection and segmentation for mixed waste.
- Add historical dashboards and downloadable sustainability reports.
- Add database-backed multi-cafeteria analytics.
- Introduce automated alerts for high-risk waste periods.

## 📄 License

This project is released under the MIT License.

---

**WasteWise AI — Predict less waste. Plan smarter. Operate sustainably.** 🌱
