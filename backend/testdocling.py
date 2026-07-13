from docling.document_converter import DocumentConverter

converter = DocumentConverter()

result = converter.convert("storage/papers/5dba1814-0f0a-4523-a7e8-06f8f195b3b8/original.pdf")

markdown = result.document.export_to_markdown()

print("Pages:", len(result.document.pages))
print("Markdown length:", len(markdown))

with open("test_output.md", "w", encoding="utf-8") as f:
    f.write(markdown)

print("Done.")