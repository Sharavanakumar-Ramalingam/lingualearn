import spacy
import random

# Load German language model
nlp_de = spacy.load("de_core_news_sm")

# Sample paragraph (replace with your own dataset)
paragraph_de = "Albert Einstein war ein deutschstämmiger theoretischer Physiker, der die Relativitätstheorie entwickelte, eine der beiden Grundpfeiler der modernen Physik. Seine Arbeit ist auch für ihren Einfluss auf die Wissenschaftsphilosophie bekannt. Er wurde in Ulm im Königreich Württemberg im Deutschen Reich am 14. März 1879 geboren."

def introduce_mispelling_de(sentence):
    # Process the sentence using spaCy
    doc = nlp_de(sentence)

    # Introduce a misspelling error
    words = [token.text for token in doc]
    idx = random.randint(0, len(words) - 1)
    error_word = words[idx]
    error_word_with_typo = list(error_word)
    random.shuffle(error_word_with_typo)
    error_word_with_typo = ''.join(error_word_with_typo)
    words[idx] = error_word_with_typo
    return " ".join(words), error_word_with_typo, "misspelling"

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

# Process the paragraph using spaCy
doc_de = nlp_de(paragraph_de)

# Extract sentences from the paragraph
sentences_de = [sent.text for sent in doc_de.sents]

# Start the conversation with the user
print("Willkommen zum Grammatik-Tutor!")
print("Ich werde Ihnen Sätze mit grammatikalischen Fehlern präsentieren, die Sie identifizieren und korrigieren müssen.")
print("Lassen Sie uns Ihre Grammatikkenntnisse verbessern!")

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
        sentence = random.choice(sentences_de)

        # Introduce a misspelling error into the selected sentence based on the current level
        sentence_with_error, error_word, error_type = introduce_mispelling_de(sentence)

        # Generate options for the user to choose from
        options = generate_options(sentence_with_error, error_word)

        # Present the sentence with error and options to the user
        print(f"\nLevel {level}: Find the grammatical error in the following sentence:")
        print(sentence_with_error)
        print("Options:")
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")

        # Get user's answer
        user_answer = input("What is the grammatical error? (Enter the number of the option): ")

        # Verify the answer
        if verify_answer(user_answer, error_word):
            print("Correct! You found the error.")
            level_score += 1
        else:
            print(f"Incorrect. The error is introducing '{error_word}' in place of another word.")

        # Explain the type of error
        print("The error is a misspelling, where one of the words in the sentence is spelled incorrectly.")

    # Update user's score
    user_score += level_score

    # Display user's score for this level
    print(f"\nLevel {level} completed. Your score for this level: {level_score}/{max_questions_per_level}. Total score: {user_score}/{level * max_questions_per_level}.")
    print("Keep up the good work!")

# Display final score
print(f"\nCongratulations! You completed all levels. Your final score: {user_score}/15.")
print("Would you like to review any specific grammar topics or continue practicing? Let me know!")
