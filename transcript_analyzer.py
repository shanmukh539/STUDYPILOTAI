import re
from pypdf import PdfReader


def analyze_transcript(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"

    subjects = {}

    pattern = r"([A-Za-z][A-Za-z &]+?)\s+100\s+(\d+)\s+[A-Z][+]?"

    matches = re.findall(pattern, text)

    for subject, marks in matches:
        subject = subject.strip()
        marks = int(marks)
        subjects[subject] = marks

    if not subjects:
        return "No subjects could be detected."

    ranked = sorted(subjects.items(), key=lambda x: x[1])

    output = []
    output.append("===== TRANSCRIPT ANALYSIS =====\n")

    for subject, marks in ranked:

        if marks < 60:
            priority = "HIGH"
        elif marks < 70:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        output.append(
            f"{subject}: {marks}/100 → {priority} priority"
        )

    average = sum(subjects.values()) / len(subjects)

    best_subject = max(subjects.items(), key=lambda x: x[1])
    top_priority = ranked[0]

    output.append(f"\nOverall Average: {average:.2f}/100")

    output.append("\nTop Priority:")
    output.append(
        f"{top_priority[0]} - {top_priority[1]}/100"
    )

    output.append("\nBest Subject:")
    output.append(
        f"{best_subject[0]} - {best_subject[1]}/100"
    )

    return "\n".join(output)

if __name__ == "__main__":
    print(
        analyze_transcript(
            "documents/transcript.pdf"
        )
    )

def get_academic_data(pdf_path):
    from pypdf import PdfReader
    import re

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"

    pattern = r"([A-Za-z][A-Za-z &]+?)\s+100\s+(\d+)\s+[A-Z][+]?"

    matches = re.findall(pattern, text)

    subjects = {}

    for subject, marks in matches:
        subjects[subject.strip()] = int(marks)

    return subjects