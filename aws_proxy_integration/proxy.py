"""
aws_proxy_integration.proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module processes requests from API Gateway using Lambda proxy integration.
"""

class Proxy():
    """API Gateway Lambda proxy integration"""

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
