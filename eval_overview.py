import json
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sentiment_analyzer = SentimentIntensityAnalyzer()


def read_json_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # 使用正则表达式匹配所有独立的JSON对象
        json_objects = re.findall(r'\{.*?\}', content)
        for json_str in json_objects:
            try:
                data.append(json.loads(json_str))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {file_path}: {e}")
    return data


def calculate_scores(files):
    total_scores = {"accuracy": [], "satisfaction": [], "richness": []}
    user_scores = {}

    for file_index, file_content in enumerate(files):
        user_accuracy = []
        user_satisfaction = []
        user_richness = []
        user_comments = []
        for score in file_content:
            total_scores["accuracy"].append(score["accuracy_score"])
            total_scores["satisfaction"].append(score["satisfaction_score"])
            total_scores["richness"].append(score["content_richness_score"])
            user_accuracy.append(score["accuracy_score"])
            user_satisfaction.append(score["satisfaction_score"])
            comment = score.get("overall_comment", "")
            if comment:
                sentiment = sentiment_analyzer.polarity_scores(comment)
                user_comments.append({"comment": comment, "sentiment": sentiment})

        user_scores[f"User {file_index + 1}"] = {
            "accuracy": sum(user_accuracy) / len(user_accuracy) if user_accuracy else 0,
            "satisfaction": sum(user_satisfaction) / len(user_satisfaction) if user_satisfaction else 0,
            "richness": sum(user_richness) / len(user_richness) if user_richness else 0,
            "comments": user_comments
        }

    question_scores = {
        "accuracy": sum(total_scores["accuracy"]) / len(total_scores["accuracy"]),
        "satisfaction": sum(total_scores["satisfaction"]) / len(total_scores["satisfaction"]),
        "richness": sum(total_scores["richness"]) / len(total_scores["richness"])
    }

    return question_scores, user_scores


def generate_markdown_table(question_scores, user_scores):
    md_table = "| Question/Metric | Accuracy | Satisfaction | Richness |\n"
    md_table += "|----------------|----------|--------------|---------|\n"
    for i in range(1, 8):  # 假设有7个问题
        md_table += f"| Question {i} | {question_scores['accuracy']:.2f} | {question_scores['satisfaction']:.2f} | {question_scores['richness']:.2f} |\n"

    md_table += "\n| User/File | Accuracy | Satisfaction | Richness |\n"
    md_table += "|-----------|----------|--------------|---------|\n"
    for user, scores in user_scores.items():
        md_table += f"| {user} | {scores['accuracy']:.2f} | {scores['satisfaction']:.2f} | {scores['richness']:.2f} |\n"

    # 筛选并添加情感倾向性强的评论
    for user, scores in user_scores.items():
        sorted_comments = sorted(scores["comments"], key=lambda x: abs(x["sentiment"]["compound"]), reverse=True)[:3]
        md_table += f"\n## {user}'s Top 3 Comments\n"
        md_table += "| Comment | Sentiment Score |\n"
        md_table += "|---------|-----------------|\n"
        for comment in sorted_comments:
            md_table += f"| {comment['comment']} | {comment['sentiment']['compound']:.2f} |\n"
    return md_table


def main(file_paths):
    files = []
    for path in file_paths:
        file_content = read_json_file(path)
        if file_content:
            files.append(file_content)
        else:
            print(f"Skipping file {path} due to JSON decoding error.")
    if not files:
        print("No valid JSON files found.")
        return

    question_scores, user_scores = calculate_scores(files)
    md_table = generate_markdown_table(question_scores, user_scores)

    # 将结果保存到Markdown文件
    with open("report.md", "w", encoding='utf-8') as md_file:
        md_file.write(md_table)

    print("Markdown report has been generated.")


if __name__ == "__main__":
    # 假设这里是主函数中给出的文件路径列表
    file_paths = [
        "E:\\study\\hk-polyu\\NLP\\group\\feedback_lzr.json",
        "E:\\study\\hk-polyu\\NLP\\group\\feedback_jz.json",
        "E:\\study\\hk-polyu\\NLP\\group\\feedback_zlt.json",
        "E:\\study\\hk-polyu\\NLP\\group\\feedback_wjy.json"
    ]
    main(file_paths)