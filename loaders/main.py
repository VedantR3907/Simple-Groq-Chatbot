import os
from llamaparse_loader import llamaparser
from pdf_loader import pdfLoader

def process_files(input_dir: str, output_dir: str):
    """
    Process files in the input directory based on their extensions and
    save the output to the specified directory.

    Args:
        input_dir (str): The directory containing files to process.
        output_dir (str): The directory to save the output files.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List all files in the input directory
    files = os.listdir(input_dir)
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    text_files = [f for f in files if f.lower().endswith('.txt') or f.lower().endswith('.doc')]

    # Process PDF files
    if pdf_files:
        print("Processing PDF files...")
        pdfLoader(input_dir=input_dir, output_dir=output_dir)

    # Process .txt and .doc files
    if text_files:
        print("Processing text and doc files...")
        llamaparser(input_dir=input_dir, output_dir=output_dir)

    print("Processing complete. Output files are located in '{}'.".format(output_dir))

if __name__ == "__main__":
    # Replace with the path to your directories
    input_dir = '../documents'
    output_dir = '../extracted_output'
    process_files(input_dir, output_dir)
