import os
import pytest
import logging
from unittest import mock

LOGGER = logging.getLogger(__name__)

@pytest.fixture
def mocker():
    return mock.Mock()

# @pytest.fixture
# def stub_mail_fixture(mocker, stub_data):
#     stubed_data = {}
#     for key, val  in stub_data.items():
#         stubed_data[key] = mocker.patch(val['path'])
#         stubed_data[key].return_value = val['response']

#     return stubed_data