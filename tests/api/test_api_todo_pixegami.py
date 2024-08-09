"""
A file that contains todo pixegami API test functions.
"""
import pytest
import json
import logging
import requests
import random
from constant.framework_constant import FrameworkConstant 
from constant.endpoint_constant import EndpointConstant
from tests.helper.test_helper import HelperClass

logging.basicConfig(level=logging.DEBUG)
Logger = logging.getLogger(__name__)

json_file = open("./tests/data/payload.json")
json_payload = json.load(json_file) 

"""
Test function to get message from root API endpoint.  
"""
@pytest.mark.smoke
def test_api_get():
    Logger.info('getting response message')
    response = requests.get(EndpointConstant.ENDPOINT)
    response_data = response.json()
    print(response_data)

    status_code = response.status_code
    print(status_code)
    assert FrameworkConstant.STATUS_CODE_SUCCESS == status_code


"""
Test function to crate task.  
"""
@pytest.mark.smoke
def test_api_put_create_task():
    global task_id, invalid_task_id, user_id
    response = HelperClass.create_task(json_payload["create_task_payload"])
    response_data = response.json()
    print(response_data)
    task_id = response_data[FrameworkConstant.TASK][FrameworkConstant.TASK_ID]
    invalid_task_id =  response_data[FrameworkConstant.TASK][FrameworkConstant.TASK_ID] + str(random.randint(1,100))
    user_id = response_data[FrameworkConstant.TASK][FrameworkConstant.USER_ID]
    print(task_id)
    
    Logger.info('Created new task with id: '+task_id)
    status_code = response.status_code
    print(status_code)
    assert json_payload["create_task_payload"]["content"] == response_data[FrameworkConstant.TASK]["content"]
    assert FrameworkConstant.STATUS_CODE_SUCCESS == status_code
    Logger.info("New task created successfully.")


"""
Test function to crate task.  
"""
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
    Logger.info('Task is not created as we have given data with invalid data type.')


"""
Test function to crate task with missing one of required field.  
"""
def test_api_put_create_task_missing_required_field():
    Logger.info("Creating task with missing one of required field.")
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
    Logger.info("Task is not created as one of required field is missing.")


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


"""
Test function to get task by specifying task id.  
"""
@pytest.mark.smoke
def test_api_get_task_by_id():
    print(task_id)
    Logger.info('Get task by task id: '+task_id)
    response = requests.get(EndpointConstant.ENDPOINT_GET_TASK.format(task_id))
    response_data = response.json()
    print(response_data)

    ststus_code = response.status_code
    print(ststus_code)
    assert FrameworkConstant.STATUS_CODE_SUCCESS == ststus_code
    Logger.info("Get task by task id is completed.")


"""
Test function to get task by id which is not exist.  
"""
def test_api_get_task_by_id_not_exist():
    Logger.info('Get task by task id: '+str(invalid_task_id)+" which is not created.")
    response = requests.get(EndpointConstant.ENDPOINT_GET_TASK.format(invalid_task_id))
    response_data = response.json()
    print(response_data)

    ststus_code = response.status_code
    print(ststus_code)
    assert FrameworkConstant.MSG_TASK_NOT_FOUND_WITH_ID.format(invalid_task_id) == response_data["detail"]
    assert FrameworkConstant.STATUS_CODE_NOT_FOUND == ststus_code
    Logger.info("Task with specified id, is not found.")


"""
Test function to get list of tasks associated with specified user id.  
"""
@pytest.mark.smoke
def test_api_get_task_by_user_id():
    Logger.info("Get list of tasks associated with specified user id: "+user_id)
    response = requests.get(EndpointConstant.ENDPOINT_GET_TASKS_USERID.format(user_id))
    response_data = response.json()
    print(response_data)

    status_code = response.status_code
    print(status_code) 
    assert FrameworkConstant.STATUS_CODE_SUCCESS == status_code
    Logger.info("Get list of task with specified user id is completed.")


"""
Test function to update task.  
"""
@pytest.mark.smoke
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

    Logger.info("Get task with id: "+updated_task_id+" and validate if task is updated or not.")
    response_updated_task = requests.get(EndpointConstant.ENDPOINT_GET_TASK.format(updated_task_id))
    response_updated_data = response_updated_task.json()
    print(response_updated_data)
    assert response_updated_data["content"] == json_payload["update_task_payload"]["content"]
    Logger.info("Task is updated with the new parameters.")


"""
Test function to update task with missing one of required field.  
"""
def test_api_update_task_missing_required_field():
    Logger.info("Update task with missing required field 'content'.")
    response = HelperClass.update_task(json_payload["update_task_missing_required_field"])
    response_data = response.json()
    print(response_data)

    Logger.info("Validate task is updated or not as required field is missing.")
    status_code = response.status_code
    print(status_code)
    print(response_data[ "detail"][0]["msg"])
    assert FrameworkConstant.MSG_MISSING_REQUIRED_FIELD == response_data[ "detail"][0]["msg"]
    assert FrameworkConstant.STATUS_CODE_INVALID_DATA == status_code
    Logger.info("Task is not updated as required field is missing.")


@pytest.mark.skip
def test_api_update_task_creation_time():

    Logger.info("Update creation time task with id: "+task_id)
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


"""
Test function to delete task specified by id.  
"""
@pytest.mark.smoke
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
    assert FrameworkConstant.STATUS_CODE_NOT_FOUND == ststus_code
    Logger.info("Task deleted successfully")


"""
Test function to delete task by id which is not exist.  
"""
def test_api_del_task_by_missing_id():
    Logger.info("Delete task without id.")
    response = requests.delete(EndpointConstant.ENDPOINT_DELETE_TASK)
    response_data = response.json()
    print(response_data)

    ststus_code = response.status_code
    print(ststus_code)
    assert FrameworkConstant.STATUS_CODE_NOT_FOUND == ststus_code
    Logger.info("Task not found.")

