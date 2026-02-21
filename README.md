# 🤖 Agentic Sales AI (SellSenseai)

**Multi-Agent AI System for Social Media Marketing**

Agentic Sales AI is a powerful, Flask-based web application designed to revolutionize social media marketing for small businesses. It leverages a multi-agent AI system powered by Google Gemini to analyze sales data, formulate marketing strategies, and generate ready-to-post content automatically.

---

## 🚀 Key Features

*   **🤖 Multi-Agent AI Architecture:**
    *   **Analyst Bot:** Analyzes sales data to identify trends, best-selling products, and customer insights.
    *   **Strategy Bot:** Develops targeted marketing campaigns based on analyst insights.
    *   **Content Bot:** Generates engaging social media posts (captions + image prompts) tailored to your brand voice.
*   **🧠 Google Gemini Integration:** Uses the advanced reasoning capabilities of Google's Gemini models (100% Free Tier compatible).
*   **📊 Real-time Dashboard:** Visualize sales performance, campaign status, and engagement metrics in a modern dark-themed UI.
*   **⚡ n8n Workflow Automation:** Built-in integration support for n8n to automate the flow of data between agents and external platforms.
*   **📈 Sales Analytics:** Detailed breakdown of revenue, items sold, and week-over-week performance.
*   **📱 Campaign Management:** Create, track, and manage marketing campaigns directly from the dashboard.

---

## 🛠 Tech Stack

*   **Backend:** Python, Flask
*   **Database:** SQLAlchemy (SQLite default, scalable to PostgreSQL)
*   **AI Engine:** Google Generative AI (Gemini)
*   **Authentication:** Flask-Login
*   **Frontend:** HTML5, CSS3, JavaScript (Jinja2 Templates)
*   **Automation:** n8n (Workflows included in `n8n_workflows/`)
*   **Environment:** managed via `.env`

---

## 📂 Project Structure

```
SellSenseai/
├── app.py                 # Main application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
├── ai_services/           # Logic for interacting with Google Gemini
├── api/                   # API Blueprint definitions
│   ├── analyst_bot.py     # AI Agent: Data Analysis
│   ├── strategy_bot.py    # AI Agent: Strategy Formulation
│   ├── content_bot.py     # AI Agent: Content Generation
│   └── ...                # Other API endpoints
├── database/              # Database models and initialization
├── n8n_workflows/         # JSON workflows for n8n automation
├── static/                # CSS, JS, and image assets
└── templates/             # HTML templates
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
*   Python 3.8 or higher
*   Git

### 2. Installation

Clone the repository and navigate to the project folder:

```bash
cd SellSenseai
```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the root directory and add your Google Gemini API key:

```env
GOOGLE_GEMINI_API_KEY=your_api_key_here
FLASK_APP=app.py
FLASK_ENV=development
```

> **Note:** You can get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### 4. Running the Application

Initialize the database and start the server:

```bash
python app.py
```

Open your browser and navigate to:
**http://localhost:5000**

---

## 🎮 Demo & Usage

Once the application is running, you can access specific demo pages designed for hackathon presentations:

*   **Main Dashboard:** `http://localhost:5000` (Login/Signup required)
*   **Live AI Demo:** `http://localhost:5000/demo/live` - Watch the agents work in real-time.
*   **Architecture View:** `http://localhost:5000/demo/architecture` - Visual breakdown of the system.

### How to Use:
1.  **Sign Up:** Create an account with your business details (Niche, Target Audience, Brand Voice).
2.  **Dashboard:** View your simulated sales data.
3.  **Generate Campaign:** Go to the "Campaigns" tab and click "New Campaign".
4.  **Watch the Magic:** The AI Agents will analyze your data, propose a strategy, and generate content.

---

## 🤝 Contribution

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.