"""
pages/2_Disease_Lookup.py — MediSafe White Theme
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.utils import (
    load_css, load_model, DISEASE_DRUG_MAP,
    RISK_COLORS, SAFETY_ICONS, SAFETY_NOTES, RISK_CSS, RISK_EMOJIS
)

st.set_page_config(page_title="Disease Lookup · MediSafe", page_icon="📖", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

clf, le, all_syms, sym_idx, disease_profiles, dis_to_syms = load_model()

st.markdown("""
<div class="top-nav">
  <div class="nav-icon-btn">←</div>
  <div class="top-nav-brand">Medi<span>Safe</span> · Disease Lookup</div>
  <div class="nav-icon-btn">🔍</div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="sec-header">
  <div class="sec-label">Reference Database</div>
  <div class="sec-title">Disease Risk &amp; Medicine</div>
  <div class="sec-sub">Browse all 41 disease profiles with clinical info.</div>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    sel_dis = st.selectbox("Select Disease", sorted([d.title() for d in disease_profiles.keys()]), label_visibility="visible")
with col2:
    risk_filter = st.selectbox("Risk Filter", ["All", "High", "Medium", "Low"])

if risk_filter != "All":
    valid_diseases = [d.title() for d, p in disease_profiles.items() if p.get("risk_level", "").lower() == risk_filter.lower()]
    if sel_dis not in valid_diseases and valid_diseases:
        sel_dis = valid_diseases[0]

match_key = next((k for k in disease_profiles if k.title() == sel_dis or k == sel_dis.lower()), None)
if not match_key:
    st.warning("Disease not found in database.")
    st.stop()

profile   = disease_profiles[match_key]
drug_info = DISEASE_DRUG_MAP.get(match_key, {"drug": "Consult a doctor", "safety": "unknown"})
risk      = profile.get("risk_level", "unknown")
severity  = profile.get("severity_score", 0)
desc      = profile.get("description", "No description available.")
precs     = profile.get("precautions", [])
drug_name = drug_info["drug"]
drug_sf   = drug_info["safety"]
rc        = RISK_COLORS.get(risk, "#888")
sp        = min(100, int((severity / 77) * 100))
risk_cls  = RISK_CSS.get(risk, "risk-low")
syms_for  = dis_to_syms.get(match_key, [])
ring_cls  = {"high": "red", "medium": "yellow", "low": "green"}.get(risk, "green")
risk_color = {"high": "#dc2626", "medium": "#d97706", "low": "#0fa76e"}.get(risk, "#0fa76e")

st.markdown('<div class="scroll-section">', unsafe_allow_html=True)

# Header card
st.markdown(f"""
<div class="med-card featured {{'safety-red' if risk=='high' else 'safety-yellow' if risk=='medium' else 'safety-green'}}">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
    <div>
      <div class="badge {'red' if risk=='high' else 'yellow' if risk=='medium' else ''}">{'🔴 High Risk' if risk=='high' else '🟡 Moderate Risk' if risk=='medium' else '🟢 Low Risk'}</div>
      <div class="card-title" style="font-size:24px;">{sel_dis}</div>
      <div style="font-size:15px;color:#666;">Disease profile · Severity {severity}/77</div>
    </div>
    <div class="safety-ring {ring_cls}">{severity}</div>
  </div>
  <div style="background:#f9f9f9;border-radius:9999px;height:6px;overflow:hidden;margin-bottom:8px;">
    <div style="width:{sp}%;background:{rc};height:100%;border-radius:9999px;"></div>
  </div>
  <div style="font-size:13px;color:#666;display:flex;justify-content:space-between;">
    <span>Mild</span><span style="font-weight:600;color:{risk_color};">{severity}/77</span><span>Severe</span>
  </div>
</div>""", unsafe_allow_html=True)

# 4-metric row
m1, m2, m3, m4 = st.columns(4)
for col, lbl, val_html in [
    (m1, "Risk Level", f"<span class='risk-badge {risk_cls}'>{RISK_EMOJIS.get(risk,'')} {risk.upper()}</span>"),
    (m2, "Severity", f"<span style='font-size:26px;font-weight:600;color:{risk_color};'>{severity}</span><span style='color:#999;font-size:14px;'>/77</span>"),
    (m3, "Symptoms", f"<span style='font-size:26px;font-weight:600;color:#0d0d0d;'>{len(syms_for)}</span>"),
    (m4, "Drug Safety", f"<span class='risk-badge {'risk-low' if drug_sf=='safe' else 'risk-medium' if drug_sf=='moderate' else 'risk-high'}'>{SAFETY_ICONS.get(drug_sf,'')} {drug_sf.capitalize()}</span>"),
]:
    with col:
        st.markdown(f'<div class="metric-box" style="margin-bottom:10px;"><div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:8px;">{lbl}</div>{val_html}</div>', unsafe_allow_html=True)

# Traffic light
st.markdown(f"""
<div class="med-card">
  <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:12px;">Safety Assessment</div>
  <div class="traffic-light"><div class="tl-dot {'green' if risk=='low' else ''}" style="background:{'#22c55e' if risk=='low' else '#e5e7eb'}"></div><div class="tl-label" style="color:{'#16a34a' if risk=='low' else '#9ca3af'};">🟢 OTC safe — no prescription needed</div></div>
  <div class="traffic-light"><div class="tl-dot {'yellow' if risk=='medium' else ''}" style="background:{'#f59e0b' if risk=='medium' else '#e5e7eb'}"></div><div class="tl-label" style="color:{'#d97706' if risk=='medium' else '#9ca3af'};">🟡 Consult pharmacist before buying</div></div>
  <div class="traffic-light"><div class="tl-dot {'red' if risk=='high' else ''}" style="background:{'#ef4444' if risk=='high' else '#e5e7eb'}"></div><div class="tl-label" style="color:{'#dc2626' if risk=='high' else '#9ca3af'};">🔴 Doctor required — do not self-medicate</div></div>
</div>""", unsafe_allow_html=True)

# Medicine card
st.markdown(f"""
<div class="med-card {'safety-green' if drug_sf=='safe' else 'safety-yellow' if drug_sf=='moderate' else 'safety-red'}">
  <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:8px;">💊 Medicine</div>
  <div class="card-title">{drug_name}</div>
  <div style="margin-top:8px;"><span class="risk-badge {'risk-low' if drug_sf=='safe' else 'risk-medium' if drug_sf=='moderate' else 'risk-high'}">{SAFETY_ICONS.get(drug_sf,'')} {drug_sf.capitalize()}</span></div>
  <div style="font-size:15px;color:#666;margin-top:8px;line-height:1.5;">{SAFETY_NOTES.get(drug_sf,'')}</div>
  <div class="card-footer-note">💬 Consult a pharmacist before buying any medicine.</div>
</div>""", unsafe_allow_html=True)

# Description
st.markdown(f"""
<div class="med-card">
  <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:8px;">📋 Description</div>
  <div style="font-size:16px;color:#333;line-height:1.5;">{desc}</div>
</div>""", unsafe_allow_html=True)

# Precautions
if precs:
    prec_html = "".join(f"<span style='display:inline-flex;background:#f3f4f6;color:#333;border-radius:9999px;padding:4px 12px;font-size:13px;margin:3px;'>{p.strip().capitalize()}</span>" for p in precs if p.strip())
    st.markdown(f"""
    <div class="med-card">
      <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:10px;">🛡️ Precautions</div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;">{prec_html}</div>
    </div>""", unsafe_allow_html=True)

# Associated symptoms
if syms_for:
    sym_html = "".join(f"<span style='display:inline-flex;background:#d4fae8;color:#0fa76e;border-radius:9999px;padding:4px 12px;font-size:13px;margin:3px;'>{s.replace('_',' ').title()}</span>" for s in sorted(syms_for))
    st.markdown(f"""
    <div class="med-card">
      <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:10px;">🩺 Associated Symptoms ({len(syms_for)})</div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;">{sym_html}</div>
    </div>""", unsafe_allow_html=True)

# Risk alert
if risk == "high":
    st.markdown("""<div class="alert-danger">⛔ <strong>Do not self-medicate.</strong> High-risk diseases require professional diagnosis, lab tests, and physician-monitored treatment.</div>""", unsafe_allow_html=True)
elif risk == "medium":
    st.markdown("""<div class="alert-caution">⚠️ <strong>Moderate risk.</strong> Doctor's evaluation strongly advised before any medication.</div>""", unsafe_allow_html=True)
else:
    st.markdown("""<div class="alert-ok">✅ <strong>Lower risk.</strong> If symptoms persist or worsen beyond 3–5 days, consult a healthcare provider.</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="med-card" style="text-align:center;padding:24px;">
  <div style="font-size:18px;font-weight:600;color:#0d0d0d;margin-bottom:4px;">Was this helpful?</div>
  <div style="font-size:15px;color:#666;">Help us improve our treatment systems</div>
  <div style="display:flex;justify-content:center;gap:16px;margin-top:16px;">
    <span style="font-size:28px;cursor:pointer;">👍</span>
    <span style="font-size:28px;cursor:pointer;">👎</span>
  </div>
</div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="footer-pad"></div>', unsafe_allow_html=True)
