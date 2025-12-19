from container import Container

# init app container
try:
    app_container = Container()
    app_container.config.crowdin.token.override("089303ac7303cc370f40dd38ef1b4e75cd4850842d87181cb5b23eb0f370d90d089c9c5410065356")
    print("initialized")
except Exception as e:
    print(f"Error initializing container: {e}")

try:
    crowdin_client = app_container.crowdin_client()
    projs = crowdin_client.projects.list_projects()
    print(projs)
except Exception as e:
    print(e)