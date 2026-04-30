from llm import get_answer

def summarize_tool(context):
    return get_answer(context, "Summarize this content clearly")


def explain_tool(context):
    return get_answer(context, "Explain this in simple terms")


def compare_tool(context):
    return get_answer(context, "Compare the concepts in detail")