import matplotlib.pyplot as plt
import os
import re
import streamlit as st
from code_editor import code_editor
import io
import sys
import json


def generate_header_id(header_text):
    """Generate a valid HTML id from the header text by removing special characters."""
    # Convert to lowercase
    header_id = header_text.lower()
    # Replace spaces with hyphens
    header_id = re.sub(r'\s+', '-', header_id)
    # Remove any characters that are not alphanumeric, hyphens, or underscores
    header_id = re.sub(r'[^a-z0-9\-_]', '', header_id)
    return header_id

def insert_toc(content):
    """Generate a floating Table of Contents based on second and third level markdown headers."""
    toc = []
    # Match only second (##) and third (###) level headers
    headers = re.findall(r'^(#{2,3})\s*(.*)', content, re.MULTILINE)
    
    # Only proceed if there are second or third level headers
    if headers:
        # Create a TOC entry for each header
        for level, header_text in headers:
            header_id = generate_header_id(header_text)  # Generate valid HTML id
            if level == '##':
                toc.append(f'<a class="toc-level-2" href="#{header_id}">{header_text}</a>')
            elif level == '###':
                toc.append(f'<a class="toc-level-3" href="#{header_id}">{header_text}</a>')

        # Create the TOC as HTML
        toc_html = """
        <div class="toc">
            <h4>Contents</h4>
            {links}
        </div>
        """.format(links='\n'.join(toc))

        # Inject the TOC into the Streamlit app
        st.markdown(toc_html, unsafe_allow_html=True)

        # Add custom CSS for floating sidebar TOC with a transparent background and different header styles
        st.markdown("""
        <style>
            .toc {
                position: fixed;
                top: 100px;
                right: 20px;
                background-color: rgba(255, 255, 255, 0); /* Transparent background */
                padding: 1rem;
                border-radius: 5px;
                box-shadow: none;
                z-index: 100;
                width: 250px;
                max-height: 70vh;
                overflow-y: auto;
            }
            .toc h4 {
                font-size: 16px;
                margin-bottom: 10px;
            }
            .toc a {
                color: #0366d6;
                text-decoration: none;
                display: block;
                margin-bottom: 8px;
            }
            .toc a:hover {
                text-decoration: underline;
            }
            .toc a.toc-level-2 {
                font-size: 15px;
                font-weight: bold;
                margin-left: 0px; /* No indent for second-level headers */
            }
            .toc a.toc-level-3 {
                font-size: 13px;
                margin-left: 10px; /* Indent for third-level headers */
            }
            /* Allow the TOC to scroll */
            .toc {
                overflow-y: scroll;
            }
        </style>
        """, unsafe_allow_html=True)

def load_markdown_file_with_images(filename, folder, language):
    """Load markdown content, display images with captions, and render text."""
    # Construct the file path based on the selected language
    base_path = f"docs/{language.lower()}/{folder}/{filename}"
    
    if os.path.exists(base_path):
        with open(base_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Insert Table of Contents (TOC) only if there are second or third level headers
        insert_toc(content)

        # Parse the content and replace image references
        markdown_buffer = []
        for line in content.splitlines():
            # Search for image markdown syntax ![caption](image_path)
            image_match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            
            if image_match:
                # Extract caption and image path
                caption, img_path = image_match.groups()
                # Render the previous markdown content before the image
                if markdown_buffer:
                    st.markdown('\n'.join(markdown_buffer))
                    markdown_buffer = []
                
                # Display the image with caption
                st.image(img_path, caption=caption, width=650)
            else:
                # Add line to the markdown buffer if it's not an image
                markdown_buffer.append(line)

        # Render any remaining markdown content
        if markdown_buffer:
            st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)

    else:
        st.error(f"File not found for language: {language}. Check the file path.")

def get_first_level_headers(language, folder, filenames):
    headers = []
    for filename in filenames:
        base_path = f"docs/{language.lower()}/{folder}/{filename}"
        try:
            with open(base_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.startswith('# '):
                        header = line.strip('# ').strip()
                        headers.append(header)
                        break  # Stop after the first header is found
        except FileNotFoundError:
            print(f"File not found: {base_path}")
    return headers

def load_sidebar_tabs(language, folder="docs"):
    """Load tabs from the side_bar.md file based on the selected language."""
    sidebar_file_path = f"{folder}/{language.lower()}/side_bar.md"

    if os.path.exists(sidebar_file_path):
        with open(sidebar_file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip().splitlines()

        # Return the lines as the tabs list (assuming each line is a tab)
        return [line.strip() for line in content if line.strip()]
    else:
        st.error(f"Sidebar file not found for language: {language}. Check the file path.")
        return []  # Return an empty list if file not found

def run_code_editor(default_code, global_namespace, height=[2,6]):
    """
    Run the code editor in Streamlit with a shared global namespace.

    Args:
        default_code (str): The default Python code to show in the editor.
        global_namespace (dict): A dictionary shared between all code cells for global variables/functions.
        height (list): The height of the code editor component.
    """
    # JSON for the custom buttons (including "Run")
    with open('custom/buttons_code_cells.json') as json_button_file:
        custom_buttons = json.load(json_button_file)

    # Ace code editor with Python syntax highlighting and custom buttons
    response_dict = code_editor(
        default_code,
        lang="python",
        height=height,
        theme="monokai",
        buttons=custom_buttons
    )

    # Check if the "Run" button in the editor was clicked
    if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
        code = response_dict['text']

        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        try:
            # Execute the user's code in the shared global namespace
            exec(code, global_namespace)  # Only global_namespace is passed here
        except IndentationError as e:
            st.error(f"Indentation Error: {e}")
        except Exception as e:
            st.error(f"Error: {e}")

        # Get the output and display it in a non-editable block
        output = buffer.getvalue()
        if output:
            st.code(output, language="python")  # Use `st.code` to display the output as non-editable text

        # Reset stdout
        sys.stdout = old_stdout

        # Check if any matplotlib plots were created and display them
        if plt.get_fignums():  # Check if there are any active figures
            st.pyplot(plt.gcf())  # Display the current figure
            plt.close('all')  # Close the plot to prevent duplication in subsequent cells

def load_markdown_file_with_images_and_code(filename, folder, global_namespace, language):
    """Load markdown content, display images with captions, render text, and execute code blocks."""
    # Construct the file path based on the selected language
    base_path = f"docs/{language.lower()}/{folder}/{filename}"
    
    if os.path.exists(base_path):
        with open(base_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Insert Table of Contents (TOC) only if there are second or third level headers
        insert_toc(content)

        # Variables to hold parsed content
        markdown_buffer = []
        in_code_block = False
        code_buffer = []

        # Parse the content and handle images, text, and code in the correct order
        for line in content.splitlines():
            # Detect start or end of a code block
            if line.startswith("```"):
                if not in_code_block:
                    # Start of a new code block
                    in_code_block = True
                    # If there's any accumulated markdown content, render it
                    if markdown_buffer:
                        st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
                        markdown_buffer = []
                else:
                    # End of a code block
                    in_code_block = False
                    # Render the code block
                    code = '\n'.join(code_buffer)
                    run_code_editor(code, global_namespace)
                    code_buffer = []
            elif in_code_block:
                # Collect lines for the current code block
                code_buffer.append(line)
            else:
                # Check if the line contains an image markdown syntax: ![caption](image_path)
                image_match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
                if image_match:
                    # Extract caption and image path
                    caption, img_path = image_match.groups()
                    # Render any accumulated markdown content before the image
                    if markdown_buffer:
                        st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
                        markdown_buffer = []
                    # Display the image
                    st.image(img_path, caption=caption, width=650)
                else:
                    # Add the line to the markdown buffer if it's not an image or code block
                    markdown_buffer.append(line)

        # Render any remaining markdown content
        if markdown_buffer:
            st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)

    else:
        st.error(f"File not found for language: {language}. Check the file path.")