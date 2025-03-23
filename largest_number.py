import PyPDF2
import re


def extract_text_from_pdf(pdf_path):
    """Extracts and returns all combined text from a given PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"Error extracting text from doc: {e} ")


def extract_largest_number(text):
    """Finds the largest number in the text"""
    # Regex explanation:
    # (\d{1,3}(?:,\d{3})*(?:\.\d+)?) captures numbers with optional commas and decimals.
    # \s* matches any whitespace between the number and the scaling word.
    # (hundred|thousand|million|billion)? optionally captures the scale.
    pattern = re.compile(r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(hundred|thousand|million|billion)?", re.IGNORECASE)

    numbers = []
    for match in pattern.findall(text):
        num_str, scale = match
        num = float(num_str.replace(",", ""))
        scale_factors = {
            "hundred": 100,
            "thousand": 1_000,
            "million": 1_000_000,
            "billion": 1_000_000_000
        }

        if scale:
            num *= scale_factors.get(scale.lower(), 1)

        numbers.append(num)

    return numbers


def extract_largest_numerical_value(text):
    """
     Parameters:
      text (str): The text from which to extract numbers.
    Returns:
      Highest number found not taking verbiage or formatting into account
    """
    # Regex explanation:
    # (?<![\w.]) ensures the match is not immediately preceded by a letter or dot.
    # \-? optionally matches a minus sign.
    # \d+(?:\.\d+)? matches an integer or a decimal number.
    # (?![\w.]) ensures the match is not followed by a letter or dot.
    number_pattern = re.compile(r"(?<![\w.])\-?\d+(?:\.\d+)?(?![\w.])")
    numbers_found = number_pattern.findall(text)

    extracted_numbers = []
    for num_str in numbers_found:
        value = float(num_str)
        extracted_numbers.append(value)
    return extracted_numbers


def find_largest_number(numbers):
    """
    Finds the largest number in a given list.

    Returns:
        float or None: The largest number, or None if the list is empty.
    """
    return max(numbers, default=None)


def process_pdf(pdf_path):
    """
    Extracts text from a PDF and finds the largest number and numerical value.

    Returns:
        dict: A dictionary with the largest scaled and raw numerical values.
    """
    text = extract_text_from_pdf(pdf_path)

    # Extract numbers in different contexts
    largest_number = extract_largest_number(text)
    largest_numerical_value = extract_largest_numerical_value(text)

    return {
        "largest_number": find_largest_number(largest_number),
        "largest_numerical_value": find_largest_number(largest_numerical_value),
    }


def main(pdf_path):
    """
       Main function to process the PDF and display results.

    """
    print("Processing PDF...")
    results = process_pdf(pdf_path)

    # Display results
    largest_number = results["largest_number"]
    largest_numerical_value = results["largest_numerical_value"]

    if largest_number:
        print(f"Largest number: {largest_number:,.0f}")
    else:
        print(f"Largest scaled number not found")

    if largest_numerical_value:
        print(f"Largest numerical value: {largest_numerical_value}")
    else:
        print(f"Largest numerical value not found")


if __name__ == "__main__":
    pdf_file_path = "C:\\Your\\Path\\Here\\filename.pdf"  #Update this to your actual file path
    main(pdf_file_path)
