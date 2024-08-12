"""
A file that contain constant used in framework
"""

class FrameworkConstant:
    """
    A class contains framework constant.
    """
    """
    Key constant.
    """
    MSG = "msg"
    TASK = "task"
    DETAIL = "detail"
    TASK_ID = "task_id"
    USER_ID = "user_id"
    CONTENT = "content"
    MISSING_REQUIRED_FIELD = "missing_required_field"
    INVALID_DATA_TYPE = "invalid_data_type"
    UPDATED_TASK_ID = "updated_task_id"
    DELETED_TASK_ID = "deleted_task_id"
    CREATE_TASK_PAYLOAD = "create_task_payload"
    UPDATE_TASK_PAYLOAD = "update_task_payload"
    UPDATE_TASK_MISSING_REQUIRED_FIELD = "update_task_missing_required_field"
    
    """
    Server response status code.
    """
    STATUS_CODE_SUCCESS = 200
    STATUS_CODE_NOT_FOUND = 404
    STATUS_CODE_INVALID_DATA = 422
    STATUS_CODE_INTERNAL_ERROR = 500

    """
    Server response message.
    """
    MSG_INVALID_DATA_TYPE = "value could not be parsed to a boolean"
    MSG_TASK_NOT_FOUND_WITH_ID = "Task {} not found"
    MSG_MISSING_REQUIRED_FIELD = "field required"
    

    """
    Maximum response time for API endpoints.
    """
    MAX_RESPONSE_TIME_GET_TASK = 2.0
    MAX_RESPONSE_TIME_CREATE_TASK = 1.9
    MAX_RESPONSE_TIME_UPDATE_TASK = 1.5
    MAX_RESPONSE_TIME_DELETE_TASK = 1.4
    MAX_RESPONSE_TIME_CREATE_TASK_NEGATIVE = 1.0 
   
    
    
    

