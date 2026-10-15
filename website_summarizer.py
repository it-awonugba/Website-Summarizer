import requests
from bs4 import BeautifulSoup
import ollama
from IPython.display import Markdown, display

class WebsiteSummarizer:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name

    def fetch_website_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the website content: {e}")
            return None

    def extract_text(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        # Remove script,style, input and image elements
        for unwanted_element in soup(['script', 'style', 'input', 'img']):
            unwanted_element.decompose()
        text = soup.get_text(separator='\n', strip=True)
        return text

    def summarize_text(self, text):
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": f"Summarize the following text:\n{text}"}]
            )
            summary = response.choices[0].message.content
            return summary
        except Exception as e:
            print(f"Error summarizing the text: {e}")
            return None

    def summarize_website(self, url):
        html_content = self.fetch_website_content(url)
        if html_content:
            text_content = self.extract_text(html_content)
            summary = self.summarize_text(text_content)
            if summary:
                display(Markdown(f"### Summary of {url}\n\n{summary}"))


summarizer = WebsiteSummarizer()
summarizer.summarize_website("www.chelseafc.com")