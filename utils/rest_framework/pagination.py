from rest_framework.pagination import PageNumberPagination


def pagination_class_factory(name: str, page_size: int = None, page_size_query_param: str = None,
                             max_page_size: int = None):
    """
        A factory which dynamically creates pagination classes with specified parameters based on PageNumberPagination
    :param name: A name for a new class to be created
    :param page_size: page_size attribute to be set on a newly created PageNumberPagination's child class
    :param page_size_query_param: page_size_query_param attribute to be set on a newly created
        PageNumberPagination's child class
    :param max_page_size: max_page_size attribute to be set on a newly created PageNumberPagination's child class
    :return:
    """
    PaginationClass = type(
        name,
        (PageNumberPagination,),
        {'page_size': page_size,
         'page_size_query_param': page_size_query_param,
         'max_page_size': max_page_size}
    )

    return PaginationClass
