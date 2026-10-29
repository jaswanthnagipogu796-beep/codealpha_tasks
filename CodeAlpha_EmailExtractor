"""Task 3: Email Address Extractor"""

import re
from pathlib import Path


# This pattern targets common email formats suitable for a simple text-file
# utility. It is not intended to validate every address allowed by email specs.
EMAIL_PATTERN = re.compile(
    r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])",
    re.IGNORECASE,
)

DEFAULT_INPUT = "emails.txt"
DEFAULT_OUTPUT = "extracted_emails.txt"


def find_unique_emails(text: str) -> list[str]:
    """Return unique email addresses in order, ignoring letter case.

    The first spelling found in the source is kept. For example, if
    Alex@example.com appears before ALEX@example.com, the first form is saved.
    """
    matches = EMAIL_PATTERN.findall(text)
    unique_addresses: dict[str, str] = {}

    for address in matches:
        normalized_address = address.casefold()
        if normalized_address not in unique_addresses:
            unique_addresses[normalized_address] = address

    return list(unique_addresses.values())


def read_emails_from_file(input_path: Path) -> list[str]:
    """Read UTF-8 text from input_path and return its unique email addresses."""
    text = input_path.read_text(encoding="utf-8")
    return find_unique_emails(text)


def save_emails_to_file(emails: list[str], output_path: Path) -> None:
    """Write one email per line, including an empty file when none are found."""
    content = "\n".join(emails)
    if emails:
        content += "\n"
    output_path.write_text(content, encoding="utf-8")


def get_file_path(prompt: str, default: str) -> Path:
    """Ask for a path and use the supplied default when the answer is blank."""
    answer = input(f"{prompt} [{default}]: ").strip()
    return Path(answer or default).expanduser()


def main() -> None:
    """Collect paths, run the extraction, and report the result to the user."""
    print("\n" + "=" * 52)
    print("              EMAIL EXTRACTOR")
    print("=" * 52)
    print("Find email addresses in a text file and save a clean list.")

    input_path = get_file_path("Input .txt file", DEFAULT_INPUT)
    output_path = get_file_path("Save results to", DEFAULT_OUTPUT)

    # Avoid accidentally replacing the source if the same path is entered twice.
    if input_path.resolve() == output_path.resolve():
        print("Error: the output path must be different from the input path.")
        return

    try:
        emails = read_emails_from_file(input_path)
    except FileNotFoundError:
        print(f"Input file not found: {input_path.resolve()}")
        print("Create the file or enter the correct path, then run the program again.")
        return
    except UnicodeDecodeError:
        print("The input file could not be read as UTF-8 text.")
        return
    except OSError as error:
        print(f"Could not read the input file: {error}")
        return

    try:
        save_emails_to_file(emails, output_path)
    except OSError as error:
        print(f"Could not save the output file: {error}")
        return

    print("\nEXTRACTION COMPLETE")
    print(f"Unique email addresses found: {len(emails)}")
    print(f"Saved results to: {output_path.resolve()}")
    if emails:
        print("\nPreview:")
        for address in emails[:5]:
            print(f"  - {address}")
        if len(emails) > 5:
            print(f"  ...and {len(emails) - 5} more (see output file).")
    else:
        print("No email addresses were found; the output file is empty.")


if __name__ == "__main__":
    main()
