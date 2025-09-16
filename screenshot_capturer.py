import os
from google_search_module import ScreenshotCapturer

def test_capturer():
    # Example usage:
    url = "https://dwd-concepts.de/de/produkte/led-signage/"
    selectors = ["#list_370d110b > ul > li:nth-child(11) > div"] # Example selectors: Google logo, "Sign In" button
    name_selectors= ["#list_370d110b > ul > li:nth-child(4) > div > div.listEntryElement.listEntryElement_var0.listEntryElementPadding_var0.listEntryContent > div > div.col.col1 > div > div.listEntryElement.listEntryElement_var0.listEntryElementPadding_var100050.listEntryElementFontSize_var370.listEntryElementFontFamily_var0"] # Example selectors for naming files
    # Create a capturer instance
    capturer = ScreenshotCapturer()

    try:
        # Launch browser
        capturer.launch_browser()

        # Capture screenshots
        # captured_files = capturer.capture_element_screenshots(url, selectors)
        
        for i in range(6):
            selector = f"#list_1d2883fc > ul > li:nth-child({i+1}) > div"
            name_selector = f"#list_1d2883fc > ul > li:nth-child({i+1}) > div > div.listEntryElement.listEntryElement_var0.listEntryElementPadding_var0.listEntryContent > div > div"
            captured_files = capturer.capture_element_screenshots(url, [selector], name_selectors=name_selector)
            print(f"Captured screenshot for selector {selector}: {captured_files}")

        # print(f"Captured screenshots: {captured_files}")

        # Verify if files exist
        for f in captured_files:
            if os.path.exists(f):
                print(f"File '{f}' exists.")
            else:
                print(f"File '{f}' does NOT exist.")

    except Exception as e:
        print(f"An error occurred during testing: {e}")
    finally:
        # Close browser
        capturer.close_browser()

if __name__ == "__main__":
    test_capturer()
