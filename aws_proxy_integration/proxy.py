"""
aws_proxy_integration.proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module processes requests from API Gateway using Lambda proxy integration.
"""
from http import HTTPStatus

class Proxy():
    """API Gateway Lambda proxy integration

    When using proxy interation the API Gateway maps incoming request
    information in the event parameter of the lambda function as follows.
    {
        "resource":
            String containing the resource path
        "path":
            String containing the URI path
        "httpMethod":
            String containing the HTTP method in uppercase
        "headers":
            Dictionary of case sensitive HTTP request headers
        "multiValueHeaders":
            Dictionary of case sensitive multi-value HTTP request headers
        "queryStringParameters":
            Dictionary of case sensitive query string parameters
        "multiValueQueryStringParameters":
            Dictionary of case sensitive multi-value query string parameters
        "pathParameters":
            Dictionary of case sensitive path parameters
        "stageVariables":
            Dictionary of case sensitive API Gateway stage variables
        "requestContext":
            Dictionary of case sensitive Request Context information
        "body":
            JSON string of the request body
        "isBase64Encoded":
            Boolean to indicate if the request body is Base64-encoded
    }

    The Lambda function response must be in the following format.
    {
        "statusCode":
            String containing a valid HTTP status code
        "headers": May be omitted
            Dictionary containing a any API-specific custom headers
        "body": May be empty string
            JSON string of the response body, binary body must be Base64-encoded
        "isBase64Encoded":
            Boolean to indicate if the response body is Base64-encoded
    }
    """

    def __init__(self):
        self.routes = {}

    def route(self, resource):
        """Route Decorator"""
        def decorator(view_function):
            self.routes[resource] = view_function
            return view_function

        return decorator

    def __call__(self, event, context):
        """Process API Gateway event"""
        resource = event.get('resource')
        if resource is None:
            raise ValueError('No resource provided')

        view_function = self.routes.get(resource)
        if view_function is None:
            raise ValueError('Route not registered: %s' % resource)

        response = view_function()
        if isinstance(response, str):
            return Response(response).to_dict()

        return Response('', status_code=500).to_dict()

# pylint: disable=too-few-public-methods
class Response():
    """Proxy Integration response

    The Lambda function response must be in the following format.
    {
        "statusCode":
            String containing a valid HTTP status code
        "headers": May be omitted
            Dictionary containing a any API-specific custom headers
        "body": May be empty string
            JSON string of the response body, binary body must be Base64-encoded
        "isBase64Encoded":
            Boolean to indicate if the response body is Base64-encoded
    }
    """

    def __init__(self, body,
                 status_code=200, headers=None, is_base_64_encoded=False):
        if isinstance(body, str):
            self._body = body
        else:
            raise ValueError('body must be a string')

        if any(status_code == code.value for code in HTTPStatus):
            self._status_code = str(status_code)
        else:
            raise ValueError('status_code must be a valid HTTP status code')

        if headers is None:
            self._headers = {}
        elif isinstance(headers, dict):
            self._headers = headers
        else:
            raise ValueError('headers must be a dictionary')

        if isinstance(is_base_64_encoded, bool):
            self._is_base_64_encoded = is_base_64_encoded
        else:
            raise ValueError('is_base_64_encoded must be a Boolean')

    def to_dict(self):
        """Return Response object as a dictionary"""
        return {
            'body': self._body,
            'statusCode': self._status_code,
            'headers': self._headers,
            'isBase64Encoded': self._is_base_64_encoded,
        }
