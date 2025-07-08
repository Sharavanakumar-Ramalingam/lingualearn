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
    # Split the sentence into words
    words = sentence.split()

    # Remove punctuation and lowercase words
    words = [word.lower().strip(".,?!") for word in words]

    # Remove duplicate words and the error word
    unique_words = list(set(words) - {error_word.lower()})

    # Randomly select three incorrect options
    incorrect_options = random.sample(unique_words, 3)

    # Add the error word to one of the incorrect options
    incorrect_options[random.randint(0, 2)] = error_word

    return incorrect_options

def verify_answer(user_answer, correct_option):
    # Convert both answers to lowercase for case insensitivity
    user_answer_lower = user_answer.lower()
    correct_option_lower = correct_option.lower()

    # Check if user's answer matches the correct option
    return user_answer_lower.strip() == correct_option_lower.strip()

def get_error_type_description(error_type):
    if error_type == "misspelling":
        return "The error is a misspelling, where one of the words in the sentence is spelled incorrectly."
    elif error_type == "verb tense":
        return "The error is related to verb tense, indicating an incorrect tense for a verb in the sentence."
    elif error_type == "subject-verb agreement":
        return "The error involves subject-verb agreement, where the subject and verb in the sentence do not agree in number or person."

# Process the paragraph using spaCy
doc = nlp(paragraph)

# Extract sentences from the paragraph
sentences = [sent.text for sent in doc.sents]

# Start the conversation with the user
print("Welcome to the Grammar Tutor!")
print("I will present you with sentences containing grammatical errors, and you need to identify and correct them.")
print("Let's improve your grammar skills!")

# Initialize user score
user_score = 0

# Main loop for interacting with the user
for level in range(1, 4):
    # Set the maximum number of questions per level
    max_questions_per_level = 5

    # Initialize score for this level
    level_score = 0

    # Loop for each question in this level
    for _ in range(max_questions_per_level):
        # Randomly select a sentence
        sentence = random.choice(sentences)

        # Introduce a grammatical error into the selected sentence based on the current level
        if level == 1:
            sentence_with_error, error_word_or_verb, error_type = introduce_mispelling(sentence)
        elif level == 2:
            sentence_with_error, error_word_or_verb, error_type = introduce_verb_tense_error(sentence)
        elif level == 3:
            # Attempt to introduce a subject-verb agreement error
            sentence_with_error, error_word_or_verb, error_type = introduce_subject_verb_agreement_error(sentence)

            # If no suitable sentence found, try again with a different sentence
            while sentence_with_error is None:
                sentence = random.choice(sentences)
                sentence_with_error, error_word_or_verb, error_type = introduce_subject_verb_agreement_error(sentence)

                if sentence_with_error is not None:
                    break

            # If still unable to find a suitable sentence, display error message and skip to next level
            if sentence_with_error is None:
                print("Error: Unable to introduce grammatical error for this sentence. Please try again.")
                break

        # Generate options for the user to choose from
        options = generate_options(sentence_with_error, error_word_or_verb)

        # Present the sentence with error and options to the user
        print(f"\nLevel {level}: Find the grammatical error in the following sentence:")
        print(sentence_with_error)
        print("Options:")
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")

        # Get user's answer
        user_answer = input("What is the grammatical error? (Enter the number of the option): ")

        # Verify the answer
        if verify_answer(user_answer, error_word_or_verb):
            print("Correct! You found the error.")
            level_score += 1
        else:
            print(f"Incorrect. The error is introducing '{error_word_or_verb}' in place of another word.")

        # Explain the type of error
        print(get_error_type_description(error_type))

    # Update user's score
    user_score += level_score

    # Display user's score for this level
    print(f"\nLevel {level} completed. Your score for this level: {level_score}/{max_questions_per_level}. Total score: {user_score}/{level * max_questions_per_level}.")
    print("Keep up the good work!")

# Display final score
print(f"\nCongratulations! You completed all levels. Your final score: {user_score}/15.")
print("Would you like to review any specific grammar topics or continue practicing? Let me know!")
