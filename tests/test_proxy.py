"""Tests for the aws_proxy_integration.proxy module"""
from http import HTTPStatus
import pytest
from aws_proxy_integration.proxy import Proxy

# The following prevents pylint error when using fixtures
# pylint: disable=redefined-outer-name
################################################################################
# Test Fixtures
################################################################################
@pytest.fixture
def event():
    """Return an empty API Gateway proxy event"""
    return {
        "resource": "",
        "path": "",
        "httpMethod": "",
        "headers": {},
        "multiValueHeaders": {},
        "queryStringParameters": {},
        "multiValueQueryStringParameters": {},
        "pathParameters": {},
        "stageVariables": {},
        "requestContext": {},
        "body": "",
        "isBase64Encoded": False,
    }

@pytest.fixture
def context():
    """Return an empty Lambda context"""
    return {}

@pytest.fixture
def proxy():
    """Create a Proxy object"""
    return Proxy()

@pytest.fixture
def proxy_with_index_route(proxy):
    """Add an index route to Proxy"""
    @proxy.route('/')
    def index():    # pylint: disable=unused-variable
        return ''
    return proxy

################################################################################
# Tests for Proxy class
################################################################################
def test_proxy_init(proxy):
    """Proxy creation"""
    assert proxy

def test_proxy_add_route(event, context, proxy_with_index_route):
    """Add a route to Proxy"""
    event['resource'] = '/'
    response = proxy_with_index_route(event, context)

    assert is_proxy_integration_response(response)
    assert response['statusCode'] == HTTPStatus.OK

def test_proxy_route_not_registered(event, context, proxy_with_index_route):
    """Provided route not registered with Proxy"""
    event['resource'] = '/wrong'
    with pytest.raises(ValueError) as exception_info:
        proxy_with_index_route(event, context)
    assert str(exception_info.value) == 'Route not registered: /wrong'

def test_proxy_no_return(event, context, proxy):
    """Add a route to Proxy"""
    @proxy.route('/')
    def index():    # pylint: disable=unused-variable
        pass

    event['resource'] = '/'
    response = proxy(event, context)

    assert is_proxy_integration_response(response)
    assert response['statusCode'] == HTTPStatus.INTERNAL_SERVER_ERROR


def is_proxy_integration_response(response):
    """Determine if the Proxy response is in the proper format"""
    return (
        isinstance(response, dict) and
        isinstance(response['statusCode'], int) and
        isinstance(response['headers'], dict) and
        isinstance(response['body'], str) and
        isinstance(response['isBase64Encoded'], bool)
    )
