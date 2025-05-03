import os
import re
import base64
import pptx
from pptx.util import Inches
import argparse

# Import the necessary functions from MinerU.py
from MinerU import extract_pdf_to_markdown

# 导入 OpenAI API
from openai import OpenAI

# Setup command line argument parser
parser = argparse.ArgumentParser(description='Generate PowerPoint slides from PDF papers')
parser.add_argument('--model', type=str, default='openai', 
                    help='LLM model to use (default: openai, options: openai, gemini, claude, grok)')
parser.add_argument('--pdf', type=str, default='data/Example.pdf',
                    help='Path to PDF file (default: data/Example.pdf)')
parser.add_argument('--output', type=str, default='Generated_Slides.pptx',
                    help='Output PowerPoint file name (default: Generated_Slides.pptx)')
args = parser.parse_args()

# Set API keys
os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"

# Inform user about model selection
if args.model != 'openai':
    print(f"You selected the {args.model} model, but currently only the OpenAI model is implemented.")
    print(f"To use {args.model}, please ensure you have set the appropriate API keys and modify the code accordingly.")
    print("Continuing with the OpenAI model...")

# Define file paths
pdf_file_name = args.pdf  # Use PDF path from command line arguments
local_md_dir = "output"
os.makedirs(local_md_dir, exist_ok=True)

# Get the expected markdown file path
pdf_base_name = os.path.splitext(os.path.basename(pdf_file_name))[0]
expected_md_path = os.path.join(local_md_dir, pdf_base_name, "auto", f"{pdf_base_name}.md")

# Check if Markdown file already exists
if os.path.exists(expected_md_path):
    print(f"Markdown file already exists: {expected_md_path}, skipping PDF parsing")
    md_file_path = expected_md_path
else:
    # If not, extract PDF content using function from MinerU.py
    print(f"Markdown file does not exist, parsing PDF content...")
    md_file_path = extract_pdf_to_markdown(pdf_file_name, local_md_dir)

# Load the extracted markdown content
with open(md_file_path, "r", encoding="utf-8") as f:
    md_text = f.read()

# Extract image paths from Markdown
image_paths = re.findall(r'!\[.*?\]\((.*?)\)', md_text)

# Function to encode images to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Create image messages with base64-encoded images
image_messages = []
for image_path in image_paths:
    full_image_path = "/".join(["output", pdf_base_name, "auto", image_path])
    base64_image = encode_image(full_image_path)
    image_messages.append(
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
            }
        }
    )

# Function to load prompt template
def load_prompt_template(template_path):
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

# Load the prompt template
prompt_template = load_prompt_template("GenerateSlidesOutlinePrompt.md")

# Initialize OpenAI client
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# If you want to use other models, you can change the client and model name here
# import google.generativeai as genai
# gemeni_client = genai.GenerativeModel(api_key=os.environ.get("GEMINI_API_KEY"))

# grok_client = OpenAI(
#     api_key=os.environ.get("GROK_API_KEY"),
#     base_url=os.environ.get("GROK_API_ENDPOINT"),
# )   

# Build the messages list with base64-encoded images
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt_template.format(content=md_text),
            },
        ] + image_messages,
    }
]

# Generate PowerPoint outline using OpenAI model
print(f"Generating presentation outline using OpenAI model...")
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages
)

# Extract the generated PowerPoint outline
ppt_outline = response.choices[0].message.content.split("\n")

# Format the PowerPoint outline
formatted_outline = "\n".join(ppt_outline)
print(formatted_outline)

# Function to create a PowerPoint presentation from the outline
def create_ppt_from_outline(outline, output_file="Generated_Slides.pptx"):
    """
    Create a PowerPoint presentation from the generated outline
    
    Parameters:
    - outline: Generated presentation outline text
    - output_file: Output PowerPoint file name
    """
    prs = pptx.Presentation()
    slides = outline.split('---')

    # Keep track of the image number
    image_counter = 0

    for slide in slides:
        lines = slide.strip().split('\n')
        if not lines:
            continue

        slide_title = lines[0].replace('**', '').strip()
        slide_content = lines[1:]

        slide_layout = prs.slide_layouts[1]  # Title and content layout
        slide = prs.slides.add_slide(slide_layout)
        title = slide.shapes.title
        title.text = slide_title

        content = slide.placeholders[1].text_frame
        for line in slide_content:
            line = line.strip()
            # Remove leading '- ' if present
            if line.startswith('- '):
                line = line[2:]
            if line:
                if '[Image' in line:
                    # Extract image number from the line
                    match = re.search(r'\[Image (\d+)\]', line)
                    if match:
                        image_number = int(match.group(1)) - 1
                        if image_number < len(image_paths):
                            image_path = os.path.join('output', pdf_base_name, 'auto', image_paths[image_number])
                            # Insert image below the text content
                            left = Inches(1)
                            top = Inches(2.5)
                            height = Inches(4)
                            slide.shapes.add_picture(image_path, left, top, height=height)
                else:
                    p = content.add_paragraph()
                    p.text = line
                    p.level = 0

    prs.save(output_file)
    print(f"PowerPoint presentation saved as '{output_file}'")

# Create the PowerPoint presentation
create_ppt_from_outline(formatted_outline, args.output)

# Display usage instructions
print("\n" + "="*80)
print("PaperToSlides: Generate PowerPoint presentations from academic papers")
print("="*80)
print("\nUsage Examples:")
print("  Basic usage:")
print("    python GenerateSlidesOutline.py")
print("\n  Specify a PDF file:")
print("    python GenerateSlidesOutline.py --pdf path/to/your/paper.pdf")
print("\n  Specify output filename:")
print("    python GenerateSlidesOutline.py --output MyPresentation.pptx")
print("\n  Combine options:")
print("    python GenerateSlidesOutline.py --pdf path/to/paper.pdf --output MyPresentation.pptx")
print("\nNote: Currently only the OpenAI model is implemented. To use other models,")
print("you'll need to modify the code to include the appropriate API calls.")
print("="*80)