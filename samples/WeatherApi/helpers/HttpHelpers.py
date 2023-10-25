def isNotPositiveResponse(statusCode):
    return statusCode < 200 or statusCode > 300


def __getValue(valueType, fieldName, collection) -> (object, str):
    try:
        return valueType(collection[fieldName]), None
    except ValueError:
        return None, f'Invalid value for "{fieldName}"'
    except KeyError:
        return None, f'Missing "{fieldName}"'


def getParameterValue(valueType, parameterName, request) -> (object, str):
    return __getValue(valueType, parameterName, request.args)


def getBodyFieldValue(valueType, fieldName, request) -> (object, str):
    return __getValue(valueType, fieldName, request.form)


def getHeaderValue(valueType, headerName, request) -> (object, str):
    return __getValue(valueType, headerName, request.headers)


def getJsonValue(valueType, fieldName, request) -> (object, str):
    return __getValue(valueType, fieldName, request.json)
