import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f4efe6;
            --surface: rgba(255, 252, 247, 0.82);
            --ink: #132a22;
            --muted: #5f6d67;
            --line: rgba(19, 42, 34, 0.1);
            --accent: #d96c31;
            --accent-soft: rgba(217, 108, 49, 0.14);
            --safe: #1b7f5c;
            --danger: #b63b2d;
            --shadow: 0 18px 60px rgba(55, 36, 22, 0.12);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(217,108,49,0.16), transparent 28%),
                radial-gradient(circle at 85% 15%, rgba(27,127,92,0.14), transparent 24%),
                linear-gradient(180deg, #f8f3ea 0%, var(--bg) 100%);
            color: var(--ink);
        }

        [data-testid="stSidebar"] {
            background: rgba(19, 42, 34, 0.96);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] * {
            color: #f8f3ea !important;
        }

        .hero-card, .panel-card, .metric-card, .status-card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 24px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(14px);
        }

        .hero-card {
            padding: 2rem;
            min-height: 320px;
            background:
                linear-gradient(135deg, rgba(255,250,242,0.96), rgba(255,245,230,0.82)),
                var(--surface);
        }

        .hero-kicker {
            display: inline-block;
            font-size: 0.82rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--accent);
            font-weight: 700;
            margin-bottom: 1rem;
        }

        .hero-title {
            font-size: clamp(2.3rem, 4vw, 4.5rem);
            line-height: 0.95;
            font-weight: 800;
            margin: 0;
            color: var(--ink);
        }

        .hero-subtitle {
            color: var(--muted);
            margin-top: 1rem;
            font-size: 1.02rem;
            max-width: 42rem;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin-top: 1.4rem;
        }

        .metric-card, .status-card {
            padding: 1.1rem 1.15rem;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.88rem;
            margin-bottom: 0.35rem;
        }

        .metric-value {
            font-size: 1.65rem;
            font-weight: 800;
            color: var(--ink);
        }

        .panel-card {
            padding: 1.35rem;
            height: 100%;
        }

        .panel-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--ink);
            margin-bottom: 0.45rem;
        }

        .panel-copy {
            color: var(--muted);
            font-size: 0.94rem;
            line-height: 1.6;
        }

        .prediction-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            border-radius: 999px;
            padding: 0.65rem 1rem;
            font-size: 0.92rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        .chip-safe {
            background: rgba(27, 127, 92, 0.12);
            color: var(--safe);
            border: 1px solid rgba(27, 127, 92, 0.22);
        }

        .chip-danger {
            background: rgba(182, 59, 45, 0.1);
            color: var(--danger);
            border: 1px solid rgba(182, 59, 45, 0.18);
        }

        .signal-pill {
            display: inline-block;
            padding: 0.35rem 0.7rem;
            margin: 0.15rem 0.3rem 0.15rem 0;
            border-radius: 999px;
            background: var(--accent-soft);
            color: var(--accent);
            font-size: 0.8rem;
            font-weight: 700;
        }

        .stTextArea textarea {
            min-height: 260px;
            border-radius: 18px;
            background: rgba(255, 250, 242, 0.88);
            border: 1px solid rgba(19, 42, 34, 0.1);
            color: var(--ink);
            font-size: 1rem;
        }

        .stButton > button {
            background: linear-gradient(135deg, #d96c31, #e58f4f);
            color: white;
            border: none;
            border-radius: 14px;
            font-weight: 700;
            padding: 0.75rem 1.15rem;
            box-shadow: 0 10px 28px rgba(217,108,49,0.28);
        }

        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #1b7f5c, #d96c31);
        }

        @media (max-width: 900px) {
            .metric-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
