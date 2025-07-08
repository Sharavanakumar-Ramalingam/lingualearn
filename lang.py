import openai

# Set up OpenAI API key
openai.api_key = "##"

def get_chat_completions():
    """
    Generate completions using the ChatGPT model.

    Returns:
        str: The generated completion from the model.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # Extracting the last message which contains the model response
        completion = response.choices[-1].message.content
        return completion.strip()
    except openai.error.RateLimitError:
        print("You have exceeded your current quota. Please try again later.")
        return None

def main():
    print("Welcome to Chat Completions Demo!")

    # Generate completions using the ChatGPT model
    completion = get_chat_completions()
    if completion is not None:
        print("Completion:", completion)
    else:
        print("Failed to generate a completion. Please try again later.")

if __name__ == "__main__":
    main()
