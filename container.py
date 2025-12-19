import os
from dependency_injector import containers, providers
from webhook import StringCommentWebhook
from crowdin_api import CrowdinClient
from db_connector import DBConnection
from utils import Utils
from scraper import Scraper
from labels import CrowdinLabels
from xliff import XLIFF

class Container(containers.DeclarativeContainer):
    # Configuration and environment variables
    config = providers.Configuration()
    #crowdin.token = os.environ.get("CROWDIN_API_KEY")


    # Singleton: CrowdinClient (reused across the app)
    crowdin_client = providers.Singleton(
        CrowdinClient,
        token = config.crowdin.token
        )

    # Factory: Utils (stateless, can be reused or recreated)
    utils = providers.Factory(Utils)

    db_connection = providers.Factory(DBConnection)

    scraper = providers.Factory(Scraper)

    crowdin_labels = providers.Factory(
        CrowdinLabels,
        crowdin_client=crowdin_client
    )

    crowdin_comment = providers.Singleton(StringCommentWebhook)

    xliff = providers.Singleton(XLIFF)
