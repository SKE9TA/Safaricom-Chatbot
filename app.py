import streamlit as st
import openai

st.title('FAQ Chatbot')
st.header('Safaricom FAQ Database GPT Response ')

# Set your OpenAI API key
api_key = "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"
openai.api_key = api_key

# Read the contents of your documents into a list
document_files = ["faq1.txt", "faq2.txt", "faq3.txt"]

documents = []
for file_name in document_files:
    with open(file_name, 'r') as file:
        document_text = file.read()
        documents.append(document_text)

# Function to split text into chunks of at least 500 tokens
def split_text_into_chunks(text, min_tokens=500):
    chunks = []
    current_chunk = ""
    current_chunk_tokens = 0

    for token in text.split():
        current_chunk_tokens += 1

        if current_chunk_tokens < min_tokens:
            current_chunk += token + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = ""
            current_chunk_tokens = 0

    if current_chunk_tokens > 0:
        chunks.append(current_chunk.strip())

    return chunks

# Split each document into chunks of at least 500 tokens
document_chunks = {}
for i, document_text in enumerate(documents):
    chunks = split_text_into_chunks(document_text, min_tokens=500)
    document_chunks[f"Document {i + 1}"] = chunks

# User input using Streamlit
user_input = st.text_input("Ask a question:")
search_button = st.button("Search")

if search_button:
    best_answer = None
    best_document = None

    for document_name, chunks in document_chunks.items():
        context = ""

        for chunk in chunks:
            if len(context.split()) + len(chunk.split()) <= 500:
                context += chunk + " "
            else:
                break

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Context from {document_name}:\n{context}\nQuestion: {user_input}\nAnswer:",
            max_tokens=100
        )

        answer = response.choices[0].text.strip()

        # Scoring results
        if best_answer is None:
            best_answer = answer
            best_document = document_name

    st.subheader(f"Best answer from {best_document}:")
    st.write(best_answer)
