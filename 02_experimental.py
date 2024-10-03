import streamlit as st
from utils import load_markdown_file_with_images, get_first_level_headers

def run(selected_tab=None):
    folder = "experimental"
    # Initialize session state for selected tab
    if "selected_tab" not in st.session_state:
        st.session_state["selected_tab"] = selected_tab

    # Get the selected language from session state
    selected_language = st.session_state.get("language", "english").lower()
    # Create tabs for each section
    tabs_path = ['01_accelerators.md', '02_detectors.md']
    tab_titles = get_first_level_headers(selected_language, folder, tabs_path)
    tabs = st.tabs(tab_titles)

    # Map tab titles to tab objects
    tab_dict = dict(zip(tab_titles, tabs))

    # Display content based on selected tab
    for tab_title in tab_titles:
        with tab_dict[tab_title]:
            # Update the session state when the tab is selected
            if tab_title != st.session_state["selected_tab"]:
                st.session_state["selected_tab"] = tab_title
            if tab_title == tab_titles[0]:
                # Pass the selected language to the function
                load_markdown_file_with_images(tabs_path[0], folder, selected_language)
                st.video("https://www.youtube.com/embed/pQhbhpU9Wrg")
            
            elif tab_title == tab_titles[1]:
                # Pass the selected language to the function
                load_markdown_file_with_images(tabs_path[1], folder, selected_language)
