from __future__ import annotations

import pickle
import re
import string
from pathlib import Path

import streamlit as st
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


DEFAULT_ARTIFACT_DIR = Path(__file__).resolve().parent
SPAM_TERMS = {
    "winner",
    "won",
    "urgent",
    "claim",
    "free",
    "cash",
    "offer",
    "limited",
    "click",
    "prize",
    "bonus",
    "guaranteed",
}


st.set_page_config(
    page_title="MailShield AI",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f4efe6;
            --surface: rgba(255, 252, 247, 0.82);
            --surface-strong: #fffaf2;
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


def clean_text(text: str) -> list[str]:
    normalized = text.lower()
    normalized = re.sub(r"http\\S+|www\\.\\S+", " ", normalized)
    normalized = normalized.translate(str.maketrans("", "", string.punctuation))
    tokens = re.findall(r"\b[a-z]+\b", normalized)
    return [token for token in tokens if token not in ENGLISH_STOP_WORDS]


@st.cache_resource(show_spinner=False)
def load_artifacts(artifact_dir: str):
    base = Path(artifact_dir).expanduser()
    required_files = {
        "model": base / "gru_model.keras",
        "tokenizer": base / "tokenizer.pkl",
        "config": base / "config.pkl",
        "label_mapping": base / "label_mapping.pkl",
    }

    missing = [name for name, path in required_files.items() if not path.exists()]
    if missing:
        missing_items = ", ".join(missing)
        raise FileNotFoundError(f"Missing required artifact files: {missing_items}")

    model = load_model(required_files["model"])
    with required_files["tokenizer"].open("rb") as file:
        tokenizer = pickle.load(file)
    with required_files["config"].open("rb") as file:
        config = pickle.load(file)
    with required_files["label_mapping"].open("rb") as file:
        label_mapping = pickle.load(file)
    return model, tokenizer, config, label_mapping


def predict_message(text: str, artifact_dir: str):
    model, tokenizer, config, label_mapping = load_artifacts(artifact_dir)
    tokens = clean_text(text)
    sequence = tokenizer.texts_to_sequences([tokens])
    padded = pad_sequences(sequence, maxlen=config["max_length"], padding="post")
    spam_score = float(model.predict(padded, verbose=0)[0][0])
    predicted_index = int(spam_score >= 0.5)
    label = label_mapping.get(predicted_index, "Spam" if predicted_index else "Ham")
    highlighted_terms = [token for token in tokens if token in SPAM_TERMS]
    return {
        "label": label,
        "spam_score": spam_score,
        "ham_score": 1 - spam_score,
        "tokens": tokens,
        "signal_terms": sorted(set(highlighted_terms)),
    }


def confidence_copy(spam_score: float) -> str:
    if spam_score >= 0.85 or spam_score <= 0.15:
        return "High confidence"
    if spam_score >= 0.65 or spam_score <= 0.35:
        return "Moderate confidence"
    return "Borderline result"


inject_styles()

with st.sidebar:
    st.markdown("## Model Setup")
    artifact_dir = st.text_input("Artifact folder", value=str(DEFAULT_ARTIFACT_DIR))
    st.caption("Point this to the folder that contains the saved GRU model and pickle files.")

    st.markdown("## Quick Samples")
    sample_options = {
        "Promotional spam": "Congratulations. You have won a free cash prize. Click the link now to claim your reward.",
        "Normal work email": "Hi team, the client review is moved to 3 PM tomorrow. Please share your updated slides before lunch.",
        "Urgent finance bait": "Urgent action required. Your account will be suspended unless you confirm payment details immediately.",
    }
    selected_sample = st.selectbox("Load example", ["None"] + list(sample_options.keys()))
    if selected_sample != "None" and st.button("Use Selected Sample"):
        st.session_state["email_text"] = sample_options[selected_sample]

    st.markdown("## About")
    st.write(
        "This interface uses your saved GRU classifier, tokenizer, and config files to score one message at a time."
    )


left, right = st.columns([1.35, 0.9], gap="large")

with left:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-kicker">Streamlit interface for your spam detector</div>
            <h1 class="hero-title">MailShield AI</h1>
            <p class="hero-subtitle">
                A polished review screen for classifying incoming email text as Ham or Spam with your trained GRU model.
                Paste a message, run the detector, and inspect the confidence and text signals in one place.
            </p>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Model family</div>
                    <div class="metric-value">GRU</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Sequence length</div>
                    <div class="metric-value">500</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Vocabulary cap</div>
                    <div class="metric-value">5,000</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")
    email_text = st.text_area(
        "Email content",
        key="email_text",
        placeholder="Paste the email body here for classification...",
        label_visibility="collapsed",
    )

    predict_clicked = st.button("Analyze Email", use_container_width=False)

with right:
    st.markdown(
        """
        <div class="panel-card">
            <div class="panel-title">How this UI works</div>
            <div class="panel-copy">
                The app mirrors your notebook pipeline: lowercase text, remove punctuation and links,
                filter common stopwords, tokenize the message, pad the sequence, and send it to the saved GRU model.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")
    st.markdown(
        """
        <div class="panel-card">
            <div class="panel-title">Best for demos and viva</div>
            <div class="panel-copy">
                The layout is built to look presentation-ready, not just functional. It gives you a strong first screen,
                clear confidence bars, and quick examples so you can show the project smoothly.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if predict_clicked:
    if not email_text.strip():
        st.warning("Please enter an email message before running the classifier.")
    else:
        try:
            result = predict_message(email_text, artifact_dir)
        except Exception as exc:
            st.error(f"Could not load the model artifacts: {exc}")
        else:
            is_spam = result["label"].lower() == "spam"
            chip_class = "chip-danger" if is_spam else "chip-safe"
            spam_percent = result["spam_score"] * 100
            ham_percent = result["ham_score"] * 100

            st.markdown("---")
            result_col, detail_col = st.columns([1.1, 0.9], gap="large")

            with result_col:
                st.markdown(
                    f"""
                    <div class="status-card">
                        <div class="prediction-chip {chip_class}">
                            Predicted class: {result["label"]}
                        </div>
                        <div class="panel-title">Confidence snapshot</div>
                        <div class="panel-copy">{confidence_copy(result["spam_score"])}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.write("")
                st.metric("Spam probability", f"{spam_percent:.2f}%")
                st.progress(min(max(result["spam_score"], 0.0), 1.0))
                st.metric("Ham probability", f"{ham_percent:.2f}%")

            with detail_col:
                st.markdown(
                    """
                    <div class="panel-card">
                        <div class="panel-title">Processed text signals</div>
                        <div class="panel-copy">
                            These are lightweight cues from the cleaned message that often appear in suspicious mail.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if result["signal_terms"]:
                    st.markdown(
                        "".join(
                            f'<span class="signal-pill">{term}</span>' for term in result["signal_terms"]
                        ),
                        unsafe_allow_html=True,
                    )
                else:
                    st.info("No high-risk keywords from the demo signal list were found in this message.")

                st.caption(f"Clean token count: {len(result['tokens'])}")
                preview = " ".join(result["tokens"][:40]) if result["tokens"] else "No usable tokens after cleaning."
                st.code(preview, language="text")

st.markdown("---")
footer_left, footer_right = st.columns(2, gap="large")
with footer_left:
    st.markdown(
        """
        <div class="panel-card">
            <div class="panel-title">Run locally</div>
            <div class="panel-copy">
                Start the interface with <code>streamlit run app.py</code>. If you move the model files, just update the artifact path in the sidebar.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with footer_right:
    st.markdown(
        """
        <div class="panel-card">
            <div class="panel-title">What you can add next</div>
            <div class="panel-copy">
                Batch CSV upload, probability history, confusion matrix visuals, and class explanations can all be layered on top without changing the model.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
