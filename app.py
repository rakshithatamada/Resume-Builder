import streamlit as st
from fpdf import FPDF

def sanitize_text(text):
    if not text:
        return ""
    replacements = {
        '\u2013': '-', '\u2014': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '-', '\xa0': ' '
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", 'B', 16)
        self.cell(0, 10, self.title.upper(), ln=True, align='C')  
        self.ln(5)

    def section_title(self, title):
        self.set_font("Helvetica", 'B', 14)
        self.set_text_color(0, 0, 0)  # Section titles in black
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)

    def section_body(self, body):
        self.set_font("Helvetica", size=12)
        self.multi_cell(0, 10, sanitize_text(body))
        self.ln(2)

def create_resume_pdf(data):
    pdf = PDF()
    pdf.title = data['name']
    pdf.add_page()

    # Contact Information
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, f"Email: {data['email']}", ln=True)
    pdf.cell(0, 10, f"Contact: {data['phone']}", ln=True)
    pdf.ln(5)

    # Objective
    pdf.section_title("Objective")
    pdf.section_body(data['objective'])

    # Education Details
    pdf.section_title("Educational Qualifications")
    pdf.set_font("Helvetica", 'B', 12)
    col_widths = [40, 50, 40, 20, 20]
    headers = ["Qualification", "Institution", "Board", "CGPA", "Year"]
    for i in range(len(headers)):
        pdf.cell(col_widths[i], 10, headers[i], border=1)
    pdf.ln()

    pdf.set_font("Helvetica", size=12)  # Regular font for entries
    edu_rows = data['education'].split('\n')
    for row in edu_rows:
        clean_row = sanitize_text(row)
        columns = [col.strip() for col in clean_row.split(',')]
        while len(columns) < 5:
            columns.append("")
        for i in range(5):
            pdf.cell(col_widths[i], 10, columns[i][:25], border=1)
        pdf.ln()
    pdf.ln(3)

    # Technical Skills
    pdf.section_title("Technical Skills Acquired")
    pdf.set_font("Helvetica", size=12)
    for skill in data['skills'].split(','):
        pdf.cell(0, 10, sanitize_text(skill.strip()), ln=True)
    pdf.ln(3)

    # Certifications
    pdf.section_title("Online Certification Programs")
    pdf.set_font("Helvetica", size=12)
    for cert in data['certifications'].split('\n'):
        pdf.cell(0, 10, sanitize_text(cert.strip()), ln=True)
    pdf.ln(3)

    # Projects
    pdf.section_title("Projects")
    pdf.section_body(data['projects'])

    # Personal Traits
    pdf.section_title("Personal Traits")
    pdf.set_font("Helvetica", size=12)
    for trait in data['traits'].split(','):
        pdf.cell(0, 10, sanitize_text(trait.strip()), ln=True)
    pdf.ln(3)

    # Declaration
    
    pdf.section_title("Declaration")
    pdf.section_body("I hereby declare that the above-mentioned details are true according to my best knowledge.")
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, sanitize_text(data['name']), ln=True, align='R')
    pdf.output("Resume.pdf")

# Streamlit UI
st.title("🧠 Smart Resume Builder")

name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
objective = st.text_area("Objective")
education = st.text_area("Educational Qualifications (comma-separated: Qualification, Institution, Board, CGPA, Year)")
skills = st.text_area("Technical Skills (comma-separated)")
certifications = st.text_area("Online Certifications (one per line)")
projects = st.text_area("Projects Description")
traits = st.text_area("Personal Traits (comma-separated)")

if st.button("Generate Resume"):
    required = all([name, email, phone, objective, education])
    if required:
        create_resume_pdf({
            "name": name,
            "email": email,
            "phone": phone,
            "objective": objective,
            "education": education,
            "skills": skills,
            "certifications": certifications,
            "projects": projects,
            "traits": traits
        })
        st.success("✅ Resume generated successfully!")

        with open("Resume.pdf", "rb") as file:
            st.download_button(
                "📄 Download Resume",
                file,
                file_name="Resume.pdf",
                mime="application/pdf"
            )
    else:
        st.error("❌ Please fill in all required fields.")






