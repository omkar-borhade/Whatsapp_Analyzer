# 📊 WhatsApp Chat Analyzer  

A simple tool to analyze **WhatsApp chat exports** and generate insights like message frequency, most active users, word clouds, and more.  

---
💻 project Link:-
 https://whatsappanalyzer-ayczz6ikwwafxyxjcpdappc.streamlit.app/

## ✨ Features
- 📅 **Timeline Analysis** – messages per day, month, or year  
- 👥 **User Statistics** – most active users, message counts  
- 🕐 **Activity Heatmap** – when users are most active (hours/days)  
- 🔤 **Word Cloud** – most frequently used words  
- 😂 **Emoji Analysis** – most used emojis in conversations  
- 📈 **Visualizations** – interactive charts for better understanding  

--
## 📋 How to Export WhatsApp Chat

Open WhatsApp

Select a chat → Tap More → Export Chat

Choose Without Media for best performance

Save the .txt file and place it inside the data/ folder

--

## 🚀 Getting Started  

1. Clone the Repository  
```bash
git clone https://github.com/omkar-borhade/Whatsapp_Analyzer.git
cd Whatsapp_Analyzer

2. Install Dependencies
pip install -r requirements.txt
3. Run the App
streamlit run main.py

📂 Project Structure
```
Whatsapp_Analyzer/
│── main.py               # Streamlit app entry point
│── preprocess.py        # Preprocessing of WhatsApp chat text
│── helper.py            # Functions for stats & visualizations
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation
├── data/                # Place your exported chat file here
├──p1.ipynb
├──.gitignore
├── .python-version
├── README.md
├── pyproject.toml
├── requirements.txt
└── uv.lock


```
🛠️ Tech Stack

Python 🐍

Streamlit – for interactive web app

Matplotlib / Seaborn – visualizations

WordCloud – for generating word clouds