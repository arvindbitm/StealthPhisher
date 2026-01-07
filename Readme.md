# StealthPhisher

**StealthPhisher** — Defensive phishing detection framework using hybrid deep learning and generative AI.

A cybersecurity project that detects whether a URL is phishing or legitimate using advanced feature engineering and machine learning techniques, and generates detailed AI-powered reports for users. :contentReference[oaicite:0]{index=0}

---

## 🚀 What StealthPhisher Does

StealthPhisher is designed to:

- 🛡️ **Detect phishing URLs** with high accuracy using hybrid deep learning methods.
- 📊 Extract statistical and structural features from URLs.
- 🤖 Use Generative AI to build human-readable reports explaining detection results.
- 📈 Provide insights into dataset feature importance, model performance, and robustness.

This project was developed as part of research on phishing detection and defense. :contentReference[oaicite:1]{index=1}

---

## 📁 What’s Included

Inside this repo you’ll find:

📌 **Jupyter Notebooks (.ipynb)**  
- Data exploration and visualizations  
- Feature extraction and extended features  
- Model training, evaluation, and selection  
- Adversarial attack robustness testing

📌 **Python Scripts**
- `StealthPhisher_Google_Safe_Browsing.py` – integrate with Google Safe Browsing checks  
- `StealthPhisher_Sitemap.py` – sitemap creation/extraction module

⚠️ There’s no packaged executable yet — this is research and analysis code.

---

## 🧠 Key Concepts Used

- URL structural & statistical features (length, TLD, entropy, complexity)  
- Hybrid machine learning / deep learning models  
- Adversarial robustness evaluation  
- Generative AI for report creation

The full research framework described here achieves high detection accuracy and robust performance against adversarial examples. :contentReference[oaicite:2]{index=2}

---

## 💡 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/arvindbitm/StealthPhisher.git
cd StealthPhisher
