"""Tests for the aws_proxy_integration.proxy module"""

import pytest
from aws_proxy_integration.proxy import Proxy

def test_proxy_init():
    """Proxy creation"""
    proxy = Proxy()
    assert proxy

def test_proxy_add_route():
    """Add a route to Proxy"""
    proxy = Proxy()
    @proxy.route('/')
    def index():    # pylint: disable=unused-variable
        pass

    event = {'resource': '/'}
    context = {}
    proxy(event, context)

def test_proxy_no_route_provided():
    """No route provided to Proxy"""
    proxy = Proxy()
    @proxy.route('/')
    def index():    # pylint: disable=unused-variable
        pass

    event = {}
    context = {}
    with pytest.raises(ValueError) as exception_info:
        proxy(event, context)
    assert str(exception_info.value) == 'No resource provided'

def test_proxy_route_not_registered():
    """Provided route not registered with Proxy"""
    proxy = Proxy()
    @proxy.route('/')
    def index():    # pylint: disable=unused-variable
        pass

    event = {'resource': '/wrong'}
    context = {}
    with pytest.raises(ValueError) as exception_info:
        proxy(event, context)
    assert str(exception_info.value) == 'Route not registered: /wrong'
