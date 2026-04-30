from llm import get_answer
from tools import summarize_tool, explain_tool, compare_tool
from rag_pipeline import get_relevant_chunks

def select_tool(question):
    prompt = f"""
    Decide the best tool for this question:
    
    Question: {question}
    
    Options:
    - summarize
    - explain
    - compare
    
    Answer only one word.
    """
    
    tool = get_answer("", prompt).lower()
    
    return tool

# 🧠 Step 1: Plan the question
def plan_question(question):
    prompt = f"""
    Break this question into 2-3 smaller sub-questions:
    Question: {question}
    
    Give output as numbered list.
    """
    
    plan = get_answer("", prompt)
    
    # Convert into list
    sub_questions = [q.strip() for q in plan.split("\n") if q.strip()]
    
    return sub_questions


# 🔍 Step 2: Get answers for each sub-question
def solve_subquestions(sub_questions, index, chunks):
    answers = []
    
    for sub_q in sub_questions:
        relevant_chunks = get_relevant_chunks(sub_q, index, chunks)
        context = " ".join(relevant_chunks)
        
        ans = get_answer(context, sub_q)
        
        answers.append((sub_q, ans))
    
    return answers


# 🤖 Step 3: Combine into final answer
def generate_final_answer(question, sub_answers):
    
    combined_text = ""
    
    for q, a in sub_answers:
        combined_text += f"{q}\n{a}\n\n"
    
    # 🧠 Select tool
    tool = select_tool(question)
    
    # 🔥 Use selected tool
    if "summarize" in tool:
        final_answer = summarize_tool(combined_text)
    
    elif "compare" in tool:
        final_answer = compare_tool(combined_text)
    
    else:
        final_answer = explain_tool(combined_text)
    
    return final_answer, tool