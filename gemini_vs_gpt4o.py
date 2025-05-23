import json
from fpdf import FPDF
import sqlite3

# Data as if it were SQL records
data = [
    {"category": "Languages Used", "gemini": "Python, C++, Go, Java", "gpt_4o": "Python, C++, JavaScript, more"},
    {"category": "ML Framework", "gemini": "TensorFlow, JAX/Flax", "gpt_4o": "PyTorch"},
    {"category": "Hardware", "gemini": "Google TPUs", "gpt_4o": "NVIDIA GPUs (e.g., A100, H100)"},
    {"category": "Training Infra", "gemini": "Google Cloud, TPU pods", "gpt_4o": "Azure Cloud, GPU clusters"},
    {"category": "API Access", "gemini": "Google AI Studio, Vertex AI, Gemini API", "gpt_4o": "OpenAI Platform API, GPTs, plugins"},
    {"category": "Ecosystem", "gemini": "Embedded in Google Search, Bard, Android", "gpt_4o": "Cross-platform, open customization"},
]

# Markdown table generation
markdown_table = "| " + " | ".join(["Category", "Google Gemini", "OpenAI ChatGPT (GPT-4o)"]) + " |\n"
markdown_table += "|---" * 3 + "|\n"
for row in data:
    markdown_table += "| " + " | ".join([row["category"], row["gemini"], row["gpt_4o"]]) + " |\n"

# Save to a Markdown file
with open("gemini_vs_gpt4o.md", "w") as f:
    f.write(markdown_table)

# JSON generation
json_data = {"comparison": data}
with open("gemini_vs_gpt4o.json", "w") as f:
    json.dump(json_data, f, indent=4)

# Create PDF using FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 14)
pdf.cell(200, 10, "Gemini vs GPT-4o: Technical Comparison (by FallguyAI)", ln=True, align="C")
pdf.ln(10)
pdf.set_font("Arial", size=10)

# Adding table rows to PDF
for row in data:
    row_text = f"{row['category']} | {row['gemini']} | {row['gpt_4o']}"
    pdf.multi_cell(0, 8, row_text)

# Save PDF file
pdf.output("gemini_vs_gpt4o.pdf")

# Connect to a new SQLite database file
conn = sqlite3.connect("gemini_vs_gpt4o.db")
c = conn.cursor()

# Create table
c.execute("""
    CREATE TABLE IF NOT EXISTS comparison (
        category TEXT,
        gemini TEXT,
        gpt_4o TEXT
    )
""")

# Clear old entries (optional, so re-running doesn't duplicate)
c.execute("DELETE FROM comparison")

# Insert rows
for row in data:
    c.execute("INSERT INTO comparison (category, gemini, gpt_4o) VALUES (?, ?, ?)", 
              (row["category"], row["gemini"], row["gpt_4o"]))

# Commit and close
conn.commit()
conn.close()
