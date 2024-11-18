import gradio as gr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import google.generativeai as genai
from retrieval import TextMatcher
from API_example import LLM_API


# Sample data visualization function
def generate_plot(data):
    # Simulate generating a plot from data
    x = np.linspace(0, 10, 50)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Sample Plot")

    # Convert figure to PNG bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)

    # Check if any plot was generated
    if buf.getvalue():
        return buf.getvalue()
    else:
        return "No plot generated."


with gr.Blocks() as demo:
    gr.Markdown("## Chatbot with Data Visualization")

    with gr.Row():
        text_input = gr.Textbox(placeholder="Ask me anything...")
        submit_btn = gr.Button("Submit")

    text_output = gr.Textbox(label="Response")
    # plot_output = gr.Image(label="Data Visualization")

    # Initialize the LLM_API
    api_key_Gemini = "AIzaSyCLFFxeTtwHObbN2HlaCLZo-MxppsszChg"  # Replace with your actual API key
    api_key_OpenAI = "sk-fOm2221aa87eef6a86afa9e29c1af54ddab98e7e637IxpP0"
    matcher = TextMatcher()
    analyzer = LLM_API(api_type='openai', api_key=api_key_OpenAI, matcher=matcher)

    submit_btn.click(analyzer.generate_summary, inputs=text_input, outputs=text_output)
    # submit_btn.click(generate_plot, inputs=text_input, outputs=plot_output)

demo.launch()
