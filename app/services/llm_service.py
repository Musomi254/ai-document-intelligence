from transformers import pipeline

# Lightweight local generation model
generator = pipeline(
    "text-generation",
    model="google/flan-t5-base"
)


def generate_answer(context: str, question: str,conversation_history: str = ""):

    prompt = f"""
You are a helpful and professional assistant. Answer the user's question using ONLY the provided context. 
If the answer cannot be found in the provided context, say "I cannot find the answer to that in the available documents." Do not use any outside knowledge, assume any information, or make up facts. 

Always cite the relevant sources using the document titles or links provided in the context when possible.

Conversation History:
{conversation_history}

Context:
{context}

Question:
{question}

Answer:
"""

    result = generator(
        prompt,
        max_new_tokens=200,
        temperature=0.3
    )

    return result[0]["generated_text"]