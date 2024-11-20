import gradio as gr
import re
import plotly.graph_objects as go
from retrieval import TextMatcher
from API_example import LLM_API


def create_pie_chart(response_data):
    """
    Create a pie chart using the response data.
    Args:
        response_data (dict): Dictionary containing 'category' and 'number' lists
    Returns:
        plotly.graph_objects.Figure: Pie chart figure
    """
    if not response_data or 'category' not in response_data or 'number' not in response_data:
        return None

    fig = go.Figure(data=[go.Pie(
        labels=response_data['category'],
        values=response_data['number'],
        hole=0.3,  # Creates a donut chart effect
        textinfo='percent+label',
        textposition='inside',
        showlegend=True
    )])

    fig.update_layout(
        title="Category Distribution",
        width=600,
        height=400,
        margin=dict(t=30, b=0, l=0, r=0)
    )

    return fig


# Function to handle the query and generate response and table
def handle_query(query):
    # Generate the summary using the query
    response_text = analyzer.generate_summary(query, top_n=1000)
    response_data = analyzer.get_data(response_text)

    # Extract the concise answer and the table
    concise_answer, table_data = extract_concise_answer_and_table(response_text)

    # Check if table_data is empty and set the notice accordingly
    notice = "No supporting data available for visualization." if not table_data else ""

    return concise_answer, table_data, notice, response_data


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


def handle_query_with_visualizations(query):
    concise_answer, table_data, notice, response_data = handle_query(query)

    # Prepare table data configuration
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

    # Create pie chart
    pie_chart = create_pie_chart(response_data)

    return concise_answer, table_data_config, notice, pie_chart


# Initialize Gradio interface
with gr.Blocks(theme=gr.themes.Ocean()) as demo:
    gr.Markdown("## Chatbot with Data Visualization")

    with gr.Row(show_progress=True):
        text_input = gr.Textbox(placeholder="Ask me anything...", label="Your Question")
        submit_btn = gr.Button("Submit")

    text_output = gr.Textbox(label="Response")

    # First visualization row for table
    with gr.Row():
        table_output = gr.Dataframe(label="Supporting Data Visualization", scale=1)

    # Add a notice component, only show when there is no available supporting data
    with gr.Row():
        notice_output = gr.Textbox(label="Notice",
                                   placeholder="Words will be more convincing with supporting data, right?")

    # Second visualization row for pie chart
    with gr.Row():
        pie_chart_output = gr.Plot(label="Category Distribution")

    # Initialize the LLM_API (rest of your code remains the same)
    api_key_Gemini = "AIzaSyCLFFxeTtwHObbN2HlaCLZo-MxppsszChg"
    api_key_OpenAI = "sk-fOm2221aa87eef6a86afa9e29c1af54ddab98e7e637IxpP0"
    matcher = TextMatcher()
    analyzer = LLM_API(api_type='openai', api_key=api_key_OpenAI, matcher=matcher)

    submit_btn.click(
        handle_query_with_visualizations,
        inputs=text_input,
        outputs=[text_output, table_output, notice_output, pie_chart_output]
    )

if __name__ == "__main__":
    demo.launch()
