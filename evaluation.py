import gradio as gr
from API_example import LLM_API
from retrieval import TextMatcher
import json

# 初始化API
api_key = "AIzaSyCLFFxeTtwHObbN2HlaCLZo-MxppsszChg"  # 替换为你的实际API密钥
api_key_OpenAI = "sk-fOm2221aa87eef6a86afa9e29c1af54ddab98e7e637IxpP0"
matcher = TextMatcher()
analyzer = LLM_API("openai", api_key_OpenAI, matcher)


# 定义处理和保存反馈的函数
def save_feedback(accuracy_score, satisfaction_score, content_richness_score, overall_comment):
    feedback = {
        "accuracy_score": accuracy_score,
        "satisfaction_score": satisfaction_score,
        "content_richness_score": content_richness_score,
        "overall_comment": overall_comment
    }
    # 将反馈保存到文件
    with open("feedback.json", "a") as f:
        json.dump(feedback, f)
        f.write("\n")

# 定义收集用户反馈的函数
def collect_feedback(response):
    accuracy_score = gr.Slider(minimum=1, maximum=5, step=1, label="Accuracy Score (1-5)", value=3)
    satisfaction_score = gr.Slider(minimum=1, maximum=5, step=1, label="Satisfaction Score (1-5)", value=3)
    content_richness_score = gr.Slider(minimum=1, maximum=5, step=1, label="Content Richness Score (1-5)", value=3)
    overall_comment = gr.Textbox(label="Overall Comment (Optional)")
    return accuracy_score, satisfaction_score, content_richness_score, overall_comment

# 设置Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("## Chatbot with Data Visualization")

    with gr.Row():
        text_input = gr.Textbox(placeholder="Ask me anything...")
        generate_btn = gr.Button("Generate Response")

    text_output = gr.Textbox(label="Response")

    # 生成回答按钮
    generate_btn.click(
        fn=lambda query: analyzer.generate_summary(query),
        inputs=text_input,
        outputs=text_output
    )

    # 评估回答
    accuracy_score = gr.Slider(minimum=1, maximum=5, step=1, label="Accuracy Score (1-5)", value=3)
    satisfaction_score = gr.Slider(minimum=1, maximum=5, step=1, label="Satisfaction Score (1-5)", value=3)
    content_richness_score = gr.Slider(minimum=1, maximum=5, step=1, label="Content Richness Score (1-5)", value=3)
    overall_comment = gr.Textbox(label="Overall Comment (Optional)")
    evaluate_btn = gr.Button("Submit Feedback")

    # 提交反馈按钮
    evaluate_btn.click(
        fn=save_feedback,
        inputs=[accuracy_score, satisfaction_score, content_richness_score, overall_comment],
        outputs=[]
    )

demo.launch()