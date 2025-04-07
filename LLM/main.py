from transformers import T5Tokenizer, T5ForConditionalGeneration


tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

print("Type anything and I'll turn it into a poem. Type 'quit' to exit.")

while True:
    user_input = input(" What should I write a poem about? ")
    if user_input.lower() == "quit":
        break

    # Prompt the model to write a poem
    prompt = f"Write a beautiful poem with emotion and imagery about: {user_input}"

    # Tokenize input
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    # Generate output
    outputs = model.generate(
        input_ids,
        max_length=128,
        do_sample=True,
        temperature=0.9,
        num_beams=4,
        early_stopping=True
    )


    poem = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("\nPoem:\n", poem, "\n")