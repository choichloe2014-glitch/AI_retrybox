import streamlit as st

import uuid
from datetime import date

from card_store import load_cards, save_cards


SUBJECTS = ["Math", "Science", "English", "Other"]

FORM_KEYS = ["question", "my_answer", "correct_answer", "note"]

st.title("Add a mistake")

with st.form("new_card"):
    st.selectbox("Subject", SUBJECTS, key="subject")
    st.text_area("Question", key="question", placeholder="Copy the problem you got wrong.")
    left, right = st.columns(2)
    with left:
        st.text_input("My answer", key="my_answer", placeholder="What did you write?")
    with right:
        st.text_input("Correct answer", key="correct_answer", placeholder="What is the right answer?")
    st.text_input("Note (optional)", key="note", placeholder="Why do you think you got it wrong?")
    st.form_submit_button("Save card", type="primary", on_click=save_new_card, width="stretch")

box_name = st.session_state["box_name"]

cards = load_cards(box_name)

st.subheader(f"My mistake cards  ({len(cards)})")

# pop() so the message is shown only once.
feedback = st.session_state.pop("form_feedback", None)
if feedback is not None:
    kind, message = feedback
    if kind == "error":
        st.error(message)
    else:
        st.success(message)


def form_error(question, my_answer, correct_answer):
    """Return an error message for invalid input, otherwise None.
    The form is invalid if any of the three fields are empty, or if the user's answer is the same as the correct answer.
    This is when the user is not actually making a mistake, does not have a mistake to save, or left it blank."""
    if question == "":
        return "Please write the question you got wrong."
    if my_answer == "":
        return "Please write your answer. If you left it blank, type: blank"
    if correct_answer == "":
        return "Please write the correct answer."
    if my_answer.lower() == correct_answer.lower():
        return "Your answer is the same as the correct answer. This is not a mistake!"
    return None

form_error("","","")

def save_new_card():
    """Callback for[Save card]. Validates the form, saves the card, and resets for inputs before redraw."
    It runs before page is redrawn, which is the only time the inputs can be cleared from code.
    The inputs are cleared only if the card is valid and saved successfully. 
    If there is an error, the inputs are not cleared so the user can fix it."""
    box_name = st.session_state["box_name"]

    question = st.session_state["question"].strip()
    my_answer = st.session_state["my_answer"].strip()
    correct_answer = st.session_state["correct_answer"].strip()
    note = st.session_state["note"].strip()

    error = form_error(question, my_answer, correct_answer)
    if error is not None:
        st.session_state["form_feedback"] = ("error", error)
        return

    card = {
        "id": uuid.uuid4().hex[:8],
        "subject": st.session_state["subject"],
        "question": question,
        "my_answer": my_answer,
        "correct_answer": correct_answer,
        "note": note,
        "created_at": date.today().isoformat(),
    }

    cards = load_cards(box_name)
    cards.insert(0, card)
    save_cards(box_name, cards)

    for key in FORM_KEYS:
        # Clear the form inputs after saving a card. Give feedback to the user that the card was saved successfully.
    st.session_state["form_feedback"] = ("success", "Saved! Your card is in the list below.")


def delete_card(card_id):
    """Callback for [Yes, delete].
    Checks the card id, loads the cards, removes the card with the given id, and saves the remaining cards."""
    box_name = st.session_state["box_name"]
    cards = load_cards(box_name)
    # list comprehension
    remaining = [card for card in cards if card["id"] != card_id]
    save_cards(box_name, remaining)

    def show_card(card):
        """Show a card in the list of saved cards.
        The card is shown in a container with a border, with the subject and date at the top, the question in the middle, and the user's answer and the correct answer at the bottom.
        The user can delete the card by clicking the delete button, which shows a popover asking for confirmation."""
        with st.container(border=True):
            left, right = st.columns([5, 1], vertical_alignment="center")
        with left:
            st.badge(card["subject"], color="orange")
            st.caption(card["created_at"])
        with right:
            # Ask once more so a card isn't deleted by accident.
            with st.popover("Delete", type="tertiary"):
                st.write("Delete this card?")
                st.button(
                    "Yes, delete",
                    key=f"delete_{card['id']}",
                    on_click=delete_card,
                    args=(card["id"],),
                    type="primary",
                )

        st.text(card["question"])

        mine, right_answer = st.columns(2)
        with mine:
            st.caption("My answer")
            st.text(card["my_answer"])
        with right_answer:
            st.caption("Correct answer")
            st.text(card["correct_answer"])

        if card["note"] != "":
            st.caption("Note")
            st.text(card["note"])

with st.form("new_card"):
    st.selectbox("Subject", SUBJECTS, key="subject")
    st.text_area("Question", key="question", placeholder="Copy the problem you got wrong.")
    left, right = st.columns(2)
    with left:
        st.text_input("My answer", key="my_answer", placeholder="What did you write?")
    with right:
        st.text_input("Correct answer", key="correct_answer", placeholder="What is the right answer?")
    st.text_input("Note (optional)", key="note", placeholder="Why do you think you got it wrong?")
    st.form_submit_button("Save card", type="primary", on_click=save_new_card, width="stretch")

    feedback = st.session_state.pop("form_feedback", None)
    if feedback is not None:
        kind, message = feedback
        if kind == "error":
            st.error(message)
        else:
            st.success(message)

    cards = load_cards(box_name)

    st.subheader(f"My mistake cards  ({len(cards)})")
    if len(cards) == 0:
        st.info("No mistake cards yet. Add the first one above.")

    for card in cards:
        show_card(card)
