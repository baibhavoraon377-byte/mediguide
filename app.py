"""
app.py — MediSafe Advisor · Clean White Clinical UI
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from components.utils import load_css, BODY_SVG

st.set_page_config(
    page_title="MediSafe Advisor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(load_css(), unsafe_allow_html=True)

# ── SIDEBAR NAV ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:24px 16px 16px;border-bottom:1px solid rgba(0,0,0,0.05);margin-bottom:8px;">
      <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#0fa76e;margin-bottom:4px;">MediSafe</div>
      <div style="font-size:20px;font-weight:600;color:#0d0d0d;letter-spacing:-0.4px;">Advisor</div>
    </div>
    """, unsafe_allow_html=True)
    nav_items = [
        ("🏠","Home","app"),("🔬","Symptom Checker","pages/1_Symptom_Checker"),
        ("📖","Disease Lookup","pages/2_Disease_Lookup"),
        ("📊","Drug Safety","pages/3_Drug_Safety"),("ℹ️","About","pages/4_About"),
    ]
    for icon, label, _ in nav_items:
        active = " active" if label == "Home" else ""
        st.markdown(f'<div class="sidebar-nav-item{active}"><span class="sidebar-nav-icon">{icon}</span>{label}</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-top:24px;padding:0 8px;">
      <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#888;margin-bottom:12px;">Model Info</div>
      <div style="font-size:14px;color:#666;line-height:1.9;">🌲 Random Forest · 150 trees<br>🎯 CV Accuracy: 100%<br>🩺 131 symptoms · 41 diseases<br>💊 206,383 drug reviews</div>
    </div>""", unsafe_allow_html=True)

# ── TOP NAV ──────────────────────────────────────────────────
st.markdown("""
<div class="top-nav">
  <div class="nav-icon-btn">☰</div>
  <div class="top-nav-brand">Medi<span>Safe</span></div>
  <div class="nav-icon-btn">🔔</div>
</div>""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-section">
  <div class="hero-badge">🤖 ML-Powered · Random Forest</div>
  <div class="hero-title">Check your<br><span class="accent">symptoms</span> safely</div>
  <div class="hero-subtitle">AI-powered analysis that predicts disease, finds medicines, and tells you when to see a doctor.</div>
  <div style="display:flex;justify-content:center;align-items:flex-end;gap:32px;margin-top:8px;flex-wrap:wrap;">
    <div style="position:relative;width:120px;flex-shrink:0;">{BODY_SVG}
      <div class="body-glow-dot head"></div><div class="body-glow-dot chest"></div>
      <div class="body-glow-dot arm-l"></div><div class="body-glow-dot arm-r"></div>
      <div class="body-glow-dot belly"></div><div class="body-glow-dot leg-l"></div><div class="body-glow-dot leg-r"></div>
    </div>
    <div style="text-align:left;max-width:240px;">
      <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#0fa76e;margin-bottom:12px;">How It Works</div>
      <div style="display:flex;flex-direction:column;gap:10px;">
        {"".join([f'<div style="display:flex;align-items:center;gap:10px;font-size:15px;color:#333;"><span style="width:24px;height:24px;background:#d4fae8;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#0fa76e;flex-shrink:0;">{i}</span>{s}</div>' for i,s in enumerate(["Select your symptoms","ML model predicts disease","Get medicine & risk level","Know when to see a doctor"],1)])}
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ── DISCLAIMER ────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer-banner">
  ⚠️ <strong>Important:</strong> This tool is for educational awareness only. Self-medication without proper diagnosis risks antibiotic resistance, drug interactions, and delayed treatment. <strong>Always consult a qualified doctor.</strong>
</div>""", unsafe_allow_html=True)

# ── GENDER ────────────────────────────────────────────────────
st.markdown("""<div class="sec-header"><div class="sec-label">Step 1 · Patient Info</div><div class="sec-title">Choose Gender</div></div>""", unsafe_allow_html=True)
if "gender" not in st.session_state:
    st.session_state.gender = None
g_col1, g_col2 = st.columns(2)
with g_col1:
    mc = "selected" if st.session_state.gender == "male" else ""
    st.markdown(f'<div class="gender-row" style="grid-template-columns:1fr;padding:0 8px;"><div class="gender-card {mc}"><div class="gender-icon">👨</div><div class="gender-name">Male</div></div></div>', unsafe_allow_html=True)
    if st.button("Select Male", key="btn_male", use_container_width=True): st.session_state.gender = "male"
with g_col2:
    fc = "selected" if st.session_state.gender == "female" else ""
    st.markdown(f'<div class="gender-row" style="grid-template-columns:1fr;padding:0 8px;"><div class="gender-card {fc}"><div class="gender-icon">👩</div><div class="gender-name">Female</div></div></div>', unsafe_allow_html=True)
    if st.button("Select Female", key="btn_female", use_container_width=True): st.session_state.gender = "female"
if st.session_state.gender:
    st.markdown(f'<div style="text-align:center;padding:8px;"><span class="badge">✓ {st.session_state.gender.title()} selected</span></div>', unsafe_allow_html=True)

# ── TYPE ──────────────────────────────────────────────────────
st.markdown("""
<div class="sec-header"><div class="sec-label">Step 2 · Analysis Mode</div><div class="sec-title">Choose Type</div></div>
<div class="type-row">
  <div class="type-card selected"><div class="type-icon">📋</div><div class="type-name">Standard</div><div class="type-sub">Step-by-step symptom selection</div></div>
  <div class="type-card selected"><div class="type-icon">🤖</div><div class="type-name">Smart ML</div><div class="type-sub">Random Forest with smart analysis</div></div>
</div>""", unsafe_allow_html=True)

# ── STATS ─────────────────────────────────────────────────────
st.markdown("""<div class="sec-header" style="padding-bottom:8px;"><div class="sec-label">Dataset Overview</div></div>""", unsafe_allow_html=True)
stats = [("🌲","100%","ML Accuracy"),("💊","1,705","Medications"),("🩺","41","Diseases"),("📊","206K","Drug Reviews"),("🔬","131","Symptom Types"),("🏥","825","Conditions")]
s_cols = st.columns(3)
for i,(icon,val,lbl) in enumerate(stats):
    with s_cols[i%3]:
        st.markdown(f'<div class="metric-box" style="margin-bottom:10px;"><div style="font-size:20px;margin-bottom:4px;">{icon}</div><div class="metric-val" style="font-size:22px;">{val}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

# ── CTA + INFO ────────────────────────────────────────────────
st.markdown("""
<div style="padding:16px 16px 8px;">
  <div style="background:linear-gradient(135deg,rgba(24,226,153,0.08),rgba(24,226,153,0.03));border:1px solid rgba(24,226,153,0.2);border-radius:24px;padding:24px;text-align:center;">
    <div style="font-size:20px;font-weight:600;color:#0d0d0d;margin-bottom:6px;letter-spacing:-0.2px;">Ready to check your symptoms?</div>
    <div style="font-size:15px;color:#666;margin-bottom:20px;">Use the sidebar to navigate between pages.</div>
  </div>
</div>
<div class="scroll-section" style="padding-top:8px;">
  <div class="med-card">
    <div class="badge">💡 Tips</div>
    <div class="card-title">How to get best results</div>
    <div class="card-sub">Navigate to Symptom Checker to select your symptoms. Our Random Forest ML model, trained on 4,920 disease records across 131 symptom types, will predict the most likely conditions and show associated medicines, risk levels, and precautions.</div>
  </div>
  <div class="med-card">
    <div class="badge red">⚠️ Safety First</div>
    <div class="card-title">Always consult a doctor</div>
    <div class="card-sub">Drug selection, dosage, and treatment plans must always be determined by a licensed doctor. Never self-medicate based on AI predictions alone.</div>
    <div class="traffic-light" style="margin-top:12px;">
      <div class="tl-dot green"></div><div class="tl-label">🟢 OTC safe</div>
    </div>
    <div class="traffic-light">
      <div class="tl-dot yellow"></div><div class="tl-label">🟡 Consult pharmacist</div>
    </div>
    <div class="traffic-light">
      <div class="tl-dot red"></div><div class="tl-label">🔴 Doctor required</div>
    </div>
  </div>
  <div style="text-align:center;padding:16px 0 8px;">
    <div style="font-size:14px;color:#666;">Was this helpful?</div>
    <div style="margin-top:12px;display:flex;justify-content:center;gap:16px;">
      <span style="font-size:28px;cursor:pointer;">👍</span>
      <span style="font-size:28px;cursor:pointer;">👎</span>
    </div>
  </div>
</div>
<div class="footer-pad"></div>""", unsafe_allow_html=True)
