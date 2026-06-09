from groq import Groq
from embed import retrieve
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(question):
    # Retrieve relevant chunks
    chunks = retrieve(question)
    
    # Build context from retrieved chunks
    context = "\n\n".join([c["text"] for c in chunks])
    sources = list(set([c["source"] for c in chunks]))
    
    # Generate grounded response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that answers questions about "
                    "Cleveland State University dining based only on student reviews. "
                    "Answer using only the information in the provided reviews. "
                    "If the reviews don't contain enough information to answer, "
                    "say 'I don't have enough information on that.' "
                    "Do not use any outside knowledge."
                )
            },
            {
                "role": "user",
                "content": f"Reviews:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    
    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }