"""
components/utils.py — MediSafe Advisor v2.0
Shared helpers, model loading, CSS, constants.
CSS is fully inline — zero file I/O, works on Streamlit Cloud.
"""
import numpy as np
import pickle
import json
import os

# ── PATHS ─────────────────────────────────────────────────────────────────────
_HERE     = os.path.dirname(os.path.abspath(__file__))
BASE      = os.path.dirname(_HERE)
MODEL_DIR = os.path.join(BASE, "models")
DATA_DIR  = os.path.join(BASE, "data")

# ── LOOKUP TABLE ──────────────────────────────────────────────────────────────
DISEASE_DRUG_MAP = {
    "gerd":{"drug":"Omeprazole / Dexilant","safety":"safe"},
    "peptic ulcer diseae":{"drug":"Pantoprazole / Protonix","safety":"safe"},
    "aids":{"drug":"Dronabinol (symptom relief)","safety":"moderate"},
    "diabetes":{"drug":"Metformin / Liraglutide","safety":"safe"},
    "gastroenteritis":{"drug":"Ondansetron / ORS","safety":"safe"},
    "bronchial asthma":{"drug":"Salbutamol / Montelukast","safety":"safe"},
    "hypertension":{"drug":"Amlodipine / Propranolol","safety":"safe"},
    "migraine":{"drug":"Sumatriptan / Topiramate","safety":"safe"},
    "malaria":{"drug":"Chloroquine / Malarone","safety":"safe"},
    "hepatitis c":{"drug":"Harvoni / Sofosbuvir","safety":"safe"},
    "tuberculosis":{"drug":"Isoniazid / Rifampin (DOTS)","safety":"safe"},
    "pneumonia":{"drug":"Levofloxacin / Amoxicillin","safety":"safe"},
    "heart attack":{"drug":"Aspirin / Clopidogrel","safety":"risky"},
    "hypothyroidism":{"drug":"Levothyroxine / Synthroid","safety":"safe"},
    "hyperthyroidism":{"drug":"Methimazole / Propranolol","safety":"safe"},
    "arthritis":{"drug":"Diclofenac / Meloxicam","safety":"moderate"},
    "(vertigo) paroymsal  positional vertigo":{"drug":"Meclizine / Antivert","safety":"safe"},
    "acne":{"drug":"Isotretinoin / Doxycycline","safety":"safe"},
    "urinary tract infection":{"drug":"Nitrofurantoin / Ciprofloxacin","safety":"safe"},
    "psoriasis":{"drug":"Apremilast / Adalimumab","safety":"safe"},
    "impetigo":{"drug":"Retapamulin / Mupirocin","safety":"safe"},
    "fungal infection":{"drug":"Miconazole / Fluconazole","safety":"safe"},
    "allergy":{"drug":"Cetirizine / Loratadine","safety":"safe"},
    "chronic cholestasis":{"drug":"Ursodiol / Cholestyramine","safety":"moderate"},
    "drug reaction":{"drug":"Prednisone / Antihistamine","safety":"risky"},
    "dengue":{"drug":"Paracetamol (supportive only)","safety":"safe"},
    "typhoid":{"drug":"Ciprofloxacin / Azithromycin","safety":"safe"},
    "hepatitis a":{"drug":"Supportive care / Vaccination","safety":"safe"},
    "hepatitis b":{"drug":"Tenofovir / Entecavir","safety":"safe"},
    "hepatitis d":{"drug":"Peginterferon alfa-2a","safety":"moderate"},
    "hepatitis e":{"drug":"Ribavirin (supportive)","safety":"moderate"},
    "alcoholic hepatitis":{"drug":"Prednisolone / Pentoxifylline","safety":"risky"},
    "common cold":{"drug":"Paracetamol / Decongestant","safety":"safe"},
    "chicken pox":{"drug":"Acyclovir / Calamine lotion","safety":"safe"},
    "jaundice":{"drug":"Supportive care / Silymarin","safety":"moderate"},
    "dimorphic hemmorhoids(piles)":{"drug":"Docusate / Hydrocortisone cream","safety":"safe"},
    "varicose veins":{"drug":"Compression stockings / Daflon","safety":"safe"},
    "hypoglycemia":{"drug":"Dextrose / Glucagon","safety":"risky"},
    "cervical spondylosis":{"drug":"Ibuprofen / Physiotherapy","safety":"safe"},
    "paralysis (brain hemorrhage)":{"drug":"Physiotherapy / Aspirin (post-acute)","safety":"risky"},
    "osteoarthristis":{"drug":"Acetaminophen / Naproxen","safety":"safe"},
}

RISK_COLORS  = {"high":"#ef4444","medium":"#fbbf24","low":"#22d3a0"}
SAFETY_ICONS = {"safe":"✅","moderate":"⚠️","risky":"❌"}
SAFETY_NOTES = {
    "safe":    "Generally safe when prescribed correctly.",
    "moderate":"Moderate risk — use only under medical supervision.",
    "risky":   "High-risk — ONLY under strict physician oversight.",
}
RISK_EMOJIS = {"high":"🔴","medium":"🟡","low":"🟢"}
RISK_CSS    = {"high":"risk-high","medium":"risk-medium","low":"risk-low"}
CHIP_CSS    = {"high":"red","medium":"orange","low":"green"}
# ── INLINE CSS (new white clinical theme) ────────────────────────────────────
_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'
)

_CSS = """
*,*::before,*::after{overflow-wrap:break-word!important;word-break:break-word!important;box-sizing:border-box!important;}
html,body{overflow-x:hidden!important;max-width:100vw!important;}
:root{
  --white:#ffffff;--black:#0d0d0d;--text-primary:#0d0d0d;--text-secondary:#333333;--text-tertiary:#666666;
  --text-placeholder:#888888;--accent:#18E299;--accent-bg:#d4fae8;--accent-text:#0fa76e;
  --border-default:rgba(0,0,0,0.05);--border-interactive:rgba(0,0,0,0.08);
  --shadow-card:rgba(0,0,0,0.03) 0px 2px 4px;--shadow-btn:rgba(0,0,0,0.06) 0px 1px 2px;
  --radius-card:16px;--radius-featured:24px;--radius-pill:9999px;
  --font:'Inter',-apple-system,sans-serif;
}
html,body,[class*="css"]{font-family:var(--font)!important;background:#ffffff!important;color:var(--text-primary)!important;}
#MainMenu,footer,header,.stDeployButton,[data-testid="stToolbar"],[data-testid="stDecoration"],.css-1rs6os,.css-17ziqus{display:none!important;}
.main .block-container{padding:0!important;max-width:100%!important;overflow-x:hidden!important;}
.stApp{background:#ffffff!important;min-height:100vh;overflow-x:hidden!important;}
.block-container,[data-testid="stAppViewContainer"],section[data-testid="stSidebarContent"]{overflow-x:hidden!important;}
[data-testid="stSidebar"]{background:#ffffff!important;border-right:1px solid var(--border-default)!important;padding-top:0!important;}
[data-testid="stSidebar"]>div{padding:0!important;}
.top-nav{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;background:rgba(255,255,255,0.96);backdrop-filter:blur(12px);border-bottom:1px solid var(--border-default);position:sticky;top:0;z-index:100;width:100%;}
.top-nav-brand{font-size:15px;font-weight:600;color:var(--text-primary);letter-spacing:-0.15px;}
.top-nav-brand span{color:var(--accent);}
.nav-icon-btn{width:36px;height:36px;background:transparent;border:1px solid var(--border-interactive);border-radius:var(--radius-card);display:flex;align-items:center;justify-content:center;cursor:pointer;color:var(--text-primary);font-size:1rem;transition:all 0.2s;flex-shrink:0;}
.nav-icon-btn:hover{border-color:var(--accent);color:var(--accent);}
.hero-section{background:linear-gradient(160deg,rgba(24,226,153,0.07) 0%,rgba(24,226,153,0.02) 40%,#ffffff 80%);padding:48px 24px 40px;text-align:center;position:relative;overflow:hidden;}
.hero-badge{display:inline-flex;align-items:center;gap:6px;background:var(--accent-bg);color:var(--accent-text);font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;padding:4px 12px;border-radius:var(--radius-pill);margin-bottom:20px;}
.hero-title{font-size:40px;font-weight:600;line-height:1.10;letter-spacing:-0.8px;color:var(--text-primary);margin-bottom:16px;}
.hero-title .accent{color:var(--accent);}
.hero-subtitle{font-size:18px;font-weight:400;color:var(--text-tertiary);line-height:1.5;max-width:400px;margin:0 auto 32px;}
.disclaimer-banner{margin:0 16px 8px;background:#fff8e1;border:1px solid rgba(245,158,11,0.3);border-left:3px solid #f59e0b;border-radius:var(--radius-card);padding:12px 16px;font-size:14px;color:#92400e;line-height:1.5;}
.red-banner{margin:0 16px 12px;background:#fef2f2;border:1px solid rgba(239,68,68,0.25);border-left:3px solid #ef4444;border-radius:var(--radius-card);padding:14px 16px;font-size:15px;font-weight:500;color:#991b1b;line-height:1.5;}
.lockout-screen{margin:16px;background:#fef2f2;border:2px solid rgba(239,68,68,0.3);border-radius:var(--radius-featured);padding:32px 24px;text-align:center;}
.lockout-screen .lockout-icon{font-size:48px;margin-bottom:16px;}
.lockout-screen .lockout-title{font-size:24px;font-weight:600;color:#dc2626;margin-bottom:8px;letter-spacing:-0.24px;}
.lockout-screen .lockout-sub{font-size:16px;color:#666;line-height:1.5;margin-bottom:24px;}
.sec-header{padding:32px 24px 16px;}
.sec-label{font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:var(--text-tertiary);margin-bottom:6px;}
.sec-title{font-size:24px;font-weight:500;line-height:1.30;letter-spacing:-0.24px;color:var(--text-primary);}
.sec-sub{font-size:16px;color:var(--text-tertiary);margin-top:4px;line-height:1.5;}
.med-card{background:#ffffff;border:1px solid var(--border-default);border-radius:var(--radius-card);padding:24px;margin:0 16px 12px;box-shadow:var(--shadow-card);transition:border-color 0.2s;position:relative;}
.med-card:hover{border-color:var(--border-interactive);}
.med-card.featured{border-radius:var(--radius-featured);padding:28px;}
.med-card.safety-green{border-color:rgba(24,226,153,0.3);}
.med-card.safety-yellow{border-color:rgba(245,158,11,0.3);}
.med-card.safety-red{border-color:rgba(239,68,68,0.3);}
.card-title{font-size:20px;font-weight:600;letter-spacing:-0.2px;line-height:1.30;color:var(--text-primary);margin-bottom:6px;}
.card-sub{font-size:16px;color:var(--text-tertiary);line-height:1.5;margin-bottom:16px;}
.card-footer-note{font-size:13px;color:var(--text-tertiary);margin-top:16px;padding-top:12px;border-top:1px solid var(--border-default);}
.badge{display:inline-flex;align-items:center;gap:5px;background:var(--accent-bg);color:var(--accent-text);font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;padding:4px 12px;border-radius:var(--radius-pill);margin-bottom:12px;}
.badge.yellow{background:#fef3c7;color:#92400e;}
.badge.red{background:#fee2e2;color:#991b1b;}
.badge.gray{background:#f3f4f6;color:#374151;}
.traffic-light{display:flex;align-items:center;gap:8px;margin:8px 0;}
.tl-dot{width:12px;height:12px;border-radius:50%;flex-shrink:0;}
.tl-dot.green{background:#22c55e;}
.tl-dot.yellow{background:#f59e0b;}
.tl-dot.red{background:#ef4444;}
.tl-label{font-size:15px;font-weight:500;color:var(--text-secondary);}
.safety-ring-wrap{display:flex;align-items:center;gap:16px;margin:12px 0;}
.safety-ring{width:56px;height:56px;border-radius:50%;border:3px solid;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:600;flex-shrink:0;}
.safety-ring.green{border-color:#22c55e;color:#22c55e;background:rgba(34,197,94,0.06);}
.safety-ring.yellow{border-color:#f59e0b;color:#f59e0b;background:rgba(245,158,11,0.06);}
.safety-ring.red{border-color:#ef4444;color:#ef4444;background:rgba(239,68,68,0.06);}
.risk-badge{display:inline-flex;align-items:center;gap:6px;padding:5px 14px;border-radius:var(--radius-pill);font-size:13px;font-weight:500;letter-spacing:0.3px;}
.risk-high{background:#fee2e2;color:#dc2626;}
.risk-medium{background:#fef3c7;color:#92400e;}
.risk-low{background:var(--accent-bg);color:var(--accent-text);}
.stTextInput>div>div>input{background:#ffffff!important;border:1px solid var(--border-interactive)!important;border-radius:var(--radius-pill)!important;color:var(--text-primary)!important;padding:10px 20px!important;font-family:var(--font)!important;font-size:16px!important;transition:border-color 0.2s,box-shadow 0.2s!important;}
.stTextInput>div>div>input:focus{border-color:var(--accent)!important;box-shadow:0 0 0 3px rgba(24,226,153,0.15)!important;outline:none!important;}
.stTextInput>div>div>input::placeholder{color:var(--text-placeholder)!important;}
div[data-testid="stMultiSelect"]>div{background:#ffffff!important;border:1px solid var(--border-interactive)!important;border-radius:16px!important;}
div[data-testid="stMultiSelect"]>div:focus-within{border-color:var(--accent)!important;box-shadow:0 0 0 3px rgba(24,226,153,0.12)!important;}
.stMultiSelect [data-baseweb="tag"]{background:var(--accent-bg)!important;border:none!important;border-radius:var(--radius-pill)!important;color:var(--accent-text)!important;font-family:var(--font)!important;font-size:13px!important;}
div[data-testid="stSelectbox"]>div>div{background:#ffffff!important;border:1px solid var(--border-interactive)!important;border-radius:var(--radius-pill)!important;color:var(--text-primary)!important;}
.stButton>button{background:var(--black)!important;color:#ffffff!important;border:none!important;border-radius:var(--radius-pill)!important;padding:8px 24px!important;font-family:var(--font)!important;font-weight:500!important;font-size:15px!important;width:100%!important;transition:all 0.2s!important;box-shadow:var(--shadow-btn)!important;}
.stButton>button:hover{background:#1a1a1a!important;transform:translateY(-1px)!important;}
.btn-secondary{display:inline-flex;align-items:center;justify-content:center;background:#ffffff;color:var(--text-primary);border:1px solid var(--border-interactive);border-radius:var(--radius-pill);padding:4.5px 12px;font-family:var(--font);font-weight:500;font-size:15px;cursor:pointer;transition:all 0.2s;text-decoration:none;}
.btn-secondary:hover{border-color:var(--accent);color:var(--accent);}
.btn-primary{display:inline-flex;align-items:center;justify-content:center;background:var(--black);color:#ffffff;border:none;border-radius:var(--radius-pill);padding:8px 24px;font-family:var(--font);font-weight:500;font-size:15px;cursor:pointer;transition:all 0.2s;box-shadow:var(--shadow-btn);text-decoration:none;}
.btn-primary:hover{background:#1a1a1a;transform:translateY(-1px);}
.btn-accent{display:inline-flex;align-items:center;justify-content:center;background:var(--accent);color:var(--black);border:none;border-radius:var(--radius-pill);padding:8px 24px;font-family:var(--font);font-weight:600;font-size:15px;cursor:pointer;transition:all 0.2s;box-shadow:var(--shadow-btn);}
.btn-accent:hover{opacity:0.9;transform:translateY(-1px);}
.metric-box{background:#ffffff;border:1px solid var(--border-default);border-radius:var(--radius-card);padding:20px 16px;text-align:center;box-shadow:var(--shadow-card);}
.metric-val{font-size:28px;font-weight:600;line-height:1.2;color:var(--text-primary);letter-spacing:-0.5px;}
.metric-lbl{font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:var(--text-tertiary);margin-top:4px;}
.alert-danger{background:#fef2f2;border:1px solid rgba(239,68,68,0.2);border-left:3px solid #ef4444;border-radius:var(--radius-card);padding:14px 16px;color:#991b1b;font-size:15px;line-height:1.5;margin:8px 0;}
.alert-caution{background:#fffbeb;border:1px solid rgba(245,158,11,0.2);border-left:3px solid #f59e0b;border-radius:var(--radius-card);padding:14px 16px;color:#78350f;font-size:15px;line-height:1.5;margin:8px 0;}
.alert-ok{background:#f0fdf4;border:1px solid rgba(34,197,94,0.2);border-left:3px solid #22c55e;border-radius:var(--radius-card);padding:14px 16px;color:#14532d;font-size:15px;line-height:1.5;margin:8px 0;}
.chat-bubble-user{background:var(--black);color:#ffffff;padding:12px 16px;border-radius:18px 18px 4px 18px;font-size:16px;line-height:1.5;max-width:80%;margin-left:auto;margin-bottom:8px;}
.chat-bubble-agent{background:#f9f9f9;border:1px solid var(--border-default);color:var(--text-primary);padding:12px 16px;border-radius:18px 18px 18px 4px;font-size:16px;line-height:1.5;max-width:85%;margin-right:auto;margin-bottom:8px;}
.chat-disclaimer{background:#fef3c7;border:1px solid rgba(245,158,11,0.25);border-radius:var(--radius-card);padding:10px 14px;font-size:13px;color:#78350f;margin:0 16px 12px;line-height:1.4;}
.body-svg-container{position:relative;width:130px;filter:drop-shadow(0 2px 8px rgba(0,0,0,0.08));}
.body-svg-container svg{width:100%;height:auto;}
.body-glow-dot{position:absolute;width:14px;height:14px;background:var(--accent);border-radius:50%;border:2.5px solid #ffffff;box-shadow:0 0 0 3px rgba(24,226,153,0.2);cursor:pointer;animation:pulse-dot 2.5s ease-in-out infinite;transition:transform 0.2s;}
.body-glow-dot:hover{transform:scale(1.3)!important;}
.body-glow-dot.head{top:4%;left:50%;transform:translateX(-50%);}
.body-glow-dot.chest{top:32%;left:50%;transform:translateX(-50%);}
.body-glow-dot.arm-l{top:38%;left:10%;}
.body-glow-dot.arm-r{top:38%;right:10%;}
.body-glow-dot.belly{top:54%;left:50%;transform:translateX(-50%);}
.body-glow-dot.leg-l{top:74%;left:30%;}
.body-glow-dot.leg-r{top:74%;right:30%;}
@keyframes pulse-dot{0%,100%{box-shadow:0 0 0 3px rgba(24,226,153,0.2);}50%{box-shadow:0 0 0 6px rgba(24,226,153,0.1);}}
.pipeline-track{display:flex;align-items:center;padding:16px 20px;gap:0;overflow-x:auto;scrollbar-width:none;width:100%;border-bottom:1px solid var(--border-default);}
.pipeline-track::-webkit-scrollbar{display:none;}
.pipe-node{display:flex;flex-direction:column;align-items:center;gap:6px;flex:1;min-width:56px;}
.pipe-orb{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:600;transition:all 0.3s;}
.pipe-orb.idle{background:#f9fafb;border:1.5px solid var(--border-interactive);color:var(--text-tertiary);}
.pipe-orb.active{background:var(--black);border:1.5px solid var(--black);color:#ffffff;}
.pipe-orb.done{background:var(--accent-bg);border:1.5px solid var(--accent);color:var(--accent-text);}
.pipe-text{font-size:10px;font-weight:500;letter-spacing:0.5px;text-transform:uppercase;color:var(--text-tertiary);text-align:center;}
.pipe-text.active{color:var(--text-primary);}
.pipe-text.done{color:var(--accent-text);}
.pipe-connector{flex-shrink:0;height:1px;width:20px;background:var(--border-default);margin-bottom:22px;}
.pipe-connector.done{background:var(--accent);}
.gender-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:0 16px 16px;}
.gender-card{background:#ffffff;border:1.5px solid var(--border-interactive);border-radius:var(--radius-card);padding:20px 16px;text-align:center;cursor:pointer;transition:all 0.2s;box-shadow:var(--shadow-card);}
.gender-card:hover{border-color:var(--accent);}
.gender-card.selected{border-color:var(--accent);background:rgba(24,226,153,0.04);}
.gender-icon{font-size:32px;margin-bottom:8px;}
.gender-name{font-size:15px;font-weight:500;color:var(--text-primary);}
.type-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:0 16px 16px;}
.type-card{background:#ffffff;border:1.5px solid var(--border-interactive);border-radius:var(--radius-card);padding:20px 16px;text-align:center;cursor:pointer;transition:all 0.2s;box-shadow:var(--shadow-card);}
.type-card:hover{border-color:var(--accent);}
.type-card.selected{border-color:var(--black);background:#fafafa;}
.type-icon{font-size:28px;margin-bottom:8px;}
.type-name{font-size:15px;font-weight:600;color:var(--text-primary);}
.type-sub{font-size:13px;color:var(--text-tertiary);margin-top:4px;line-height:1.4;}
.sidebar-nav-item{display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:var(--radius-card);margin-bottom:4px;cursor:pointer;transition:all 0.15s;font-size:15px;font-weight:500;color:var(--text-tertiary);}
.sidebar-nav-item:hover{background:#f9f9f9;color:var(--text-primary);}
.sidebar-nav-item.active{background:var(--accent-bg);color:var(--accent-text);}
.sidebar-nav-icon{font-size:18px;}
.padded{padding:0 16px;}
.footer-pad{height:32px;}
.scroll-section{padding:0 16px;}
.stMarkdown p{margin:0;}
label[data-testid="stWidgetLabel"]{color:var(--text-secondary)!important;font-family:var(--font)!important;font-size:15px!important;}
div[data-testid="column"]{padding:0 6px!important;}
.element-container{margin-bottom:0!important;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:var(--border-interactive);border-radius:4px;}
::-webkit-scrollbar-thumb:hover{background:var(--accent);}
"""



def load_css() -> str:
    """Return inline CSS + Google Fonts."""
    return _FONTS + "<style>" + _CSS + "</style>"


# ── MODEL LOADING ─────────────────────────────────────────────────────────────
def load_model():
    import streamlit as st

    @st.cache_resource
    def _load():
        with open(os.path.join(MODEL_DIR, "rf_model.pkl"), "rb") as f:
            clf = pickle.load(f)
        with open(os.path.join(MODEL_DIR, "label_encoder.pkl"), "rb") as f:
            le = pickle.load(f)
        with open(os.path.join(DATA_DIR, "symptoms_list.json")) as f:
            all_syms = json.load(f)
        with open(os.path.join(DATA_DIR, "disease_profiles.json")) as f:
            profiles = json.load(f)
        with open(os.path.join(DATA_DIR, "dis_to_syms.json")) as f:
            dis_syms = json.load(f)
        sym_idx = {s: i for i, s in enumerate(all_syms)}
        return clf, le, all_syms, sym_idx, profiles, dis_syms

    return _load()


# ── PREDICTION ────────────────────────────────────────────────────────────────
def predict_diseases(selected_syms, clf, le, all_syms, sym_idx, top_n=5):
    vec = np.zeros((1, len(all_syms)), dtype=np.int8)
    for s in selected_syms:
        if s in sym_idx:
            vec[0, sym_idx[s]] = 1
    proba   = clf.predict_proba(vec)[0]
    top_idx = np.argsort(proba)[::-1][:top_n]
    return [(le.classes_[i], float(proba[i])) for i in top_idx if proba[i] > 0]


# ── PIPELINE BANNER ───────────────────────────────────────────────────────────
PIPE_STEPS = ["User Input", "ML Model", "Predict", "Lookup", "Results"]


def pipeline_html(stage: int) -> str:
    parts = []
    for i, label in enumerate(PIPE_STEPS):
        if i < stage:
            cls, icon = "done", "✓"
        elif i == stage:
            cls, icon = "active", str(i + 1)
        else:
            cls, icon = "idle", str(i + 1)
        parts.append(
            f'<div class="pipe-node">'
            f'<div class="pipe-orb {cls}">{icon}</div>'
            f'<div class="pipe-text {cls}">{label}</div>'
            f'</div>'
        )
        if i < len(PIPE_STEPS) - 1:
            conn = "done" if i < stage else ("active" if i == stage else "")
            parts.append(f'<div class="pipe-connector {conn}"></div>')
    return '<div class="pipeline-track">' + "".join(parts) + "</div>"


# ── BODY SVG ──────────────────────────────────────────────────────────────────
BODY_SVG = (
    '<svg viewBox="0 0 120 300" fill="none" xmlns="http://www.w3.org/2000/svg">'
    "<defs>"
    '<linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">'
    '<stop offset="0%" style="stop-color:#e8f8f0;stop-opacity:1"/>'
    '<stop offset="100%" style="stop-color:#d4fae8;stop-opacity:1"/></linearGradient>'
    '<linearGradient id="bodyStroke" x1="0%" y1="0%" x2="100%" y2="0%">'
    '<stop offset="0%" style="stop-color:#18E299;stop-opacity:0.6"/>'
    '<stop offset="100%" style="stop-color:#0fa76e;stop-opacity:0.4"/></linearGradient>'
    "</defs>"
    '<ellipse cx="60" cy="22" rx="16" ry="18" fill="url(#bodyGrad)" stroke="url(#bodyStroke)" stroke-width="1.5"/>'
    '<rect x="53" y="37" width="14" height="10" fill="url(#bodyGrad)" stroke="url(#bodyStroke)" stroke-width="1"/>'
    '<path d="M30 47 Q25 60 26 100 Q27 120 30 130 L90 130 Q93 120 94 100 Q95 60 90 47 Z" fill="url(#bodyGrad)" stroke="url(#bodyStroke)" stroke-width="1.5"/>'
    '<path d="M30 52 Q18 70 15 100 Q14 110 18 115 L26 112 Q28 100 30 80 Q32 65 34 55 Z" fill="url(#bodyGrad)" stroke="url(#bodyStroke)" stroke-width="1.2"/>'
    '<path d="M90 52 Q102 70 105 100 Q106 110 102 115 L94 112 Q92 100 90 80 Q88 65 86 55 Z" fill="url(#bodyGrad)" stroke="url(#bodyStroke)" stroke-width="1.2"/>'
    '<path d="M37 130 Q33 170 32 210 Q31 230 34 245 L46 245 Q50 230 52 210 Q54 170 53 130 Z" fill="url(#bodyGrad)" stroke="url(#bodyStroke)" stroke-width="1.2"/>'
    '<path d="M83 130 Q87 170 88 210 Q89 230 86 245 L74 245 Q70 230 68 210 Q66 170 67 130 Z" fill="url(#bodyGrad)" stroke="url(#bodyStroke)" stroke-width="1.2"/>'
    '<line x1="60" y1="50" x2="60" y2="120" stroke="rgba(15,167,110,0.15)" stroke-width="1" stroke-dasharray="4,4"/>'
    '<line x1="40" y1="65" x2="80" y2="65" stroke="rgba(15,167,110,0.10)" stroke-width="1"/>'
    '<line x1="38" y1="78" x2="82" y2="78" stroke="rgba(15,167,110,0.10)" stroke-width="1"/>'
    '<line x1="36" y1="91" x2="84" y2="91" stroke="rgba(15,167,110,0.10)" stroke-width="1"/>'
    "</svg>"
)

BODY_SVG = (
    '<svg viewBox="0 0 120 300" fill="none" xmlns="http://www.w3.org/2000/svg">'
    "<defs>"
    '<filter id="bodyGlow"><feGaussianBlur stdDeviation="3" result="blur"/>'
    "<feMerge><feMergeNode in=\"blur\"/><feMergeNode in=\"SourceGraphic\"/></feMerge></filter>"
    '<linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">'
    '<stop offset="0%" style="stop-color:#1a4a8a;stop-opacity:1"/>'
    '<stop offset="100%" style="stop-color:#0e2a5a;stop-opacity:1"/></linearGradient>'
    '<linearGradient id="glowEdge" x1="0%" y1="0%" x2="100%" y2="0%">'
    '<stop offset="0%" style="stop-color:#00d4ff;stop-opacity:0.8"/>'
    '<stop offset="50%" style="stop-color:#4de8ff;stop-opacity:0.4"/>'
    '<stop offset="100%" style="stop-color:#00d4ff;stop-opacity:0.8"/></linearGradient>'
    "</defs>"
    '<ellipse cx="60" cy="22" rx="16" ry="18" fill="url(#bodyGrad)" stroke="url(#glowEdge)" stroke-width="1.5" filter="url(#bodyGlow)"/>'
    '<rect x="53" y="37" width="14" height="10" fill="url(#bodyGrad)" stroke="url(#glowEdge)" stroke-width="1"/>'
    '<path d="M30 47 Q25 60 26 100 Q27 120 30 130 L90 130 Q93 120 94 100 Q95 60 90 47 Z" fill="url(#bodyGrad)" stroke="url(#glowEdge)" stroke-width="1.5" filter="url(#bodyGlow)"/>'
    '<path d="M30 52 Q18 70 15 100 Q14 110 18 115 L26 112 Q28 100 30 80 Q32 65 34 55 Z" fill="url(#bodyGrad)" stroke="url(#glowEdge)" stroke-width="1.2"/>'
    '<path d="M90 52 Q102 70 105 100 Q106 110 102 115 L94 112 Q92 100 90 80 Q88 65 86 55 Z" fill="url(#bodyGrad)" stroke="url(#glowEdge)" stroke-width="1.2"/>'
    '<path d="M37 130 Q33 170 32 210 Q31 230 34 245 L46 245 Q50 230 52 210 Q54 170 53 130 Z" fill="url(#bodyGrad)" stroke="url(#glowEdge)" stroke-width="1.2"/>'
    '<path d="M83 130 Q87 170 88 210 Q89 230 86 245 L74 245 Q70 230 68 210 Q66 170 67 130 Z" fill="url(#bodyGrad)" stroke="url(#glowEdge)" stroke-width="1.2"/>'
    '<line x1="60" y1="50" x2="60" y2="120" stroke="rgba(0,212,255,0.15)" stroke-width="1" stroke-dasharray="4,4"/>'
    '<line x1="40" y1="65" x2="80" y2="65" stroke="rgba(0,212,255,0.10)" stroke-width="1"/>'
    '<line x1="38" y1="78" x2="82" y2="78" stroke="rgba(0,212,255,0.10)" stroke-width="1"/>'
    '<line x1="36" y1="91" x2="84" y2="91" stroke="rgba(0,212,255,0.10)" stroke-width="1"/>'
    "</svg>"
)


# ── FORMAT HELPERS ────────────────────────────────────────────────────────────
def fmt_sym(s: str) -> str:
    return s.replace("_", " ").title()
