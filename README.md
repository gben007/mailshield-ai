# Email Spam Detection Using GRU and Streamlit

This project detects whether an email is **Ham** or **Spam** using a trained **GRU-based deep learning model** and presents predictions through a polished **Streamlit** interface.

## Features

- Streamlit web interface for live email classification
- GRU model trained for spam detection
- Saved tokenizer, label mapping, and config for inference
- Demo-ready UI with confidence score and text signal display

## Project Files

- `app.py` - Streamlit frontend for the spam detector
- `gru_model.keras` - trained GRU model
- `tokenizer.pkl` - saved tokenizer
- `config.pkl` - sequence configuration used during inference
- `label_mapping.pkl` - maps model output to Ham/Spam
- `emailspamusing_rnn_lstm_gru.ipynb` - notebook used for training and experimentation
- `requirements.txt` - Python dependencies

## Setup

Use Python 3.11 for best compatibility with TensorFlow.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- `combined_data.csv` is intentionally excluded from GitHub because it is too large for a normal repository push.
- If you want to share the dataset too, use Git LFS or provide a download link in this README.

## Sample Test Emails

### Spam-like sample

```text
Congratulations! You have won a free cash reward. Click the link now to claim your prize before the offer expires.
```

### Normal email sample

```text
Hi team, the project review meeting is scheduled for tomorrow at 3 PM. Please send your updated slides before lunch.
```

## Author

Shreya
