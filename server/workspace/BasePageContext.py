from django.http import HttpRequest


class BasePageContext:

    class TitleLinkPair:
        title: str
        link: str

        def __init__(self, link, title) -> None:
            self.title = title
            self.link = link

    path_title_link_list = [
        TitleLinkPair("/", "Main"),
        TitleLinkPair("/workspace", "Workspace"),
        TitleLinkPair("/accounts/login", "Log in"),
        TitleLinkPair("/accounts/logout", "Log out"),
        TitleLinkPair("/tutorial", "Tutorial"),
        TitleLinkPair("/about_us", "About us")
    ]

    def __init__(self, request: HttpRequest):
        self.request = request
        self.user_is_authenticated = self.request.user.is_authenticated
        self.username = self.request.user.get_username()
        self.is_workspace = False
        print(f"Trying to upload base context: self.request.path = {self.request.path}")
        print(type(self.request.path))

        self.header_links = []

        self.createHeaderLinksByUrl()

    def createHeaderLinksByUrl(self) -> None:
        for path_title_pair in BasePageContext.path_title_link_list:
            if self.request.path == path_title_pair.link:
                continue
            elif path_title_pair.title == "Workspace" and not self.request.user.is_authenticated:
                continue
            elif path_title_pair.title == "Log in" and self.request.user.is_authenticated:
                continue
            elif path_title_pair.title == "Log out" and not self.request.user.is_authenticated:
                continue

            self.header_links.append(path_title_pair)