"""
pages/3_Drug_Safety.py — MediSafe White Theme
"""
import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.utils import load_css, DATA_DIR

st.set_page_config(page_title="Drug Safety · MediSafe", page_icon="📊", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

st.markdown("""
<div class="top-nav">
  <div class="nav-icon-btn">←</div>
  <div class="top-nav-brand">Medi<span>Safe</span> · Drug Safety</div>
  <div class="nav-icon-btn">🔍</div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="sec-header">
  <div class="sec-label">206,383 Patient Reviews</div>
  <div class="sec-title">Drug Safety Explorer</div>
  <div class="sec-sub">Browse 1,705 medications across 825 conditions.</div>
</div>""", unsafe_allow_html=True)

# Stats
s_cols = st.columns(4)
for col, val, lbl, color in [
    (s_cols[0], "206K", "Reviews", "#0d0d0d"),
    (s_cols[1], "65.8%", "Safe", "#0fa76e"),
    (s_cols[2], "22.0%", "Risky", "#dc2626"),
    (s_cols[3], "12.2%", "Moderate", "#d97706"),
]:
    with col:
        st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:{color};font-size:22px;">{val}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="scroll-section" style="padding-top:16px;">', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    q = st.text_input("", placeholder="Search condition or drug name…", label_visibility="collapsed")
with col2:
    tier = st.selectbox("Safety Tier", ["All", "Safe", "Moderate", "Risky"])

try:
    raw = pd.read_csv(os.path.join(DATA_DIR, "final_cleaned_combined_dataset__3_.csv"))
    raw = raw[~raw["condition"].str.contains("span|users found", na=False)]
    raw["condition"] = raw["condition"].str.strip().str.lower()
    raw["drugName"]  = raw["drugName"].str.strip().str.lower()
    if tier != "All":
        raw = raw[raw["safety"] == tier.lower()]
    if q:
        mask = raw["condition"].str.contains(q.lower(), na=False) | raw["drugName"].str.contains(q.lower(), na=False)
        raw = raw[mask]

    top = raw.groupby(["condition", "safety"]).size().reset_index(name="n").sort_values("n", ascending=False).head(15)

    try:
        import plotly.graph_objects as go
        if not top.empty:
            fig = go.Figure()
            color_map = {"safe": "#18E299", "moderate": "#f59e0b", "risky": "#ef4444"}
            for t, color in [("safe", "#18E299"), ("moderate", "#f59e0b"), ("risky", "#ef4444")]:
                d = top[top["safety"] == t]
                if not d.empty:
                    fig.add_trace(go.Bar(
                        name=t.capitalize(),
                        x=d["condition"].str.title(),
                        y=d["n"],
                        marker_color=color,
                        marker_line_width=0,
                        marker=dict(cornerradius=4)
                    ))
            fig.update_layout(
                barmode="stack",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font=dict(family="Inter, sans-serif", color="#0d0d0d", size=12),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=0, r=0, t=32, b=0),
                height=320,
                xaxis=dict(showgrid=False, tickangle=-30, color="#666", tickfont=dict(size=11)),
                yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)", color="#666"),
            )
            st.plotly_chart(fig, use_container_width=True)
    except ImportError:
        st.info("Install plotly for chart visualization.")

    # Drug list
    if not raw.empty:
        drug_grp = raw.groupby(["drugName", "safety"]).agg(
            conditions=("condition", lambda x: ", ".join(sorted(set(x))[:3])),
            count=("condition", "count"),
            avg_rating=("usefulCount", "mean") if "usefulCount" in raw.columns else ("condition", "count")
        ).reset_index().sort_values("count", ascending=False).head(20)

        st.markdown("""
        <div style="margin-top:16px;">
          <div style="font-size:13px;font-weight:500;letter-spacing:0.65px;text-transform:uppercase;color:#666;margin-bottom:12px;">Top Drugs by Review Count</div>
        </div>""", unsafe_allow_html=True)

        for _, row in drug_grp.iterrows():
            safety   = row["safety"]
            ring_cls = {"safe": "green", "moderate": "yellow", "risky": "red"}.get(safety, "green")
            risk_cls = {"safe": "risk-low", "moderate": "risk-medium", "risky": "risk-high"}.get(safety, "risk-low")
            icon     = {"safe": "✅", "moderate": "⚠️", "risky": "❌"}.get(safety, "")
            border   = {"safe": "safety-green", "moderate": "safety-yellow", "risky": "safety-red"}.get(safety, "")

            st.markdown(f"""
            <div class="med-card {border}" style="margin-bottom:8px;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;">
                <div style="flex:1;">
                  <div class="card-title" style="font-size:17px;">{row['drugName'].title()}</div>
                  <div style="font-size:14px;color:#666;margin-top:2px;">Conditions: {row['conditions'].title()}</div>
                  <div style="font-size:13px;color:#888;margin-top:4px;">{row['count']} reviews</div>
                </div>
                <div>
                  <span class="risk-badge {risk_cls}">{icon} {safety.capitalize()}</span>
                </div>
              </div>
              <div class="traffic-light" style="margin-top:10px;">
                <div class="tl-dot {'green' if safety=='safe' else 'yellow' if safety=='moderate' else 'red'}"></div>
                <div class="tl-label" style="font-size:13px;">{'🟢 OTC safe' if safety=='safe' else '🟡 Consult pharmacist' if safety=='moderate' else '🔴 Doctor required'}</div>
              </div>
              <div class="card-footer-note">💬 Consult a pharmacist before buying.</div>
            </div>""", unsafe_allow_html=True)

except FileNotFoundError:
    st.markdown("""
    <div class="med-card">
      <div class="badge gray">Dataset</div>
      <div class="card-title">Full dataset not found</div>
      <div class="card-sub">The complete drug review dataset is not included in this version. The symptom checker and disease lookup modules are fully functional.</div>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="footer-pad"></div>', unsafe_allow_html=True)
