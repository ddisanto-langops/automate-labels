from container import Container

# init app container
try:
    app_container = Container()
    print("initialized")
except Exception as e:
    print(f"Error initializing container: {e}")

try:
    scraper = app_container.scraper()
    title = scraper.get_title("https://www.thetrumpet.com/33136-germany-and-europe-need-a-crisis")
    print(title)
except Exception as e:
    print(e)