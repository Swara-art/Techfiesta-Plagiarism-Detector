# 🛡️ Plagiarism & Authentication Detector

An **AI-powered web application** that detects plagiarism and verifies originality across **text, code, and handwritten content**. Built with modern NLP and code analysis techniques, this system goes beyond copy‑paste detection to understand **meaning, structure, and intent**.

---

## ✨ What We Are Building

🔹 **Web-based demo** for both **Text & Code plagiarism detection**
🔹 **Real-time AI-powered analysis**
🔹 **Separate Student & Teacher dashboards**
🔹 **LMS-ready architecture** (simulated LTI integration)
🔹 **Explainable originality reports** (clear, human‑readable insights)

---

## 🎯 Problem We Solve

Traditional plagiarism checkers:

* Fail on **paraphrased content** ❌
* Detect only **exact code copy-paste** ❌
* Provide **unclear similarity scores** ❌

### ✅ Our Solution

We analyze **semantic meaning**, **logical structure**, and **citation context** to deliver **accurate, fair, and explainable plagiarism detection**.

---

## 🧠 How Our Solution Works

### 📄 Text Plagiarism Detection

* Semantic similarity using **Sentence Transformers**
* Paraphrase & meaning-level comparison
* Citation suggestion engine
* Context-aware originality scoring

### 💻 Code Plagiarism Detection

* **AST-based analysis** using Tree-sitter
* Logic & structure comparison (not formatting-based)
* Detects renamed variables, reordered logic, and hidden similarities

### ✍️ Handwriting to Text

* Converts handwritten submissions to text
* Applies the same semantic plagiarism checks
* Enables offline → online submission verification

---

## 📊 Originality Report (Explainable AI)

Each submission generates:

* 🔢 **Originality Score (%)**
* 🧩 Highlighted similar sections
* 📌 Source references
* 🧠 Explanation of why content is flagged
* 📚 Citation recommendations

Designed to be **easy to read for students** and **actionable for teachers**.

---

## 👥 User Views

### 🎓 Student View

* Upload text / code / handwritten work
* View originality score instantly
* Learn how to improve citations
* Transparent feedback (no black-box scoring)

### 👩‍🏫 Teacher View

* Batch submission analysis
* Side-by-side similarity comparison
* Class-level plagiarism insights
* Exportable reports

---

## 🧰 Tech Stack

### 🌐 Frontend

* **Languages:** JavaScript, HTML, CSS
* **Frameworks:** React.js / Streamlit
* Clean UI with real-time feedback

### ⚙️ Backend

* **Language:** Python
* **Frameworks:** FastAPI / Flask
* REST-based architecture

### 🗄️ Database & Storage

* **ChromaDB** – Vector similarity storage
* **JSON** – Lightweight metadata storage

### 🤖 AI / ML Engine

* **NLP Models:** Sentence-Transformers (Semantic Embeddings)
* **Techniques:** Cosine Similarity, Paraphrase Detection
* **Code Analysis:** Tree-sitter (AST-based structural comparison)

---

## 🔄 System Architecture (High Level)

```
User Input
   ↓
Preprocessing (Text / Code / Handwriting)
   ↓
AI Similarity Engine
   ↓
Vector Database (ChromaDB)
   ↓
Scoring + Explanation Layer
   ↓
Student / Teacher Dashboard
```
<img width="2279" height="1138" alt="image" src="https://github.com/user-attachments/assets/2da8c150-8ce8-46bf-888d-f29a889cc1f3" />

---

## 🚀 Key Features

✅ Semantic plagiarism detection
✅ Code logic similarity analysis
✅ Citation suggestion engine
✅ Explainable AI reports
✅ LMS‑ready design
✅ Scalable & modular architecture

---
![WhatsApp Image 2026-01-05 at 09 56 49](https://github.com/user-attachments/assets/3635915d-6dc2-4756-84fc-add0b09ff761)
![WhatsApp Image 2026-01-05 at 09 59 11](https://github.com/user-attachments/assets/db73482e-555d-4219-ad35-6746fd0c7edd)



## 🔮 Future Enhancements

* Multi-language plagiarism detection
* Voice-to-text submission analysis
* Blockchain-based submission authentication
* Direct LMS (Moodle / Canvas) integration
* AI-based academic integrity scoring

---

## 🧑‍💻 Contributors

* **Krishna Lagad** – Frontend & System design
* **Koyal Kembhavi** - Frontend & System design
* **Swara Deshpande** - Backend & Architechture design
* **Rucha Katte** - Full Stack & ML model
* **Gargi Joshi** - Backend & ML model
* **AI Models & Logic** – NLP + AST Analysis

---

## 📜 License

This project is licensed under the **MIT License**.

---

⭐ *If you like this project, consider starring the repository!*
