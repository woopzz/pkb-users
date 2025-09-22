from pydantic import BaseModel


class BaseError(BaseModel):
    detail: str


_STATUS_CODE_TO_DESCRIPTION = {
    400: 'Client Error',
    401: 'Not authenticated',
    403: 'Invalid token',
    404: 'Not Found',
}


def generate_openapi_error_responses(status_codes: set[int], add_token_related_errors=False):
    if add_token_related_errors:
        status_codes.add(401)
        status_codes.add(403)
    return {
        code: {'model': BaseError, 'description': descr}
        for code, descr in _STATUS_CODE_TO_DESCRIPTION.items()
        if code in status_codes
    }
