# TaxPro-AI: HMRC-Compliant Expense Categorizer & Tracker

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B)](https://streamlit.io/)
![HMRC Compliant](https://img.shields.io/badge/HMRC-2025%2F26--2026%2F27-orange)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered application designed for UK sole traders, freelancers, and self-employed individuals to streamline expense categorization and tracking in compliance with HMRC guidelines. TaxPro-AI leverages advanced AI models to process receipts, categorize expenditures, and provide actionable insights for Self Assessment tax returns.

## ✨ Features

-   **HMRC-Aligned AI Categorization**: Utilizes AI to categorize expenses based on current HMRC allowable rules (2025/26–2026/27), including categories such as Office Costs, Travel & Subsistence, Motor Expenses, Home Office, Equipment & Tools, Stock, Marketing, Professional Fees, Insurance, Staff, Clothing, and Other Allowable expenses.
-   **Multi-source Input**: Supports various input methods for expense data:
    -   PDF receipts/statements (with text extraction and basic OCR fallback)
    -   Image uploads (JPG/PNG) with EasyOCR text extraction
    -   Manual entry for cash expenses or text descriptions
-   **Smart JSON Output**: AI models extract key expense details into a structured JSON format, including date, description, category, amount_gbp, business_use_%, deductible_amount, VAT reclaimable, and notes.
-   **Local SQLite Database**: Ensures persistent tracking of all saved expenses, including timestamp, business type, and source, stored securely in a local database.
-   **Interactive Interface**: Features an intuitive Streamlit interface with dedicated tabs for:
    -   📥 **Add / Analyze**: Upload and AI-process new expenses.
    -   📋 **List & Export**: View and export expense data (DataFrame + CSV download).
    -   📊 **Dashboard**: Visualize monthly deductible expenses and total summaries.
    -   💡 **Tax Advice**: A placeholder for future expansion into personalized tax guidance.
-   **Flexible LLM Backends**: Supports various Large Language Model (LLM) providers for AI processing, offering cost-effective and high-performance options:
    -   Groq (e.g., Llama 3.1/3.3 models) for rapid processing.
    -   OpenRouter (e.g., DeepSeek, Qwen) for diverse model access.
    -   OpenAI (e.g., gpt-4o-mini) for robust AI capabilities.

## 🚀 Getting Started

### Prerequisites

-   Python 3.10+
-   `pip` package manager

### Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/haseeb099/TaxPro-AI-Powered-UK-HMRC-Expense-Categorizer-Tracker.git
    cd TaxPro-AI-Powered-UK-HMRC-Expense-Categorizer-Tracker
    ```

2.  **Create a virtual environment**:

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    *Note: If `requirements.txt` is missing, create it with the following content:*

    ```
    streamlit
    openai
    python-dotenv
    pandas
    PyPDF2
    easyocr
    pillow
    numpy
    ```

    *(Optional: Install `torch` for GPU acceleration with EasyOCR if available.)*

4.  **Set up API key(s)**:

    Create a `.env` file in the root directory of the project and add your API key(s) for your chosen LLM backend. Example:

    ```ini
    GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # or
    OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxx
    # or
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
    ```

5.  **Run the application**:

    ```bash
    streamlit run app.py
    ```

    The application will open in your web browser at `http://localhost:8501`.

## ⚠️ Important Notes & Limitations

-   **Not Professional Tax Advice**: This tool is for informational purposes only and should not be considered professional tax advice. Always verify categories, amounts, and deductibility with a qualified accountant or HMRC. Tax rules are subject to change.
-   **Database Persistence**: The local `expenses.db` does not persist on ephemeral file systems (e.g., Streamlit Cloud). For production deployments, consider using a persistent cloud database solution like Supabase or PostgreSQL.
-   **OCR Limitations**: The basic EasyOCR implementation may require better preprocessing or conversion of scanned PDFs to images for optimal results. This is an area for future improvement.
-   **Token Limits**: Input text is truncated to approximately 3500 characters, suitable for single receipts but less ideal for very long statements.
-   **No User Authentication**: Currently, this is a single-user local application without built-in user authentication.

## 📈 Roadmap & Future Enhancements

-   **Cloud Database Integration**: Implement persistent cloud database solutions (e.g., Supabase free tier, SQLite on mounted volumes).
-   **Mileage Calculator**: Develop a comprehensive mileage calculator based on HMRC rates (45p/25p).
-   **Income Tracking & Self Assessment Preview**: Introduce income tracking features and a basic Self Assessment preview (profit, tax estimate).
-   **Advanced PDF OCR**: Enhance PDF processing with page-by-page image conversion and layout analysis for improved OCR accuracy.
-   **VAT Handling**: Improve VAT reclaim logic (e.g., 20% reclaim per category).
-   **Multi-user Support**: Implement user authentication and multi-user capabilities.
-   **Export Options**: Add export functionality to Excel and HMRC-compatible CSV formats.
-   **Model Optimization**: Continuously refine LLM prompts and explore additional models for higher accuracy and performance.

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and ensure tests pass (if applicable).
4.  Submit a pull request. Please use conventional commits (e.g., `feat:`, `fix:`, `docs:`) if possible.

Areas where contributions are particularly valuable:

-   Improving OCR reliability.
-   Adding more HMRC-specific prompts and rules.
-   Implementing income/tax estimate features.
-   Developing comprehensive tests (e.g., using `pytest`).
-   Enhancing UI polish and adding loading indicators.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Built with ❤️ for UK freelancers & sole traders. If this project helps you, please consider starring the repository! For questions or issues, feel free to open an issue.

Happy tracking & lower taxes! 🇬🇧💰
