def analyze_transcript():
    subjects = {
        "C Programming": 82,
        "Web Technology": 76,
        "Computer Architecture": 61,
        "Mathematical Fundamentals of Computer": 55,
        "Database Management Systems": 48,
        "English Communication": 88
    }

    # Sort subjects from lowest marks to highest
    ranked_subjects = sorted(subjects.items(), key=lambda x: x[1])

    print("\n===== ACADEMIC ANALYSIS =====\n")

    print("Weak / Priority Subjects:")

    for subject, marks in ranked_subjects:
        if marks < 60:
            priority = "HIGH"
        elif marks < 70:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        print(f"{subject}: {marks}/100 → {priority} priority")

    average = sum(subjects.values()) / len(subjects)

    print(f"\nOverall Average: {average:.2f}/100")

    print("\nTop Priority:")
    print(f"{ranked_subjects[0][0]} - {ranked_subjects[0][1]}/100")


# Test the tool
analyze_transcript()