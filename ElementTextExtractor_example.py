from google_search_module import ElementTextExtractor

if __name__ == "__main__":

    # Example url to extract text from
    url="https://www.digikala.com/mag/best-gaming-laptops/"

    # Define the sections to extract from the webpage
    extraction_sections = [
        "#post-1419579 > article > div.post-module__content > p:nth-child(1)",
        "#post-1419579 > article > div.post-module__content > p:nth-child(6)"
    ]

    extractor = ElementTextExtractor(url, extraction_sections=extraction_sections, filename='data/result.txt')
    try:
        extracted_data = extractor.extract()
        print("\n--- Extracted Product Information ---")
        for section in extracted_data:
            print(section)
            print("-" * 5)

        # Optionally save to a file
        extractor.save_to_file()

    except RuntimeError as e:
        print(f"Error during product information extraction: {e}")
