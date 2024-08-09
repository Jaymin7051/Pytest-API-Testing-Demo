"""
A file that contain constant used in framework
"""

class FrameworkConstant:
    """
    A class contains framework constant.
    """ 
    TASK = "task"
    TASK_ID = "task_id"
    USER_ID = "user_id"
    STATUS_CODE_SUCCESS = 200
    STATUS_CODE_NOT_FOUND = 404
    STATUS_CODE_INVALID_DATA = 422
    STATUS_CODE_INTERNAL_ERROR = 500
    MSG_INVALID_DATA_TYPE = "value could not be parsed to a boolean"
    MSG_MISSING_REQUIRED_FIELD = "field required"
    MSG_TASK_NOT_FOUND_WITH_ID = "Task {} not found"
    MAX_RESPONSE_TIME_CREATE_TASK = 1.9
    MAX_RESPONSE_TIME_UPDATE_TASK = 1.0
    MAX_RESPONSE_TIME_DELETE_TASK = 1.2
    MAX_RESPONSE_TIME_GET_TASK = 1

