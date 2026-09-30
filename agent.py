from rag_tool import answer_question 
from langchain_ollama import ChatOllama 
from transcript_analyzer import analyze_transcript 
from study_plan import create_study_plan 
from job_tool import search_jobs 
 
 
llm = ChatOllama( 
    model="qwen3:0.6b" 
) 
 
question = input("\nStudent: ") 
 
prompt = f""" 
You are an education assistant. 
 
Classify the student's request into exactly ONE category: 
 
ANALYZE 
STUDY_PLAN 
RAG 
JOB_SEARCH 
OTHER 
 
ANALYZE = marks, weak subjects, strengths, academic performance. 
 
STUDY_PLAN = create or modify a study plan. 
 
RAG = explain or answer something using information from the student's 
transcript or study material. 
 
JOB_SEARCH = ANY request involving: 
- jobs 
- job opportunities 
- internships 
- internship opportunities 
- vacancies 
- hiring 
- employment 
- career opportunities 
- finding a role 
 
Examples: 
- Find Java internships in Hyderabad. 
- Find Python developer jobs in Bangalore. 
- Search for AI jobs. 
- Show me software internships. 
- Find backend developer vacancies. 
 
OTHER = anything else. 
 
Student request: 
 
{question} 
 
Return ONLY the category name. 
""" 
 
decision = llm.invoke(prompt).content.strip().upper() 
 
print("\nAgent decision:", decision) 
 
 
if "ANALYZE" in decision: 
 
 
    print("\nRunning academic analysis...") 
 
    result = analyze_transcript( 
        "documents/transcript.pdf" 
    ) 
 
    print(result) 
 
 
elif "STUDY_PLAN" in decision: 
 
    result = create_study_plan( 
    "documents/transcript.pdf" 
    ) 
 
    print(result) 
 
 
 
elif "RAG" in decision: 
 
    print("\nRAG answer:") 
 
    answer = answer_question(question) 
 
    print(answer) 
 
 
elif "JOB_SEARCH" in decision: 
 
    print("\nSearching for jobs...") 
 
    extraction_prompt = f""" 
Extract the job search information from this student request. 
 
Student request: 
{question} 
 
Return EXACTLY in this format: 
 
KEYWORD: <job skill or job title> 
LOCATION: <city> 
 
Example: 
KEYWORD: Python developer 
LOCATION: Hyderabad 
 
Do not add anything else. 
""" 
 
    extraction = llm.invoke(extraction_prompt).content.strip() 
 
    print("\nSearch details:") 
    print(extraction) 
 
    keyword = "" 
    location = "Hyderabad" 
 
    for line in extraction.splitlines(): 
 
        if line.upper().startswith("KEYWORD:"): 
            keyword = line.split(":", 1)[1].strip() 
 
        elif line.upper().startswith("LOCATION:"): 
            location = line.split(":", 1)[1].strip() 
 
    results = search_jobs( 
        keyword=keyword, 
        location=location, 
        results=5 
    ) 
 
    print("\n===== JOB RESULTS =====") 
    print(results) 
 
 
else: 
 
    print( 
        "\nI can help with your academic analysis, " 
        "study plan, study material, or job search." 
    )