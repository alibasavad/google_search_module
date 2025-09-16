from google_search_module import ProductInfoExtractor, ImageDownloader


items = [
    {
     "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/callu-led-lichtleiste/",
     "name" : "CALLU LED-Lichtleiste"
     }, 
    {
     "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/callu-mdc-led-lichtleiste/",
     "name" : "CALLU MDC LED-Lichtleiste"
     },
     
]


# this code is for extracting product information and their images

for item in items:
    extractor = ProductInfoExtractor(item['url'])
    extractor.extract()
    extractor.save_to_file(f"{item['name']}.txt")
    downloader = ImageDownloader(item['url'], "#blockBodyInner")
    image_urls = downloader.extract_image_urls()
    if image_urls:
        downloader.download_images(item['name'])
        print(f"Images downloaded to '{item['name']}' folder.")