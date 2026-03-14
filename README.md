# MailShield AI - Email Spam Detection Using GRU and Streamlit

MailShield AI is an email spam detection project that classifies email content as **Ham** or **Spam** using a trained **GRU-based deep learning model**. The project also includes a polished **Streamlit** web interface for testing predictions in real time.

## Overview

This project combines natural language preprocessing, sequence modeling, and web deployment into a complete end-to-end machine learning application. Users can paste email text into the interface and instantly receive a classification result along with model confidence.

## Features

- Real-time email classification through a Streamlit web app
- GRU-based deep learning model for spam detection
- Saved tokenizer, label mapping, and config for inference
- Clean and demo-ready user interface
- Confidence-based output for predictions

## Project Files

- `app.py` - Streamlit frontend for the spam detection app
- `gru_model.keras` - trained GRU model
- `tokenizer.pkl` - saved tokenizer
- `config.pkl` - sequence configuration used during inference
- `label_mapping.pkl` - maps model output to Ham/Spam
- `emailspamusing_rnn_lstm_gru.ipynb` - notebook used for training and experimentation
- `requirements.txt` - Python dependencies

## Tech Stack

- Python
- TensorFlow / Keras
- Streamlit
- scikit-learn
- Natural Language Processing (NLP)

## Setup

Use Python 3.11 for best compatibility with TensorFlow.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- `combined_data.csv` is excluded from this repository due to file size limitations.
- If needed, the dataset can be shared separately via Git LFS or an external download link.

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

Gaurav Beniwal
