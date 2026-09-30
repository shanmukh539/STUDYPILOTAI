from pypdf import PdfReader
import re


def create_study_plan(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"

    subjects = {}

    pattern = r"([A-Za-z][A-Za-z &]+?)\s+100\s+(\d+)\s+[A-Z][+]?"

    matches = re.findall(pattern, text)

    for subject, marks in matches:
        subjects[subject.strip()] = int(marks)

    if not subjects:
        return "No subjects found."

    ranked = sorted(subjects.items(), key=lambda x: x[1])

    output = []

    output.append("╔════════════════════════════════════════════╗")
    output.append("║        🎯 PERSONALIZED STUDY PLAN         ║")
    output.append("╚════════════════════════════════════════════╝")

    # --------------------------------------------------------
    # OVERVIEW
    # --------------------------------------------------------

    average = sum(subjects.values()) / len(subjects)

    output.append("")
    output.append(f"📊 Overall Average: {average:.2f}/100")
    output.append(f"📚 Subjects Analyzed: {len(subjects)}")
    output.append(f"🎯 Main Focus: {ranked[0][0]}")

    # --------------------------------------------------------
    # STUDY PLAN
    # --------------------------------------------------------

    output.append("")
    output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output.append("📅 YOUR PERSONALIZED LEARNING ROADMAP")
    output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    for position, (subject, marks) in enumerate(ranked, 1):

        if marks < 60:
            priority = "HIGH"
            sessions = 5

            focus = [
                "Learn the core fundamentals",
                "Study important concepts",
                "Practice problems",
                "Solve previous questions",
                "Revision + self-test"
            ]

        elif marks < 70:
            priority = "MEDIUM"
            sessions = 3

            focus = [
                "Revise important concepts",
                "Practice questions",
                "Revision + self-test"
            ]

        else:
            priority = "LOW"
            sessions = 1

            focus = [
                "Quick revision and practice"
            ]

        output.append("")
        output.append(f"#{position}  📘 {subject}")
        output.append(f"Score: {marks}/100")
        output.append(f"Priority: {priority}")
        output.append(f"Recommended sessions: {sessions}")

        output.append("")
        output.append("Study roadmap:")

        for session, task in enumerate(focus, 1):
            output.append(
                f"  Session {session}: {task}"
            )

        # ----------------------------------------------------
        # SCORE-BASED GOAL
        # ----------------------------------------------------

        if marks < 60:
            target = min(marks + 20, 85)
        elif marks < 70:
            target = min(marks + 15, 85)
        else:
            target = min(marks + 10, 95)

        output.append("")
        output.append(
            f"🎯 Improvement target: {marks} → {target}/100"
        )

        output.append("─" * 44)

    # --------------------------------------------------------
    # TOP PRIORITY
    # --------------------------------------------------------

    top_subject, top_marks = ranked[0]

    output.append("")
    output.append("🏆 TOP PRIORITY SUBJECT")
    output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output.append(f"📘 {top_subject}")
    output.append(f"Current score: {top_marks}/100")

    if top_marks < 60:
        output.append(
            "⚠️ This subject needs immediate attention."
        )
        output.append(
            "Recommended approach: fundamentals → practice → revision."
        )

    elif top_marks < 70:
        output.append(
            "⚠️ This subject needs consistent revision."
        )
        output.append(
            "Recommended approach: concepts → practice → revision."
        )

    else:
        output.append(
            "✅ Maintain this subject with regular revision."
        )

    # --------------------------------------------------------
    # WEEKLY STRATEGY
    # --------------------------------------------------------

    output.append("")
    output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output.append("🗓️ WEEKLY STUDY STRATEGY")
    output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    high_priority = [
        subject for subject, marks in ranked
        if marks < 60
    ]

    medium_priority = [
        subject for subject, marks in ranked
        if 60 <= marks < 70
    ]

    low_priority = [
        subject for subject, marks in ranked
        if marks >= 70
    ]

    if high_priority:
        output.append("")
        output.append("🔴 HIGH PRIORITY")
        for subject in high_priority:
            output.append(f"  • {subject}")

    if medium_priority:
        output.append("")
        output.append("🟡 MEDIUM PRIORITY")
        for subject in medium_priority:
            output.append(f"  • {subject}")

    if low_priority:
        output.append("")
        output.append("🟢 MAINTAIN")
        for subject in low_priority:
            output.append(f"  • {subject}")

    output.append("")
    output.append("💡 Recommended routine:")
    output.append("  • Start with your weakest subject")
    output.append("  • Practice after learning concepts")
    output.append("  • Revise before moving to a new topic")
    output.append("  • Take a short self-test every week")

    output.append("")
    output.append("╔════════════════════════════════════════════╗")
    output.append("║     🚀 KEEP IMPROVING — YOU GOT THIS!     ║")
    output.append("╚════════════════════════════════════════════╝")

    return "\n".join(output)