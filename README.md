# 🩺 MediSafe Advisor

**AI-Powered Self-Medication Risk Awareness Tool**  
Deep Navy · Cyan Glow · Medical Grade UI

> ⚠️ Educational tool only. Always consult a qualified healthcare professional.

---

## 📸 UI Reference
Design inspired by the Symptoms Checker app concept (deep navy + cyan glow aesthetic).

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/medisafe-advisor.git
cd medisafe-advisor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

---

## 📁 GitHub Repository Structure

```
medisafe-advisor/
│
├── app.py                          # 🏠 Main landing page (Home)
│
├── pages/
│   ├── 1_Symptom_Checker.py        # 🔬 ML Pipeline: Symptoms → Disease → Medicine
│   ├── 2_Disease_Lookup.py         # 📖 Browse all 41 disease profiles
│   ├── 3_Drug_Safety.py            # 📊 Drug safety explorer (206K reviews)
│   └── 4_About.py                  # ℹ️  About, ML architecture, disclaimer
│
├── components/
│   └── utils.py                    # 🔧 Shared helpers, model loader, constants
│
├── assets/
│   ├── style.css                   # 🎨 Full custom CSS (deep navy theme)
│   └── reference.jpeg              # 📷 UI reference image
│
├── models/
│   ├── rf_model.pkl                # 🌲 Trained Random Forest (150 trees)
│   └── label_encoder.pkl           # 🏷️  Label encoder for 41 disease classes
│
├── data/
│   ├── symptoms_list.json          # 🩺 131 unique symptoms
│   ├── disease_profiles.json       # 🔬 41 disease profiles (desc, prec, severity)
│   ├── dis_to_syms.json            # 🗺️  Disease → symptom mapping
│   ├── cleaned_final_dataset.csv   # 📊 Disease risk dataset (4,920 records)
│   └── final_cleaned_combined_dataset__3_.csv  # 💊 Drug reviews (206,383 records)
│
├── .streamlit/
│   └── config.toml                 # ⚙️  Streamlit theme config (dark navy)
│
├── requirements.txt                # 📦 Python dependencies
├── .gitignore                      # 🚫 Ignore large files / cache
└── README.md                       # 📖 This file
```

---

## 🧠 ML Pipeline

```
User selects symptoms (131 types)
        ↓
Binary feature vector [1 × 131]
        ↓
Random Forest Classifier (150 trees)
  · Trained on 4,920 disease records
  · 5-fold CV accuracy: 100%
        ↓
Probability scores across 41 disease classes
        ↓
Top-5 diseases ranked by confidence %
        ↓
Lookup Table → medicine, risk level, description, precautions
        ↓
Result cards with animated pipeline tracker
```

---

## 🎨 Design System

| Token | Value |
|-------|-------|
| Background | `#0b0f2a` |
| Card | `#1a2050` |
| Accent | `#00d4ff` (cyan glow) |
| Risk High | `#ef4444` |
| Risk Medium | `#fbbf24` |
| Risk Low | `#22d3a0` |
| Font Head | Poppins 800 |
| Font Body | Nunito |

---

## 📊 Datasets

| Dataset | Records | Features |
|---------|---------|---------|
| Drug Safety Reviews | 206,383 | 1,705 drugs · 825 conditions |
| Disease Risk Profiles | 4,920 | 41 diseases · 131 symptoms |

---

## 🏥 Features

- **🔬 Symptom Checker** — Select from 131 symptoms → ML predicts top-5 diseases with confidence %
- **📖 Disease Lookup** — Browse all 41 diseases: description, medicine, risk, precautions
- **📊 Drug Safety Explorer** — Search 206K reviews by condition/drug with Plotly charts
- **🌊 Animated Pipeline** — Visual 5-step pipeline tracker (Input→Model→Predict→Lookup→Result)
- **🧬 Body Map** — Glowing anatomical body diagram with pulsing hot-spot dots
- **⚠️ Risk Alerts** — Contextual danger/caution/ok banners per prediction
- **📱 Mobile-First** — Deep navy UI matching medical app reference design

---

## ⚠️ Disclaimer

This application is for **educational and awareness purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified physician.

---

## 📝 License

MIT License — free to use for educational purposes.
