NOTE_WORDS = {
"Memory": ["forgot", "remember", "spell"],
"Misreading": ["misread", "question", "asked"],
"Calculation": ["calculat", "careless"],
"Concept": ["understand", "confus"],
}

HINTS = {
"Concept":"Study the rule or idea of the question and think about the main concept.",
"Calculation": "Check your calculation once again and double-check your math.",
"Misreading": "Read the question carefully and make sure you understand what is being asked.",
"Memory": "Try to recall the information you learned, then write down what you forgot this time and remember it for next time.",
}

def has_number(text):
    """
    Check if the text contains any numbers."""
    for char in text:
        if char.isdigit():
            return True
    return False

def guess_type(card):
    """
    Guess the type of mistake based on the card's note and answers.
    """
    note = card["note"].lower()
    for mistake_type in NOTE_WORDS:
        for word in NOTE_WORDS[mistake_type]:
            if word in note:
                return mistake_type
                
    if has_number(card["my_answer"]) and not has_number(card["correct_answer"]):
        """
        If the user's answer contains a number but the correct answer does not, it is likely a calculation mistake."""
        return "Calculation"
    # in English, a wrong word is usually a word or spelling you forgot
    if card["subject"] == "English":
        """
        If the subject is English, it is likely a memory mistake."""
        return "Memory"
    return "Concept"

def guess_mistake(card):
    """
    Guess the mistake type and provide a hint based on the card's note and answers.
    """
    # same keys as the AI result, but no twin problem
    mistake_type = guess_type(card)
    return {
        "mistake_type": mistake_type,
        "hint": HINTS[mistake_type],
        "twin_question": "",
        "twin_answer": "",
        "source": "rules",
    }

def only_numbers(text):
    # "$1,700" -> "1700"
    """
    Extract only the numbers and decimal points from the text. Take out any currency symbols or commas."""
    result = ""
    for char in text:
        if char.isdigit() or char in ".,-":
            result += char
    return result