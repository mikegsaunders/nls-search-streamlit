import streamlit as st
import os
import requests

# Set page configuration
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

primo_api = os.environ.get("PRIMO_SANDBOX_API")
google_api = os.environ.get("NLS_GOOGLE_CUSTOM_SEARCH")
cse_id = "00056ba479f1e4368"

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

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
        "limit": "4",
        "sort": "rank",
        "conVoc": "true",
        "skipDelivery": "true",
        "disableSplitFacets": "false",
    }
    primo_url = "https://api-eu.hosted.exlibrisgroup.com/primo/v1/search"
    r_primo = requests.get(primo_url, params=primo_params, headers=headers).json()
    p_results = r_primo["docs"]
    books = []
    for item in p_results:
        title = item["pnx"]["addata"]["btitle"][0]
        au = item["pnx"]["addata"].get("au")
        id = item["pnx"]["control"]["recordid"][0]
        link = f"https://nls.primo.exlibrisgroup.com/permalink/44NLS_INST/3luoid/{id}"
        book = {"title": title, "link": link}
        if au is not None:
            author = " ".join(part.strip(".") for part in reversed(au[0].split(", ")))
            book["author"] = author
        books.append(book)

    g_results = []
    start = 1
    try:
        while start <= 30:
            google_params = {
                "q": f"{search_input}",
                "cx": cse_id,
                "key": google_api,
                "start": start,
            }
            google_url = "https://customsearch.googleapis.com/customsearch/v1"
            r_google = requests.get(google_url, params=google_params, headers=headers)
            r_google_json = r_google.json()
            g_results.extend(r_google_json["items"])
            start += 10
    except KeyError:
        st.error("Google CSE results maxed out for the day")
        pass
    digi_gallery = []
    manuscripts = []
    films = []
    content = []
    events = []
    guides = []
    maps = []
    for item in g_results:
        link = item["link"]
        if "digital.nls.uk" in link:
            digi_gallery.append(item)
        if "www.nls.uk" in link and "whats-on" not in link and "papercut" not in link:
            guides.append(item)
        if "whats-on" in link:
            events.append(item)
        if "papercut" in link:
            content.append(item)
        if "manuscripts.nls.uk" in link:
            manuscripts.append(item)
        if "movingimage.nls.uk" in link:
            films.append(item)
        if "maps.nls.uk" in link:
            maps.append(item)
    col1, col2 = st.columns(2)
    max_results = 4
    with col1:
        if len(content) > 0:
            with st.container(border=True):
                st.write("## Articles")
                returned = 0
                for item in content:
                    title = item["title"]
                    link = item["link"]
                    # thumbnail = item["pagemap"]["cse_thumbnail"][0]["src"]
                    # st.markdown(f"[![{title}]({thumbnail})]({link})")
                    # st.image(thumbnail, caption=title)
                    # st.write(f"#### {title}  \n{link}")
                    st.markdown(f"[{title}]({link})")
                    returned += 1
                    if returned == max_results:
                        break
                # st.divider()
        if len(events) > 0:
            with st.container(border=True):
                st.write("## Events")
                returned = 0
                for item in events:
                    title = item["title"]
                    link = item["link"]
                    st.markdown(f"[{title}]({link})")
                    returned += 1
                    if returned == max_results:
                        break
        if len(guides) > 0:
            with st.container(border=True):
                st.write("## Guides")
                returned = 0
                for item in guides:
                    title = item["title"]
                    link = item["link"]
                    st.markdown(f"[{title}]({link})")
                    returned += 1
                    if returned == max_results:
                        break
    with col2:
        if len(books) > 0:
            with st.container(border=True):
                st.write("## Books, etc.")
                returned = 0
                for item in books:
                    title = item["title"]
                    link = item["link"]
                    author = item.get("author")
                    if author is not None:
                        st.markdown(f"[{title}]({link})&nbsp;&nbsp;_{author}_")
                    else:
                        st.markdown(f"[{title}]({link})")
                    returned += 1
                    if returned == max_results:
                        break
        if len(maps) > 0:
            with st.container(border=True):
                st.write("## Maps")
                returned = 0
                for item in films:
                    title = item["title"]
                    link = item["link"]
                    st.markdown(f"[{title}]({link})")
                    returned += 1
                    if returned == max_results:
                        break
        if len(films) > 0:
            with st.container(border=True):
                st.write("## Films")
                returned = 0
                for item in films:
                    title = item["title"]
                    link = item["link"]
                    st.markdown(f"[{title}]({link})")
                    returned += 1
                    if returned == max_results:
                        break
        if len(digi_gallery) > 0:
            with st.container(border=True):
                st.write("## Digital Gallery")
                returned = 0
                for item in digi_gallery:
                    title = item["title"]
                    link = item["link"]
                    st.markdown(f"[{title}]({link})")
                    returned += 1
                    if returned == max_results:
                        break
        if len(manuscripts) > 0:
            with st.container(border=True):
                st.write("## Manuscripts")
                returned = 0
                for item in manuscripts:
                    title = item["title"]
                    link = item["link"]
                    st.markdown(f"[{title}]({link})")
                    returned += 1
                    if returned == max_results:
                        break


st.title("NLS Search page")
search_box = st.text_input("Search the site and catalogues")

if search_box:
    search_function(search_box)
