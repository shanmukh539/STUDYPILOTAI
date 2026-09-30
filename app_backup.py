import gradio as gr

from transcript_analyzer import analyze_transcript
from study_plan import create_study_plan
from rag_tool import answer_question
from job_tool import search_jobs


def analyze_pdf(pdf):
    if pdf is None:
        return "Please upload a transcript PDF."

    return analyze_transcript(pdf)


def generate_plan(pdf):
    if pdf is None:
        return "Please upload a transcript PDF."

    return create_study_plan(pdf)


def ask_question(question):
    if not question.strip():
        return "Please enter a question."

    return answer_question(question)


def find_jobs(query):
    if not query.strip():
        return "Please enter a job or internship search."

    # For now, use Hyderabad as the default location.
    return search_jobs(
        keyword=query,
        location="Hyderabad",
        results=5
    )


with gr.Blocks(
    title="StudyPilot AI"
) as demo:

    gr.Markdown(
        """
        # 🎓 StudyPilot AI
        ### Your AI-powered academic assistant

        Upload your transcript, analyze your performance,
        generate a personalized study plan, ask academic questions,
        and discover relevant jobs and internships.
        """
    )

    with gr.Row():

        with gr.Column():

            transcript = gr.File(
                label="📄 Upload Your Transcript",
                file_types=[".pdf"],
                type="filepath"
            )

            analyze_button = gr.Button(
                "📊 Analyze My Performance",
                variant="primary"
            )

            plan_button = gr.Button(
                "📚 Generate Study Plan"
            )

        with gr.Column():

            analysis_output = gr.Textbox(
                label="📊 Academic Analysis",
                lines=15
            )

            plan_output = gr.Textbox(
                label="📚 Personalized Study Plan",
                lines=15
            )

    analyze_button.click(
        fn=analyze_pdf,
        inputs=transcript,
        outputs=analysis_output
    )

    plan_button.click(
        fn=generate_plan,
        inputs=transcript,
        outputs=plan_output
    )

    gr.Markdown("---")

    gr.Markdown(
        """
        ## 💬 Ask Your Academic Assistant

        Ask questions about your transcript and academic performance.
        """
    )

    question = gr.Textbox(
        label="Your Question",
        placeholder="Example: Explain my DBMS performance",
        lines=2
    )

    ask_button = gr.Button(
        "🤖 Ask StudyPilot",
        variant="primary"
    )

    answer = gr.Textbox(
        label="AI Answer",
        lines=8
    )

    ask_button.click(
        fn=ask_question,
        inputs=question,
        outputs=answer
    )

    gr.Markdown("---")

    gr.Markdown(
        """
        ## 💼 Jobs & Internships

        Search for real job and internship opportunities.
        """
    )

    job_query = gr.Textbox(
        label="🔎 What job are you looking for?",
        placeholder="Example: Python developer jobs",
        lines=2
    )

    job_button = gr.Button(
        "🚀 Find Jobs",
        variant="primary"
    )

    job_output = gr.Textbox(
        label="💼 Job Results",
        lines=15
    )

    job_button.click(
        fn=find_jobs,
        inputs=job_query,
        outputs=job_output
    )


demo.launch()