# AI_retrybox

## 1. About This Project

- This project is a streamlit application that helps you study, especially review. This project will help us to study better because it is way more easy and fun than just studying. 

## 2. Features

- Feature 1: This project make cards out of the problems you got wrong, and save them so that you can review easily. You can also delete the cards.
- Feature 2: AI makes you a twin question, which is a question similar to what you got wrong but in different values.
- Feature 3: This program will tell you why you made a mistake.

## 3. Technologies Used

- Language: Python
- Libraries / Frameworks: Streamlit/GROQ
- Tools: GROQ AI

## 4. How to Run

1. Download or clone this repository.
2. Use UV to install the required libraries.
3. Copy secret.toml.example and change file name to secrets.toml.
4. Get a GROQ key in console.groq.com. Then put the GROQ key in the secrets.toml file.
5. Run the main program.

```bash
uv run streamlit run streamlit_app.py
```

## 5. Screenshots



## 6. Challenges and Solutions

**Challenge:**
What was difficult? 
- To use GROQ AI, I need GROQ key but I couldn't get the GROQ key from secret.toml file.

**Solution:**
I used print `GROQ key`, changed the `GROQ key`, and checked other stuff until I found out that I forgot `"` in the end.


## 7. What I Learned

- I learned how to...
- I improved my understanding of...
- I learned that...

## 8. Future Improvements

- [ ] Improvement 1
- [ ] Improvement 2
- [ ] Improvement 3