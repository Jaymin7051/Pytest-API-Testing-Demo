"""
A file that contains todo pixegami API tests.
"""
import requests
import logging
from constant.framework_constant import FrameworkConstant 
from constant.endpoint_constant import EndpointConstant
from tests.helper.test_helper import HelperClass

logging.basicConfig(level=logging.DEBUG)
Logger = logging.getLogger(__name__)

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
    payload = {
        "content": "My test content.",
        "user_id": "Test User 1",
        "task_id": "task_id 5",
        "is_done": False
    }
    response = HelperClass.create_task(payload)
    response_data = response.json()
    print(response_data)
    task_id =  response_data[FrameworkConstant.TASK][FrameworkConstant.TASK_ID]
    print(task_id)
    
    Logger.info('Creating new task with id: '+task_id)
    status_code = response.status_code
    print(status_code)
    assert payload["content"] == response_data[FrameworkConstant.TASK]["content"]
    assert FrameworkConstant.STATUS_CODE_SUCCESS == status_code


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
    assert FrameworkConstant.STATUS_CODE_SUCCESS == status_code


def test_api_update_task():
    payload = {
        "content": "Updated content",
        "user_id": "Test user updated",
        "task_id": task_id,
        "is_done": True
    }
    Logger.info("Update task with id: "+task_id)
    response = HelperClass.update_task(payload)
    response_data = response.json()
    print(response_data)

    Logger.info("Get task with id: "+task_id+" and validate update task")
    response_updated_task = requests.get(EndpointConstant.ENDPOINT_GET_TASK.format(task_id))
    response_updated_data = response_updated_task.json()
    print(response_updated_data)

    status_code = response.status_code
    print(status_code)
    assert task_id == response_data["updated_task_id"]
    assert response_updated_data["content"] == payload["content"]
    assert FrameworkConstant.STATUS_CODE_SUCCESS == status_code


def test_api_del_task_by_id():
    Logger.info("Delete task with id: "+task_id)
    response = requests.delete(EndpointConstant.ENDPOINT_DELETE_TASK_ID.format(task_id))
    response_data = response.json()
    print(response_data)

    ststus_code = response.status_code
    print(ststus_code)
    assert task_id == response_data["deleted_task_id"]
    assert FrameworkConstant.STATUS_CODE_SUCCESS == ststus_code