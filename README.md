# 📊 Strategy Intelligence Tool

### **AI-Powered Multi-Agent Business Strategy Generator (Local Ollama Version)**

The **Strategy Intelligence Tool** is a streamlined, multi-agent business strategy generator that runs entirely on your **local machine** using **Ollama LLMs** (no API keys required). It executes a structured reasoning pipeline — **Analyst → Consultant → Strategist** — to create actionable, boardroom-ready strategy reports.

---

## 🚀 Features

### 🧠 Multi-Agent Pipeline

* **Analyst** — Extracts market insights
* **Consultant** — Produces critique and structured business analysis
* **Strategist** — Generates a final actionable roadmap

### 🔐 100% Local (Runs on Your Machine)

* Powered by **Ollama** models
* No API keys required
* Zero cloud dependency
* Privacy-friendly

### 📄 Professional Output

* Market insights
* SWOT/PESTEL-style analysis
* Strategy roadmap
* Final assembled report

### 🎨 Clean Strategy-Themed UI

* Modern Streamlit interface
* Sidebar with pipeline explanation
* Simple input and rich output display

---

## 📦 Installation

### 1. Install Streamlit

```bash
pip install streamlit
```

### 2. Install LangGraph and Required Packages

```bash
pip install langgraph langchain-community
```

### 3. Install Ollama

Download and install from:
[https://ollama.com/download](https://ollama.com/download)

### 4. Pull a Model

```bash
ollama pull mistral
```

(You may use any supported model.)

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📝 How to Use

1. Launch the Streamlit app.
2. Enter a business query, such as:

   * "Market expansion strategy for a fintech startup"
   * "How should a mid-size retail brand move into e-commerce?"
3. Wait for the three-agent pipeline to complete.
4. Receive a polished, structured strategy report.

---

## 📁 Project Structure

```
.
├── app.py                     # Streamlit UI
├── business_strategy_graph.py # LangGraph multi-agent pipeline
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

---

## 🧩 Pipeline Architecture (LangGraph)

### 1. Analyst Agent

* Conducts initial assessment
* Extracts trends, insights, and context

### 2. Consultant Agent

* Generates SWOT and PESTEL-style reasoning
* Identifies risks, opportunities, and industry impacts

### 3. Strategist Agent

* Produces short-term to long-term roadmap
* Defines KPIs, actionable steps, and resource requirements

### 4. Report Compiler

* Formats and assembles final markdown output

---

## 🎯 Suitable For

* Business strategy teams
* Consultants
* Startup founders
* Product managers
* Investors preparing briefs
* Anyone needing structured strategic thinking

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

