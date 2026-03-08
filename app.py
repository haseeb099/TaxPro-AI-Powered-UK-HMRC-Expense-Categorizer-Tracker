import streamlit as st
import openai
import json
import pandas as pd
from datetime import datetime
import sqlite3
import os
from dotenv import load_dotenv
import re
import io
import PyPDF2
import easyocr
from PIL import Image
import numpy as np

# ──────────────────────────────────────────────── Load environment
load_dotenv()

# ──────────────────────────────────────────────── Sidebar - Provider & Model
provider = st.sidebar.selectbox("API Provider", ["Groq (Free)", "OpenRouter (Free Credits)", "OpenAI (Paid)"])

client = None
model = None

if provider == "Groq (Free)":
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.sidebar.error("Add GROQ_API_KEY to .env → https://console.groq.com/keys")
        st.stop()
    client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    model = st.sidebar.selectbox("Model", [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama3-8b-8192"
    ])
elif provider == "OpenRouter (Free Credits)":
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        st.sidebar.error("Add OPENROUTER_API_KEY to .env → https://openrouter.ai/keys")
        st.stop()
    client = openai.OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    model = st.sidebar.selectbox("Model", [
        "deepseek/deepseek-v3.2",
        "qwen/qwen3.5-plus",
        "deepseek/deepseek-r1"
    ])
else:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.sidebar.error("Add OPENAI_API_KEY to .env")
        st.stop()
    client = openai.OpenAI(api_key=api_key)
    model = "gpt-4o-mini"

# ──────────────────────────────────────────────── System Prompt (compact)
HMRC_PROMPT = """
UK HMRC expert 2025/26–2026/27. Categorize sole trader/freelancer expenses.
One category only: Office Costs|Travel & Subsistence|Motor Expenses|Home Office|Equipment & Tools|Stock|Marketing|Professional Fees|Insurance|Staff|Clothing|Other Allowable

Return JSON **array** of objects (even for one item).
Each: {"date":"YYYY-MM-DD","description":"","category":"","amount_gbp":0.0,"business_use_percent":100,"is_deductible":true,"deductible_amount":0.0,"vat_reclaimable":null,"notes":""}
JSON only – no extra text.
"""

# ──────────────────────────────────────────────── Database
conn = sqlite3.connect("expenses.db", check_same_thread=False)
conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    description TEXT,
    category TEXT,
    amount REAL,
    business_use_percent REAL,
    deductible REAL,
    vat_reclaimable REAL,
    notes TEXT,
    timestamp TEXT,
    business_type TEXT,
    source TEXT
)''')
conn.commit()

# ──────────────────────────────────────────────── Text extraction (ALWAYS returns str)
def extract_text_from_file(uploaded_file, use_ocr=False):
    if uploaded_file is None:
        return ""

    content = ""
    file_type = uploaded_file.type
    filename = uploaded_file.name.lower()

    try:
        if file_type == "application/pdf" or filename.endswith(".pdf"):
            pdf_bytes = uploaded_file.read()
            uploaded_file.seek(0)  # reset for possible OCR
            reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    content += text + "\n"

            # Fallback OCR if little/no text extracted or forced
            if use_ocr or len(content.strip()) < 30:
                reader = easyocr.Reader(['en'], gpu=False)  # gpu=False → more stable on many machines
                # Very basic OCR – real apps would convert pages to images properly
                content += "\n[OCR not fully implemented in this simple version – install better tools if needed]"

        elif file_type.startswith("image/") or filename.endswith((".jpg", ".jpeg", ".png")):
            reader = easyocr.Reader(['en'], gpu=False)
            img = Image.open(uploaded_file)
            result = reader.readtext(np.array(img))
            content = "\n".join([det[1] for det in result])

        elif file_type in ["text/plain", "text/csv"] or filename.endswith((".txt", ".csv")):
            content = uploaded_file.read().decode("utf-8", errors="replace")

        else:
            content = f"[Unsupported file type: {file_type}]"

    except Exception as e:
        content = f"[Extraction error: {str(e)}]"

    return content.strip() or "[No text extracted]"

# ──────────────────────────────────────────────── Analyze
def analyze_expense(text: str, business_type: str):
    if not text.strip():
        return []

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": HMRC_PROMPT},
                {"role": "user", "content": f"Business: {business_type}\n\n{text[:3500]}"}
            ],
            temperature=0.0,
            max_tokens=700,
            response_format={"type": "json_object"}
        )

        raw = response.choices[0].message.content.strip()
        if raw.startswith("```json"):
            raw = raw.split("```json", 1)[1].split("```", 1)[0].strip()

        data = json.loads(raw)

        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            return data
        return []
    except Exception as e:
        st.error(f"LLM error: {str(e)[:250]}")
        return []

# ──────────────────────────────────────────────── Save
def save_expenses(items, business_type, source):
    if not items:
        return 0
    count = 0
    now = datetime.now().isoformat()
    for item in items:
        try:
            conn.execute(
                """INSERT INTO expenses
                (date, description, category, amount, business_use_percent, deductible, vat_reclaimable, notes, timestamp, business_type, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    item.get("date"),
                    item.get("description"),
                    item.get("category"),
                    item.get("amount_gbp"),
                    item.get("business_use_percent", 100),
                    item.get("deductible_amount", item.get("amount_gbp", 0)),
                    item.get("vat_reclaimable"),
                    item.get("notes"),
                    now,
                    business_type,
                    source
                )
            )
            count += 1
        except Exception as e:
            st.warning(f"Save failed for one item: {str(e)}")
    if count > 0:
        conn.commit()
    return count

# ──────────────────────────────────────────────── UI
st.title("💼 TaxPro UK Expense Categorizer & Tracker (HMRC 2025–27)")

business_type = st.selectbox("Business type", ["Freelancer", "E-commerce", "Services", "Trades", "Other"])

tab1, tab2, tab3, tab4 = st.tabs(["📥 Add / Analyze", "📋 List & Export", "📊 Dashboard", "💡 Tax Advice"])

# ─── Tab 1 ───────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Upload receipts / statements / enter cash")

    if "last_analysis" not in st.session_state:
        st.session_state.last_analysis = None

    uploaded_files = st.file_uploader(
        "Upload files (PDF, JPG, PNG, TXT, CSV)",
        type=["pdf", "jpg", "jpeg", "png", "txt", "csv"],
        accept_multiple_files=True
    )

    use_ocr = st.checkbox("Try OCR on scanned documents", value=True)

    manual_text = st.text_area("Paste receipt text or describe cash expense", height=110)

    if st.button("🔍 Analyze", type="primary"):
        combined_text = manual_text.strip()

        for f in uploaded_files or []:
            file_text = extract_text_from_file(f, use_ocr)
            if file_text:
                combined_text += "\n\n─── " + f.name + " ───\n" + file_text

        if combined_text:
            with st.spinner("Analyzing with AI..."):
                results = analyze_expense(combined_text, business_type)
                st.session_state.last_analysis = results
                if results:
                    st.success(f"Detected {len(results)} expense item(s)")
                else:
                    st.warning("No valid expenses recognized")
        else:
            st.warning("No text to analyze")

    # Show results & save button
    if st.session_state.last_analysis:
        st.subheader("Detected expenses")
        for i, exp in enumerate(st.session_state.last_analysis, 1):
            with st.expander(f"#{i}  {exp.get('description','—')}  £{exp.get('amount_gbp','?')}"):
                st.json(exp)

        if st.button("💾 Save All to Database"):
            count = save_expenses(
                st.session_state.last_analysis,
                business_type,
                source="ai-upload" if uploaded_files else "manual"
            )
            if count > 0:
                st.success(f"Saved {count} expense(s) successfully!")
                st.session_state.last_analysis = None
                st.rerun()
            else:
                st.error("Save failed – check terminal or database")

# ─── Tab 2 ───────────────────────────────────────────────────────────────
with tab2:
    try:
        df = pd.read_sql_query("SELECT * FROM expenses ORDER BY date DESC", conn)
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            col1, col2 = st.columns(2)
            col1.download_button("Download CSV", df.to_csv(index=False).encode('utf-8'), "expenses.csv")
            # col2.download_button("Download Excel", df.to_excel(index=False, engine='openpyxl'), "expenses.xlsx")  # needs openpyxl
        else:
            st.info("No expenses saved yet.")
    except Exception as e:
        st.error(f"Database read error: {e}")

# ─── Tab 3 & 4 (simple version) ─────────────────────────────────────────
with tab3:
    try:
        df = pd.read_sql_query("SELECT date, deductible FROM expenses", conn)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            st.bar_chart(df.groupby(df['date'].dt.to_period('M'))['deductible'].sum())
            st.metric("Total deductible", f"£{df['deductible'].sum():,.2f}")
        else:
            st.info("No data yet")
    except:
        st.info("No data or database issue")

with tab4:
    st.info("Tax advice & prediction coming soon… (add income tracking next?)")
    st.caption("Always verify with a qualified accountant – this is not professional advice.")

st.caption("v0.3 • Free Groq / OpenRouter • Local SQLite • OCR via EasyOCR")