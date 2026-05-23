"""
Centralized styles and HTML templates for the DataPulse dashboard.
"""

# --- Dashboard Styles (app.py) ---

DASHBOARD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #090b12;
    --panel: #101421;
    --panel-2: #151b2c;
    --line: #273148;
    --text: #eef3ff;
    --muted: #94a3b8;
    --accent: #14b8a6;
    --accent-2: #8b5cf6;
    --warn: #f59e0b;
}

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: #0d111d;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    border: 1px solid var(--line);
    background:
        linear-gradient(135deg, rgba(20, 184, 166, 0.16), rgba(139, 92, 246, 0.11)),
        linear-gradient(135deg, #101421, #0d111d);
    border-radius: 8px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}

.eyebrow {
    color: var(--accent);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

.hero h1 {
    margin: 0;
    color: var(--text);
    font-size: 2.35rem;
    line-height: 1.1;
}

.hero p {
    color: var(--muted);
    max-width: 760px;
    margin: 0.9rem 0 0;
    line-height: 1.65;
}

.section-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--text);
    margin: 1.5rem 0 0.6rem;
}

.note {
    color: var(--muted);
    font-size: 0.9rem;
    line-height: 1.6;
}

[data-testid="stMetric"] {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 1rem;
}

[data-testid="stMetricLabel"] {
    color: var(--muted);
}

.stDataFrame,
[data-testid="stTable"] {
    border: 1px solid var(--line);
    border-radius: 8px;
}
</style>
"""

DASHBOARD_PLOT_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "Inter", "color": "#cbd5e1"},
    "margin": {"l": 10, "r": 10, "t": 35, "b": 10},
    "legend": {"bgcolor": "rgba(0,0,0,0)"},
    "xaxis": {"gridcolor": "rgba(148, 163, 184, 0.12)", "zeroline": False},
    "yaxis": {"gridcolor": "rgba(148, 163, 184, 0.12)", "zeroline": False},
}

HERO_HTML = """
<div class="hero">
    <div class="eyebrow">Sales intelligence dashboard</div>
    <h1>DataPulse turns raw sales tables into decisions.</h1>
    <p>
        Explore revenue movement, regional performance, product mix,
        and customer segments from a simple star-schema sales dataset.
    </p>
</div>
"""

def section_title(title: str) -> str:
    return f'<div class="section-title">{title}</div>'


# --- EDA Styles (analysis/eda.py) ---

EDA_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');
:root{--bg:#08090d;--surface:#0f1118;--card:#141720;--border:#1e2235;
      --accent:#00e5ff;--accent2:#7b61ff;--green:#00ffa3;--amber:#ffb647;
      --red:#ff4d6d;--text:#e8eaf0;--muted:#6b7280;
      --font-head:'Syne',sans-serif;--font-mono:'JetBrains Mono',monospace;}
html,body,[class*="css"]{font-family:var(--font-mono);background:var(--bg)!important;color:var(--text);}
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border);}
[data-testid="metric-container"]{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px!important;}
[data-testid="metric-container"] label{color:var(--muted)!important;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:var(--accent)!important;font-family:var(--font-head);font-size:2rem!important;}
.stButton>button{background:transparent;border:1px solid var(--accent);color:var(--accent);font-family:var(--font-mono);font-size:12px;letter-spacing:1px;border-radius:6px;padding:8px 20px;transition:all .2s;}
.stButton>button:hover{background:var(--accent);color:var(--bg);}
hr{border-color:var(--border)!important;}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:transparent;border-bottom:1px solid var(--border);}
.stTabs [data-baseweb="tab"]{background:transparent;color:var(--muted);font-family:var(--font-mono);font-size:12px;letter-spacing:1px;border-radius:4px 4px 0 0;padding:8px 18px;}
.stTabs [aria-selected="true"]{background:var(--card)!important;color:var(--accent)!important;border-bottom:2px solid var(--accent)!important;}
</style>
"""

EDA_PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono", color="#e8eaf0", size=11),
    margin=dict(l=10, r=10, t=35, b=10),
    xaxis=dict(showgrid=True, gridcolor="#1e2235", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#1e2235", zeroline=False),
)

EDA_COLORS = ["#00e5ff","#7b61ff","#00ffa3","#ffb647","#ff4d6d","#e879f9"]
