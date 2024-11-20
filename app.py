import gradio as gr
import re
from retrieval import TextMatcher
from API_example import LLM_API


# Function to handle the query and generate response and table
def handle_query(query):
    # Generate the summary using the query
    response_text = analyzer.generate_summary(query, top_n=1000)

    # Extract the concise answer and the table
    concise_answer, table_data = extract_concise_answer_and_table(response_text)

    # Check if table_data is empty and set the notice accordingly
    notice = "No supporting data available for visualization." if not table_data else ""

    return concise_answer, table_data, notice


def extract_concise_answer_and_table(response_text):
    # Use regex to separate the concise answer and the table
    concise_answer_match = re.search(r"### Concise Answer\n(.*?)\n###", response_text, re.DOTALL)
    table_match = re.search(r"### Organized Information into a Table\n\n(.*)", response_text, re.DOTALL)

    concise_answer = concise_answer_match.group(1).strip() if concise_answer_match else "No concise answer found."
    table_markdown = table_match.group(1).strip() if table_match else ""

    # Convert the markdown table to a list of lists
    table_data = convert_markdown_to_list_of_lists(table_markdown)

    return concise_answer, table_data


def convert_markdown_to_list_of_lists(markdown_table):
    # Convert markdown table to a list of lists
    try:
        lines = markdown_table.split('\n')
        table_data = []
        for line in lines:
            if line.strip():  # Skip empty lines
                table_data.append([cell.strip() for cell in line.split('|') if cell.strip()])
        return table_data
    except Exception as e:
        print(f"Error converting markdown to list of lists: {e}")
        return []  # Return an empty list on error


with gr.Blocks(theme=gr.themes.Ocean()) as demo:
    gr.Markdown("## Chatbot with Data Visualization")

    with gr.Row(show_progress=True):
        text_input = gr.Textbox(placeholder="Ask me anything...", label="Your Question")
        submit_btn = gr.Button("Submit")

    text_output = gr.Textbox(label="Response")
    table_output = gr.Dataframe(label="Supporting Data Visualization")

    # Add a notice component
    notice_output = gr.Textbox(label="Notice")

    # Initialize the LLM_API
    api_key_Gemini = "AIzaSyCLFFxeTtwHObbN2HlaCLZo-MxppsszChg"
    api_key_OpenAI = "sk-fOm2221aa87eef6a86afa9e29c1af54ddab98e7e637IxpP0"
    matcher = TextMatcher()
    analyzer = LLM_API(api_type='openai', api_key=api_key_OpenAI, matcher=matcher)


    def handle_query_with_table_width(query):
        concise_answer, table_data, notice = handle_query(query)
        table_data_config = {}
        if table_data:
            table_data_config = {
                "headers": table_data[0],
                "data": table_data[1:],
                "metadata": None,
                "max_height": "auto",
                "min_width": "100%",
                "scale": 2,
                "column_widths": ["20%"] * len(table_data[0]) if table_data else None,
            }

        return concise_answer, table_data_config, notice


    submit_btn.click(handle_query_with_table_width, inputs=text_input,
                     outputs=[text_output, table_output, notice_output])

demo.launch()
