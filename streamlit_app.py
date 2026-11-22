import streamlit as st
import ai_check

from streamlit.errors import StreamlitSecretNotFoundError
st.set_page_config(page_title="AI Retry Box")

### save a mistake card, save button, list of saved cards.

def read_secret(name, default):
    # st.secrets crashes if there is no secrets.toml at all
    try:
        return st.secrets.get(name, default)
    except StreamlitSecretNotFoundError:
        return default



def name_error(name):
    if not name.isalnum():
        return "Use only letters and numbers in your name(no space or symbols)."
    return None

st.set_page_config(page_title="AI Retry Box", page_icon=":material/inventory_2:")
st.sidebar.title("Retry Box")

# Keep the name in the URL(?owner=your-name)
typed_name = st.sidebar.text_input(
    "Your name",
    key = "owner",
    bind = "query-params",
    max_chars = 20,
    placeholder = "e.g. Jiyoung"
)

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

st.session_state["box_name"] = box_name
st.sidebar.caption(f"Your cards are saved in data/{box_name}.json")

groq_key = read_secret("GROQ_API_KEY", "")
groq_model = read_secret("GROQ_MODEL", "")

if groq_key == "" or groq_model == "":
    use_ai = False
    st.sidebar.warning("The AI is off, so simple rules check your mistakes. To turn on the AI, add your GROQ_API_KEY and GROQ_MODEL to secrets.toml.")
else:
    use_ai = st.sidebar.toggle("Use AI", value=True, key ="ai_switch")

st.session_state["use_ai"] = use_ai


    # ask_ai in ai_check.py calls Groq with this model
ai_check.MODEL = groq_model

page = st.navigation(
     [
     st.Page("add_page.py", title= "Add", icon=":material/add_circle:"),

    ]
)
page.run()