"""Test for aws_proxy_integration.proxy.Response class"""
import pytest
from aws_proxy_integration.proxy import Request

def api_gateway_proxy_event():
    """Return the event"""
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

################################################################################
# Tests for Request class
################################################################################
def test_request_init():
    """Request creation"""
    event = api_gateway_proxy_event()
    request = Request(event)
    assert request
    assert request.resource == event['resource']
    assert request.path == event['path']
    assert request.http_method == event['httpMethod']
    assert request.headers == event['headers']
    assert request.multivalue_headers == event['multiValueHeaders']
    assert request.query_string_parameters == event['queryStringParameters']
    assert request.multivalue_query_string_parameters == event['multiValueQueryStringParameters']
    assert request.path_parameters == event['pathParameters']
    assert request.stage_variables == event['stageVariables']
    assert request.request_context == event['requestContext']
    assert request.body == event['body']
    assert request.is_base64_encoded == event['isBase64Encoded']

@pytest.mark.parametrize(
    "key", [
        'resource',
        'path',
        'httpMethod',
        'headers',
        'multiValueHeaders',
        'queryStringParameters',
        'multiValueQueryStringParameters',
        'pathParameters',
        'stageVariables',
        'requestContext',
        'body',
        'isBase64Encoded',
    ]
)
def test_request_missing_event_key(key):
    """Request with invalid event (missing key)"""
    event = api_gateway_proxy_event()
    del event[key]
    with pytest.raises(KeyError) as exception_info:
        Request(event)
    assert str(exception_info.value) == f"'{key}'"
