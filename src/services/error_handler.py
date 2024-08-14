from functools import wraps

from fastapi import HTTPException

from src.error_messages.messages import ERROR_INVALID_INPUT, ERROR_TYPE_ERROR, ERROR_KEY_ERROR, ERROR_ATTRIBUTE_ERROR, \
    ERROR_SYNTAX_ERROR
from src.exceptions.custom_exceptions import NotFoundException


def handle_errors(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):

        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=ERROR_INVALID_INPUT.format(details=str(e)))
        except TypeError as e:
            raise HTTPException(status_code=400, detail=ERROR_TYPE_ERROR.format(details=str(e)))
        except KeyError as e:
            raise HTTPException(status_code=400, detail=ERROR_KEY_ERROR.format(details=str(e)))
        except AttributeError as e:
            raise HTTPException(status_code=400, detail=ERROR_ATTRIBUTE_ERROR.format(details=str(e)))
        except SyntaxError as e:
            raise HTTPException(status_code=400, detail=ERROR_SYNTAX_ERROR.format(details=str(e)))
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    return wrapper
