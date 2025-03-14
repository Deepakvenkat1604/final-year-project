import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

pdf_path = "C:\Users\Deepa\OneDrive\Desktop\sip reference\income-tax-act-1961-amended-by-finance-no.-2-act-2024.pdf"  # Replace with your file
text = extract_text_from_pdf(pdf_path)

with open("raw_tax_laws.txt", "w", encoding="utf-8") as f:
    f.write(text)
