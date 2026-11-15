import json
from streamlit.errors import StreamlitSecretNotFoundError

from groq import Groq

from rule_check import guess_mistake

MODEL = ""

MISTAKE_TYPES = ["Concept", "Calculation", "Misreading", "Memory"]

CHECK_INSTRUCTIONS = """You are a kind and helpful tutor. A student made a mistake.
"You are a kind and helpful tutor. A student made a mistake."
Reply in JSON with the following format:
-"mistake_type": one of these
"Concept" (didn't understand the whole point of question), "Calculation" (mathematical mistake),
 "Misreading" (didn't read the question right), "Memory"(forgot a fact or word)
-"hint": a small clue or hint to help the student remember or find the correct answer. One short word, not the correct answer.
-"twin_question": a similar question with different numbers or values.
-"twin_answer": the correct answer to the twin question.
"""
class AiError(Exception):
    pass
def ask_ai(api_key, instructions, prompt, keys):
    """
    Ask the AI for a response based on the instructions and prompt."""
    client = Grog(api_key=api_key)
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": prompt},
    ]
    try:
        # Response from the AI is expected to be a JSON object with the specified keys. If the response is not valid JSON or does not contain the expected keys, an AiError will be raised."""
   
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
    except Exception:
        # wrong key, old model name, free limit used up, no internet, or not JSON
        raise AiError("Check the AI key, model name, and internet connection, then try again.")

    # the AI sometimes forgets a key, so check before using it
    for key in keys:
        # If the key is not in the result, raise an AiError indicating that the AI gave a strange answer."""
        if key not in result:
            raise AiError("The AI gave a strange answer. Please try again.")

    result["source"] = "ai"
    return result


def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except StreamlitSecretNotFoundError:
        return ""

def check_mistake(card, use_ai: bool = True):
   """ Check the mistake type and provide a hint based on the
     card's note and answers. If an API key is provided, use the AI to determine the mistake type.
     Otherwise, use the rule-based method."""
   api_key = get_api_key() if use_ai else ""
   if not use_ai or api_key == "":
        return guess_mistake(card)
   
   note = card["note"]
   
   if note == "":
    note = "(none)"
    prompt = f"""Subject: {card['subject']}
    Problem: {card['question']}
    Student's answer: {card['my_answer']}
    Correct answer: {card['correct_answer']}
    Student's note: {note}"""

    keys = ["mistake_type", "hint", "twin_question", "twin_answer"]
    result = ask_ai(api_key, CHECK_INSTRUCTIONS, prompt, keys)
    if result["mistake_type"] not in MISTAKE_TYPES:
        raise AiError("The AI gave a strange answer. Please try again.")
    return result