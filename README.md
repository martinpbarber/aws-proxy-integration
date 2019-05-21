# AWS Proxy Integration

A Python package for Lambda proxy integration with AWS API Gateway.

## Overview

AWS API Gateway provides a streamlined integration method between API Gateway and AWS Lambda functions known as proxy integration. When using this integration method no integration request or integration response is configured in API Gateway, instead the incoming request is sent directly to the Lambda function. The function then returns a result to API Gateway using a predetermined format. Please refer to the AWS API Gateway documentation for additional details.

This package provides objects that encapsulate the API Gateway request and response definitions, as well as a basic request routing capability similar to other web frameworks such as Flask, Express and Sinatra.

## Installation

Use pip (or pipenv) to install AWS Proxy Integration.

```
$ pip install aws-proxy-integration
```
