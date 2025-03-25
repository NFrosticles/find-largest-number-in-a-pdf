import pymupdf
import re


def extract_text_from_pdf(pdf_path):
    """Extracts and returns all combined text from a given PDF file."""
    text = ""
    try:
        with pymupdf.open(pdf_path) as pdf:
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                text += page.get_text() + "\n"
            return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def extract_largest_number(text):
    """Finds the largest number in the text, considering explicit and contextual scaling factors."""

    # Regex to match numbers with optional scaling words like million/billion
    pattern = re.compile(r'\$?\(?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?(?:\s*(million|billion|thousand|hundred))?', re.IGNORECASE)

    scale_factors = {
        "hundred": 1e2,
        "thousand": 1e3,
        "million": 1e6,
        "billion": 1e9
    }

    max_value = 0

    # Split text into sections to check for contextual headers to handle financial charts
    for section in re.split(r'\n\s*\n', text):
        section_scale = 1  # Default scale
        if re.search(r'\(.*?\bMillions\b.*?\)', section, re.IGNORECASE):
            section_scale = 1e6
        elif re.search(r'\(.*?\bBillions\b.*?\)', section, re.IGNORECASE):
            section_scale = 1e9
        elif re.search(r'\(.*?\bThousands\b.*?\)', section, re.IGNORECASE):
            section_scale = 1e3

        for match in pattern.finditer(section):
            full = match.group(0)
            scale_word = match.group(1)

            # Clean number string (remove $, commas, parentheses)
            num_str = re.sub(r'[^\d\.\-]', '', full.replace(",", ""))

            try:
                num = float(num_str)
                # User explicit scaling word or chart scaling (Dollars in Millions)
                if scale_word:
                    num *= scale_factors.get(scale_word.lower(), 1)
                else:
                    num *= section_scale
                if max_value is None or num > max_value:
                    max_value = num
            except Exception as e:
                print(f"Skipping invalid entry: {full}, Error: {e}")
                continue

    return [max_value]


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
        except (ValueError, KeyError) as e:
            print(f"Skipping invalid entry: {num_str}, Error: {e}")
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
    pdf_file_path = "C:\\Your\\File\\Here\\filename.pdf"  # Update this to your actual file path
    main(pdf_file_path)
