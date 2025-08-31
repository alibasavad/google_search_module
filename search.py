import os
from dotenv import load_dotenv
import pandas as pd
from google_search_module import GoogleSearchAgent , ProductInfoExtractor , CategoryInfoExtractor

load_dotenv()  # Load environment variables from .env file

if __name__ == "__main__":
    api_key = os.getenv("SERPAPI_API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")
    
    inurl=""
    inurl=input("enter inurl: ")

    intext=""
    intext=input("enter intext: ")

    title=""
    title=input("enter intitle: ")

    exclude=""
    exclude=input("enter exclude: ")

    search_query = ""
    search_query=input("enter query: ")

    search_result = GoogleSearchAgent.google_search(api_key, search_engine_id, search_query, inurl=inurl , exclude=exclude, title=title, intext=intext)

    if "items" in search_result:  # Check if search results exist
        items = search_result["items"]

        for index, item in enumerate(items):
            url = item.get("link")
            if GoogleSearchAgent.classify_url(item.get("link")) == "product":
                extractor = ProductInfoExtractor(url)
            else:
                extractor = CategoryInfoExtractor(url)
            extractor.extract()
            extractor.save_to_file(f"{index}.data.txt")

    else:
        print("No results found or error in search response.")
     
