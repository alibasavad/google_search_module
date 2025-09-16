import httpx
import requests
import re  # For regex cleanup
from bs4 import BeautifulSoup, NavigableString, Tag
import copy  # To create a modifiable copy of the element
from urllib.parse import urlparse
import os # For creating directories

class GoogleSearchAgent:
    """
    A class to encapsulate Google search functionality.
    """
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
            response = requests.get(self.url, verify=False)
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
                if child.name in ['h1','div', "dd" , "dl" , "ul", "br","li"]:
                    if text_parts and text_parts[-1].strip():  # Only add newline if content exists before
                        text_parts.append('\n')
                    # Recursively get text for this div/h1
                    text_parts.append(self._get_formatted_text(child))  # Recursive call
                    # Ensure newline after the div/h1 itself
                    # text_parts.append('\n')
                    
                elif child.name in ["br", "dt"]:
                    if text_parts and text_parts[-1]:  # Only add newline if content exists before
                        text_parts.append(' . ')
                    text_parts.append(self._get_formatted_text(child))  # Recursive call
                    text_parts.append(' ')
                    
                elif child.name in [ 'h2', 'h3', 'h4']:
                    if text_parts and text_parts[-1].strip():  # Only add newline if content exists before
                        text_parts.append(': ')
                    text_parts.append(self._get_formatted_text(child))  # Recursive call
                    text_parts.append(': ')
                    
                else:  # For other tags, just get text, space separated
                    text_parts.append(self._get_formatted_text(child))  # Recursive call for other tags too

        # Join parts and clean up spaces
        combined_text = ' '.join(filter(None, text_parts)).strip()
        return combined_text

    def _select_divs(self, selector_list : list):
        selected_divs = []
        for selector in selector_list:
            divs = self.soup.select(selector)
            selected_divs.extend(divs)
        return selected_divs

    def extract(self):
        if self.soup is None:
            self.fetch_url()

        product_info_divs = self._select_divs([
            "#sectionProduct > div > div > div.col.col1 > div > div > div",
            "#sectionProductData > div > div > div > div",
            "#blockContentInner > div.elementSection.elementSection_var0.elementSectionPadding_var10000.elementSectionMargin_var0.elementSectionInnerWidth_var0 > div > div.elementSection.elementSection_var0.elementSectionPadding_var10001.elementSectionMargin_var0.elementSectionInnerWidth_var0 > div > div > div.col.col1 > div > div.elementText.elementText_var0.elementTextListStyle_var0.last-child > ul",
        ])

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
            # content += f"\n\nURL: {self.url}"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content.strip())
        except IOError as e:
            raise RuntimeError(f"Error writing to '{filename}': {e}")


class ImageDownloader:
    def __init__(self, url, selector, base_url=None):
        self.url = url
        self.selector = selector
        self.base_url = base_url if base_url else urlparse(url).scheme + "://" + urlparse(url).netloc
        self.soup = None
        self.image_urls = []

    def _fetch_html(self):
        try:
            response = requests.get(self.url, verify=False)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error fetching the URL: {e}")

    def extract_image_urls(self):
        if self.soup is None:
            self._fetch_html()

        target_element = self.soup.select_one(self.selector)
        if not target_element:
            raise ValueError(f"No element found with selector: {self.selector}")

        picture_tags = target_element.find_all('picture')
        for picture in picture_tags:
            best_image_url = None
            best_width = 0
            
            # Prioritize webp if available, otherwise fall back to jpg/jpeg
            source_elements = picture.find_all('source')
            
            # First pass: look for the highest resolution webp image
            for source in source_elements:
                if source.get('type') == 'image/webp' and source.get('srcset'):
                    # srcset can contain multiple URLs and their descriptors (e.g., 1152w)
                    for srcset_item in source['srcset'].split(','):
                        parts = srcset_item.strip().split(' ')
                        if len(parts) == 2:
                            url = parts[0]
                            width_str = parts[1]
                            if width_str.endswith('w'):
                                width = int(width_str[:-1])
                                if width > best_width:
                                    best_width = width
                                    best_image_url = url
            
            # If no webp found or if jpeg has an even higher resolution, check jpeg
            # This part ensures that if webp is found, we stick with it unless a JPEG is significantly better
            # (which is unlikely given the usual srcset patterns, but good to be robust)
            for source in source_elements:
                if source.get('type') == 'image/jpeg' and source.get('srcset'):
                    for srcset_item in source['srcset'].split(','):
                        parts = srcset_item.strip().split(' ')
                        if len(parts) == 2:
                            url = parts[0]
                            width_str = parts[1]
                             # Check if it ends with 'w'
                            if width_str.endswith('w'):
                                width = int(width_str[:-1])
                                if width > best_width :
                                    best_width = width
                                    best_image_url = url
            
            # Fallback to img tag if no source elements provided valid srcset, or for a base image
            if not best_image_url:
                img_tag = picture.find('img')
                if img_tag and img_tag.get('src'):
                    best_image_url = img_tag['src']
            
            
            if best_image_url:
                # Resolve relative URLs
                if not urlparse(best_image_url).scheme:
                    if best_image_url.startswith('/'):
                        self.image_urls.append(self.base_url + best_image_url)
                    else:
                        self.image_urls.append(self.base_url + "/" + best_image_url)
                else:
                    self.image_urls.append(best_image_url)
        return self.image_urls

    def download_images(self, folder_name="downloaded_images"):
        if not self.image_urls:
            print("No image URLs extracted. Please run extract_image_urls first.")
            return

        os.makedirs(folder_name, exist_ok=True)
        print(f"Downloading {len(self.image_urls)} images to '{folder_name}'...")

        for i, img_url in enumerate(self.image_urls):
            try:
                img_data = requests.get(img_url, verify=False).content
                img_name = os.path.join(folder_name, f"image_{i+1}_{os.path.basename(urlparse(img_url).path)}")
                with open(img_name, 'wb') as handler:
                    handler.write(img_data)
                print(f"Downloaded: {img_name}")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {img_url}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred for {img_url}: {e}")
        print("Image download complete.")


class CategoryInfoExtractor:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.extracted_sections = []

    def fetch_url(self):
        try:
            response = requests.get(self.url, verify=False)
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
        print(f"Saving extracted content to '{filename}'")
        if not self.extracted_sections:
            content = "No extractable text found."
        else:
            content = ('\n\n' + '-'*50 + '\n\n').join(self.extracted_sections)
            # content += f"\n\nURL: {self.url}"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content.strip())
        except IOError as e:
            raise RuntimeError(f"Error writing to '{filename}': {e}")


from playwright.sync_api import sync_playwright

class ScreenshotCapturer:
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.page = None

    def launch_browser(self):
        self._playwright_instance = sync_playwright().start()
        self.browser = self._playwright_instance.chromium.launch(headless=self.headless)
        # self.page = self.browser.new_page()
        self.page = self.browser.new_page(viewport={'width': 1800, 'height': 2500})

    def close_browser(self):
        if self.browser:
            self.browser.close()
        if self._playwright_instance:
            self._playwright_instance.stop()

    def capture_element_screenshots(self, url, selectors, output_dir="element_screenshots" , name_selectors = ""):
        if not self.browser or not self.page:
            self.launch_browser()

        os.makedirs(output_dir, exist_ok=True)
        self.page.goto(url)
        
        # get text in name_selector element if provided
        name = None
        if name_selectors:
            try:
                self.page.wait_for_selector(name_selectors, state='visible', timeout=5000)
                name_element = self.page.locator(name_selectors)
                name = name_element.inner_text().strip().replace(" ", "_")[:50]  # Limit length for filename
                # Sanitize name to remove invalid filename characters
                name = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in name)
                print(f"Using '{name}' as base name for screenshots.")
            except Exception as e:
                print(f"Could not retrieve name from selector '{name_selectors}': {e}")
                name = None

        # Handle cookie pop-up if present
        cookie_notice_selector = "#cookieNoticeInner > div"
        cookie_closer_selector = "#cookieNoticeCloser"

        try:
            # Check if the cookie notice is visible
            self.page.wait_for_selector(cookie_notice_selector, state='visible', timeout=5000)
            # If visible, click the closer button
            self.page.click(cookie_closer_selector)
            print("Closed cookie notice pop-up.")
            # Give some time for the pop-up to disappear
            self.page.wait_for_timeout(1000)
        except Exception:
            print("No cookie notice pop-up found or could not close it.")
            # Continue without closing if not found or cannot be closed

        screenshots_paths = []
        for i, selector in enumerate(selectors):
            try:
                # Wait for the element to be visible
                self.page.wait_for_selector(selector, state='visible', timeout=11000)
                element = self.page.locator(selector)
                
                # Scroll to the element to ensure it's in the viewport
                element.scroll_into_view_if_needed()

                # Sanitize selector for filename
                # Replace invalid characters with underscores to create a valid filename
                sanitized_selector = "".join(c if c.isalnum() else "_" for c in selector)
                
                if name:
                    # Append .png extension when a custom name is used
                    screenshot_path = os.path.join(output_dir, f"{name}.png")
                else:
                    # Use the default naming convention with .png extension
                    screenshot_path = os.path.join(output_dir, f"element_{i+1}_{sanitized_selector[:50]}.png")
                
                element.screenshot(path=screenshot_path)
                screenshots_paths.append(screenshot_path)
                print(f"Captured screenshot for selector '{selector}': {screenshot_path}")
            except Exception as e:
                print(f"Could not capture screenshot for selector '{selector}': {e}")
        return screenshots_paths
