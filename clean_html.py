import sys
import re

def clean_html(html_content):
    # Remove script and style elements
    text = re.sub(r'<(script|style).*?>.*?</\1>', '', html_content, flags=re.DOTALL)
    # Remove all HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Decode common HTML entities
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    # Remove extra whitespace
    text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
    return text

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python clean_html.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
        sys.exit(1)


    cleaned_text = clean_html(html_content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    print(f"Successfully cleaned {input_file} and saved to {output_file}")
