# PaperToSlides

🚀 **PaperToSlides** is an AI-driven tool designed to automatically convert academic papers in PDF format into polished presentation slides—perfect for research group meetings, conference rehearsals, and quick paper summaries.

## Key Features

- 📄 **Efficient Content Extraction**: Utilizes [MinerU](https://github.com/opendatalab/MinerU?tab=readme-ov-file#2-download-model-weight-files) for high-quality content extraction from academic PDFs.
- 🤖 **AI-Powered Summarization**: Integrates OpenAI’s API to interpret and summarize the paper's content, including both text and visual data.
- 🎨 **Slide Generation**: Produces a structured, ready-to-present PowerPoint file.
- 🖼️ **Visual Preservation**: Retains original figures, tables, and images, ensuring content integrity.
- 📊 **Presentation-Ready**: Tailored for academic settings, making it ideal for presentations, discussions, and research insights.

## Use Cases

- 📘 **Research Paper Presentations**: Summarize and present papers with minimal manual preparation.
- 👥 **Academic Group Meetings**: Share findings efficiently in lab or study group settings.
- 🎤 **Conference Rehearsals**: Practice presenting key points ahead of conferences.
- 🔍 **Quick Overviews**: Generate concise summaries for rapid information sharing.

## Installation and Setup

To get started, follow these steps:

1. **Clone this repository**:
    ```bash
    git clone [https://github.com/yourusername/PaperToSlides.git]
    cd PaperToSlides
    ```

2. **Set up MinerU and dependencies**:
    ```bash
    cd MinerU
    git clone https://github.com/opendatalab/MinerU.git && cd ..
    ```

3. **Create a virtual environment**:
    ```bash
    conda create -n MinerU python=3.10
    conda activate MinerU
    ```

4. **Install dependencies**:
    ```bash
    pip install magic-pdf[full]==0.7.0b1 --extra-index-url https://wheels.myhloli.com
    pip install python-pptx
    ```

5. **Set up model weights using Git LFS**:
    ```bash
    cd model
    git lfs clone https://huggingface.co/wanderkid/PDF-Extract-Kit
    ```

6. **Configuration**:
   Update `magic-pdf.json` to specify the `models-dir` and `cuda` settings according to your environment.
