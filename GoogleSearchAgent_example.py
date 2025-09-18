from google_search_module import GoogleSearchAgent
import dotenv
import os

dotenv.load_dotenv()

# Load your API key and Search Engine ID from environment variables or configuration
API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID =  os.getenv("SEARCH_ENGINE_ID")


if __name__ == "__main__":
    try:
        # Site to include in the search (optional)
        site="https://www.digikala.com"

        # Intitle of the search (optional)
        title="MacBook"

        # Keywords to exclude in the search (optional)
        exclude="Surface"

        # Inurl to include in the search (optional)
        inurl="product"

        # Keywords to include in the search (optional)
        intext="MacBook"

        # Query for the search
        query = "laptop "

        # Perform the search
        results = GoogleSearchAgent.google_search(API_KEY, SEARCH_ENGINE_ID,query, site, title, exclude, inurl, intext)

        if len(results.get("items", [])) == 0:
            print("No results found.")

        if "error" in results:
            print(f"Search error: {results['error']} - {results.get('details', '')}")
        else:
            for item in results.get("items", []):
                print(f"Title: {item['title']}")
                print(f"Link: {item['link']}")
                print(f"Snippet: {item['snippet']}\n")

    except Exception as e:
        print(f"An error occurred: {e}")