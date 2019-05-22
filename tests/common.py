"""Common code used by multiple tests"""

def api_gateway_proxy_event():
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
