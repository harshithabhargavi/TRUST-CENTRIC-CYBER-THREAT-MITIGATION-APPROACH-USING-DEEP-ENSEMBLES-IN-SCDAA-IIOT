# 🛡️ Trust-Centric Cyber Threat Mitigation Using Deep Ensembles in SCADA-IIoT

This project presents a machine learning-based system for detecting and mitigating cyber threats in Industrial IoT (IIoT) environments. It uses an ensemble of ML models integrated into a Django web application for real-time threat prediction.

---

## 🚀 Project Overview

With the rapid growth of IIoT systems, cyber threats have become more advanced. This system uses the **CIMD-2024 dataset** to classify network traffic into:

- Benign (Normal Traffic)
- Botnet
- Ransomware
- Spyware
- Trojan
- Worm

---

## 🛠️ Tech Stack

- **Backend:** Python, Django  
- **Machine Learning:** Scikit-learn, Pandas, NumPy  
- **Models:** Random Forest, Decision Tree, SVM, MLP  
- **Database:** SQLite3  
- **Storage:** Git LFS  

---

## 📊 Methodology

1. **Data Preprocessing**
   - Missing value handling (mean imputation)
   - Label Encoding
   - Feature Scaling

2. **Ensemble Learning**
   - Soft Voting Classifier combining multiple models
   - Improves accuracy and reduces false positives

3. **Deployment**
   - Integrated into Django for real-time predictions

---

## 🖥️ Output Screens

### 🔐 Login Page
<p align="center">
  <img src="images/login.png" width="700"/>
</p>

---

### 📊 Admin Dashboard
<p align="center">
  <img src="trustworthy_and_reliable_deep_learning/images/admin_dashboard.png" width="700"/>
   
</p>

---

### 🧠 Cyber Attack Prediction Input
<p align="center">
  <img src="images/prediction_input.png" width="700"/>
</p>

---

### 📈 Attack Analytics
<p align="center">
  <img src="images/analytics.png" width="700"/>
</p>

---

## ⚙️ Installation & Setup

### 1. Clone Repository
bash
git clone https://github.com/harshithabhargavi/TRUST-CENTRIC-CYBER-THREAT-MITIGATION-APPROACH-USING-DEEP-ENSEMBLES-IN-SCDAA-IIOT.git
cd TRUST-CENTRIC-CYBER-THREAT-MITIGATION-APPROACH-USING-DEEP-ENSEMBLES-IN-SCDAA-IIOT

### 2. Install Git LFS & Pull Models
bash
git lfs install
git lfs pull

3. Install Dependencies
pip install -r requirements.txt

4.Run Project
python manage.py migrate
python manage.py runserver

### 💡 Quick Note
Make sure:
- You already installed Git LFS (one-time):
```bash
git lfs install
