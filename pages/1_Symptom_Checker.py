"""
pages/1_Symptom_Checker.py — MediSafe White Theme
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.utils import (
    load_css, load_model, predict_diseases, pipeline_html,
    BODY_SVG, DISEASE_DRUG_MAP, RISK_COLORS, SAFETY_ICONS,
    SAFETY_NOTES, RISK_CSS, CHIP_CSS, RISK_EMOJIS, fmt_sym
)

st.set_page_config(page_title="Symptom Checker · MediSafe", page_icon="🔬", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

clf, le, all_syms, sym_idx, disease_profiles, dis_to_syms = load_model()
display_syms  = [fmt_sym(s) for s in all_syms]
sym_label_map = {d: r for d, r in zip(display_syms, all_syms)}

# ── TOP NAV ──────────────────────────────────────────────────
st.markdown("""
<div class="top-nav">
  <div class="nav-icon-btn">←</div>
  <div class="top-nav-brand">Medi<span>Safe</span> · Symptom Checker</div>
  <div class="nav-icon-btn">⚙</div>
</div>""", unsafe_allow_html=True)

pipe_slot = st.empty()
pipe_slot.markdown(pipeline_html(0), unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section" style="padding:32px 24px 24px;">
  <div class="hero-badge">🩺 AI-Powered Analysis</div>
  <div class="hero-title" style="font-size:32px;">Select your <span class="accent">symptoms</span></div>
  <div class="hero-subtitle" style="font-size:16px;">Choose your symptoms below. Our ML model predicts the disease and shows the safest treatment path.</div>
</div>""", unsafe_allow_html=True)

# ── RED FLAG WARNING ─────────────────────────────────────────
st.markdown("""
<div class="red-banner">
  ⚠️ <strong>Stop — See a doctor immediately</strong> if you have: chest pain, high fever lasting &gt;3 days, blood in stool, difficulty breathing, or sudden severe headache.
</div>""", unsafe_allow_html=True)

# ── SYMPTOM INPUT ────────────────────────────────────────────
col_body, col_form = st.columns([1, 2])
with col_body:
    st.markdown(f"""
    <div style="padding:24px 8px;display:flex;justify-content:center;">
      <div class="body-svg-container" style="position:relative;width:120px;">
        {BODY_SVG}
        <div class="body-glow-dot head" title="Head"></div>
        <div class="body-glow-dot chest" title="Chest"></div>
        <div class="body-glow-dot arm-l" title="Left Arm"></div>
        <div class="body-glow-dot arm-r" title="Right Arm"></div>
        <div class="body-glow-dot belly" title="Abdomen"></div>
        <div class="body-glow-dot leg-l" title="Left Leg"></div>
        <div class="body-glow-dot leg-r" title="Right Leg"></div>
      </div>
    </div>""", unsafe_allow_html=True)

with col_form:
    st.markdown('<div style="padding:20px 8px 0;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:8px;">Search &amp; Select Symptoms</div>', unsafe_allow_html=True)
    search_q = st.text_input("", placeholder="Search symptoms…", key="sym_search", label_visibility="collapsed")
    filtered = [s for s in display_syms if search_q.lower() in s.lower()] if search_q else display_syms
    categories = {
        "🧠 Head & Neuro":    ["Headache","High Fever","Blurred And Distorted Vision","Altered Sensorium","Loss Of Balance","Unsteadiness","Dizziness","Spinning Movements","Visual Disturbances"],
        "🫁 Respiratory":     ["Breathlessness","Cough","Rusty Sputum","Blood In Sputum","Mucoid Sputum","Continuous Sneezing"],
        "🤢 Digestive":       ["Nausea","Vomiting","Acidity","Stomach Pain","Belly Pain","Abdominal Pain","Diarrhoea","Constipation","Loss Of Appetite"],
        "🦠 Skin":            ["Itching","Skin Rash","Blackheads","Nodal Skin Eruptions","Blister","Pus Filled Pimples","Dischromic _Patches","Skin Peeling"],
        "🌡️ General":        ["Fatigue","Malaise","Lethargy","Chills","Shivering","Sweating","Weight Loss","Weight Gain"],
        "💉 Musculoskeletal": ["Joint Pain","Muscle Pain","Back Pain","Neck Pain","Knee Pain","Hip Joint Pain","Muscle Weakness","Swollen Joints"],
    }
    selected_display = st.multiselect("", options=filtered, placeholder="e.g. High Fever, Headache, Fatigue…", label_visibility="collapsed", key="sym_select")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="padding:0 8px;">', unsafe_allow_html=True)
st.markdown("""
<div style="padding:8px 16px 4px;">
  <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:8px;">Quick Select by Category</div>
</div>""", unsafe_allow_html=True)

cat_cols = st.columns(3)
extra_from_cats = []
for i, (cat_name, cat_syms) in enumerate(categories.items()):
    with cat_cols[i % 3]:
        avail = [s for s in cat_syms if s in display_syms]
        if avail:
            picks = st.multiselect(cat_name, avail, key=f"cat_{i}", label_visibility="visible")
            extra_from_cats.extend(picks)

all_selected_display = list(dict.fromkeys(selected_display + extra_from_cats))
selected_raw = [sym_label_map.get(d, d.replace(" ", "_").lower()) for d in all_selected_display]
st.markdown('</div>', unsafe_allow_html=True)

# ── SELECTED PREVIEW ─────────────────────────────────────────
if all_selected_display:
    pipe_slot.markdown(pipeline_html(1), unsafe_allow_html=True)
    pills = "".join(f"<span style='display:inline-flex;align-items:center;background:#d4fae8;color:#0fa76e;border-radius:9999px;padding:4px 12px;font-size:13px;font-weight:500;margin:3px;'>{s}</span>" for s in all_selected_display)
    st.markdown(f"""
    <div style="padding:8px 16px;">
      <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:8px;">✅ Selected ({len(all_selected_display)} symptoms)</div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;">{pills}</div>
    </div>""", unsafe_allow_html=True)

# ── LOCKOUT CHECK ─────────────────────────────────────────────
HIGH_RISK_SYMPTOMS = ["chest pain", "blood in sputum", "breathlessness", "high fever"]
severe_selected = [s for s in [d.lower() for d in all_selected_display] if any(h in s for h in HIGH_RISK_SYMPTOMS)]
if severe_selected:
    st.markdown("""
    <div class="lockout-screen">
      <div class="lockout-icon">🚨</div>
      <div class="lockout-title">See a Doctor Immediately</div>
      <div class="lockout-sub">You've selected high-risk symptoms that require immediate medical attention. We cannot suggest medicines for these symptoms.</div>
      <a class="btn-primary" style="display:inline-flex;margin:0 auto;" href="#">Find Nearest Hospital →</a>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── RUN BUTTON ────────────────────────────────────────────────
st.markdown('<div style="padding:8px 16px 16px;">', unsafe_allow_html=True)
run_btn = st.button("Analyse Symptoms  →", use_container_width=True, key="run_ml")
st.markdown('</div>', unsafe_allow_html=True)

# ── ML PIPELINE ──────────────────────────────────────────────
if all_selected_display and run_btn:
    pipe_slot.markdown(pipeline_html(2), unsafe_allow_html=True)
    with st.spinner(""):
        predictions = predict_diseases(selected_raw, clf, le, all_syms, sym_idx, top_n=5)

    if not predictions:
        st.warning("No predictions returned. Try adding more symptoms.")
        st.stop()

    top_disease, top_conf = predictions[0]
    top_profile = disease_profiles.get(top_disease, {})
    top_risk    = top_profile.get("risk_level", "unknown")

    pipe_slot.markdown(pipeline_html(3), unsafe_allow_html=True)

    # ── STATS ─────────────────────────────────────────────────
    st.markdown("""
    <div class="sec-header" style="padding-top:24px;">
      <div class="sec-label">ML Model Output</div>
      <div class="sec-title">Analysis Result</div>
    </div>""", unsafe_allow_html=True)

    conf_pct = round(top_conf * 100, 1)
    sev0     = top_profile.get("severity_score", 0)
    rc0      = RISK_COLORS.get(top_risk, "#888")

    risk_tl = {"high": ("red", "🔴", "Doctor required"), "medium": ("yellow", "🟡", "Consult pharmacist"), "low": ("green", "🟢", "OTC safe")}.get(top_risk, ("green", "🟢", "OTC safe"))
    tl_color, tl_emoji, tl_label = risk_tl

    s_cols = st.columns(3)
    with s_cols[0]:
        st.markdown(f'<div class="metric-box"><div class="metric-val">{len(all_selected_display)}</div><div class="metric-lbl">Symptoms</div></div>', unsafe_allow_html=True)
    with s_cols[1]:
        st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#0fa76e;">{conf_pct}%</div><div class="metric-lbl">Confidence</div></div>', unsafe_allow_html=True)
    with s_cols[2]:
        risk_color_map = {"high": "#dc2626", "medium": "#d97706", "low": "#0fa76e"}
        st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:{risk_color_map.get(top_risk,"#333")};font-size:20px;">{tl_emoji} {top_risk.upper()}</div><div class="metric-lbl">Risk Level</div></div>', unsafe_allow_html=True)

    # ── TRAFFIC LIGHT ─────────────────────────────────────────
    st.markdown(f"""
    <div class="med-card" style="margin-top:12px;">
      <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:12px;">Safety Assessment</div>
      <div class="traffic-light"><div class="tl-dot {'green' if top_risk=='low' else 'gray'}" style="{'background:#22c55e' if top_risk=='low' else 'background:#e5e7eb'}"></div><div class="tl-label" style="{'color:#16a34a;font-weight:600' if top_risk=='low' else 'color:#9ca3af'}">🟢 OTC safe — no prescription needed</div></div>
      <div class="traffic-light"><div class="tl-dot {'yellow' if top_risk=='medium' else 'gray'}" style="{'background:#f59e0b' if top_risk=='medium' else 'background:#e5e7eb'}"></div><div class="tl-label" style="{'color:#d97706;font-weight:600' if top_risk=='medium' else 'color:#9ca3af'}">🟡 Consult pharmacist before buying</div></div>
      <div class="traffic-light"><div class="tl-dot {'red' if top_risk=='high' else 'gray'}" style="{'background:#ef4444' if top_risk=='high' else 'background:#e5e7eb'}"></div><div class="tl-label" style="{'color:#dc2626;font-weight:600' if top_risk=='high' else 'color:#9ca3af'}">🔴 Doctor required — do not self-medicate</div></div>
    </div>""", unsafe_allow_html=True)

    # ── CONFIDENCE BARS ───────────────────────────────────────
    st.markdown('<div style="padding:0 16px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:12px;">Model Confidence — Top Predictions</div>', unsafe_allow_html=True)
    for dis, prob in predictions:
        pct  = round(prob * 100, 1)
        prof = disease_profiles.get(dis, {})
        r    = prof.get("risk_level", "")
        bar_color = {"high": "#ef4444", "medium": "#f59e0b", "low": "#18E299"}.get(r, "#18E299")
        is_t = dis == top_disease
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
          <div style="font-size:15px;color:{'#0d0d0d' if is_t else '#666'};font-weight:{'600' if is_t else '400'};width:180px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{'★ ' if is_t else ''}{dis.title()}</div>
          <div style="flex:1;background:#f3f4f6;border-radius:9999px;height:8px;overflow:hidden;">
            <div style="width:{pct}%;background:{bar_color};height:100%;border-radius:9999px;"></div>
          </div>
          <div style="font-size:13px;color:{bar_color};font-weight:500;width:40px;text-align:right;">{pct}%</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    pipe_slot.markdown(pipeline_html(4), unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-header">
      <div class="sec-label">Medicine &amp; Risk Lookup</div>
      <div class="sec-title">Results</div>
    </div>""", unsafe_allow_html=True)
    pipe_slot.markdown(pipeline_html(5), unsafe_allow_html=True)

    st.markdown('<div class="scroll-section">', unsafe_allow_html=True)
    for rank, (disease, conf) in enumerate(predictions):
        profile   = disease_profiles.get(disease, {})
        drug_info = DISEASE_DRUG_MAP.get(disease, {"drug": "Consult a doctor", "safety": "unknown"})
        risk      = profile.get("risk_level", "unknown")
        severity  = profile.get("severity_score", 0)
        desc      = profile.get("description", "No description available.")
        precs     = profile.get("precautions", [])
        drug_name = drug_info["drug"]
        drug_sf   = drug_info["safety"]
        cp        = round(conf * 100, 1)
        sp        = min(100, int((severity / 77) * 100))
        is_top    = rank == 0
        bar_color = {"high": "#ef4444", "medium": "#f59e0b", "low": "#18E299"}.get(risk, "#18E299")
        ring_cls  = {"high": "red", "medium": "yellow", "low": "green"}.get(risk, "green")
        risk_cls  = {"high": "risk-high", "medium": "risk-medium", "low": "risk-low"}.get(risk, "risk-low")
        safety_icon = SAFETY_ICONS.get(drug_sf, "")
        safety_note = SAFETY_NOTES.get(drug_sf, "")
        prec_html = "".join(f"<span style='display:inline-flex;background:#f3f4f6;color:#333;border-radius:9999px;padding:3px 10px;font-size:13px;margin:2px;'>{p.strip().capitalize()}</span>" for p in precs if p.strip())
        card_cls  = "featured" if is_top else ""
        safety_border = {"safe": "safety-green", "moderate": "safety-yellow", "risky": "safety-red"}.get(drug_sf, "")

        st.markdown(f"""
        <div class="med-card {card_cls} {safety_border}">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:16px;">
            <div>
              <div class="badge {'gray' if not is_top else ''}">{"🏆 Top Match" if is_top else f"#{rank+1} · {cp}% confidence"}</div>
              <div class="card-title">{disease.title()}</div>
              <div style="font-size:15px;color:#666;">Severity {severity}/77</div>
            </div>
            <div class="safety-ring-wrap" style="margin:0;">
              <div class="safety-ring {ring_cls}">{cp:.0f}%</div>
            </div>
          </div>

          <div style="margin-bottom:16px;">
            <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:6px;">Severity</div>
            <div style="background:#f3f4f6;border-radius:9999px;height:6px;overflow:hidden;">
              <div style="width:{sp}%;background:{bar_color};height:100%;border-radius:9999px;"></div>
            </div>
          </div>

          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px;">
            <div>
              <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:6px;">💊 Medicine</div>
              <div style="font-size:15px;font-weight:600;color:#0d0d0d;margin-bottom:4px;">{drug_name}</div>
              <span class="risk-badge {risk_cls}">{safety_icon} {drug_sf.capitalize()}</span>
            </div>
            <div>
              <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:6px;">🛡️ Precautions</div>
              <div style="display:flex;flex-wrap:wrap;gap:4px;">{prec_html}</div>
            </div>
          </div>

          <div style="background:#fafafa;border:1px solid rgba(0,0,0,0.05);border-radius:12px;padding:12px;">
            <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:6px;">📋 Description</div>
            <div style="font-size:15px;color:#333;line-height:1.5;">{desc}</div>
          </div>

          <div class="card-footer-note">💬 Consult a pharmacist before buying any medicine listed above.</div>
        </div>""", unsafe_allow_html=True)

    # Risk alert
    if top_risk == "high":
        st.markdown("""<div class="alert-danger">⛔ <strong>High-Risk Condition Predicted.</strong> Self-medicating without proper diagnosis, lab tests, and physician oversight can be life-threatening. <strong>Visit a qualified doctor or hospital immediately.</strong></div>""", unsafe_allow_html=True)
    elif top_risk == "medium":
        st.markdown("""<div class="alert-caution">⚠️ <strong>Moderate-Risk Condition.</strong> A doctor's evaluation is strongly recommended before any medication.</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="alert-ok">✅ <strong>Lower-Risk Condition.</strong> Even low-risk conditions benefit from professional diagnosis to rule out complications.</div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif run_btn and not all_selected_display:
    st.markdown("""<div class="alert-caution" style="margin:0 16px;">⚠️ Please select at least one symptom before running the analysis.</div>""", unsafe_allow_html=True)

if not run_btn:
    st.markdown("""
    <div class="scroll-section" style="margin-top:16px;">
      <div class="med-card">
        <div class="badge">💡 Tips</div>
        <div class="card-title">How to get best results</div>
        <div class="card-sub">Select all symptoms you are currently experiencing. The more symptoms you provide, the more accurate the ML prediction. Always verify results with a qualified healthcare professional.</div>
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="footer-pad"></div>', unsafe_allow_html=True)
