import random

def load_sentences():
  """Loads pre-defined Hindi sentences from within the program."""
  sentences = [
      "अल्बर्ट आइंस्टीन एक जर्मन मूल के सैद्धांतिक भौतिक विज्ञानी थे।",
      "उन्होंने सापेक्षता का सिद्धांत विकसित किया, जो आधुनिक भौतिकी के दो आधार स्तंभों में से एक है।",
      "उनका कार्य विज्ञान के दर्शन पर उनके प्रभाव के लिए भी जाना जाता है।",
      "उनका जन्म 14 मार्च 1879 को जर्मन साम्राज्य के वुर्टेमबर्ग राज्य के उल्म में हुआ था।",
      "आप कंप्यूटर का उपयोग करके क्या कर सकते हैं?"  # Add more sentences here
  ]
  return sentences

def introduce_misspelling(sentence):
  """Introduces a random misspelling in the sentence (using character-based approach)."""
  words = []
  current_word = ""

  # Split the sentence into words based on whitespace and special characters
  for char in sentence:
    if char.isspace() or not char.isalpha():
      if current_word:
        words.append(current_word)
      current_word = ""
    else:
      current_word += char

  # Handle the last word
  if current_word:
    words.append(current_word)

  if len(words) < 2:
    return sentence, None  # Handle sentences with less than 2 words
  idx = random.randint(0, len(words) - 1)
  error_word = words[idx]

  # Simulate misspelling by swapping adjacent characters
  if len(error_word) > 1:
    i, j = random.sample(range(1, len(error_word)), 2)
    error_word_with_typo = error_word[:i] + error_word[j] + error_word[i:j] + error_word[j + 1:]
  else:
    error_word_with_typo = error_word  # No misspelling for single-letter words

  words[idx] = error_word_with_typo
  return " ".join(words), error_word

def verify_answer(user_answer, error_word):
  """Checks if the user identified the correct misspelling."""
  return user_answer.lower().strip() == error_word.lower().strip()

# Pre-defined Hindi sentences within the program
sentences = load_sentences()

print("व्याकरण ट्यूटर में आपका स्वागत है!")
print("मैं आपको वाक्यों में व्याकरण संबंधी त्रुटियां (वर्तनी संबंधी गलतियाँ) दिखाऊंगा, जिन्हें आपको पहचानना होगा।")
print("चलिए आपके व्याकरण कौशल को बेहतर बनाते हैं!")

user_score = 0

for level in range(1, 4):
  max_questions_per_level = 5
  level_score = 0

  for _ in range(max_questions_per_level):
    sentence = random.choice(sentences)
    sentence_with_error, error_word = introduce_misspelling(sentence)

    print(f"\nस्तर {level}: निम्नलिखित वाक्य में वर्तनी संबंधी त्रुटि ढूंढें:")
    print(sentence_with_error)

    user_answer = input("त्रुटिपूर्ण शब्द क्या है? (पूरे शब्द को टाइप करें): ")

    if verify_answer(user_answer, error_word):
      print("सही! आपको त्रुटिपूर्ण शब्द मिल गया।")
      level_score += 1
    else:
      print(f"गलत। त्रुटिपूर्ण शब्द '{error_word}' था।")

    print("वाक्य में एक अक्षर का स्थान बदला गया था, जिससे वर्तनी में गड़बड़ी हुई।")

  user_score += level_score

  print(f"\nस्तर {level} पूरा हुआ। इस स्तर के लिए आपका स्कोर: {level_score}/{max_questions_per_level}। कुल स्कोर: {user_score}/{level * max_questions_per_level}।")
  print("क्या आप अभ्यास जारी रखना चाहते हैं? (कार्यक्रम को पुनः आरंभ करें")
