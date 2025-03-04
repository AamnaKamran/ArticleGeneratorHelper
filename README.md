# ArticleGeneratorHelper

ArticleGeneratorHelper is a Python-based tool designed to automate the process of generating comprehensive articles on specified topics. By leveraging web scraping and OpenAI's GPT-4 model, this tool fetches relevant content from the web, processes it, and produces structured articles complete with meta details and internal links.

## Features

- **Web Content Scraping**: Fetches and processes content from top Google search results related to a given topic.
- **Internal Linking**: Identifies and suggests internal links based on extracted keywords to enhance SEO.
- **Meta Details Generation**: Utilizes GPT-4 to create meta titles, descriptions, and URL suggestions tailored to the topic.
- **Article Outline and Generation**: Produces a detailed article outline and generates comprehensive content sections using GPT-4.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/ArticleGeneratorHelper.git
   ```


2. **Navigate to the Project Directory**:

   ```bash
   cd ArticleGeneratorHelper
   ```


3. **Create and Activate a Virtual Environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```


4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```


## Usage

1. **Set Your OpenAI API Key**:

   Replace `"your-api-key"` in the script with your actual OpenAI API key.

2. **Run the Script**:

   ```bash
   python ArticleGeneratorHelper.py
   ```

3. **Follow On-Screen Prompts**:

   Enter the desired topic and website URL when prompted. The tool will then perform the following:

   - Scrape relevant web content.
   - Search for internal links based on extracted keywords.
   - Generate meta details using GPT-4.
   - Produce an article outline and generate comprehensive content sections.
