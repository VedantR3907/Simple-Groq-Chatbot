import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

# Load environment variables
load_dotenv()

# Set up parser
parser = LlamaParse(
    api_key=os.environ.get("LLAMAPARSE_API_KEY"),
    result_type="markdown", # "markdown" and "text" are available,
    show_progress=True,
    parsing_instruction='The provided documents can be a research paper or a simple book or a resume your task is to extract each and every relevant information without skippinga single piece of word from the document. Please do not remove any information from the document extract each and every information from the document.'
)

def llamaparser(input_dir, output_dir):


    # Use SimpleDirectoryReader to parse our file
    file_extractor = {".txt": parser, '.doc': parser}
    input_dir = input_dir
    documents = SimpleDirectoryReader(input_dir=input_dir, file_extractor=file_extractor, required_exts=['.txt']).load_data()

    # Ensure the output directory exists
    output_dir = output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save each document's content to a separate .txt file
    for doc in documents:
        file_name = doc.metadata.get('file_name')  # Get the file name from metadata
        file_name_without_ext = os.path.splitext(file_name)[0]  # Remove the extension
        output_file_path = os.path.join(output_dir, f"{file_name_without_ext}.txt")
        
        # Write the content to the file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(doc.text)  # Assuming 'text' contains the document content

    print("Documents have been processed and saved in the extracted_output folder.")
