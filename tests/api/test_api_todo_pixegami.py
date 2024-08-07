"""
A file that contains todo pixegami API test functions.
"""
import pytest
import json
import logging
import requests
from constant.framework_constant import FrameworkConstant 
from constant.endpoint_constant import EndpointConstant
from tests.helper.test_helper import HelperClass

logging.basicConfig(level=logging.DEBUG)
Logger = logging.getLogger(__name__)

json_file = open("./tests/data/payload.json")
json_payload = json.load(json_file) 

global task_id

def test_api_get():
    Logger.info('getting response message')
    response = requests.get(EndpointConstant.ENDPOINT)
    response_data = response.json()
    print(response_data)

    status_code = response.status_code
    print(status_code)
    assert FrameworkConstant.STATUS_CODE_SUCCESS == status_code


def test_api_put_create_task():
    global task_id
  
    response = HelperClass.create_task(json_payload["create_task_payload"])
    response_data = response.json()
    print(response_data)
    task_id =  response_data[FrameworkConstant.TASK][FrameworkConstant.TASK_ID]
    print(task_id)
    
    Logger.info('Created new task with id: '+task_id)
    status_code = response.status_code
    print(status_code)
    assert json_payload["create_task_payload"]["content"] == response_data[FrameworkConstant.TASK]["content"]
    assert FrameworkConstant.STATUS_CODE_SUCCESS == status_code


def test_api_put_create_task_invalid_data_type():

    Logger.info('Creating task with invalid data type.')
    response = HelperClass.create_task(json_payload["invalid_data_type"])
    print(response)
    response_data = response.json()
    print(response_data)
    
    status_code = response.status_code
    response_msg = response_data["detail"][0]["msg"]
    print(response_msg)
    print(status_code)
    assert FrameworkConstant.MSG_INVALID_DATA_TYPE == response_msg
    assert FrameworkConstant.STATUS_CODE_INVALID_DATA == status_code


def test_api_put_create_task_missing_required_field():
   
    Logger.info('Creating task with missing one of required field.')
    response = HelperClass.create_task(json_payload["missing_required_field"])
    print(response)
    response_data = response.json()
    print(response_data)
    
    status_code = response.status_code
    response_msg = response_data["detail"][0]["msg"]
    print(response_msg)
    print(status_code)
    assert FrameworkConstant.MSG_MISSING_REQUIRED_FIELD == response_msg
    assert FrameworkConstant.STATUS_CODE_INVALID_DATA == status_code


@pytest.mark.skip
def test_api_put_create_task_invalid_creationtime():
    global task_id
    payload = {
        "content": "My test content.",
        "user_id": "Test User 1",
        "task_id": "task_id 5",
        "is_done": False,
        "created_time": 7-8-2024
    }
    response = HelperClass.create_task(payload)
    print(response)
    response_data = response.json()
    print(response_data)
    
    Logger.info('Creating task with missing one of required field.')
    status_code = response.status_code
    response_msg = response_data["detail"][0]["msg"]
    print(response_msg)
    print(status_code)
    assert FrameworkConstant.MSG_MISSING_REQUIRED_FIELD == response_msg
    assert FrameworkConstant.STATUS_CODE_INVALID_DATA == status_code


def test_api_get_task_by_id():
    print(task_id)
    Logger.info('Get task by task id: '+task_id)
    response = requests.get(EndpointConstant.ENDPOINT_GET_TASK.format(task_id))
    response_data = response.json()
    print(response_data)

    ststus_code = response.status_code
    print(ststus_code)
    assert FrameworkConstant.STATUS_CODE_SUCCESS == ststus_code


def test_api_get_task_by_user_id():
    user_id = "Test User 1"
    Logger.info("Get task by user id: "+user_id)
    response = requests.get(EndpointConstant.ENDPOINT_GET_TASKS_USERID.format(user_id))
    response_data = response.json()
    print(response_data)

    status_code = response.status_code
    print(status_code) 
    assert FrameworkConstant.STATUS_CODE_SUCCESS == 300


def test_api_update_task():

    Logger.info("Update task with id: "+task_id)
    response = HelperClass.update_task(json_payload["update_task_payload"])
    response_data = response.json()
    print(response_data)

    status_code = response.status_code
    print(status_code)
    updated_task_id = response_data["updated_task_id"]
    assert json_payload["update_task_payload"]["task_id"] == updated_task_id
    assert FrameworkConstant.STATUS_CODE_SUCCESS == status_code

    Logger.info("Get task with id: "+updated_task_id+" and validate update task")
    response_updated_task = requests.get(EndpointConstant.ENDPOINT_GET_TASK.format(updated_task_id))
    response_updated_data = response_updated_task.json()
    print(response_updated_data)
    assert response_updated_data["content"] == json_payload["update_task_payload"]["content"]


def test_api_del_task_by_id():
    Logger.info("Delete task with id: "+task_id)
    response = requests.delete(EndpointConstant.ENDPOINT_DELETE_TASK_ID.format(task_id))
    response_data = response.json()
    print(response_data)

    ststus_code = response.status_code
    print(ststus_code)
    assert task_id == response_data["deleted_task_id"]
    assert FrameworkConstant.STATUS_CODE_SUCCESS == ststus_code

    Logger.info("Validate task is deleted or not.")
    response_deleted_task = requests.get(EndpointConstant.ENDPOINT_GET_TASK.format(task_id))
    response_deleted_data = response_deleted_task.json()
    print(response_deleted_data)
    
    ststus_code = response_deleted_task.status_code
    print(ststus_code)
    assert FrameworkConstant.STATUS_CODE_SUCCESS != ststus_code

