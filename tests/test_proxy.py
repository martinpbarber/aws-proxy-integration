import pytest
from aws_proxy_integration.proxy import Proxy

def test_proxy_init():
    proxy = Proxy()
    assert proxy

def test_proxy_add_route():
    proxy = Proxy()
    @proxy.route('/')
    def index():
        pass

    event = {'resource': '/'}
    context = {}
    proxy(event, context)

def test_proxy_no_route_provided():
    proxy = Proxy()
    @proxy.route('/')
    def index():
        pass

    event = {}
    context = {}
    with pytest.raises(ValueError) as exception_info:
        proxy(event, context)
    assert str(exception_info.value) == 'No resource provided'

def test_proxy_route_not_registered():
    proxy = Proxy()
    @proxy.route('/')
    def index():
        pass

    event = {'resource': '/wrong'}
    context = {}
    with pytest.raises(ValueError) as exception_info:
        proxy(event, context)
    assert str(exception_info.value) == 'Route not registered: /wrong'
