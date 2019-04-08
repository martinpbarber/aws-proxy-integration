"""
aws_proxy_integration.proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module processes requests from API Gateway using Lambda proxy integration.
"""

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

        return view_function()
