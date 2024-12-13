import streamlit as st
import json
import os
import requests

# Set page configuration
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

primo_api = os.environ.get("PRIMO_SANDBOX_API")
google_api = os.environ.get("NLS_GOOGLE_CUSTOM_SEARCH")
cse_id = "e39334d6bde174112"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def search_function(search_input):
    primo_params = {
        "q": f"any,contains,{search_input}",
        "apikey": primo_api,
        "vid": "44NLS_INST:44NLS_VU1",
        "tab": "LibraryCatalog",
        "scope": "MyInstitution",
        "inst": "inst",
        "lang": "eng",
        "limit": "10",
        "sort": "rank",
        "conVoc": "true",
        "skipDelivery": "true",
    }
    primo_url = "https://api-eu.hosted.exlibrisgroup.com/almaws/v1/search"
    # r_primo = requests.get(primo_url, params=primo_params, headers=headers)
    g_results = []
    start = 1
    while start <= 30:
        google_params = {
            "q": f"{search_input}",
            "cx": cse_id,
            "key": google_api,
            "start": start,
        }
        google_url = "https://customsearch.googleapis.com/customsearch/v1"
        r_google = requests.get(
            google_url, params=google_params, headers=headers
        ).json()
        g_results.extend(r_google["items"])
        start += 10
    st.write(r_google)
    digi_gallery = []
    manuscripts = []
    films = []
    content = []
    for item in g_results:
        link = item["link"]
        if "digital.nls.uk" in link:
            digi_gallery.append(item)
        if "www.nls.uk" in link:
            content.append(item)
        if "manuscripts.nls.uk" in link:
            manuscripts.append(item)
        if "movingimage.nls.uk" in link:
            films.append(item)
    if len(content) > 0:
        st.write("## Articles")
        for item in content:
            title = item["title"]
            link = item["link"]
            thumbnail = item["pagemap"]["cse_thumbnail"][0]["src"]
            st.markdown(f"[![{title}]({thumbnail})]({link})")
            # st.image(thumbnail, caption=title)
            # st.write(f"#### {title}  \n{link}")
        st.divider()
    if len(films) > 0:
        st.write("## Films")
        for item in films:
            title = item["title"]
            link = item["link"]
            st.write(f"#### {title}  \n{link}")
        st.divider()
    if len(digi_gallery) > 0:
        st.write("## Digital Gallery")
        for item in digi_gallery:
            title = item["title"]
            link = item["link"]
            st.write(f"#### {title}  \n{link}")
        st.divider()
    if len(manuscripts) > 0:
        st.write("## Manuscripts")
        for item in manuscripts:
            title = item["title"]
            link = item["link"]
            st.write(f"#### {title}  \n{link}")
        st.divider()
    # st.write(r_google)
    # # st.write(r_primo.text)


st.title("NLS Search page")
search_box = st.text_input("Search the site and catalogues")

if search_box:
    search_function(search_box)
