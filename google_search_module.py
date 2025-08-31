import httpx
import requests
import re  # For regex cleanup
from bs4 import BeautifulSoup, NavigableString, Tag
import copy  # To create a modifiable copy of the element
from urllib.parse import urlparse

class GoogleSearchAgent:
    """
    A class to encapsulate Google search functionality.
    """
    @staticmethod
    def classify_url(url: str) -> str:
        """Classify a URL as 'category' or 'product' based on path depth."""
        parsed = urlparse(url)
        # remove leading/trailing slashes and split
        parts = [p for p in parsed.path.split("/") if p]
        
        if len(parts) <= 1:
            return "category"
        else:
            return "product"

    @staticmethod
    def google_search(api_key, search_engine_id, query, title="", exclude="", inurl="", intext="", **params):
        """
        Performs a Google Custom Search using the provided API key, search engine ID, and query.

        Args:
            api_key (str): Your Google Custom Search API key.
            search_engine_id (str): Your Custom Search Engine ID (CX).
            query (str): The search query string.
            title (str): The title to include in the search. Use name of the product
            exclude (str): Terms to exclude from the search.
            inurl (str): Specific URL to include in the search. Use category URLs specified by website.
            **params: Additional parameters to pass to the Google Custom Search API.

        Returns:
            dict: The JSON response from the Google Custom Search API, or an error dictionary.
        """
        final_query = ""
        if title:
            final_query += f'intitle:"{title}" '
        if exclude:
            final_query += f'-"{exclude}" '
        if inurl:
            final_query += f'inurl:"{inurl}" '
        if intext:
            final_query += f'intext:"{intext}" '
        if query:
            final_query += f'{query}'

        print(f"searching for {final_query}")
        
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": final_query,
            **params
        }

        try:
            response = httpx.get("https://www.googleapis.com/customsearch/v1", params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            json_data = response.json()
            return json_data
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP Error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            # Attempt to get response text if available for more details
            response_text = getattr(e, 'response', None)
            response_text = response_text.text if response_text else "No response body available."
            return {"error": "Failed to retrieve search results", "details": str(e), "raw_response": response_text}


class ProductInfoExtractor:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.extracted_sections = []

    def fetch_url(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error fetching the URL: {e}")

    def _get_formatted_text(self, element_to_process):
        # Create a shallow copy to modify so original soup is untouched for other sections
        temp_element = copy.copy(element_to_process)

        # Remove input and button tags from this element and its descendants
        for unwanted_tag in temp_element.find_all(['input', 'button']):
            unwanted_tag.decompose()

        text_parts = []
        for child in temp_element.children:
            if isinstance(child, NavigableString):
                stripped_string = child.strip()
                if stripped_string:
                    text_parts.append(stripped_string)
            elif isinstance(child, Tag):
                # If it's a div or h1, ensure newlines before and after
                if child.name in ['div', 'h1']:
                    if text_parts and text_parts[-1].strip():  # Only add newline if content exists before
                        text_parts.append('\n')
                    # Recursively get text for this div/h1
                    text_parts.append(self._get_formatted_text(child))  # Recursive call
                    # Ensure newline after the div/h1 itself
                    text_parts.append('\n')
                else:  # For other tags, just get text, space separated
                    text_parts.append(self._get_formatted_text(child))  # Recursive call for other tags too

        # Join parts and clean up spaces
        combined_text = ' '.join(filter(None, text_parts)).strip()
        return combined_text

    def extract(self):
        if self.soup is None:
            self.fetch_url()
            
        product_info_divs = self.soup.select("#main_content > section:nth-child(4)")

        if product_info_divs:
            for product_div in product_info_divs:
                processed_text = self._get_formatted_text(product_div)
                # Further clean up multiple spaces and multiple newlines
                processed_text = re.sub(r' +', ' ', processed_text)  # Collapse multiple spaces
                processed_text = re.sub(r'\n+', '\n', processed_text)  # Collapse multiple newlines (e.g. from nested divs)
                self.extracted_sections.append(processed_text)
        else:
            body = self.soup.find('body')
            if body:
                processed_text = self._get_formatted_text(body)
                processed_text = re.sub(r' +', ' ', processed_text)
                processed_text = re.sub(r'\n+', '\n', processed_text)
                self.extracted_sections.append(processed_text)
            else:
                raise RuntimeError("No body tag found. Cannot extract text.")

        return self.extracted_sections

    def return_extracted(self):
        return self.extracted_sections

    def save_to_file(self, filename='extracted.txt'):
        if not self.extracted_sections:
            content = "No extractable text found."
        else:
            content = ('\n\n' + '-'*50 + '\n\n').join(self.extracted_sections)
            content += f"\n\nURL: {self.url}"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content.strip())
        except IOError as e:
            raise RuntimeError(f"Error writing to '{filename}': {e}")


class CategoryInfoExtractor:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.extracted_sections = []

    def fetch_url(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error fetching the URL: {e}")

    def _get_formatted_text(self, element_to_process):
        # Create a shallow copy to modify so original soup is untouched for other sections
        temp_element = copy.copy(element_to_process)

        # Remove input and button tags from this element and its descendants
        for unwanted_tag in temp_element.find_all(['input', 'button', 'aside']):
            unwanted_tag.decompose()

        text_parts = []
        for child in temp_element.children:
            if isinstance(child, NavigableString):
                stripped_string = child.strip()
                if stripped_string:
                    text_parts.append(stripped_string)
            elif isinstance(child, Tag):
                # If it's a div or h1, ensure newlines before and after
                if child.name in ['div', 'h1']:
                    if text_parts and text_parts[-1].strip():  # Only add newline if content exists before
                        text_parts.append('\n')
                    # Recursively get text for this div/h1
                    text_parts.append(self._get_formatted_text(child))  # Recursive call
                    # Ensure newline after the div/h1 itself
                    text_parts.append('\n')
                else:  # For other tags, just get text, space separated
                    text_parts.append(self._get_formatted_text(child))  # Recursive call for other tags too

        # Join parts and clean up spaces
        combined_text = ' '.join(filter(None, text_parts)).strip()
        return combined_text

    def extract(self):
        if self.soup is None:
            self.fetch_url()

        product_info_divs = self.soup.select("#main_content > section:nth-child(3)") 

        if product_info_divs:
            for product_div in product_info_divs:
                processed_text = self._get_formatted_text(product_div)
                # Further clean up multiple spaces and multiple newlines
                processed_text = re.sub(r' +', ' ', processed_text)  # Collapse multiple spaces
                processed_text = re.sub(r'\n+', '\n', processed_text)  # Collapse multiple newlines (e.g. from nested divs)
                self.extracted_sections.append(processed_text)
        else:
            body = self.soup.find('body')
            if body:
                processed_text = self._get_formatted_text(body)
                processed_text = re.sub(r' +', ' ', processed_text)
                processed_text = re.sub(r'\n+', '\n', processed_text)
                self.extracted_sections.append(processed_text)
            else:
                raise RuntimeError("No body tag found. Cannot extract text.")

        return self.extracted_sections

    def return_extracted(self):
        return self.extracted_sections

    def save_to_file(self, filename='extracted.txt'):
        if not self.extracted_sections:
            content = "No extractable text found."
        else:
            content = ('\n\n' + '-'*50 + '\n\n').join(self.extracted_sections)
            content += f"\n\nURL: {self.url}"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content.strip())
        except IOError as e:
            raise RuntimeError(f"Error writing to '{filename}': {e}")

# Example of how to use this module (optional, for testing/demonstration)
# if __name__ == "__main__":
#     # Load API key and search engine ID from environment variables
#     # These should be set in a .env file or as system environment variables
#     api_key = os.getenv("SERPAPI_API_KEY")
#     search_engine_id = os.getenv("SEARCH_ENGINE_ID")
    
#     if not api_key or not search_engine_id:
#         print("Error: SERPAPI_API_KEY and SEARCH_ENGINE_ID must be set in your .env file or environment variables.")
#         print('To get SERPAPI_API_KEY, use this link: "https://serpapi.com/"')
#         print('To get SEARCH_ENGINE_ID, use this link: "https://programmablesearchengine.google.com/controlpanel/all"')
#     else:
#         # Example search
#         query = "best programming languages"
#         print(f"Searching for: '{query}'")
#         results = GoogleSearchAgent.google_search(api_key, search_engine_id, query)

#         if "items" in results:
#             for i, item in enumerate(results["items"][:5]): # Print top 5 results
#                 print(f"--- Result {i+1} ---")
#                 print(f"Title: {item.get('title')}")
#                 print(f"Link: {item.get('link')}")
#                 print(f"Snippet: {item.get('snippet')}\n")
#         elif "error" in results:
#             print(f"Search error: {results['error']}")
#             print(f"Details: {results['details']}")
#         else:
#             print("No items found in search results or unexpected response format.")
#             print(results)

# from product_info_extractor import ProductInfoExtractor

# url = "https://example.com/product-page"
# extractor = ProductInfoExtractor(url)
# extractor.extract()
# extractor.save_to_file("output.txt")
