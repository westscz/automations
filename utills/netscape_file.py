from bookmarks_parser import parse

from logging import Logger
LOGGER = Logger(__name__) #create_logger(__name__)


class NetscapeFileUrl:
    def __init__(self, bookmarks_path):
        self.last_urls = None
        self.__bookmarks_json = None
        self.bookmarks_path = bookmarks_path
        self.url_title_name = "title"

    @property
    def bookmarks(self):
        """
        Bookmarks data

        :return:
        """
        if not self.__bookmarks_json:
            LOGGER.debug(self.bookmarks_path)
            self.__bookmarks_json = parse(self.bookmarks_path)
        return self.__bookmarks_json

    def get_folder(self, folder_name):
        """
        Get bookmarks from given folder name

        :param folder_name: Name of searched folder
        :return:
        """
        folder_data = self.__find_folder_in_bookmarks(folder_name, self.bookmarks)
        if not folder_data:
            raise IndexError(f"Bookmarks does not have '{folder_name}' folder")
        return folder_data

    def __find_folder_in_bookmarks(self, folder_name, bookmarks):
        for bookmark in bookmarks:
            if self._is_searched_folder(bookmark, folder_name):
                return bookmark.get("children")
            elif self._is_folder(bookmark):
                result = self.__find_folder_in_bookmarks(
                    folder_name, bookmark.get("children")
                )
                if result:
                    return result

    def _is_searched_folder(self, bookmark, folder_name):
        return (
                self._is_folder(bookmark)
                and bookmark.get(self.url_title_name, None) == folder_name
        )

    def _is_folder(self, bookmark):
        return bookmark.get("type") == "folder"
