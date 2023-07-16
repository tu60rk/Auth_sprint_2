from fastapi import Query


class PaginateQueryParams:
    def __init__(
        self,
        page_number: int = Query(
            0,
            title="Page number.",
            description="Page number to return",
            ge=0,
        ),
        page_size: int = Query(
            50,
            title="Size of page.",
            description="The number of records returned per page",
            ge=1,
            le=500,
        ),
    ):
        self.page_number = page_number
        self.page_size = page_size
