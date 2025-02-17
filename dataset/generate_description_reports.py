import pandas as pd
import os

def generate_description_reports(output_dir="description_reports"):
    """
    Generates individual Markdown reports for each ARC task,
    containing only the verified descriptions.

    Args:
        output_dir: The directory to save the Markdown reports.
                     Creates it if it doesn't exist.
    """

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the necessary CSV files
    try:
        descriptions = pd.read_csv("summary/description.csv")
        joins = pd.read_csv("summary/join.csv")
        tasks = pd.read_csv("summary/task.csv") # Load tasks.csv
    except FileNotFoundError as e:
        print(f"Error: Could not find file: {e}. Make sure you are in the 'dataset' directory and have all required CSV files.")
        return

    # Merge dataframes
    task_desc = pd.merge(joins, descriptions, on="description_id", how="left")
    task_desc = pd.merge(task_desc, tasks, on="task_id", how="left") # Merge with tasks

    # Filter for verified descriptions only
    verified_descriptions = task_desc[task_desc["is_verified"] == True]

    # Group by task_name and iterate
    for task_name, task_group in verified_descriptions.groupby("task_name"):
        # Create the Markdown content
        markdown_content = f"# Task: {task_name}\n\n"

        for _, desc_row in task_group.iterrows():
            markdown_content += f"{desc_row['description_input']}\n\n"
            markdown_content += f"{desc_row['description_output_grid_size']}\n\n"
            markdown_content += f"{desc_row['description_output']}\n\n"
            markdown_content += "---\n\n"  # Separator between descriptions

        # Save the Markdown file
        output_file = os.path.join(output_dir, f"{task_name}.md")
        with open(output_file, "w") as f:
            f.write(markdown_content)

        print(f"Generated Markdown report for task: {task_name}")

if __name__ == "__main__":
    generate_description_reports()
