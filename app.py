"""
AI Retry Box

This is a Streamlit app that allows users to save problems they got wrong and retry them later.
It is designed to help users learn from their mistakes and improve their understanding of various subjects.
Users can review their mistakes, in a personalized way, so they can learn better from their mistakes and improve.
"""

import streamlit as st

st.set_page_config(page_title="AI Retry Box")

### save a mistake card, save button, list of saved cards.

# Keep the name in the URL(?owner=your-name) so it survives a page refresh.)
# and the user can bookmark their own box.
typed_name = st.sidebar.text_input(
    "Your name",
    key = "owner",
    bind = "query-params",
    max_chars = 20,
    placeholder = "e.g. Jiyoung"
)
# Treat "Jiyoung" and "jiyoung" as the same person.
box_name = typed_name.strip().lower()

if box_name=="":
    st.title("AI Retry Box")
    st.write("Save the problems you got wrong. Beat them next time.")
    st.info("Type your name in the sidebar to open your own box.")
    st.stop()

problem = name_error(box_name)
if problem is not None:
    st.sidebar.error(problem)
    st.stop()

def name_error(name):
    """Return an error message for invalid name, otherwise None.
    Only letters and numbers are allowed, no spaces or symbols. It is because the name becomes a file name 
    (data/{name}.json) and we want to avoid any issues with file naming."""
    
    if not name.isalnum():
        return "Use only letters and numbers in your name(no space or symbols)."
    return None

# Pages can't see variables from this file, so share the name through session_state.
st.session_state["box_name"] = box_name
st.sidebar.caption(f"Your cards are saved in data/{box_name}.json")

page = st.navigation(
    [
        st.Page("add_page.py", title= "Add")

    ]
)
page.run()