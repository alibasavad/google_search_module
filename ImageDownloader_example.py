from google_search_module import ImageDownloader

if __name__ == "__main__":
    url = "https://www.digikala.com/mag/best-gaming-laptops/"  # Replace with your target URL
    download_path = "./data/images"  # Replace with your desired download path
    selectors = "#post-1419579 > article" # Replace with your desired CSS selectors

    try:
        downloader = ImageDownloader(url, selectors, base_url=url, download_path=download_path)
        downloader.download_images()
        print(f"Images downloaded successfully to {download_path}")
    except Exception as e:
        print(f"An error occurred: {e}")