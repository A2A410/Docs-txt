import os
import re

def clean_markdown(text):
    # Remove standard markdown links: [text](link) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove multiple spaces and excessive newlines
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def main():
    docs_md_path = "docs/docs/Docs.md"
    latest_dir = "docs/docs/latest"
    index_file = os.path.join(latest_dir, "index.txt")

    output_dir = "docs-txt"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    full_docs = []

    # 1. Introduction (from index.txt)
    print("Extracting Introduction...")
    full_docs.append("# Introduction\n")
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("intro/"):
                    parts = line.split(":=", 1)
                    if len(parts) > 1:
                        content = parts[1].strip()
                        content = re.sub(r'^.*?Content:.*?(?=\s[A-Z])', '', content)
                        content = re.sub(r'^.*?Back\s+\w+\s+JS\s+Py\s+Hello\s+World\s*', '', content)
                        full_docs.append(clean_markdown(content))
                        full_docs.append("\n")

    # 2. Main Docs from Docs.md
    print("Extracting Main Docs from Docs.md...")
    if os.path.exists(docs_md_path):
        with open(docs_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Split into sections by ##
            sections = re.split(r'\n##\s+', content)
            # The first part is the header # DroidScript Documentation
            # We skip it or keep it if needed. Let's keep the content but reorganize.

            for section in sections:
                if section.startswith("# DroidScript Documentation"):
                    continue # Already added Introduction and we'll add headers manually

                # Each section starts with the title (e.g. "Native")
                lines = section.split('\n', 1)
                title = lines[0].strip()
                body = lines[1] if len(lines) > 1 else ""

                if title in ["Native", "Game Engine", "Hybrid UI", "Global Helpers"]:
                    full_docs.append(f"# {title}\n")
                    full_docs.append(clean_markdown(body))
                    full_docs.append("\n\n")

    # 3. Material UI (from index.txt as it's missing from Docs.md)
    print("Extracting Material UI (MUI) Docs...")
    full_docs.append("# Material UI (MUI)\n")
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("MUI/"):
                    parts = line.split(":=", 1)
                    if len(parts) > 1:
                        content = parts[1].strip()
                        content = re.sub(r'^.*?Content:.*?(?=\s[A-Z])', '', content)
                        content = re.sub(r'^.*?Back\s+\w+\s+JS\s+Py\s+Hello\s+World\s*', '', content)
                        full_docs.append(clean_markdown(content))
                        full_docs.append("\n")

    # Write to file
    output_file = os.path.join(output_dir, "full-docs.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(full_docs))

    print(f"Done! Documentation consolidated to {output_file}")

if __name__ == "__main__":
    main()
