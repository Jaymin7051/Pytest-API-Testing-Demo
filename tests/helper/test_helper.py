"""
A file contains helper class which we use in test file. 
"""

import requests
from constant.endpoint_constant import EndpointConstant

class HelperClass:
    """
    A helper class contains the helper function which is used in test files.
    """
    def create_task(payload):
        return requests.put(EndpointConstant.ENDPOINT_CREATE_TASK, json=payload)
    
    
    def update_task(payload):
        return requests.put(EndpointConstant.ENDPOINT_UPDATE_TASK, json=payload)