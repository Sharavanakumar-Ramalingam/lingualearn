import tkinter as tk
from tkinter import messagebox
import spacy
import random

# Load English language model
nlp = spacy.load("en_core_web_sm")

# Sample paragraph (replace with your own dataset)
paragraph = "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity,one of the two pillars of modern physics. His work is also known for its influence on the philosophyof science. He was born in Ulm, in the Kingdom of Württemberg in the German Empire, on 14 March 1879."

def introduce_mispelling(sentence):
    # Process the sentence using spaCy
    doc = nlp(sentence)

    # Introduce a misspelling error
    words = [token.text for token in doc]
    idx = random.randint(0, len(words) - 1)
    error_word = words[idx]
    error_word_with_typo = list(error_word)
    random.shuffle(error_word_with_typo)
    error_word_with_typo = ''.join(error_word_with_typo)
    words[idx] = error_word_with_typo
    return " ".join(words), error_word_with_typo, "misspelling"

def introduce_verb_tense_error(sentence):
    # Process the sentence using spaCy
    doc = nlp(sentence)

    # Introduce a verb tense error
    for token in doc:
        if token.pos_ == "VERB":
            # Replace the verb with a randomly selected tense
            verb_with_error = random.choice(["is", "was", "will be", "have been"])
            return sentence.replace(token.text, verb_with_error), token.text, "verb tense"
    # If no verb found, return original sentence
    return sentence, None, None

def introduce_subject_verb_agreement_error(sentence):
    # Process the sentence using spaCy
    doc = nlp(sentence)

    # Initialize variables to store potential error values
    sentence_with_error = None
    error_word_or_verb = None
    error_type = None

    # Introduce a subject-verb agreement error
    for token in doc:
        if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
            # Replace the verb with one that doesn't agree with the subject
            verbs = [child.text for child in token.head.children if child.pos_ == "VERB"]
            if verbs:
                verb_with_error = random.choice(["is", "are", "were", "have"])
                sentence_with_error = sentence.replace(verbs[0], verb_with_error)
                error_word_or_verb = verbs[0]
                error_type = "subject-verb agreement"
                break  # Exit loop once error is found

    return sentence_with_error, error_word_or_verb, error_type

def generate_options(sentence, error_word):
    # If sentence is None, return empty options list
    if sentence is None:
        return []

    # Split the sentence into words
    words = sentence.split()

    # Remove punctuation and lowercase words
    words = [word.lower().strip(".,?!") for word in words]

    # Remove duplicate words and the error word
    unique_words = list(set(words) - {error_word.lower()})

    # Randomly select three incorrect options
    incorrect_options = random.sample(unique_words, min(3, len(unique_words)))

    # Add the error word to one of the incorrect options
    incorrect_options.append(error_word)

    return incorrect_options

def get_error_type_description(error_type):
    if error_type == "misspelling":
        return "The error is a misspelling, where one of the words in the sentence is spelled incorrectly."
    elif error_type == "verb tense":
        return "The error is related to verb tense, indicating an incorrect tense for a verb in the sentence."
    elif error_type == "subject-verb agreement":
        return "The error involves subject-verb agreement, where the subject and verb in the sentence do not agree in number or person."
    else:
        return "Unknown error type"

class GrammarTutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grammar Tutor")
        self.root.geometry("600x400")

        self.level = 1
        self.max_questions_per_level = 5
        self.user_score = 0

        self.sentences = [sent.text for sent in nlp(paragraph).sents]

        self.intro_label = tk.Label(root, text="Welcome to the Grammar Tutor!")
        self.intro_label.pack()

        self.instruction_label = tk.Label(root, text="Find the grammatical error in the following sentence:")
        self.instruction_label.pack()

        self.sentence_label = tk.Label(root, text="")
        self.sentence_label.pack()

        self.options_frame = tk.Frame(root)
        self.options_frame.pack()

        self.options_buttons = []
        for i in range(4):  # Changed to 4 buttons
            button = tk.Button(self.options_frame, text="", command=lambda idx=i: self.check_answer(idx))
            button.grid(row=0, column=i, padx=5, pady=5)
            self.options_buttons.append(button)

        self.error_label = tk.Label(root, text="")
        self.error_label.pack()

        self.submit_button = tk.Button(root, text="Submit", command=self.check_answer)
        self.submit_button.pack()

        self.next_question_button = tk.Button(root, text="Next Question", command=self.next_question, state=tk.DISABLED)
        self.next_question_button.pack()

        self.level_label = tk.Label(root, text=f"Level: {self.level}")
        self.level_label.pack()

        self.score_label = tk.Label(root, text=f"Score: {self.user_score}")
        self.score_label.pack()

        self.generate_question()

    def generate_question(self):
        if self.level <= 3:
            sentence = random.choice(self.sentences)

            if self.level == 1:
                sentence_with_error, error_word_or_verb, error_type = introduce_mispelling(sentence)
            elif self.level == 2:
                sentence_with_error, error_word_or_verb, error_type = introduce_verb_tense_error(sentence)
            elif self.level == 3:
                sentence_with_error, error_word_or_verb, error_type = introduce_subject_verb_agreement_error(sentence)

            options = generate_options(sentence_with_error, error_word_or_verb)

            self.sentence_label.config(text=sentence_with_error)
            for i, option in enumerate(options):
                if i < len(self.options_buttons):  # Check if button index is within the range
                    self.options_buttons[i].config(text=option)
                else:
                    break  # Exit loop if button index exceeds the range

            self.error_label.config(text="")

        else:
            self.sentence_label.config(text="Congratulations! You completed all levels.")
            self.instruction_label.config(text="Your final score: {}/15.".format(self.user_score))
            self.options_frame.destroy()
            self.error_label.destroy()
            self.next_question_button.destroy()

            # Start lesson 2 here

    def check_answer(self, idx=None):
        if idx is not None:
            user_answer = self.options_buttons[idx]["text"]
            correct_option = self.options_buttons[-1]["text"]
            if user_answer == correct_option:
                messagebox.showinfo("Correct", "You found the error.")
                self.user_score += 1
            else:
                messagebox.showerror("Incorrect", "The error is introducing '{}' in place of another word.".format(user_answer))
            self.score_label.config(text="Score: {}".format(self.user_score))
            self.next_question_button.config(state=tk.NORMAL)

            error_type = self.error_label.cget("text")
            messagebox.showinfo("Error Details", get_error_type_description(error_type))

    def next_question(self):
        self.level += 1
        self.level_label.config(text="Level: {}".format(self.level))
        self.next_question_button.config(state=tk.DISABLED)
        self.generate_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = GrammarTutorApp(root)
    root.mainloop()
