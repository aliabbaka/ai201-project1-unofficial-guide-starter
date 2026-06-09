import gradio as gr
from query import ask

def handle_query(question):
    if not question.strip():
        return "", ""
    try:
        result = ask(question)
    except Exception as e:
        return f"Error: {e}", ""
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(theme=gr.themes.Soft(), title="CSU Dining Guide") as demo:
    gr.HTML("""
        <div style="text-align:center; padding:1rem 0;">
            <h1 style="font-size:2rem; font-weight:700; color:#006747;">
                🍽️ CSU Unofficial Dining Guide
            </h1>
            <p style="color:#6b7280;">
                Ask anything about Cleveland State dining — answers from real student reviews.
            </p>
        </div>
    """)

    inp = gr.Textbox(
        placeholder='e.g. "Are there good vegetarian options?"',
        label="Your question"
    )
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=6)
    sources = gr.Textbox(label="Retrieved from", lines=2)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()