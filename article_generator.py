from bs4 import BeautifulSoup
from googlesearch import search
import requests
import itertools
import re
import openai
import json

openai.api_key = "your-api-key"

def scrape_google_content(query, num_results=4):
    """
    Scrape web pages from Google search results for the given query, excluding Wikipedia URLs.
    
    Parameters:
        query (str): The search query.
        num_results (int): Number of URLs to retrieve.
        
    Returns:
        tuple: Combined scraped text from pages and list of URLs.
        Also writes the scraped content to "scraped_content.txt".
    """
    combined_text = ""
    # Fetch extra URLs to account for Wikipedia filtering
    desired_url_count = max(num_results * 2, 10)  # Ensures we fetch enough initial results
    urls = list(itertools.islice(search(query), desired_url_count))
    
    # Filter out Wikipedia URLs
    filtered_urls = [url for url in urls if 'wikipedia.org' not in url]

    # Select the required number of URLs
    final_urls = filtered_urls[:num_results]
    print("Found URLs:", final_urls)
    
    for url in final_urls:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                # Remove unnecessary elements
                for element in soup(["script", "style", "nav", "footer", "header"]):
                    element.decompose()
                # Extract text only from the body
                body = soup.find("body")
                if body:
                    text = body.get_text(separator=" ", strip=True)
                else:
                    text = soup.get_text(separator=" ", strip=True)
                combined_text += text + "\n\n"
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    
    # Write scraped content to a file
    with open("scraped_content.txt", "w", encoding="utf-8") as f:
        f.write(combined_text)
    print("Scraped content saved to scraped_content.txt")
    
    return combined_text, final_urls

def internal_linking_by_keyword(topic, site_name, num_links_per_keyword=3):
    """
    Extract keywords from the topic and, for each keyword, perform a search for "<keyword> site name".
    The function will iterate over search results until it finds num_links_per_keyword links that
    contain the word "articles" in the URL. All unique links are then combined and returned.
    
    Parameters:
        topic (str): The topic from which to extract keywords.
        num_links_per_keyword (int): The number of useful links to retrieve per keyword.
        
    Returns:
        list: Combined list of unique useful links.
        Also writes the links to "internal_links.txt".
    """

    # Clean the topic: remove punctuation and convert to lowercase.
    topic_clean = re.sub(r'[^\w\s]', '', topic).lower()

    # Define a set of common stopwords to ignore
    STOPWORDS = {
        "what", "is", "a", "an", "the", "and", "it", "to", "of", "for", "with",
        "in", "on", "at", "by", "this", "that", "from", "as", "are", "was", "were", "but"
    }

    # Define additional words to exclude
    EXCLUDE_WORDS = {
        "what", "how", "compares", "best", "comprehensive", "guide", "understandin",
        "beginner's", "benefits", "better", "detailed", "demo", "with"
    }

    # Extract keywords: keep words longer than 3 characters and not in the stop/exclude lists.
    keywords = [
        word for word in topic_clean.split()
        if len(word) > 3 and word not in STOPWORDS and word not in EXCLUDE_WORDS and not word.isdigit()
    ]
    print("Extracted keywords:", keywords)
    
    combined_links = []
    for keyword in keywords:
        query = f"{keyword} {site_name}"
        print(f"\nSearching for links for keyword: '{keyword}' with query: '{query}'")

        links_for_keyword = []

        # Iterate over search results until we have enough useful links.
        for link in search(query):
            if "articles" in link.lower(): # articles refers to a subcategory of pages (if any) to narrow down the seacrh
                if link not in links_for_keyword:
                    links_for_keyword.append(link)
                    print(f"Found useful link for '{keyword}': {link}")

                if len(links_for_keyword) >= num_links_per_keyword:
                    break

        if len(links_for_keyword) < num_links_per_keyword:
            print(f"Only found {len(links_for_keyword)} useful links for '{keyword}'.")

        combined_links.extend(links_for_keyword)
    
    # Write internal links to a file
    with open("internal_links.txt", "w", encoding="utf-8") as f:
        for link in links_for_keyword:
            f.write(link + "\n")
    print("Internal links saved to internal_links.txt")
    
    return links_for_keyword

def get_meta_details(topic, site_url, filename="meta_details.txt"):
    """
    Uses the GPT-4 API to generate meta titles, meta descriptions, and site URL suggestions for a given topic,
    and writes the generated details to a file as formatted JSON.
    
    Parameters:
        topic (str): The website topic.
        filename (str): The file where the meta details will be saved.
        
    Returns:
        dict: The generated meta details.
    """

    prompt = (
        f"You are an SEO expert. For a website about \"{topic}\", please provide:\n"
        "1. Three creative meta titles.\n"
        "2. Three engaging meta descriptions within 160 characters.\n"
        "3. Three potential page URLs. Format each URL as: {site_url}/<suggestion>, "
        "where <suggestion> is a short string of up to 74 characters.\n\n"
        "Format your answer as a JSON object with keys \"meta_titles\", \"meta_descriptions\", and \"site_urls\"."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a SEO and digital marketing expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7, #balance between randomness and predictable responses
        max_tokens=300,
    )
    
    content = response.choices[0].message.content.strip()
    
    try:
        meta_details = json.loads(content)
    except json.JSONDecodeError:
        meta_details = {"raw_output": content}
    
    # Write meta details to a file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(meta_details, indent=2))
    print(f"Meta details saved to {filename}")
    
    return meta_details

def generate_outline(topic, scraped_file="scraped_content.txt"):
    """
    Generate a comprehensive article outline for the given topic using the scraped content.

    Parameters:
        topic (str): The topic for which to generate the outline.
        scraped_file (str): The filename containing the scraped content.

    Returns:
        str: The generated outline.
    """
    # Read the scraped content from file
    try:
        with open(scraped_file, "r", encoding="utf-8") as f:
            scraped_content = f.read()
    except FileNotFoundError:
        print(f"Error: The file {scraped_file} was not found.")
        return None

    # Construct the prompt using the scraped content as context
    prompt = f"""
        Use the scraped content from top articles about "{topic}" given below to generate a comprehensive outline for an article on this topic.
        Outline should have:
        - An engaging introduction.
        - Clearly defined body sections that cover the main points, insights, and data from the scraped content.
        - A conclusion summarizing the key takeaways.
        - Headings, subheadings, and bullet points where appropriate.

Scraped Content:
{scraped_content}
    """

    try:
        # Call the GPT-4 API to generate the outline
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior content strategist and technical writer specializing in AI and tech."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000  # Adjust based on the length needed
        )
    except Exception as e:
        print("Error calling GPT-4 API:", e)
        return None

    outline = response.choices[0].message.content.strip()
    print("Generated Outline:\n", outline)
    
    # Optionally, write the outline to a file
    with open("outline.txt", "w", encoding="utf-8") as f:
        f.write(outline)
    print("Outline saved to outline.txt")
    
    return outline

def article_generator(topic):
    # Read the article outline from outline.txt
    try:
        with open("outline.txt", "r", encoding="utf-8") as f:
            outline_data = f.read()
    except Exception as e:
        print("Error reading outline.txt:", e)
        return

    # Split the outline into sections (each block is one heading and its sub-headings)
    sections = re.split(r'\n\s*\n', outline_data.strip())
    
    final_article = f"Article on \"{topic}\"\n\n"
    
    # Iterate through each section and elaborate
    for idx, section in enumerate(sections, start=1):
        prompt = f"""
You are an expert content strategist and technical writer, specializing in AI and tech. I am writing an article on "{topic}". 
This is the section I need help with (Section {idx}):
{section}

Please elaborate on this section and provide detailed, engaging, and comprehensive content that fits into a full-length article. Ensure that your response is clear, uses appropriate headings and subheadings if needed, and maintains a friendly yet professional tone.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior technical writer and SEO expert specializing in AI and tech."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500  # Adjust max_tokens as needed per section
        )
        
        section_content = response.choices[0].message.content.strip()
        final_article += section_content + "\n\n"
        print(f"Section {idx} completed.")

    # Write the final article to a file named after the topic
    filename = f"generated_article.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_article)
    print(f"Generated article saved to {filename}")
    
    print(final_article)    

def main():
    topic = input("Enter a topic: ")
    website_url = input("Enter the website url: ")
    
    print("\nScraping web content...")
    scraped_content, urls = scrape_google_content(topic, num_results=4)
    print("Scraped URLs:", urls)
    
    print("\nSearching for internal links...")
    useful_links = internal_linking_by_keyword(topic, website_url, num_links_per_keyword=3)
    for link in useful_links:
        print(link)
    
    print("\nGenerating meta details...")
    get_meta_details(topic, website_url)

    print("\nGenerating article outline...")
    generate_outline(topic)

    # print("\nGenerating article...")
    # article_generator(topic)

if __name__ == "__main__":
    main()

