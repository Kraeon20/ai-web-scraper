import streamlit as stl
from scrape import scrape_website, get_body_content, clean_body_content, split_dom_content
from parse import parse_with_gemini

def display_navbar():
    stl.sidebar.title("Williams Asante")
    stl.sidebar.image("me.jpg", width=150)
    stl.sidebar.markdown("## Contact Me")

    col1, col2, col3 = stl.sidebar.columns(3)

    with col1:
        stl.markdown("[![GitHub](https://img.shields.io/badge/GitHub-000000?style=flat&logo=github&logoColor=white)](https://github.com/kraeon20)")

    with col2:
        stl.markdown("[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:williams.asante515@gmail.com)")

    with col3:
        stl.markdown("[![Phone](https://img.shields.io/badge/Phone-0D9BFF?style=flat&logo=phone&logoColor=white)](tel:+212609090882)")

display_navbar()
 
stl.title("AI WEBSITE SCRAPER")
url = stl.text_input("Enter a Website URL: ", placeholder="htps://www.example.com")


if stl.button("Scrape Site"):
    stl.write("Scrape the website...")


    result = scrape_website(url)
    body_content = get_body_content(result)
    cleaned_content = clean_body_content(body_content)

    stl.session_state.dom_content = cleaned_content

    with stl.expander("View DOM content"):
        stl.text_area("DOM Content", cleaned_content, height=200)



if "dom_content" in stl.session_state:
    parse_description = stl.text_area("Tell me what you want to parse below:")

    if stl.button("Parse Content"):
        if parse_description:
            stl.write("Parsing the content...")

            dom_chunks = split_dom_content(stl.session_state.dom_content)
            result = parse_with_gemini(dom_chunks, parse_description)
            stl.write(result)