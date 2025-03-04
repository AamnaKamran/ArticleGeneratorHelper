# ArticleGeneratorHelper

ArticleGeneratorHelper is a Python-based tool designed to automate the process of generating comprehensive articles on specified topics. By leveraging web scraping and OpenAI's GPT-4 model, this tool fetches relevant content from the web, processes it, and produces structured articles complete with meta details and internal links.

(That's the ChatGPT version of things. Let me explain in more detail (for those interested ofc). Let's be real, (almost) all of us take help from AI chatbots to make our work easier but sometimes their use can make our work more tedious. So this is an attempt to reduce the copying and pasting of content from LLM tools and create a more streamlined process that will help save your time as well, in tasks like giving gpt separate prompt for article title ideas, meta descriptions, what sections to include. Another feature is that it can also pick up content from top trending websites on the selected topic and then generate an outline based on that.. so you already have a headstart. 

Since GPT APIs are paid the article generator feature of this code is not well tested. However, I have noticed a significant improvement in the article generated when your give an outline to the bot. The idea behind the repetitive calls in the article generattion function for each section is the get detailed content.. because AI chatbots don't do well with word limits. Ofc, the generated content still requires manual editing.)

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
