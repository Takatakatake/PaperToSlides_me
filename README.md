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

---
## Additional Information

Below is a concise installation and troubleshooting guide written by [Mr. Yamauchi](https://github.com/Takatakatake ). Special thanks to him for his contribution!

This document details the installation process, provides clarifications on the instructions in the README.md file, and outlines the errors I encountered along with their solutions.

### PaperToSlides Installation and Setup (README.md Clarifications)

Here are some clarifications regarding the steps outlined in the PaperToSlides README.md:

1. Downloading the Source Code:
Regarding step 1 in the README, downloading the source code by selecting "Download ZIP" from the`< > Code` button on the GitHub repository page presented no particular issues.

2. Creating the Model Directory:
Before proceeding to step 5, it is necessary to create the `model` directory beforehand using the command `mkdir -p model`.

3. Downloading Model Files (`git lfs clone`):
The command `git lfs clone https://huggingface.co/wanderkid/PDF-Extract-Kit` is used to download the model files. However, this command may not complete successfully depending on the execution environment. Specifically, there were cases where only small files were downloaded, resulting in the error message "Not in a Git repository." In such situations, trial and error are required until the command succeeds.

Even if `git lfs clone` persistently fails, it was ultimately possible to get the tool working by running `python download_models.py` within the `./MinerU` directory (discussed later) and individually addressing the various errors that arose subsequently. However, this method is extremely time-consuming and is not recommended.

4. Running `download_models.py`:
Regardless of whether `git lfs clone` was successful, it seems often necessary to navigate to the `./MinerU` directory and execute `python download_models.py`. Some trial and error was required to get this script to complete successfully.

**Important Notes:**

- The total size of the downloaded model files is approximately 12GB, and the download process takes a significant amount of time.

- Executing this script generates a configuration file named magic-pdf.json in the user's home directory.
- Dependency errors may occur during execution. For instance, in my environment, it was necessary to run `pip install modelscope` after activating the virtual environment with `conda activate MinerU`.

### Basic Execution Steps

1. Placing the PDF File:
Place the target PDF file (the one you want to generate a slide outline from) inside the `./data` directory of the PaperToSlides installation.

2. Editing `GenerateSlidesOutline.py`:
Edit the following sections within the `GenerateSlidesOutline.py` script:

- Setting the OpenAI API Key:
Set your own OpenAI API key. Please refer to external resources for information on obtaining and using API keys.

```Python
os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
```
- Specifying the Input PDF File Name:
Specify the name of the PDF file you placed in the ./data directory.

```Python
pdf_file_name = "data/YourFileName.pdf"  # e.g., "data/Example.pdf"
```
- Enabling the PDF Parsing Function:
To enable the function that converts the PDF to Markdown, remove the comment symbol (#) from the beginning of the following two lines:

```Python
# from MinerU import extract_pdf_to_markdown  # Remove '#' from this line
# md_file_path = extract_pdf_to_markdown(pdf_file_name, local_dir) # Remove '#' from this line
```

Consequently, comment out the following existing line by adding a # at the beginning, as it becomes unnecessary:

```Python
# md_file_path = "output/Example/auto/Example.md" # Comment out this line
```

3. Executing the Script:
After activating the virtual environment with the conda activate MinerU command, run the script using the following command:

```Bash
python ./GenerateSlidesOutline.py
```

### Encountered Errors and Solutions

Even after following the steps above, several errors may occur. Below are the main errors I encountered and their respective solutions (in no particular order):

- `ModuleNotFoundError: No module named 'magic_pdf.data'`

- `subprocess.CalledProcessError: Command '['magic-pdf', 'extract', ...]' returned non-zero exit status 2.`

These errors were caused by issues related to invoking the `magic-pdf` PDF parsing library. To resolve this, the `extract_pdf_to_markdown` function within the `MinerU.py` script was significantly modified. The method for specifying arguments for the `magic-pdf` command was also changed.

Modified `MinerU.py`:

```Python

import os
import subprocess

def extract_pdf_to_markdown(pdf_file_name, output_dir):
    """
    Simple function to convert PDF file to Markdown (Modified)
    """
    # Create the output directory
    os.makedirs(output_dir, exist_ok=True)

    # Convert PDF to Markdown using the magic-pdf command
    pdf_base_name = os.path.splitext(os.path.basename(pdf_file_name))[0]
    # Note: The original code might have intended a different md_file_path structure.
    # This path is based on the original snippet but might need adjustment
    # depending on where magic-pdf actually places the output.
    md_file_path = os.path.join(output_dir, f"{pdf_base_name}.md")

    # # Original command structure (commented out)
    # cmd = [
    #     "magic-pdf", "extract", pdf_file_name,
    #     "--output-dir", output_dir,
    #     "--format", "markdown"
    # ]
    # subprocess.run(cmd, check=True)

    # MinerU.py after modification
    cmd = [
        "magic-pdf",
        "-p", pdf_file_name,      # Add "-p" before the input file path
        "-o", output_dir          # Use "-o" for the output directory
                                  # (Note: The original Japanese comment mentioned either -o or --output-dir might work)
    ]
    # It's good practice to capture output for debugging
    try:
         subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
         print(f"Error executing magic-pdf command:")
         print(f"Command: {' '.join(e.cmd)}")
         print(f"Return Code: {e.returncode}")
         print(f"Stderr: {e.stderr}")
         print(f"Stdout: {e.stdout}")
         raise e # Re-raise the exception after printing details


    # Check and return the path of the generated markdown file
    # magic-pdf seems to create a nested structure like output_dir/pdf_base_name/auto/pdf_base_name.md
    expected_md_path = os.path.join(output_dir, f"{pdf_base_name}/auto/{pdf_base_name}.md")
    if os.path.exists(expected_md_path):
        return expected_md_path

    # If not found in the usual location, search within the output directory.
    # This part tries to find the .md file more robustly if the expected path is wrong.
    print(f"Warning: Expected Markdown file not found at {expected_md_path}. Searching in {output_dir}...")
    for root, _, files in os.walk(output_dir):
        for file in files:
            # Look for a markdown file containing the base name in its filename
            if file.endswith(".md") and pdf_base_name in file:
                found_path = os.path.join(root, file)
                print(f"Found potential Markdown file: {found_path}")
                # It might be necessary to move/rename this file to the expected path
                # depending on subsequent script logic.
                return found_path # Return the path found

    # If no file is found after searching, return the originally constructed (but likely incorrect) path,
    # or better, raise an error. The original code returned md_file_path.
    print(f"Error: Markdown file could not be located in {output_dir}")
    # Returning the original md_file_path might suppress errors later.
    # Raising an error is usually better.
    # return md_file_path # Original behavior
    raise FileNotFoundError(f"Could not find the generated Markdown file in {output_dir} or its subdirectories.")
```

**Disclaimer:** The Python code modification above is based on the provided snippet. The exact arguments and output paths for `magic-pdf` might vary depending on its version and internal logic. Further adjustments may be needed.

- Installing the OpenAI Library:
If you encounter an error indicating that the `openai` module cannot be found during execution, activate the `MinerU` environment (`conda activate MinerU`) and install the library by running `conda install openai` or `pip install openai`. (The original memo mentioned running `conda install openai`.)

- `FileNotFoundError: [Errno 2] No such file or directory: '/home/user/.cache/modelscope/hub/.../weights.pt'`:
This error indicates that the pre-trained model (weight file), used for extracting elements like mathematical formulas from the PDF, could not be found. The cause is that the model files are not correctly placed in the expected cache directory.

#### Solution:

1. Confirm the location where the model files downloaded via `git lfs clone` (as discussed earlier) are stored. Typically, there should be a subdirectory named `models` (approximately 8.8GB) within the `model/PDF-Extract-Kit/` directory of your installation.

2. Copy or move this entire `models` directory into the cache directory path shown in the error message, ensuring it resides within that path as a directory named `models`. Example: Copy or move the contents of `[Your_Download_Location]/model/PDF-Extract-Kit/models to ~/.cache/modelscope/hub/models/opendatalab/PDF-Extract-Kit-1___0/models`. (Note: The exact cache path `/home/user/.cache/...` will vary depending on the user and environment.)

3. For this reason too, it is highly advisable to ensure that the model file download (`git lfs clone`) completes successfully in the first place.

#### Alternative (Not Recommended):
If formula recognition is not strictly required, this error can sometimes be bypassed by editing the m`agic-pdf.json` file generated in the home directory and disabling the formula recognition feature (set `"formula-config": { "enable": false }`). However, this is generally not recommended as it may significantly degrade the quality of the generated slides for documents containing mathematical formulas, such as academic papers.

### Conclusion

The details above cover the installation process and troubleshooting steps I experienced while setting up PaperToSlides. While the setup and error resolution can require patience and technical adjustments, I hope this detailed feedback proves helpful both to other users attempting to utilize this promising tool and potentially to the developers for improving the installation and user experience in the future.
