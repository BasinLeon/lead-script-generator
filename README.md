# ✍️ Lead Script Generator

> **Basin OS Component: Narrative Engine (Hunter)**  
> Transform raw leads into personalized, high-converting outreach scripts.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

---

## 🎯 What It Does

The Lead Script Generator takes your raw lead data and automatically generates:

- **Personalized Email Subjects** — Attention-grabbing, tailored to company type
- **Custom Email Bodies** — Written to match company DNA and pain points  
- **LinkedIn Messages** — Under 300 characters, ready to send

## 🧬 Intelligent Classification

### Priority Levels

| Priority | Criteria |
|----------|----------|
| **P1 - Hot** | C-level, VP, Director with decision authority |
| **P2 - Warm** | Senior managers, leads with influence |
| **P3 - Nurture** | Good fit, needs education or timing |

### Company DNA Profiles

| Profile | Size | Tone |
|---------|------|------|
| **High-Growth Startup** | <50 employees | Energetic, bold |
| **Mid-Market** | 50-500 employees | Balanced, consultative |
| **Enterprise** | 500+ employees | Professional, strategic |
| **Agency/Consultancy** | Service-based | Collaborative, expert |

---

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/BasinLeon/lead-script-generator.git
cd lead-script-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy `app.py`

---

## 📊 CSV Format

Your lead CSV should include these columns (flexible naming supported):

| Column | Aliases | Required |
|--------|---------|----------|
| `first_name` | `name`, `firstname` | ✅ |
| `company` | `company_name`, `organization` | ✅ |
| `title` | `job_title`, `position` | ✅ |
| `email` | `email_address` | Optional |
| `linkedin` | `linkedin_url`, `profile_url` | Optional |
| `employees` | `company_size`, `size` | Optional |

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Data Processing:** Pandas
- **Deployment:** Streamlit Cloud

---

## 📁 Project Structure

```
lead-script-generator/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── sample_leads.csv    # Example lead data
├── .gitignore
└── README.md
```

---

## 🔗 Part of Basin OS

This tool is part of the **Basin OS** revenue operations stack:

| Component | Type | Purpose |
|-----------|------|---------|
| [GTM Signal Architect](https://github.com/BasinLeon/gtm-signal-architect) | Data (Architect) | Signal detection & lead scoring |
| **Lead Script Generator** | Narrative (Hunter) | Personalized outreach generation |

---

## 👤 Author

**Leon Basin**  
Revenue Operations Architect

- GitHub: [@BasinLeon](https://github.com/BasinLeon)
- LinkedIn: [leonbasin](https://linkedin.com/in/leonbasin)
- Website: [basinleon.com](https://basinleon.com)

---

## 📄 License

MIT License - feel free to use and modify for your own outreach needs.
