import pandas as pd
import streamlit as st
from scrape import Scraper
from parse import parse_with_ollama


st.title("AI Web Scraper v1 🤖🔗")
url = st.text_input("Enter Website URL")

sc = Scraper()

if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")

        dom_content = sc.scrape_website(url)
        body_content = sc.extract_body_content(dom_content)
        cleaned_content = sc.clean_body_content(body_content)

        st.session_state.dom_content = cleaned_content



if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            dom_chunks = sc.split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)

            if isinstance(parsed_result, dict):  # Adjust this based on your actual parsed result structure
                df = pd.DataFrame.from_dict(parsed_result, orient='index', columns=['Value']).reset_index()
                df.columns = ['Description', 'Value']

                # Download button
                csv = df.to_csv(index=False)
                st.download_button("Download as CSV", csv, "parsed_result.csv", "text/csv")
            else:
                st.error("Parsed result is not in an expected format.")