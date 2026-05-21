# -*- coding: utf-8 -*-
"""
Created on Thu May 21 04:11:57 2026

@author: fa7ad
"""

import requests
import os


def download_answer_files(cloud_url, path_to_data_folder, total_respondents):
    """
    Downloads answer files from a cloud URL and saves them locally.

    Parameters:
        cloud_url (str): Base URL where files are hosted.
        path_to_data_folder (str): Local folder path to save downloaded files.
        total_respondents (int): Number of files to attempt downloading.

    Returns:
        None
    """
    os.makedirs(path_to_data_folder, exist_ok=True)
    for i in range(1, total_respondents + 1):
        url = f"{cloud_url}/a{i}.txt"
        response = requests.get(url)
        if response.status_code == 200:
            file_name = f"answers_respondent_{i}.txt"
            file_path = os.path.join(path_to_data_folder, file_name)
            with open(file_path, "w") as f:
                f.write(response.text)
            print(f"Downloaded: {file_name}")
        else:
            print(f"File a{i}.txt not found, skipping.")


def collate_answer_files(data_folder_path):
    """
    Combines all respondent answer files into one unified file.

    Parameters:
        data_folder_path (str): Path to the folder containing respondent files.

    Returns:
        None
    """
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "collated_answers.txt")
    files = sorted([f for f in os.listdir(data_folder_path)
                    if f.startswith("answers_respondent_") and f.endswith(".txt")],
                   key=lambda x: int(x.replace("answers_respondent_", "").replace(".txt", "")))
    with open(output_path, "w") as out:
        for i, file_name in enumerate(files):
            file_path = os.path.join(data_folder_path, file_name)
            with open(file_path, "r") as f:
                out.write(f.read())
            if i < len(files) - 1:
                out.write("\n*\n")
    print(f"Collated {len(files)} files into {output_path}")