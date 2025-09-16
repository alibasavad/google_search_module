from google_search_module import ProductInfoExtractor, ImageDownloader


# items = [
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/callu-led-lichtleiste/",
#      "name" : "CALLU LED-Lichtleiste"
#      }, 
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/callu-mdc-led-lichtleiste/",
#      "name" : "CALLU MDC LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/callu-l-led-lichtleiste/",
#      "name" : "CALLU L LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/caph-led-lichtleiste/",
#      "name" : "CAPH LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/caph-r32-led-lichtleiste/",
#      "name" : "CAPH R32 LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/colludo-d-led-lichtleiste/",
#      "name" : "COLLUDO D LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/colludo-led-lichtleiste/",
#      "name" : "COLLUDO LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/coulson-led-lichtleiste/",
#      "name" : "COULSON LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/crook20/",
#      "name" : "CROOK20 LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/ensa-led-lichtleiste/",
#      "name" : "ENSA LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/g610-led-lichtleiste/",
#      "name" : "G610 LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/gallery-hp-led-lichtleiste/",
#      "name" : "GALLERY HP LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/gallery-led-lichtleiste/",
#      "name" : "GALLERY LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/gallery-mdc-led-lichtleiste/",
#      "name" : "GALLERY MDC LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/planus-led-lichtleiste/",
#      "name" : "PLANUS LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/leon-led-lichtleiste/",
#      "name" : "LEON LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/m600-led-lichtleiste/",
#      "name" : "M600 LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/mini-sirius-led-lichtleiste/",
#      "name" : "MINI SIRIUS LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/ripps-led-lichtleiste/",
#      "name" : "RIPPS LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/tauri-led-lichtleiste/",
#      "name" : "TAURI LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/tita-led-lichtleiste/",
#      "name" : "TITA LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/tita-l-led-lichtleiste/",
#      "name" : "TITA L LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/tita-s-led-lichtleiste/",
#      "name" : "TITA S LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/trigona-led-lichtleiste/",
#      "name" : "TRIGONA LED-Lichtleiste"
#      },
#     {
#      "url" : "https://dwd-concepts.de/de/produkte/led-lichtleisten/versura-l-led-lichtleiste/",
#      "name" : "VERSURA L LED-Lichtleiste"
#      }     
# ]

items = [
    {
     "url" : "https://dwd-concepts.de/de/produkte/inwi-stromschienen-systeme/bbs-inwi-stromschiene/",
     "name" : "BBS INWI"
     }
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