import gradio as gr
import re
from pypdf import PdfReader

from transcript_analyzer import analyze_transcript
from study_plan import create_study_plan
from rag_tool import answer_question
from job_tool import search_jobs


# ============================================================
# BACKEND
# ============================================================

def analyze_pdf(pdf):
    if pdf is None:
        return "⚠️ Please upload your transcript PDF."

    return analyze_transcript(pdf)


def generate_plan(pdf):
    if pdf is None:
        return "⚠️ Please upload your transcript PDF."

    return create_study_plan(pdf)


def ask_question(question):
    if not question or not question.strip():
        return "⚠️ Please enter a question."

    return answer_question(question)


def find_jobs(keyword, location):

    if not keyword or not keyword.strip():
        return "<div class='empty-state'>🔎 Please enter a job title or skill.</div>"

    if not location or not location.strip():
        location = "Hyderabad"

    jobs = search_jobs(
        keyword=keyword.strip(),
        location=location.strip(),
        results=5
    )

    if isinstance(jobs, str):
        return f"<div class='empty-state'>⚠️ {jobs}</div>"

    if len(jobs) == 0:
        return """
        <div class="empty-state">
            🔎 No opportunities found.<br>
            Try another skill or location.
        </div>
        """

    cards = []

    for job in jobs:

        title = job.get("title", "Unknown title")
        company = job.get("company", "Unknown company")
        job_location = job.get("location", "Unknown location")
        url = job.get("url", "#")

        cards.append(
            f"""
            <div class="job-card">

                <div class="job-top">

                    <div class="job-icon">
                        💼
                    </div>

                    <div>

                        <div class="job-title">
                            {title}
                        </div>

                        <div class="job-company">
                            {company}
                        </div>

                    </div>

                </div>

                <div class="job-location">
                    📍 {job_location}
                </div>

                <a
                    href="{url}"
                    target="_blank"
                    class="job-button"
                >
                    View Opportunity ↗
                </a>

            </div>
            """
        )

    return "".join(cards)


def academic_dashboard(pdf):

    if pdf is None:
        return """
        <div class="empty-state">
            📄 Upload your transcript to generate your academic dashboard.
        </div>
        """

    reader = PdfReader(pdf)

    text = ""

    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"

    pattern = r"([A-Za-z][A-Za-z &]+?)\s+100\s+(\d+)\s+[A-Z][+]?"

    matches = re.findall(pattern, text)

    subjects = {}

    for subject, marks in matches:
        subjects[subject.strip()] = int(marks)

    if not subjects:
        return """
        <div class="empty-state">
            ⚠️ No subjects could be detected.
        </div>
        """

    average = sum(subjects.values()) / len(subjects)

    best_subject = max(
        subjects.items(),
        key=lambda x: x[1]
    )

    top_priority = min(
        subjects.items(),
        key=lambda x: x[1]
    )

    ranked = sorted(
        subjects.items(),
        key=lambda x: x[1]
    )

    html = f"""
    <div class="dashboard">

        <div class="stat-grid">

            <div class="stat-card blue">

                <div class="stat-icon">
                    📊
                </div>

                <div class="stat-value">
                    {average:.2f}
                </div>

                <div class="stat-label">
                    Overall Average
                </div>

            </div>


            <div class="stat-card green">

                <div class="stat-icon">
                    🏆
                </div>

                <div class="stat-value">
                    {best_subject[1]}/100
                </div>

                <div class="stat-label">
                    Best Subject
                </div>

                <div class="stat-sub">
                    {best_subject[0]}
                </div>

            </div>


            <div class="stat-card red">

                <div class="stat-icon">
                    🎯
                </div>

                <div class="stat-value">
                    {top_priority[1]}/100
                </div>

                <div class="stat-label">
                    Top Priority
                </div>

                <div class="stat-sub">
                    {top_priority[0]}
                </div>

            </div>

        </div>


        <div class="performance-card">

            <div class="performance-header">

                <div>

                    <div class="performance-title">
                        Subject Performance
                    </div>

                    <div class="performance-subtitle">
                        Your academic performance at a glance
                    </div>

                </div>

                <div class="subject-count">
                    {len(subjects)} Subjects
                </div>

            </div>
    """

    for subject, marks in ranked:

        if marks < 60:
            priority = "HIGH"
            badge = "high"

        elif marks < 70:
            priority = "MEDIUM"
            badge = "medium"

        else:
            priority = "LOW"
            badge = "low"

        html += f"""
            <div class="subject-row">

                <div class="subject-header">

                    <span class="subject-name">
                        {subject}
                    </span>

                    <span class="priority-badge {badge}">
                        {priority}
                    </span>

                </div>


                <div class="progress-wrapper">

                    <div
                        class="progress-fill"
                        style="width:{marks}%"
                    ></div>

                </div>


                <div class="score">
                    {marks}/100
                </div>

            </div>
        """

    html += """
        </div>
    </div>
    """

    return html


# ============================================================
# PREMIUM BLUE UI CSS
# ============================================================

css = """

/* =========================================================
   GLOBAL PAGE
   ========================================================= */

body {

    background:

        radial-gradient(
            circle at 15% 5%,
            rgba(37,99,235,0.13),
            transparent 28%
        ),

        radial-gradient(
            circle at 85% 10%,
            rgba(14,165,233,0.10),
            transparent 28%
        ),

        linear-gradient(
            135deg,
            #050b14,
            #091525 50%,
            #06101d
        ) !important;

    color:
        #f8fafc !important;
}


/* =========================================================
   MAIN GRADIO CONTAINER
   ========================================================= */

.gradio-container {

    max-width:
        1320px !important;

    margin:
        auto !important;

    padding:
        25px
        35px
        70px !important;

    background:
        transparent !important;
}


/* =========================================================
   DEFAULT TEXT
   ========================================================= */

.gradio-container,
.gradio-container label,
.gradio-container p,
.gradio-container span,
.gradio-container h1,
.gradio-container h2,
.gradio-container h3,
.gradio-container h4,
.gradio-container strong {

    color:
        #f8fafc !important;
}


/* =========================================================
   INPUTS
   ========================================================= */

input,
textarea {

    background:
        #0c1d33 !important;

    color:
        #f8fafc !important;

    border:
        1px solid
        rgba(96,165,250,0.28) !important;

    border-radius:
        14px !important;
}


input::placeholder,
textarea::placeholder {

    color:
        #8da4c0 !important;
}


/* =========================================================
   HERO
   ========================================================= */

#hero {

    position:
        relative;

    overflow:
        hidden;

    padding:
        52px 48px;

    margin:
        10px 0 42px;

    border-radius:
        30px;

    background:

        linear-gradient(
            135deg,
            #132e55,
            #0b1d37 55%,
            #092b3d
        ) !important;

    border:
        1px solid
        rgba(96,165,250,0.28);

    box-shadow:

        0 30px 100px
        rgba(0,0,0,0.45),

        inset
        0 1px
        rgba(255,255,255,0.08);
}


#hero::before {

    content:
        "";

    position:
        absolute;

    width:
        380px;

    height:
        380px;

    left:
        -150px;

    top:
        -180px;

    background:
        rgba(37,99,235,0.22);

    border-radius:
        50%;

    filter:
        blur(70px);
}


#hero::after {

    content:
        "";

    position:
        absolute;

    width:
        350px;

    height:
        350px;

    right:
        -160px;

    bottom:
        -180px;

    background:
        rgba(14,165,233,0.18);

    border-radius:
        50%;

    filter:
        blur(75px);
}


.hero-content {

    position:
        relative;

    z-index:
        2;

    text-align:
        center;
}


.hero-logo {

    display:
        inline-flex;

    align-items:
        center;

    gap:
        12px;

    margin-bottom:
        18px;

    font-size:
        17px;

    font-weight:
        700;

    letter-spacing:
        1px;

    color:
        #dbeafe !important;
}


.logo-mark {

    width:
        38px;

    height:
        38px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        12px;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #06b6d4
        );

    font-size:
        18px;

    font-weight:
        900;
}


#hero h1 {

    margin:
        0;

    font-size:
        58px;

    line-height:
        1;

    font-weight:
        850;

    letter-spacing:
        -2.5px;

    color:
        #ffffff !important;
}


.hero-tagline {

    margin-top:
        18px;

    font-size:
        22px;

    font-weight:
        600;

    color:
        #dbeafe !important;
}


.hero-description {

    max-width:
        700px;

    margin:
        15px auto 0;

    font-size:
        15px;

    line-height:
        1.7;

    color:
        #a9c2df !important;
}


.hero-pills {

    margin-top:
        28px;
}


.pill {

    display:
        inline-block;

    padding:
        8px 14px;

    margin:
        4px;

    border-radius:
        999px;

    background:
        rgba(59,130,246,0.13);

    border:
        1px solid
        rgba(147,197,253,0.22);

    font-size:
        12px;

    color:
        #dbeafe !important;
}


/* =========================================================
   SECTION HEADINGS
   ========================================================= */

.section-heading {

    font-size:
        28px;

    font-weight:
        800;

    letter-spacing:
        -0.7px;

    margin:
        28px 0 6px;

    color:
        #ffffff !important;
}


.section-description {

    color:
        #8eabc9 !important;

    font-size:
        14px;

    margin-bottom:
        22px;
}


/* =========================================================
   FEATURE CARDS
   ========================================================= */

.feature-card {

    min-height:
        175px;

    padding:
        27px !important;

    border-radius:
        22px !important;

    background:

        linear-gradient(
            145deg,
            #194477,
            #12345b
        ) !important;

    border:
        1px solid
        rgba(96,165,250,0.34) !important;

    box-shadow:
        0 18px 50px
        rgba(0,0,0,0.30) !important;

    transition:
        transform .25s ease,
        border-color .25s ease,
        box-shadow .25s ease;
}


.feature-card:hover {

    transform:
        translateY(-6px);

    border-color:
        rgba(147,197,253,0.65)
        !important;

    box-shadow:
        0 25px 65px
        rgba(0,0,0,0.40)
        !important;
}


.feature-icon {

    font-size:
        31px;

    margin-bottom:
        15px;
}


.feature-title {

    font-size:
        19px;

    font-weight:
        750;

    margin-bottom:
        8px;

    color:
        #ffffff !important;
}


.feature-text {

    color:
        #c2d6eb !important;

    font-size:
        13px;

    line-height:
        1.65;
}


/* =========================================================
   CONTENT CARDS
   ========================================================= */

.glass-card {

    padding:
        27px !important;

    border-radius:
        22px !important;

    background:

        linear-gradient(
            145deg,
            #173c68,
            #102f52
        ) !important;

    border:
        1px solid
        rgba(96,165,250,0.30) !important;

    box-shadow:
        0 18px 55px
        rgba(0,0,0,0.32) !important;
}


/* =========================================================
   MARKDOWN INSIDE CARDS
   ========================================================= */

.glass-card h3,
.glass-card h2,
.glass-card h4 {

    color:
        #ffffff !important;
}


.glass-card p {

    color:
        #c4d7ea !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.primary-btn {

    min-height:
        48px !important;

    border-radius:
        13px !important;

    border:
        none !important;

    font-weight:
        750 !important;

    background:

        linear-gradient(
            135deg,
            #2563eb,
            #0891b2
        ) !important;

    color:
        #ffffff !important;

    box-shadow:
        0 8px 25px
        rgba(37,99,235,0.25);

    transition:
        transform .2s ease,
        box-shadow .2s ease;
}


.primary-btn:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 14px 35px
        rgba(37,99,235,0.40);
}


/* =========================================================
   DASHBOARD
   ========================================================= */

.dashboard {

    margin-top:
        8px;
}


.stat-grid {

    display:
        grid;

    grid-template-columns:
        repeat(3,1fr);

    gap:
        17px;

    margin-bottom:
        18px;
}


.stat-card {

    position:
        relative;

    overflow:
        hidden;

    padding:
        24px;

    min-height:
        130px;

    border-radius:
        20px;

    background:

        linear-gradient(
            145deg,
            #1b4b7e,
            #143961
        ) !important;

    border:
        1px solid
        rgba(96,165,250,0.28) !important;
}


.stat-card::after {

    content:
        "";

    position:
        absolute;

    width:
        100px;

    height:
        100px;

    right:
        -40px;

    bottom:
        -50px;

    border-radius:
        50%;

    filter:
        blur(25px);
}


.stat-card.blue::after {

    background:
        rgba(56,189,248,0.25);
}


.stat-card.green::after {

    background:
        rgba(74,222,128,0.20);
}


.stat-card.red::after {

    background:
        rgba(248,113,113,0.20);
}


.stat-icon {

    font-size:
        23px;

    margin-bottom:
        10px;
}


.stat-value {

    font-size:
        30px;

    font-weight:
        850;

    color:
        #ffffff !important;
}


.stat-label {

    margin-top:
        5px;

    font-size:
        13px;

    color:
        #c1d5e9 !important;
}


.stat-sub {

    margin-top:
        5px;

    font-size:
        12px;

    color:
        #9fb8d3 !important;
}


/* =========================================================
   PERFORMANCE CARD
   ========================================================= */

.performance-card {

    padding:
        25px;

    border-radius:
        20px;

    background:

        linear-gradient(
            145deg,
            #153b65,
            #102f50
        ) !important;

    border:
        1px solid
        rgba(96,165,250,0.26);
}


.performance-header {

    display:
        flex;

    justify-content:
        space-between;

    align-items:
        center;

    margin-bottom:
        25px;
}


.performance-title {

    font-size:
        19px;

    font-weight:
        750;

    color:
        #ffffff !important;
}


.performance-subtitle {

    margin-top:
        5px;

    color:
        #9bb5d0 !important;

    font-size:
        12px;
}


.subject-count {

    padding:
        7px 12px;

    border-radius:
        999px;

    background:
        rgba(59,130,246,0.18);

    border:
        1px solid
        rgba(147,197,253,0.20);

    color:
        #dbeafe !important;

    font-size:
        11px;
}


.subject-row {

    margin-bottom:
        21px;
}


.subject-header {

    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;

    margin-bottom:
        8px;
}


.subject-name {

    font-weight:
        600;

    color:
        #ffffff !important;
}


.priority-badge {

    padding:
        4px 9px;

    border-radius:
        999px;

    font-size:
        10px;

    font-weight:
        800;
}


.priority-badge.high {

    background:
        rgba(248,113,113,0.16);

    color:
        #fecaca !important;
}


.priority-badge.medium {

    background:
        rgba(250,204,21,0.16);

    color:
        #fef08a !important;
}


.priority-badge.low {

    background:
        rgba(74,222,128,0.16);

    color:
        #bbf7d0 !important;
}


.progress-wrapper {

    height:
        8px;

    background:
        #0b223b;

    border-radius:
        999px;

    overflow:
        hidden;
}


.progress-fill {

    height:
        100%;

    background:

        linear-gradient(
            90deg,
            #2563eb,
            #06b6d4
        );

    border-radius:
        999px;
}


.score {

    text-align:
        right;

    margin-top:
        5px;

    color:
        #9ab2ca !important;

    font-size:
        11px;
}


/* =========================================================
   JOB CARDS
   ========================================================= */

.job-card {

    padding:
        22px;

    margin:
        12px 0;

    border-radius:
        18px;

    background:

        linear-gradient(
            145deg,
            #194477,
            #12345a
        ) !important;

    border:
        1px solid
        rgba(96,165,250,0.28);

    transition:
        transform .2s ease,
        border-color .2s ease;
}


.job-card:hover {

    transform:
        translateY(-4px);

    border-color:
        rgba(96,165,250,0.60);
}


.job-top {

    display:
        flex;

    align-items:
        center;

    gap:
        13px;
}


.job-icon {

    width:
        42px;

    height:
        42px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        12px;

    background:
        rgba(37,99,235,0.20);

    font-size:
        19px;
}


.job-title {

    font-size:
        17px;

    font-weight:
        750;

    color:
        #ffffff !important;
}


.job-company {

    margin-top:
        4px;

    color:
        #b9cfe5 !important;

    font-size:
        13px;
}


.job-location {

    margin-top:
        15px;

    color:
        #b9cfe5 !important;

    font-size:
        13px;
}


.job-button {

    display:
        inline-block;

    margin-top:
        15px;

    padding:
        9px 15px;

    border-radius:
        10px;

    background:
        rgba(37,99,235,0.20);

    border:
        1px solid
        rgba(147,197,253,0.25);

    color:
        #dbeafe !important;

    text-decoration:
        none !important;

    font-size:
        12px;

    font-weight:
        700;
}


.job-button:hover {

    background:
        rgba(37,99,235,0.35);
}


/* =========================================================
   EMPTY STATE
   ========================================================= */

.empty-state {

    padding:
        35px;

    text-align:
        center;

    border-radius:
        18px;

    background:

        linear-gradient(
            145deg,
            #17385f,
            #102d4d
        ) !important;

    border:
        1px dashed
        rgba(96,165,250,0.30);

    color:
        #b9cee4 !important;

    line-height:
        1.7;
}


/* =========================================================
   OUTPUT BOXES
   ========================================================= */

.output-box textarea {

    background:
        #0d223b !important;

    color:
        #f8fafc !important;

    border:
        1px solid
        rgba(96,165,250,0.28) !important;
}


/* =========================================================
   FILE UPLOAD
   ========================================================= */

.gradio-container .file-preview,
.gradio-container .upload-container {

    background:
        #12345a !important;

    border-color:
        rgba(96,165,250,0.30) !important;
}


/* =========================================================
   DIVIDER
   ========================================================= */

.soft-divider {

    height:
        1px;

    margin:
        45px 0;

    background:

        linear-gradient(
            90deg,
            transparent,
            rgba(96,165,250,0.30),
            transparent
        );
}


/* =========================================================
   FOOTER
   ========================================================= */

#footer {

    text-align:
        center;

    padding:
        60px 10px 10px;

    color:
        #6f89a5 !important;

    font-size:
        12px;

    line-height:
        1.8;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 850px) {

    .gradio-container {

        padding:
            15px !important;
    }


    #hero {

        padding:
            40px 25px;
    }


    #hero h1 {

        font-size:
            42px;
    }


    .hero-tagline {

        font-size:
            18px;
    }


    .stat-grid {

        grid-template-columns:
            1fr;
    }
}

"""


# ============================================================
# APP
# ============================================================

with gr.Blocks(
    title="StudyPilot AI",
    css=css,
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="cyan",
        neutral_hue="slate"
    )
) as demo:


    # ========================================================
    # HERO
    # ========================================================

    gr.HTML(
        """
        <div id="hero">

            <div class="hero-content">

                <div class="hero-logo">

                    <div class="logo-mark">
                        ✦
                    </div>

                    STUDYPILOT AI

                </div>


                <h1>
                    Study smarter.<br>
                    Build your future.
                </h1>


                <div class="hero-tagline">
                    Your Academic & Career Copilot
                </div>


                <div class="hero-description">

                    Understand your performance,
                    create personalized learning strategies,
                    ask your academic AI assistant,
                    and discover real career opportunities.

                </div>


                <div class="hero-pills">

                    <span class="pill">
                        📊 Academic Intelligence
                    </span>

                    <span class="pill">
                        🤖 AI Copilot
                    </span>

                    <span class="pill">
                        📚 Personalized Learning
                    </span>

                    <span class="pill">
                        💼 Career Discovery
                    </span>

                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # FEATURES
    # ========================================================

    gr.HTML(
        """
        <div class="section-heading">
            🚀 Your AI Learning Cockpit
        </div>

        <div class="section-description">
            Everything you need to understand your academics
            and plan your next move.
        </div>
        """
    )


    with gr.Row():

        with gr.Column(
            elem_classes="feature-card"
        ):

            gr.HTML(
                """
                <div class="feature-icon">
                    📊
                </div>

                <div class="feature-title">
                    Performance Intelligence
                </div>

                <div class="feature-text">
                    Analyze your transcript and instantly
                    identify strengths, weaknesses and
                    priority subjects.
                </div>
                """
            )


        with gr.Column(
            elem_classes="feature-card"
        ):

            gr.HTML(
                """
                <div class="feature-icon">
                    🧠
                </div>

                <div class="feature-title">
                    Personalized Learning
                </div>

                <div class="feature-text">
                    Turn your marks into an actionable
                    learning roadmap with targeted
                    sessions and improvement goals.
                </div>
                """
            )


        with gr.Column(
            elem_classes="feature-card"
        ):

            gr.HTML(
                """
                <div class="feature-icon">
                    💼
                </div>

                <div class="feature-title">
                    Career Discovery
                </div>

                <div class="feature-text">
                    Search live job opportunities based
                    on your skills and preferred location.
                </div>
                """
            )


    # ========================================================
    # ACADEMIC INTELLIGENCE
    # ========================================================

    gr.HTML(
        """
        <div class="soft-divider"></div>

        <div class="section-heading">
            📊 Academic Intelligence
        </div>

        <div class="section-description">
            Upload your transcript and let StudyPilot
            understand your academic performance.
        </div>
        """
    )


    with gr.Row():

        with gr.Column(
            elem_classes="glass-card"
        ):

            gr.Markdown(
                """
                ### 📄 Upload Your Transcript

                Your transcript is used to identify
                subject-wise performance and academic
                priorities.
                """
            )


            transcript = gr.File(
                label="Transcript PDF",
                file_types=[".pdf"],
                type="filepath"
            )


            analyze_button = gr.Button(
                "📊 Analyze My Performance",
                variant="primary",
                elem_classes="primary-btn"
            )


        with gr.Column(
            elem_classes="glass-card"
        ):

            gr.Markdown(
                """
                ### 📈 Performance Report

                Your academic analysis will appear here.
                """
            )


            analysis_output = gr.Textbox(
                label="Analysis",
                lines=13,
                elem_classes="output-box"
            )


    analyze_button.click(
        fn=analyze_pdf,
        inputs=transcript,
        outputs=analysis_output
    )


    gr.HTML(
        """
        <div class="section-description"
             style="margin-top:25px;">
            Your academic snapshot
        </div>
        """
    )


    dashboard_output = gr.HTML(
        label="Academic Dashboard"
    )


    analyze_button.click(
        fn=academic_dashboard,
        inputs=transcript,
        outputs=dashboard_output
    )


    # ========================================================
    # STUDY PLAN
    # ========================================================

    gr.HTML(
        """
        <div class="soft-divider"></div>

        <div class="section-heading">
            📚 Personalized Study Strategy
        </div>

        <div class="section-description">
            Convert your academic performance into
            a focused learning roadmap.
        </div>
        """
    )


    with gr.Row():

        with gr.Column(
            elem_classes="glass-card"
        ):

            gr.Markdown(
                """
                ### 🎯 Build Your Plan

                StudyPilot analyzes your subject
                performance and recommends where
                to focus your time.
                """
            )


            plan_button = gr.Button(
                "📚 Generate My Study Plan",
                variant="primary",
                elem_classes="primary-btn"
            )


        with gr.Column(
            elem_classes="glass-card"
        ):

            gr.Markdown(
                """
                ### 🗓️ Your Personalized Plan

                Your learning roadmap will appear here.
                """
            )


            plan_output = gr.Textbox(
                label="Study Strategy",
                lines=15,
                elem_classes="output-box"
            )


    plan_button.click(
        fn=generate_plan,
        inputs=transcript,
        outputs=plan_output
    )


    # ========================================================
    # AI COPILOT
    # ========================================================

    gr.HTML(
        """
        <div class="soft-divider"></div>

        <div class="section-heading">
            🤖 AI Academic Copilot
        </div>

        <div class="section-description">
            Ask questions about your transcript,
            subjects and academic performance.
        </div>
        """
    )


    with gr.Column(
        elem_classes="glass-card"
    ):

        question = gr.Textbox(
            label="💬 Ask StudyPilot",
            placeholder="Example: Why is DBMS my highest priority?",
            lines=3
        )


        ask_button = gr.Button(
            "✦ Ask StudyPilot",
            variant="primary",
            elem_classes="primary-btn"
        )


        answer = gr.Textbox(
            label="🤖 StudyPilot Response",
            lines=10,
            elem_classes="output-box"
        )


    ask_button.click(
        fn=ask_question,
        inputs=question,
        outputs=answer
    )


    # ========================================================
    # CAREER DISCOVERY
    # ========================================================

    gr.HTML(
        """
        <div class="soft-divider"></div>

        <div class="section-heading">
            💼 Career Discovery
        </div>

        <div class="section-description">
            Search live job opportunities using
            your preferred skill and location.
        </div>
        """
    )


    with gr.Column(
        elem_classes="glass-card"
    ):

        with gr.Row():

            job_keyword = gr.Textbox(
                label="🔎 Job / Skill",
                placeholder="Python developer"
            )


            job_location = gr.Textbox(
                label="📍 Location",
                placeholder="Hyderabad",
                value="Hyderabad"
            )


        job_button = gr.Button(
            "🚀 Discover Opportunities",
            variant="primary",
            elem_classes="primary-btn"
        )


        job_output = gr.HTML(
            label="💼 Live Opportunities"
        )


    job_button.click(
        fn=find_jobs,
        inputs=[
            job_keyword,
            job_location
        ],
        outputs=job_output
    )


    # ========================================================
    # FOOTER
    # ========================================================

    gr.HTML(
        """
        <div id="footer">

            ✦ STUDYPILOT AI

            <br>

            Academic Intelligence
            • Personalized Learning
            • AI Copilot
            • Career Discovery

            <br><br>

            Built for the Agentic AI Hackathon

        </div>
        """
    )


# ============================================================
# LAUNCH
# ============================================================

demo.launch()