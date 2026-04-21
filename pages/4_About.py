"""
pages/4_About.py — MediSafe White Theme
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.utils import load_css

st.set_page_config(page_title="About · MediSafe", page_icon="ℹ️", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

st.markdown("""
<div class="top-nav">
  <div class="nav-icon-btn">←</div>
  <div class="top-nav-brand">Medi<span>Safe</span> · About</div>
  <div class="nav-icon-btn">ℹ️</div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-section" style="padding:40px 24px 32px;">
  <div class="hero-badge">About This App</div>
  <div class="hero-title" style="font-size:32px;">MediSafe <span class="accent">Advisor</span></div>
  <div class="hero-subtitle" style="font-size:15px;">AI-powered symptom analysis for educational awareness. Always consult a qualified doctor.</div>
</div>""", unsafe_allow_html=True)

st.markdown('<div class="scroll-section">', unsafe_allow_html=True)

# Red banner
st.markdown("""
<div class="red-banner" style="margin:0 0 12px;">
  ⚠️ <strong>Stop — See a doctor immediately</strong> for: chest pain, fever &gt;3 days, blood in stool, breathing difficulty, sudden severe headache.
</div>""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="disclaimer-banner" style="margin:0 0 16px;">
  This tool is for <strong>educational awareness only</strong>. It does not provide medical advice, diagnosis, or treatment. Never self-medicate based on AI predictions.
</div>""", unsafe_allow_html=True)

# Model info
st.markdown("""
<div class="med-card featured">
  <div class="badge">🤖 Model</div>
  <div class="card-title">Random Forest Classifier</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;">
    <div style="background:#f9f9f9;border-radius:12px;padding:14px;">
      <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:6px;">Accuracy</div>
      <div style="font-size:24px;font-weight:600;color:#0fa76e;">100%</div>
    </div>
    <div style="background:#f9f9f9;border-radius:12px;padding:14px;">
      <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:6px;">Trees</div>
      <div style="font-size:24px;font-weight:600;color:#0d0d0d;">150</div>
    </div>
    <div style="background:#f9f9f9;border-radius:12px;padding:14px;">
      <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:6px;">Symptoms</div>
      <div style="font-size:24px;font-weight:600;color:#0d0d0d;">131</div>
    </div>
    <div style="background:#f9f9f9;border-radius:12px;padding:14px;">
      <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:6px;">Diseases</div>
      <div style="font-size:24px;font-weight:600;color:#0d0d0d;">41</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# Traffic light system
st.markdown("""
<div class="med-card">
  <div class="badge">Safety System</div>
  <div class="card-title">Traffic Light Indicators</div>
  <div class="card-sub">All medicine suggestions are rated using this safety system.</div>
  <div style="display:flex;flex-direction:column;gap:12px;margin-top:8px;">
    <div style="display:flex;align-items:center;gap:16px;padding:14px;background:#f0fdf4;border:1px solid rgba(34,197,94,0.2);border-radius:12px;">
      <div class="tl-dot green" style="width:20px;height:20px;background:#22c55e;flex-shrink:0;"></div>
      <div><div style="font-weight:600;color:#16a34a;font-size:15px;">🟢 OTC Safe</div><div style="color:#166534;font-size:14px;margin-top:2px;">Available without prescription. Low risk when used correctly.</div></div>
    </div>
    <div style="display:flex;align-items:center;gap:16px;padding:14px;background:#fffbeb;border:1px solid rgba(245,158,11,0.2);border-radius:12px;">
      <div class="tl-dot yellow" style="width:20px;height:20px;background:#f59e0b;flex-shrink:0;"></div>
      <div><div style="font-weight:600;color:#d97706;font-size:15px;">🟡 Consult Pharmacist</div><div style="color:#92400e;font-size:14px;margin-top:2px;">Ask a pharmacist before purchasing. Moderate caution required.</div></div>
    </div>
    <div style="display:flex;align-items:center;gap:16px;padding:14px;background:#fef2f2;border:1px solid rgba(239,68,68,0.2);border-radius:12px;">
      <div class="tl-dot red" style="width:20px;height:20px;background:#ef4444;flex-shrink:0;"></div>
      <div><div style="font-weight:600;color:#dc2626;font-size:15px;">🔴 Doctor Required</div><div style="color:#991b1b;font-size:14px;margin-top:2px;">Prescription required. Do not self-medicate. Seek medical care.</div></div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# Drug review data
st.markdown("""
<div class="med-card">
  <div class="badge">📊 Dataset</div>
  <div class="card-title">Drug Review Dataset</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px;">
    <div class="metric-box"><div class="metric-val" style="font-size:22px;">206K</div><div class="metric-lbl">Reviews</div></div>
    <div class="metric-box"><div class="metric-val" style="font-size:22px;color:#0fa76e;">65.8%</div><div class="metric-lbl">Safe Drugs</div></div>
    <div class="metric-box"><div class="metric-val" style="font-size:22px;color:#d97706;">22.0%</div><div class="metric-lbl">Risky</div></div>
    <div class="metric-box"><div class="metric-val" style="font-size:22px;color:#d97706;">12.2%</div><div class="metric-lbl">Moderate</div></div>
  </div>
</div>""", unsafe_allow_html=True)

# Disclaimer cards
st.markdown("""
<div class="alert-danger">⛔ <strong>Never self-medicate for high-risk conditions.</strong> Wrong dosage or wrong drug can cause irreversible harm, antibiotic resistance, or masked symptoms that delay critical treatment.</div>
<div class="alert-caution" style="margin-top:8px;">⚠️ <strong>This tool is educational only.</strong> Always confirm any AI prediction with a qualified healthcare professional before taking any medication.</div>
<div class="alert-ok" style="margin-top:8px;">✅ <strong>Prevention is best.</strong> Regular check-ups, early reporting of symptoms, and licensed pharmacist guidance are the safest path to good health.</div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="footer-pad"></div>', unsafe_allow_html=True)
