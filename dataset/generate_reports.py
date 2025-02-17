import pandas as pd
import json
import os

def generate_task_reports(output_dir="task_reports"):
    """
    Generates individual JSON reports for each ARC task, focusing on descriptions.

    Args:
        output_dir: The directory to save the JSON reports.  Creates it if it doesn't exist.
    """

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the necessary CSV files
    try:
        tasks = pd.read_csv("summary/task.csv")
        descriptions = pd.read_csv("summary/description.csv")
        joins = pd.read_csv("summary/join.csv")
        phrases = pd.read_csv("annotated_phrases.csv", sep="\t")  # Changed separator to tab
    except FileNotFoundError as e:
        print(f"Error: Could not find file: {e}. Make sure you are in the 'dataset' directory and have all required CSV files.")
        return

    # Merge the dataframes
    task_desc = pd.merge(joins, descriptions, on="description_id", how="left")
    # print(f"Columns of task_desc: {task_desc.columns}")  # Removed debugging print statements
    # print(f"Columns of tasks: {tasks.columns}")
    task_desc = pd.merge(task_desc, tasks, on="task_id", how="left")

    # Group by task_name to process each task individually
    for task_name, task_group in task_desc.groupby("task_name"):
        report = {}

        # 1. Task Identification
        report["task_number"] = int(task_group["task_id"].iloc[0])  # Convert to int
        report["task_name"] = task_name
        report["raw_data_path"] = f"tasks_json/{task_name}"

        # 2. Task Summary (using iloc[0] since these values are the same for all rows in a task group)
        task_summary = task_group.iloc[0]
        report["task_summary"] = {
            "test_input_size": task_summary["test_input_size"],
            "test_output_size": task_summary["test_output_size"],
            "example_input_sizes": task_summary["example_input_sizes"],
            "example_output_sizes": task_summary["example_output_sizes"],
            "number_of_examples": int(task_summary["number_of_examples"]),  # Convert to int
            "test_input_colors": task_summary["test_input_colors"],
            "test_output_colors": task_summary["test_output_colors"],
            "nyu_attempt": int(task_summary["nyu_attempt"]),
            "nyu_successful_1_try": int(task_summary["nyu_successful_1_try"]),
            "nyu_successful_3_tries": int(task_summary["nyu_successful_3_tries"])
        }

        # 3. Description Summary (aggregating and calculating)
        report["description_summary"] = {
            "number_of_descriptions": len(task_group),
            "average_confidence": task_group["confidence"].mean(),
            "verification_success_rate": task_group["is_verified"].mean(),
            "average_verification_attempts": task_group["num_verification_attempts"].mean(),
            "average_description_synthesis_time": task_group["description_synthesis_time"].mean(),
            "average_verification_time": task_group["verification_time"].mean(),
            "descriptions": [],
        }

        for _, desc_row in task_group.iterrows():
            report["description_summary"]["descriptions"].append({
                "description_id": desc_row["description_id"],
                "user_id": desc_row["user_id"],
                "description_input": desc_row["description_input"],
                "description_output_grid_size": desc_row["description_output_grid_size"],
                "description_output": desc_row["description_output"],
                "is_verified": bool(desc_row["is_verified"]),  # Convert to boolean
                "confidence": int(desc_row["confidence"]),  # Convert to int
                "num_verification_attempts": int(desc_row["num_verification_attempts"]), # Convert to int
                "generation": int(desc_row["generation"]),
                "user_num_prior_description_experiences": int(desc_row["user_num_prior_description_experiences"]),
                "user_num_prior_build_experiences": int(desc_row["user_num_prior_build_experiences"]),
                "description_synthesis_time": float(desc_row["description_synthesis_time"]),
                "verification_time": float(desc_row["verification_time"]),
            })

        # 4. Annotated Phrases (filtering and including)
        task_phrases = phrases[phrases["task_name"] == task_name]
        report["annotated_phrases"] = []
        for _, phrase_row in task_phrases.iterrows():
            phrase_data = {
                "phrase_number": int(phrase_row["phrase_number"]),  # Convert to int
                "phrase_kind": phrase_row["phrase_kind"],
                "nth_phrase_in_paragraph": int(phrase_row["nth_phrase_in_paragraph"]),  # Convert to int
                "phrase": phrase_row["phrase"],
            }
            # Add all tag columns
            for col in phrases.columns:
                if col.startswith("tag_"):
                    phrase_data[col] = int(phrase_row[col])  # Convert tag values to int
            report["annotated_phrases"].append(phrase_data)


        # Save the report to a JSON file
        output_file = os.path.join(output_dir, task_name)
        with open(output_file, "w") as f:
            json.dump(report, f, indent=4)  # Use indent=4 for pretty printing

        print(f"Generated report for task: {task_name}")


if __name__ == "__main__":
    generate_task_reports()
