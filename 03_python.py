import streamlit as st
import io
import sys
import json
from utils import load_markdown_file_with_images_and_code

# Define backend variables and functions that will be available to the user's code

selected_language = st.session_state.get("language", "english").lower()

def run(selected_tab=None):
    load_markdown_file_with_images_and_code('01_intro.md', 'python', selected_language)
