# AI pOWERED TaxPro-UK-HMRC-Expense-Categorizer-Tracker
AI-powered UK expense tracker: HMRC-compliant categorization, OCR receipt scanning, spending insights &amp; tax estimates for Self Assessment. Built with Streamlit — save on taxes easily!

# 💼 TaxPro UK – HMRC Expense Categorizer & Tracker

**AI-powered Streamlit app for UK sole traders, freelancers & self-employed**  
Upload receipts (PDF/image), paste text, or describe cash spends → AI analyzes & categorizes expenses according to **current HMRC allowable rules** → saves to local database → view, export & get basic tax insights.

Designed to help reduce your Self Assessment tax bill by identifying **deductible amounts** intelligently — while keeping everything local and free (Groq / OpenRouter support).

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B)](https://streamlit.io/)
![HMRC Compliant](https://img.shields.io/badge/HMRC-2025%2F26--2026%2F27-orange)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Live Demo** (once deployed): https://taxpro-uk-hmrc-expense-categorizer-tracker.streamlit.app/

**Current version**: v0.3 • Local SQLite • Multi-LLM support

## ✨ Core Features

- **HMRC-aligned AI Categorization** (2025/26–2026/27 rules)  
  One category per item from official-style list:  
  `Office Costs | Travel & Subsistence | Motor Expenses | Home Office | Equipment & Tools | Stock | Marketing | Professional Fees | Insurance | Staff | Clothing | Other Allowable`

- **Multi-source Input**  
  • Upload PDF receipts/statements (text + basic OCR fallback)  
  • Upload images (JPG/PNG) → EasyOCR text extraction  
  • Paste raw text or describe cash expenses manually

- **Smart JSON Output from LLM**  
  Extracts: date, description, category, amount_gbp, business_use_%, deductible_amount, VAT reclaimable, notes

- **Local SQLite Database**  
  Persistent tracking of all saved expenses + timestamp + business type + source

- **Interactive Tabs**  
  • 📥 Add / Analyze (upload + AI)  
  • 📋 List & Export (DataFrame + CSV download)  
  • 📊 Dashboard (monthly deductible bar chart + total)  
  • 💡 Tax Advice (placeholder - expand later)

- **Flexible LLM Backends** (all free/low-cost options)  
  • Groq (very fast & free tier) → Llama 3.1/3.3 models  
  • OpenRouter (free credits) → DeepSeek, Qwen, etc.  
  • OpenAI (paid) → gpt-4o-mini

## 📸 Screenshots
<img width="627" height="544" alt="TaxPro" src="https://github.com/user-attachments/assets/5fceffec-05e9-4de2-90a6-6a331de56dbe" />

## 🚀 Quick Start (Local)

1. **Clone the repo**
   ```bash
   git clone https://github.com/haseeb099/TaxPro-UK-HMRC-Expense-Categorizer-Tracker.git
   cd TaxPro-UK-HMRC-Expense-Categorizer-Tracker

Create virtual environment Bash python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
Install dependencies Bash pip install -r requirements.txt(Create requirements.txt if missing  see below)

# Set up API key(s)
Create .env file in root:textGROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
# or
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxx
# or
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

Run the app Bash streamlit run app.py→ Open http://localhost:8501


## 🛠 Requirements (requirements.txt)
-   streamlit
-   openai
-   python-dotenv
-   pandas
-   PyPDF2
-   easyocr
-   pillow
-   numpy

(Optional extras: torch if you want GPU OCR acceleration with EasyOCR)

⚠️ Important Notes & Limitations
--------------------------------

-   **Not professional tax advice** --- Always verify categories, amounts and deductibility with a qualified accountant or HMRC. Rules change; this uses simplified 2025/26--2026/27 logic.
-   **Database**: Local expenses.db --- does **not persist** on Streamlit Cloud (ephemeral filesystem). Use cloud DB (Supabase, PostgreSQL) for production.
-   **OCR**: Basic EasyOCR implementation. Scanned PDFs may need better preprocessing/conversion to images (future improvement).
-   **Token limits**: Truncates input to ~3500 chars --- good for single receipts, less ideal for long statements.
-   **No user auth yet** --- single-user local app for now.

📈 Roadmap & Future Enhancements
--------------------------------

-   Persistent cloud database (Supabase free tier / SQLite on mounted volume)
-   Full mileage calculator (HMRC 45p/25p rates)
-   Income tracking → basic Self Assessment preview (profit, tax estimate)
-   Better PDF OCR (page-by-page image conversion + layout analysis)
-   VAT handling improvements (20% reclaim logic per category)
-   Multi-user support + simple login
-   Export to Excel + HMRC-compatible CSV format
-   More models + prompt engineering for higher accuracy

🤝 Contributing
---------------

Love to have help! Especially:

-   Improve OCR reliability
-   Add more HMRC-specific prompts/rules
-   Implement income/tax estimate tab
-   Tests (pytest)
-   UI polish & loading indicators

Fork → branch → PR Use conventional commits if possible (feat:, fix:, docs:, etc.)

📄 License
----------

MIT License --- free to use, modify, distribute. See LICENSE file.

* * * * *

Built with ❤️ for UK freelancers & sole traders --- save time & money this tax season!

⭐ If it helps you --- star the repo! Questions → open an issue.

Happy tracking & lower taxes! 🇬🇧💰



```
