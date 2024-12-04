import os
import re
import base64
import pptx
from pptx.util import Inches

# Import the necessary functions from MinerU.py
# from MinerU import extract_pdf_to_markdown

# 导入 OpenAI API
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"

# Define file paths
pdf_file_name = "data/Example.pdf"  # replace with your PDF path
local_md_dir = "output"
os.makedirs(local_md_dir, exist_ok=True)

# Use the function from MinerU.py to extract the PDF content
# md_file_path = extract_pdf_to_markdown(pdf_file_name, local_md_dir)
md_file_path = "output/Example/auto/Example.md"

# Load the extracted markdown content
with open(md_file_path, "r", encoding="utf-8") as f:
    md_text = f.read()

# 提取 Markdown 中的图片路径
image_paths = re.findall(r'!\[.*?\]\((.*?)\)', md_text)

# Function to encode images to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Update image_messages with base64-encoded images
image_messages = []
pdf_base_name = os.path.splitext(os.path.basename(pdf_file_name))[0]
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

# Add this function after the image handling code
def load_prompt_template(template_path):
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

# Load the prompt template
prompt_template = load_prompt_template("GenerateSlidesOutlinePrompt.md")

# 初始化 OpenAI 客户端
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

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

# 使用 GPT-4o 生成 PPT 大纲
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=300,
)

# 提取生成的 PPT 大纲
ppt_outline = response.choices[0].message.content.split("\n")

# 整理 PPT 大纲
formatted_outline = "\n".join(ppt_outline)
print(formatted_outline)

# Function to create a PowerPoint presentation from the outline
def create_ppt_from_outline(outline):
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

    prs.save('Generated_Slides.pptx')

# Create the PowerPoint presentation
create_ppt_from_outline(formatted_outline)