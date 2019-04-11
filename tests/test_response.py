"""Tests for the aws_proxy_integration.proxy.Response class"""

import pytest
from aws_proxy_integration.proxy import Response

################################################################################
# Tests for Response class
################################################################################
def test_response_init():
    """Response creation"""
    response = Response('')
    assert response

def test_response_parameters():
    """Response creation"""
    response = Response('', status_code=200, headers={}, is_base_64_encoded=False)
    assert response

def test_response_invalid_body():
    """Invalid body"""
    with pytest.raises(ValueError) as exception_info:
        Response({})
    assert str(exception_info.value) == 'body must be a string'

def test_response_invalid_status():
    """Invalid status_code"""
    with pytest.raises(ValueError) as exception_info:
        Response('', status_code=600)
    assert str(exception_info.value) == 'status_code must be a valid HTTP status code'

def test_response_invalid_headers():
    """Invalid headers"""
    with pytest.raises(ValueError) as exception_info:
        Response('', headers=[])
    assert str(exception_info.value) == 'headers must be a dictionary'

def test_response_invalid_base64_encoded():
    """Invalid headers"""
    with pytest.raises(ValueError) as exception_info:
        Response('', is_base_64_encoded='true')
    assert str(exception_info.value) == 'is_base_64_encoded must be a Boolean'
