import os
import sys
import matplotlib.pyplot as plt

script_folder = os.path.dirname(os.path.abspath(__file__))
project_folder = os.path.dirname(script_folder)
os.chdir(project_folder)
sys.path.append(script_folder)

from data_preparation_M2 import download_answer_files
from data_extraction_M1 import extract_answers_sequence, write_answers_sequence


def main():
    base_url = "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main"
    data_folder = "data"
    output_folder = "output"
    total_respondents = 64

    os.makedirs(data_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(output_folder):
        if filename.startswith("answers_list_respondent_") or filename == "collated_answers.txt":
            os.remove(os.path.join(output_folder, filename))

    print("Downloading files...")
    download_answer_files(base_url, data_folder, total_respondents)

    all_answers = []

    print("Extracting sequences...")
    for i in range(1, total_respondents + 1):
        file_path = os.path.join(data_folder, f"answers_respondent_{i}.txt")

        if os.path.exists(file_path):
            answers = extract_answers_sequence(file_path)

            if len(answers) == 100:
                all_answers.append(answers)
                write_answers_sequence(answers, i, output_folder)
            else:
                print(f"Skipped respondent {i}: {len(answers)} answers")

    collated_path = os.path.join(output_folder, "collated_answers.txt")

    with open(collated_path, "w", encoding="utf-8") as file:
        for answers in all_answers:
            file.write(",".join(str(answer) for answer in answers) + "\n*\n")

    means = []

    for question in range(100):
        values = [answers[question] for answers in all_answers if answers[question] != 0]

        if values:
            means.append(sum(values) / len(values))
        else:
            means.append(0)

    print("First 10 means:", means[:10])

    plt.figure()
    plt.scatter(range(1, 101), means)
    plt.xlabel("Question number")
    plt.ylabel("Mean answer value")
    plt.title("Mean answer values by question")
    plt.show()

    plt.figure()
    plt.plot(range(1, 101), means)
    plt.xlabel("Question number")
    plt.ylabel("Mean answer value")
    plt.title("Mean answer pattern")
    plt.show()

    print("Full analysis complete.")


if __name__ == "__main__":
    main()
