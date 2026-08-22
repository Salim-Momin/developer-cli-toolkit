from devkit.services.api_service import (
    send_request,
)


def test_api_get_request():

    response = send_request(
        "GET",
        "https://jsonplaceholder.typicode.com/posts/1",
    )

    assert response is not None
