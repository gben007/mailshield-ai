from pathlib import Path

import streamlit as st

from src.mailshield.config import DEFAULT_ARTIFACT_DIR, MODEL_SPECS, SAMPLE_EMAILS
from src.mailshield.inference import predict_message
from src.mailshield.presentation import confidence_copy
from src.mailshield.ui import inject_styles


st.set_page_config(
    page_title="MailShield AI",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("## Model Setup")
        artifact_dir = st.text_input("Artifact folder", value=str(DEFAULT_ARTIFACT_DIR))
        st.caption("Point this to the folder that contains the saved GRU model and pickle files.")

        st.markdown("## Quick Samples")
        selected_sample = st.selectbox("Load example", ["None"] + list(SAMPLE_EMAILS.keys()))
        if selected_sample != "None" and st.button("Use Selected Sample"):
            st.session_state["email_text"] = SAMPLE_EMAILS[selected_sample]

        st.markdown("## About")
        st.write(
            "This interface uses your saved GRU classifier, tokenizer, and config files to score one message at a time."
        )

    return artifact_dir


def render_hero() -> tuple[str, bool]:
    left, right = st.columns([1.35, 0.9], gap="large")

    with left:
        st.markdown(
            f"""
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
                        <div class="metric-value">{MODEL_SPECS["family"]}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Sequence length</div>
                        <div class="metric-value">{MODEL_SPECS["max_length"]}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Vocabulary cap</div>
                        <div class="metric-value">{MODEL_SPECS["max_features"]:,}</div>
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

    return email_text, predict_clicked


def render_prediction(email_text: str, artifact_dir: str) -> None:
    if not email_text.strip():
        st.warning("Please enter an email message before running the classifier.")
        return

    try:
        result = predict_message(email_text, Path(artifact_dir))
    except Exception as exc:
        st.error(f"Could not load the model artifacts: {exc}")
        return

    is_spam = result.label.lower() == "spam"
    chip_class = "chip-danger" if is_spam else "chip-safe"
    spam_percent = result.spam_score * 100
    ham_percent = result.ham_score * 100

    st.markdown("---")
    result_col, detail_col = st.columns([1.1, 0.9], gap="large")

    with result_col:
        st.markdown(
            f"""
            <div class="status-card">
                <div class="prediction-chip {chip_class}">
                    Predicted class: {result.label}
                </div>
                <div class="panel-title">Confidence snapshot</div>
                <div class="panel-copy">{confidence_copy(result.spam_score)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        st.metric("Spam probability", f"{spam_percent:.2f}%")
        st.progress(min(max(result.spam_score, 0.0), 1.0))
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
        if result.signal_terms:
            st.markdown(
                "".join(f'<span class="signal-pill">{term}</span>' for term in result.signal_terms),
                unsafe_allow_html=True,
            )
        else:
            st.info("No high-risk keywords from the demo signal list were found in this message.")

        st.caption(f"Clean token count: {len(result.tokens)}")
        preview = " ".join(result.tokens[:40]) if result.tokens else "No usable tokens after cleaning."
        st.code(preview, language="text")


def render_footer() -> None:
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


def main() -> None:
    inject_styles()
    artifact_dir = render_sidebar()
    email_text, predict_clicked = render_hero()
    if predict_clicked:
        render_prediction(email_text, artifact_dir)
    render_footer()


if __name__ == "__main__":
    main()
