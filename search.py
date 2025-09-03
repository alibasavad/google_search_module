from google_search_module import ProductInfoExtractor, ImageDownloader


items = [
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=428577398&cHash=7f0cd2a057b563464606a2958e71991f",
    #  "name" : "Mercedes-Benz CLA 180 PROGRESSIVE PANORAMA SPURASSIST KAMERA"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=434212840&cHash=e65e9a7cdfbe78f4e3562f94ac7894f4",
    #  "name" : "Mercedes-Benz CLA 180 PROGRESSIVE PANORAMA SPURASSIST KAMERAMercedes-Benz CLA 250+ PROGRESSIVE NIGHT LED PANORAMA MEMORY"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=435375255&cHash=b192f5bf792335f3784bc5cbe412b0e8",
    #  "name" : "Mercedes-Benz CLA 200 AMG NIGHT 360° TOTWINKEL KEYLESS PDC LED"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=428015967&cHash=be593d0448797ef597fe05f60925a0c7",
    #  "name" : "Fiat Panda 1.0 Mild Hybrid EU6e City Paket"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=434759686&cHash=06d1c96b950c44056802aeaa5cb6f04b",
    #  "name" : "Mercedes-Benz A 250 e PROGRESSIVE DISTRONIC MEMORY MULTIBEAM"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=392527039&cHash=f5c65c3aeb53fc156ead7e4493a35a5b",
    #  "name" : "Jeep Avenger Elektro Longitude,Navi, Technology und S"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=434848311&cHash=9a93a2b2009a46ad0969b056e6c95c12",
    #  "name" : "Mercedes-Benz EQA 250+ AMG SPURPAKET KAMERA PDC LENKRADHEIZ"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=433644497&cHash=315e07530934c354b695820d1e137350",
    #  "name" : "Kia Stonic Spirit 1.0 T-GDI EU6d-T Automatic+AHK+NAV"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=423395215&cHash=0dfba87ec244db049c00f68bd6fdbb32",
    #  "name" : "Alfa Romeo Tonale Super 1.5 Mild Hybrid EU6d"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=434785922&cHash=ac98e5a2968a0e6457365355792630c2",
    #  "name" : "Mercedes-Benz CLA 180 Shooting Brake EDITION DISTRONIC NAV AHK"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=430545639&cHash=e86cd4483bae5daaed57cce25915ee65",
    #  "name" : "Mercedes-Benz E 300 e T AVANTGARDE DISTRONIC KEYLESS KAMERA"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=432250427&cHash=55f9873cf759b847e34678e3aada170e",
    #  "name" : "Mercedes-Benz E 300 de 4M T EDITION AMG NIGHT PANORAMA MEMORY"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=430685749&cHash=e4811035e5471a09ae47a4d3610106b3",
    #  "name" : "Fiat 500C Red 1.0 Mild Hybrid EU6d Navi,Klima,PDC"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=431195822&cHash=63342fc35994fb3a399cd00982e287ea",
    #  "name" : "Porsche Boxster 718 STYLE EDITION LED CHRONO BOSE MEMORY"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=421176726&cHash=09ab36085459363be225e7bce6f9c627",
    #  "name" : "Mercedes-Benz SPRINTER 317 CDI L2-H2 Kasten Hochdach Standard"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=435247036&cHash=e0946041937a0b004726a2cc568359d2",
    #  "name" : "Mercedes-Benz V 220 d Lang SPORT NIGHT NAVI PARKPAKET LED"
    #  },
    # {
    #  "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=406447605&cHash=bcd71f1c918e1ae91c12dff0e0d8f010",
    #  "name" : "Mercedes-Benz V 300 d 4M STYLE Lang  DISTRONIC STANDHEIZUNG"
    #  },
    {
     "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=434391813&cHash=2eacb02b238423b21b0da506f819a768",
     "name" : "Opel Corsa F Edition 1.2  SHZ LHZ PDC CAR-PLAY"
     },
    {
     "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=430327472&cHash=54f49ce8b31183d0e5621b9437bed807",
     "name" : "Opel Corsa F GS 1.2 Sitz.&Lenkradh. 100KW EU6d"
     },
    {
     "url" : "https://www.rkg.de/gebrauchtwagensuche/pkw/detail?tx_szsearch_pi1%5Bad%5D=411483931&cHash=f85af4462ee902b498073dc0d51f85e6",
     "name" : "Jeep Avenger Altitude 1.2 Winterpaket, Infotainment-K"
     } 
]


# this code is for extracting product information and their images

for item in items:
    extractor = ProductInfoExtractor(item['url'])
    extractor.extract()
    extractor.save_to_file(f"{item['name']}.txt")
    downloader = ImageDownloader(item['url'], "#c2868 > section.info-section.gray-gradient.sz-search-detail > div:nth-child(2) > div.big-gallery-wrap > div.gallery.hidden-print")
    image_urls = downloader.extract_image_urls()
    if image_urls:
        downloader.download_images(item['name'])
        print(f"Images downloaded to '{item['name']}' folder.")