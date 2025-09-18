from google_search_module import ScreenshotCapturer

if __name__ == "__main__":
    url = "https://www.digikala.com/mag/best-gaming-laptops/" # Example URL
    selectors = ["#post-1419579 > article > div.post-module__content > section:nth-child(24)"] # Example CSS selector
    name = "gaming_laptop" # Example name for the screenshot file

    capturer = ScreenshotCapturer(url, selectors=selectors, name=name)
    try:
        capturer.capture_element_screenshots()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        capturer.close_browser()
