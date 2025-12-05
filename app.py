"""
Lead Script Generator - Narrative Engine
=========================================
A Streamlit application that transforms raw lead data into
personalized, high-converting outreach scripts.

Basin OS Component: Narrative (Hunter)
Author: Leon Basin
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

COMPANY_DNA_PROFILES = {
    "High-Growth Startup": {
        "pain_points": ["scaling quickly", "resource constraints", "proving product-market fit"],
        "values": ["speed", "innovation", "disruption"],
        "tone": "energetic and bold"
    },
    "Enterprise": {
        "pain_points": ["legacy systems", "cross-team alignment", "compliance requirements"],
        "values": ["stability", "proven solutions", "risk mitigation"],
        "tone": "professional and strategic"
    },
    "Mid-Market": {
        "pain_points": ["growing pains", "process optimization", "competitive pressure"],
        "values": ["efficiency", "growth", "partnership"],
        "tone": "balanced and consultative"
    },
    "Agency/Consultancy": {
        "pain_points": ["client delivery", "billable utilization", "differentiation"],
        "values": ["expertise", "client success", "innovation"],
        "tone": "collaborative and expert"
    }
}

PRIORITY_CRITERIA = {
    "P1 - Hot": "Decision maker at target company with active buying signals",
    "P2 - Warm": "Right persona, good company fit, no immediate signals",
    "P3 - Nurture": "Good fit but needs education or timing alignment"
}

# ============================================================================
# SCRIPT GENERATION ENGINE
# ============================================================================

def detect_company_dna(row):
    """Automatically detect company DNA based on available data."""
    company = str(row.get('company', '')).lower()
    title = str(row.get('title', '')).lower()
    employees = row.get('employees', row.get('company_size', ''))
    
    # Size-based detection
    if employees:
        try:
            emp_count = int(str(employees).replace(',', '').replace('+', ''))
            if emp_count < 50:
                return "High-Growth Startup"
            elif emp_count < 500:
                return "Mid-Market"
            else:
                return "Enterprise"
        except:
            pass
    
    # Keyword-based detection
    if any(word in company for word in ['consulting', 'agency', 'partners', 'group']):
        return "Agency/Consultancy"
    if any(word in company for word in ['inc', 'corp', 'global', 'international']):
        return "Enterprise"
    
    return "Mid-Market"  # Default

def assign_priority(row):
    """Assign priority based on title and signals."""
    title = str(row.get('title', '')).lower()
    
    # P1: C-level, VP, Director with decision authority
    if any(level in title for level in ['ceo', 'cro', 'cmo', 'coo', 'chief', 'vp', 'vice president', 'head of']):
        return "P1 - Hot"
    
    # P2: Senior managers and directors
    if any(level in title for level in ['director', 'senior', 'manager', 'lead']):
        return "P2 - Warm"
    
    # P3: Everyone else
    return "P3 - Nurture"

def generate_email_subject(row, company_dna, value_prop):
    """Generate personalized email subject line."""
    first_name = row.get('first_name', row.get('name', 'there').split()[0])
    company = row.get('company', 'your team')
    
    subjects = {
        "High-Growth Startup": [
            f"{first_name} - scaling {company}'s revenue engine?",
            f"Quick win for {company}'s growth",
            f"{first_name}, {company} + {value_prop}?"
        ],
        "Enterprise": [
            f"Strategic alignment: {company} revenue operations",
            f"{first_name} - optimizing {company}'s GTM execution",
            f"Enterprise {value_prop} for {company}"
        ],
        "Mid-Market": [
            f"{first_name} - {company}'s next growth lever",
            f"Helping {company} scale smarter",
            f"{first_name}, quick question about {company}"
        ],
        "Agency/Consultancy": [
            f"Partnership opportunity: {company}",
            f"{first_name} - elevating {company}'s client outcomes",
            f"For {company}: {value_prop}"
        ]
    }
    
    return subjects.get(company_dna, subjects["Mid-Market"])[0]

def generate_email_body(row, company_dna, value_prop, sender_name):
    """Generate personalized email body."""
    first_name = row.get('first_name', row.get('name', 'there').split()[0])
    company = row.get('company', 'your company')
    title = row.get('title', 'your role')
    
    profile = COMPANY_DNA_PROFILES.get(company_dna, COMPANY_DNA_PROFILES["Mid-Market"])
    pain = profile["pain_points"][0]
    
    templates = {
        "High-Growth Startup": f"""Hi {first_name},

Saw {company} is making moves — congrats on the momentum.

I've been helping fast-growing teams like yours solve {pain} through {value_prop}. The results: faster pipeline, cleaner data, and sales teams that actually trust their CRM.

Would a 15-minute call this week make sense? Happy to share a quick framework that's worked for similar companies.

Best,
{sender_name}""",

        "Enterprise": f"""Hi {first_name},

I've been following {company}'s trajectory and wanted to reach out with a relevant observation.

Many enterprise revenue leaders I work with are navigating {pain} while trying to drive predictable growth. I specialize in {value_prop} — helping teams like yours turn operational complexity into competitive advantage.

Would you be open to a brief conversation to explore alignment?

Best regards,
{sender_name}""",

        "Mid-Market": f"""Hi {first_name},

Quick note — I work with mid-market companies like {company} on {value_prop}.

The common challenge I see: {pain}. The solution doesn't have to be complex.

If this resonates, I'd love to share a framework that's helped similar teams. 15 minutes — no pitch, just value.

Best,
{sender_name}""",

        "Agency/Consultancy": f"""Hi {first_name},

I came across {company} and was impressed by your work.

I partner with agencies and consultancies on {value_prop} — specifically helping with {pain}. It's often the difference between good delivery and exceptional client outcomes.

Would you be open to a quick conversation about how we might collaborate?

Best,
{sender_name}"""
    }
    
    return templates.get(company_dna, templates["Mid-Market"])

def generate_linkedin_message(row, company_dna, value_prop):
    """Generate LinkedIn connection message (under 300 chars)."""
    first_name = row.get('first_name', row.get('name', 'there').split()[0])
    company = row.get('company', 'your company')
    
    messages = {
        "High-Growth Startup": f"Hi {first_name} — impressed by {company}'s growth. I work on {value_prop} for scaling teams. Would love to connect and share ideas.",
        "Enterprise": f"Hi {first_name} — I help enterprise revenue teams with {value_prop}. Your work at {company} caught my attention. Let's connect.",
        "Mid-Market": f"Hi {first_name} — {company} looks like a great fit for some ideas I have on {value_prop}. Would love to connect.",
        "Agency/Consultancy": f"Hi {first_name} — I partner with agencies on {value_prop}. {company}'s approach resonates. Let's connect?"
    }
    
    msg = messages.get(company_dna, messages["Mid-Market"])
    return msg[:295] + "..." if len(msg) > 300 else msg

def process_leads(df, value_prop, sender_name, auto_detect_dna=True):
    """Process leads and generate all scripts."""
    results = []
    
    for idx, row in df.iterrows():
        # Normalize column names (handle various CSV formats)
        row_dict = {k.lower().replace(' ', '_'): v for k, v in row.items()}
        
        # Extract core fields with fallbacks
        lead_data = {
            'first_name': row_dict.get('first_name', row_dict.get('firstname', row_dict.get('name', 'there').split()[0] if row_dict.get('name') else 'there')),
            'last_name': row_dict.get('last_name', row_dict.get('lastname', '')),
            'company': row_dict.get('company', row_dict.get('company_name', row_dict.get('organization', 'Unknown'))),
            'title': row_dict.get('title', row_dict.get('job_title', row_dict.get('position', ''))),
            'email': row_dict.get('email', row_dict.get('email_address', '')),
            'linkedin': row_dict.get('linkedin', row_dict.get('linkedin_url', row_dict.get('profile_url', ''))),
            'employees': row_dict.get('employees', row_dict.get('company_size', row_dict.get('size', '')))
        }
        
        # Assign DNA and Priority
        company_dna = detect_company_dna(lead_data) if auto_detect_dna else row_dict.get('company_dna', 'Mid-Market')
        priority = assign_priority(lead_data)
        
        # Generate scripts
        result = {
            'First Name': lead_data['first_name'],
            'Last Name': lead_data['last_name'],
            'Company': lead_data['company'],
            'Title': lead_data['title'],
            'Email': lead_data['email'],
            'LinkedIn': lead_data['linkedin'],
            'Priority': priority,
            'Company DNA': company_dna,
            'Email Subject': generate_email_subject(lead_data, company_dna, value_prop),
            'Email Body': generate_email_body(lead_data, company_dna, value_prop, sender_name),
            'LinkedIn Message': generate_linkedin_message(lead_data, company_dna, value_prop)
        }
        results.append(result)
    
    return pd.DataFrame(results)

# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    st.set_page_config(
        page_title="Lead Script Generator",
        page_icon="✍️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            font-size: 1.1rem;
            color: #6b7280;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
        }
        .stDownloadButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<p class="main-header">✍️ Lead Script Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform raw leads into personalized, high-converting outreach scripts</p>', unsafe_allow_html=True)
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        sender_name = st.text_input(
            "Your Name",
            value="Leon Basin",
            help="This will appear in email signatures"
        )
        
        value_prop = st.text_input(
            "Your Value Proposition",
            value="revenue operations optimization",
            help="What you help companies achieve"
        )
        
        auto_detect = st.checkbox(
            "Auto-detect Company DNA",
            value=True,
            help="Automatically categorize companies based on size and signals"
        )
        
        st.divider()
        
        st.header("📊 Priority Guide")
        for priority, desc in PRIORITY_CRITERIA.items():
            st.markdown(f"**{priority}**")
            st.caption(desc)
        
        st.divider()
        
        st.header("🧬 Company DNA Profiles")
        for dna, profile in COMPANY_DNA_PROFILES.items():
            with st.expander(dna):
                st.caption(f"Tone: {profile['tone']}")
                st.caption(f"Pain points: {', '.join(profile['pain_points'])}")
    
    # Main Content
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "📋 Preview Scripts", "📖 How It Works"])
    
    with tab1:
        st.subheader("Upload Your Lead List")
        
        uploaded_file = st.file_uploader(
            "Drop your CSV file here",
            type=['csv'],
            help="CSV should include: name/first_name, company, title, email (optional: linkedin, employees)"
        )
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ Loaded {len(df)} leads")
                
                # Preview raw data
                with st.expander("Preview Raw Data"):
                    st.dataframe(df.head(10), use_container_width=True)
                
                # Process button
                if st.button("🚀 Generate Scripts", type="primary", use_container_width=True):
                    with st.spinner("Generating personalized scripts..."):
                        results_df = process_leads(df, value_prop, sender_name, auto_detect)
                        st.session_state['results'] = results_df
                        st.success(f"✅ Generated scripts for {len(results_df)} leads!")
                
                # Show results if available
                if 'results' in st.session_state:
                    results_df = st.session_state['results']
                    
                    # Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Leads", len(results_df))
                    with col2:
                        p1_count = len(results_df[results_df['Priority'] == 'P1 - Hot'])
                        st.metric("P1 - Hot", p1_count)
                    with col3:
                        p2_count = len(results_df[results_df['Priority'] == 'P2 - Warm'])
                        st.metric("P2 - Warm", p2_count)
                    with col4:
                        p3_count = len(results_df[results_df['Priority'] == 'P3 - Nurture'])
                        st.metric("P3 - Nurture", p3_count)
                    
                    st.divider()
                    
                    # Download button
                    csv_buffer = io.StringIO()
                    results_df.to_csv(csv_buffer, index=False)
                    
                    st.download_button(
                        label="📥 Download Results CSV",
                        data=csv_buffer.getvalue(),
                        file_name=f"lead_scripts_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    with tab2:
        if 'results' in st.session_state:
            results_df = st.session_state['results']
            
            # Filter by priority
            priority_filter = st.selectbox(
                "Filter by Priority",
                ["All"] + list(PRIORITY_CRITERIA.keys())
            )
            
            if priority_filter != "All":
                filtered_df = results_df[results_df['Priority'] == priority_filter]
            else:
                filtered_df = results_df
            
            # Display each lead
            for idx, row in filtered_df.iterrows():
                with st.expander(f"**{row['First Name']} {row['Last Name']}** — {row['Company']} ({row['Priority']})"):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown(f"**Title:** {row['Title']}")
                        st.markdown(f"**DNA:** {row['Company DNA']}")
                        st.markdown(f"**Priority:** {row['Priority']}")
                        if row['Email']:
                            st.markdown(f"**Email:** {row['Email']}")
                    
                    with col2:
                        st.markdown("**📧 Email Subject:**")
                        st.code(row['Email Subject'], language=None)
                        
                        st.markdown("**📝 Email Body:**")
                        st.text_area("", row['Email Body'], height=200, key=f"email_{idx}", disabled=True)
                        
                        st.markdown("**💼 LinkedIn Message:**")
                        st.text_area("", row['LinkedIn Message'], height=100, key=f"li_{idx}", disabled=True)
        else:
            st.info("👆 Upload and process a CSV file first to preview scripts")
    
    with tab3:
        st.subheader("How the Lead Script Generator Works")
        
        st.markdown("""
        ### 1️⃣ Upload Your Lead List
        Upload a CSV with your raw leads. The system handles various column formats automatically.
        
        **Supported columns:** `name`, `first_name`, `last_name`, `company`, `title`, `email`, `linkedin`, `employees`
        
        ### 2️⃣ Automatic Classification
        Each lead is automatically classified by:
        - **Priority Level** (P1/P2/P3) based on title and seniority
        - **Company DNA** based on company size and characteristics
        
        ### 3️⃣ Personalized Script Generation
        For each lead, the system generates:
        - **Email Subject Line** — Personalized, attention-grabbing
        - **Email Body** — Tailored to company DNA and pain points
        - **LinkedIn Message** — Under 300 characters, connection-ready
        
        ### 4️⃣ Export & Execute
        Download your ready-to-use scripts and start your outreach campaign.
        
        ---
        
        ### 🧬 Company DNA Profiles
        
        | Profile | Characteristics | Tone |
        |---------|----------------|------|
        | **High-Growth Startup** | <50 employees, scaling fast | Energetic, bold |
        | **Mid-Market** | 50-500 employees, growing | Balanced, consultative |
        | **Enterprise** | 500+ employees, established | Professional, strategic |
        | **Agency/Consultancy** | Service-based, client-focused | Collaborative, expert |
        
        ---
        
        *Built by Leon Basin — Part of the Basin OS Revenue Operations Stack*
        """)
    
    # Footer
    st.divider()
    st.caption("Lead Script Generator v1.0 | Basin OS — Narrative Engine | Built with Streamlit")

if __name__ == "__main__":
    main()
