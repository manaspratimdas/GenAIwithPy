import os

def merge_files_in_folder(folder_path, output_file):
    with open(output_file, 'w') as outfile:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # Add a newline character after each file's content

# Example usage
folder_path = 'C:\\Users\\mandas3\\log\\log1'  # Replace with the path to your folder containing the files
output_file = 'log_merged_output.txt'  # Replace with the desired output file name

merge_files_in_folder(folder_path, output_file)