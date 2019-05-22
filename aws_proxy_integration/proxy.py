"""
aws_proxy_integration.proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module processes requests from API Gateway using Lambda proxy integration.
"""
import logging
from http import HTTPStatus

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

class Proxy():
    """API Gateway Lambda proxy integration"""
    def __init__(self):
        self._logger = LOGGER
        self._router = Router()
        self._request = None

    def route(self, path):
        """Route Decorator"""
        def decorator(view_function):
            self._router.add_route(path, view_function)
            return view_function
        return decorator

    def __call__(self, event, context):
        """Process API Gateway event"""
        self._request = Request(event)
        response = self._router.route(self._request)
        return response

    @property
    def logger(self):
        """Logger property"""
        return self._logger

    @property
    def request(self):
        """Request property"""
        return self._request


class Router():
    """Register and process routes"""
    def __init__(self):
        self.routes = {}

    def add_route(self, path, function):
        """Add a route"""
        self.routes[path] = function

    def route(self, request):
        """Route a request to the associated function"""
        function = self._get_function(request)

        response = function()
        if isinstance(response, str):
            return Response(response).to_dict()
        return Response('', status_code=HTTPStatus.INTERNAL_SERVER_ERROR).to_dict()

    def _get_function(self, request):
        """Get the function associated with a request"""
        function = self.routes.get(request.path)
        if function is None:
            raise ValueError('Route not registered: %s' % request.path)
        return function


# pylint: disable=too-many-instance-attributes
class Request():
    """Proxy Integration request

    When using proxy interation the API Gateway maps incoming request
    information in the event parameter of the lambda function as follows.
        resource:
            String containing the resource path
        path:
            String containing the URI path
        httpMethod:
            String containing the HTTP method in uppercase
        headers:
            Dictionary of case sensitive HTTP request headers
        multiValueHeaders:
            Dictionary of case sensitive multi-value HTTP request headers
        queryStringParameters:
            Dictionary of case sensitive query string parameters
        multiValueQueryStringParameters:
            Dictionary of case sensitive multi-value query string parameters
        pathParameters:
            Dictionary of case sensitive path parameters
        stageVariables:
            Dictionary of case sensitive API Gateway stage variables
        requestContext:
            Dictionary of case sensitive Request Context information
        body:
            JSON string of the request body
        isBase64Encoded:
            Boolean to indicate if the request body is Base64-encoded
    """
    def __init__(self, event):
        self._resource = event['resource']
        self._path = event['path']
        self._http_method = event['httpMethod']
        self._headers = event['headers']
        self._multivalue_headers = event['multiValueHeaders']
        self._query_string_parameters = event['queryStringParameters']
        self._multivalue_query_string_parameters = event['multiValueQueryStringParameters']
        self._path_parameters = event['pathParameters']
        self._stage_variables = event['stageVariables']
        self._request_context = event['requestContext']
        self._body = event['body']
        self._is_base64_encoded = event['isBase64Encoded']

    @property
    def resource(self):
        """Resource property"""
        return self._resource

    @property
    def path(self):
        """Path property"""
        return self._path

    @property
    def http_method(self):
        """HTTP Method property"""
        return self._http_method

    @property
    def headers(self):
        """Headers property"""
        return self._headers

    @property
    def multivalue_headers(self):
        """Multivalue Headers property"""
        return self._multivalue_headers

    @property
    def query_string_parameters(self):
        """Query String Parameters property"""
        return self._query_string_parameters

    @property
    def multivalue_query_string_parameters(self):
        """Multivalue Query String Parameters property"""
        return self._multivalue_query_string_parameters

    @property
    def path_parameters(self):
        """Path Parameters property"""
        return self._path_parameters

    @property
    def stage_variables(self):
        """Stage Variables property"""
        return self._stage_variables

    @property
    def request_context(self):
        """Request Context property"""
        return self._request_context

    @property
    def body(self):
        """Body property"""
        return self._body

    @property
    def is_base64_encoded(self):
        """Base64 Encoding property"""
        return self._is_base64_encoded


# pylint: disable=too-few-public-methods
class Response():
    """Proxy Integration response

    The Lambda function response must be a Python dictionary with the following keys.
        statusCode:
            String containing a valid HTTP status code
        headers: May be omitted
            Dictionary containing a any API-specific custom headers
        body: May be empty string
            JSON string of the response body, binary body must be Base64-encoded
        isBase64Encoded:
            Boolean to indicate if the response body is Base64-encoded
    """

    def __init__(self, body,
                 status_code=200, headers=None, is_base_64_encoded=False):
        if isinstance(body, str):
            self._body = body
        else:
            raise ValueError('body must be a string')

        if any(status_code == code.value for code in HTTPStatus):
            self._status_code = str(status_code)
            self._status_code = status_code
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
