from attrs import define

class PageInfo:
    def __init__(self, raw_page: str):
        raw_data = [int(val) for val in raw_page.split(':')]

        self.total = raw_data[0]
        self.offset = raw_data[1]
        self.page_size = raw_data[2]

    def __repr__(self):
        return f"PageInfo({self.offset+1} to {self.offset + self.page_size} of {self.total})"

@define
class Page[T]:
    content: list[T]
    page_info: PageInfo
