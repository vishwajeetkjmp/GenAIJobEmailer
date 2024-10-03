import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from PyPDF2 import PdfReader

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Generate mail to Hiring Manager")
    url_input = st.text_input("Enter a URL:", value="https://www.atlassian.com/company/careers/details/15802")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

def create_streamlit_app_referral(llm, portfolio, clean_text):
    st.title("📧 Generate mail for Referral")
    url_input_referral = st.text_input("Enter a URL:", value="https://www.atlassian.com/company/careers/details/158023")
    submit_button_ = st.button("Generate")

    if submit_button_:
        try:
            loader_ = WebBaseLoader([url_input_referral])
            data_ = clean_text(loader_.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data_)
            for job in jobs:
                email = llm.write_mail_for_referral(job, url_input_referral)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

def create_streamlit_app_resumeLoad(llm, portfolio, clean_text):
    st.title("Upload resume")
    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

    upload_button = st.button("Upload")

    if upload_button:
        try:
            reader = PdfReader(pdf_file)
            st.write("PDF file uploaded successfully.")
            st.write("PDF Content:")
            pdf_text = ""
            for page in reader.pages:
                pdf_text += page.extract_text()
            st.text(pdf_text)
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
    create_streamlit_app_referral(chain, portfolio, clean_text)
    create_streamlit_app_resumeLoad(chain, portfolio, clean_text)