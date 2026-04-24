import PyPDF2

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            return text
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    pdf_text = extract_text_from_pdf("Health_Chatbot_Using_Natural_Language_Processing_for_Disease_Prediction_and_Treatment.pdf")
    with open("pdf_content.txt", "w", encoding="utf-8") as f:
        f.write(pdf_text)
    print("Extracted to pdf_content.txt")
