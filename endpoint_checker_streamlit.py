
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("API Endpoint Checker")

url = st.text_input("Enter the endpoint URL:")

if st.button("Check Endpoint"):
    if not url:
        st.error("Please enter a URL.")
    else:
        try:
            response = requests.get(url, timeout=10)
            content_type = response.headers.get("Content-Type", "")

            if "application/json" in content_type:
                try:
                    data = response.json()
                    st.success("✅ Valid JSON detected!")
                    st.json(data)
                except ValueError:
                    st.error("❌ Response is not valid JSON.")
            elif "text/html" in content_type:
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.title.string if soup.title else "No title"
                metas = {meta.get("name", ""): meta.get("content", "") for meta in soup.find_all("meta") if meta.get("name")}
                st.warning("⚠️ HTML content detected.")
                st.write("Title:", title)
                st.write("Meta Tags:", metas if metas else "No named meta tags found.")
            else:
                st.info("ℹ️ Non-JSON/HTML content type detected.")
                st.write("Content-Type:", content_type)
        except requests.exceptions.RequestException as e:
            st.error(f"🚫 Request failed: {e}")
