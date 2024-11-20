import gradio as gr
from retrieval import TextMatcher
from API_example import LLM_API

# 假设这是从API获取的新闻数据
def format_news_data(news_data):
    # 格式化新闻数据为Markdown格式
    formatted_data = f"<h3>{news_data['headline']}</h3>"
    formatted_data += f"<strong>Category:</strong> {news_data['category']}<br>"
    formatted_data += f"<strong>Short Description:</strong> {news_data['short_description']}<br>"
    formatted_data += f"<strong>Authors:</strong> {news_data['authors']}<br>"
    formatted_data += f"<strong>Date:</strong> {news_data['date']}"
    return formatted_data

with gr.Blocks() as demo:
    gr.Markdown("## Chatbot with Data Visualization")

    with gr.Row():
        text_input = gr.Textbox(placeholder="Ask me anything...")
        submit_btn = gr.Button("Submit")

    text_output = gr.Textbox(label="Response", element="div")  # 使用div元素以便支持HTML
    # plot_output = gr.Image(label="Data Visualization")

    # Initialize the LLM_API
    api_key = "AIzaSyCLFFxeTtwHObbN2HlaCLZo-MxppsszChg"  # Replace with your actual API key
    matcher = TextMatcher()
    analyzer = LLM_API(api_key, matcher)

    submit_btn.click(fn=lambda x: format_news_data(analyzer.generate_summary(x)),
                     inputs=text_input,
                     outputs=text_output)  # 将生成的摘要格式化为新闻数据

    demo.launch()