from transformers import pipeline

# Load a strong, instruction-following model
generator = pipeline("text2text-generation", model="google/flan-t5-base")

print("Type anything and I'll turn it into a poem. Type 'quit' to exit.\n")

while True:
    user_input = input("What should I write a poem about? ")
    if user_input.lower() == "quit":
        break

    # Poetic prompt
    prompt = f"Write a short poem about: {user_input}"

    response = generator(prompt, max_length=128, temperature=0.9, do_sample=True)

    print("Poem:\n", response[0]["generated_text"], "\n")