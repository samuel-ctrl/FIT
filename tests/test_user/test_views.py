import pytest
import logging

from rest_framework.test import APIClient

from tests.test_user.data import VALID_LOGIN_VIEW_API
from unittest.mock import patch
from rest_framework.test import RequestsClient, APITestCase

LOGGER = logging.getLogger(__name__)
client = APIClient()


@pytest.mark.parametrize(
    "url, method, ex_request, ex_response, stub_data",
    [VALID_LOGIN_VIEW_API],
)
@patch('user.views.LoginView.try_method')
def test_views_api(
    mocker, url, method, ex_request, ex_response, stub_data
):
    stubed_data = mocker.patch(url)
    stubed_data.return_value = "stubed value"

    client_method = getattr(client, method)
    response = client_method(url, ex_request)

    LOGGER.info(f"--------- {stubed_data.called} ----------")
    assert response.status_code == ex_response['status']
    assert response.data['detail'] == "stubed value"
    # LOGGER.info(f" \n {stub_mail_fixture} \n {stub_mail_fixture['mail']} \n {stub_mail_fixture['mail'].called}")
    # assert stub_mail_fixture['mail'].called, f"Mail not stubed - {stub_mail_fixture['mail']}"
    # assert response.data == ex_response['data']
