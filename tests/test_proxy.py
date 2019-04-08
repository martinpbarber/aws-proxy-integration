"""Tests for the aws_proxy_integration.proxy module"""

import pytest
from aws_proxy_integration.proxy import Proxy

# The following prevents pylint error when using fixtures
# pylint: disable=redefined-outer-name

################################################################################
# Test Fixtures
################################################################################
@pytest.fixture
def proxy():
    """Create a Proxy object"""
    return Proxy()

@pytest.fixture
def proxy_with_index_route(proxy):
    """Add an index route to Proxy"""
    @proxy.route('/')
    def index():    # pylint: disable=unused-variable
        pass
    return proxy

################################################################################
# Tests for Proxy class
################################################################################
def test_proxy_init(proxy):
    """Proxy creation"""
    assert proxy

def test_proxy_add_route(proxy_with_index_route):
    """Add a route to Proxy"""
    event = {'resource': '/'}
    context = {}
    proxy_with_index_route(event, context)

def test_proxy_no_route_provided(proxy_with_index_route):
    """No route provided to Proxy in event"""
    event = {}
    context = {}
    with pytest.raises(ValueError) as exception_info:
        proxy_with_index_route(event, context)
    assert str(exception_info.value) == 'No resource provided'

def test_proxy_route_not_registered(proxy_with_index_route):
    """Provided route not registered with Proxy"""
    event = {'resource': '/wrong'}
    context = {}
    with pytest.raises(ValueError) as exception_info:
        proxy_with_index_route(event, context)
    assert str(exception_info.value) == 'Route not registered: /wrong'
