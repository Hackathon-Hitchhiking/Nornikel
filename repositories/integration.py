from abc import ABC, abstractmethod

from typing import List
from notion_client import Client
from atlassian import confluence

from schemas.integrations import PageResponse, ResponseType


class BaseIntegrator(ABC):
    """
    A base class for integrating with different documentation platforms.
    """

    @abstractmethod
    def fetch_data(self, page_id: str) -> PageResponse:
        """
        Download a page given its ID.
        """
        pass

    @abstractmethod
    def source(self) -> str:
        """
        Return the source of the integrator.
        """
        pass

    @abstractmethod
    def close(self):
        pass


class ConfluenceIntegration(BaseIntegrator):
    def __init__(self, url: str, username: str, password: str):
        self._conn = confluence.Confluence(
            url=url, username=username, password=password
        )

    def fetch_data(self, page_id: str) -> List[PageResponse]:
        pages = self._conn.get_all_pages_by_label(label=page_id, start=0, limit=100)

        pdfs = []

        for page in pages:
            response = self._conn.get_page_as_pdf(page["id"])

            pdfs.append(
                PageResponse(
                    title=page["title"], content=response, type=ResponseType.PDF
                )
            )

        return pdfs

    def source(self) -> str:
        return "Confluence"

    def close(self):
        self._conn.close()


class NotionIntegration(BaseIntegrator):
    def __init__(self, api_token: str):
        self._conn = Client(auth=api_token)

    def fetch_data(self, page_id: str) -> List[PageResponse]:
        # page = self._conn.pages.retrieve(page_id)

        # TODO fix this and testing

        contents = []
        # page_title = page["properties"]["title"]["title"][0]["plain_text"]

        children = self._conn.blocks.children.list(page_id=page_id).get("results", [])

        for child in children:
            content = ""
            if child["type"] == "child_page":
                sub_page_id = child["id"]
                contents += self.fetch_data(sub_page_id)
            elif child["type"] == "paragraph":
                paragraph_text = "".join(
                    [text["plain_text"] for text in child["paragraph"]["rich_text"]]
                )
                content += f"{paragraph_text}\n\n"

        return contents

    def source(self) -> str:
        return "Notion"

    def close(self):
        self._conn.close()
