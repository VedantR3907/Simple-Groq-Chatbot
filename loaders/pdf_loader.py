import asyncio
import os
import fitz

async def process_page(doc: fitz.Document, page_num: int) -> str:
    """
    Process a single page of the PDF to extract text and replace images with their descriptions.

    Args:
        doc (fitz.Document): The PDF document object.
        page_num (int): The page number to be processed.

    Returns:
        str: The modified text of the page with image descriptions included.

    Raises:
        RuntimeError: If there is an error during the page processing.
    """
    try:
        page = doc.load_page(page_num)
        text = page.get_text()
        return text

    except (ValueError, TypeError, AttributeError, IndexError) as e:
        raise RuntimeError(f"Error processing page {page_num + 1}: {e}") from e


async def process_pdf(pdf_path: str, output_dir: str) -> str:
    """
    Extract text from a PDF and save it to a .txt file in the specified output directory.

    Args:
        pdf_path (str): The path to the PDF file.
        output_dir (str): The directory to save the output text file.

    Returns:
        str: The path to the output text file with the extracted text.

    Raises:
        RuntimeError: If there is an error during the PDF processing.
    """
    try:
        doc = fitz.open(pdf_path)
        tasks = [process_page(doc, page_num) for page_num in range(len(doc))]
        modified_content = []

        # Process pages in batches to manage async tasks efficiently
        for i in range(0, len(tasks), 5):
            batch = tasks[i: i + 5]
            page_texts = await asyncio.gather(*batch)
            modified_content.extend(page_texts)

        final_text = "\n".join(modified_content)
        file_name = os.path.basename(pdf_path).replace(".pdf", ".txt")
        output_path = os.path.join(output_dir, file_name)

        try:
            # Write the final text to an output file
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(final_text)

        except IOError as e:
            raise IOError(f"Error writing to output file: {e}") from e

        return output_path

    except (ValueError, IOError, TypeError) as e:
        raise RuntimeError(f"Failed to process PDF {pdf_path}: {e}") from e

async def process_directory(input_dir: str, output_dir: str):
    """
    Process all PDF files in the input directory and save the output text files in the output directory.

    Args:
        input_dir (str): The directory containing PDF files to process.
        output_dir (str): The directory to save the output text files.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    tasks = [process_pdf(os.path.join(input_dir, pdf_file), output_dir) for pdf_file in pdf_files]

    # Process all PDF files
    output_paths = await asyncio.gather(*tasks)

    print(f"Processed {len(output_paths)} PDFs. Output files are located in '{output_dir}'.")

def pdfLoader(input_dir: str, output_dir: str):
    """
    Run the PDF processing for all files in the input directory.

    Args:
        input_dir (str): The directory containing PDF files to process.
        output_dir (str): The directory to save the output text files.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_directory(input_dir, output_dir))

if __name__ == "__main__":
    # Replace with the path to your directory containing PDF files
    input_dir = '../documents'
    output_dir = '../extracted_output'
    pdfLoader(input_dir, output_dir)
