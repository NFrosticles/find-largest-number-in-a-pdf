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
        print(f"Error extracting text from PDF: {e}")
        return ""


def extract_largest_number(text):
    """Finds the largest number in the text, considering scaling factors."""

    # This regex matches numerical values with optional scaling keywords, such as:
    # - Plain numbers (e.g., "123", "1,234", "123.45")
    # - Numbers with scaling factors (e.g., "1,000 thousand", "12.3 million")
    # It has two capturing groups:
    # 1. (\d{1,3}(?:,\d{3})*(?:\.\d+)?): Captures the numeric portion, including:
    #    - Comma-separated numbers (e.g., "1,000")
    #    - Decimal numbers (e.g., "123.45")
    #    - Whole numbers (e.g., "123")
    # 2. (hundred|thousand|million|billion)?: Captures optional scaling factors
    #    (e.g., "thousand", "million"), making this group optional.
    pattern = re.compile(r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(hundred|thousand|million|billion)?", re.IGNORECASE)

    numbers = []
    scale_factors = {
        "hundred": 100,
        "thousand": 1_000,
        "million": 1_000_000,
        "billion": 1_000_000_000
    }

    for num_str, scale in pattern.findall(text):
        num = float(num_str.replace(",", ""))
        if scale:
            num *= scale_factors.get(scale.lower(), 1)
        numbers.append(num)

    return numbers


def extract_largest_numerical_value(text):
    """Extracts raw numerical values without scaling."""

    # This regex matches raw numerical values in a text, supporting:
    # - Plain numbers (e.g., "123", "45678")
    # - Numbers with commas as thousands separators (e.g., "1,234", "12,345,678")
    # - Decimal numbers (e.g., "123.45", "1,234.56")
    # - Negative numbers (e.g., "-123", "-1,234.56")
    # It ensures matches are not part of a larger alphanumeric string
    # (e.g., avoids matching "123" in "ABC123" or ".456" in "0.4567").
    # Lookbehind and lookahead patterns are used to verify that numbers
    # are standalone and not surrounded by invalid characters.
    raw_number_pattern = re.compile(r"(?<![a-zA-Z0-9.\-])(\-?(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d+)?)(?![a-zA-Z0-9])")

    numbers = []
    for match in raw_number_pattern.finditer(text):
        num_str = match.group()
        try:
            num = float(num_str.replace(",", ""))
            numbers.append(num)
        except ValueError:
            continue
    return numbers


def find_largest_number(numbers):
    """Finds the largest number in a given list."""
    return max(numbers, default=None)


def process_pdf(pdf_path):
    """Extracts text from a PDF and finds the largest number and numerical value."""
    text = extract_text_from_pdf(pdf_path)
    largest_number = extract_largest_number(text)
    largest_numerical_value = extract_largest_numerical_value(text)

    return {
        "largest_number": find_largest_number(largest_number),
        "largest_numerical_value": find_largest_number(largest_numerical_value),
    }


def main(pdf_path):
    """Main function to process the PDF and display results."""
    print("Processing PDF...")
    results = process_pdf(pdf_path)

    largest_number = results["largest_number"]
    largest_numerical_value = results["largest_numerical_value"]

    if largest_number:
        print(f"Largest number: {largest_number:,.0f}")
    else:
        print("Largest scaled number not found")

    if largest_numerical_value:
        print(f"Largest numerical value: {largest_numerical_value}")
    else:
        print("Largest numerical value not found")


if __name__ == "__main__":
    pdf_file_path = "C:\\Your\\File\\Path\\yourfilename.pdf"  # Update this to your actual file path
    main(pdf_file_path)
