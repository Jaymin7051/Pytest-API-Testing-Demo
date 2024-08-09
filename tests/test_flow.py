import json
import logging
import requests
from tests.helper.test_helper import HelperClass
from constant.framework_constant import FrameworkConstant
from constant.endpoint_constant import EndpointConstant

logging.basicConfig(level=logging.DEBUG)
Logger = logging.getLogger(__name__)

json_file = open("./tests/data/flow_payload.json")
json_payload = json.load(json_file)

"""
A test fucntion that contain CRUD flow for the API endpoints.
"""
def test_api_task_flow():
    Logger.info("Creating task.")
    response = HelperClass.create_task(json_payload["create_task_payload"])
    response_data = response.json()
    print(response_data)
    response_time = response.elapsed.total_seconds()
    print(response_time)
    assert response_time <= FrameworkConstant.MAX_RESPONSE_TIME_CREATE_TASK

    task_id = response_data[FrameworkConstant.TASK][FrameworkConstant.TASK_ID]
    print(response.status_code)
    assert FrameworkConstant.STATUS_CODE_SUCCESS == response.status_code 
    Logger.info("Task created successfully.")
    
    Logger.info("Updating task.")
    json_payload["update_task_payload"]["task_id"] = task_id
    response = HelperClass.update_task(json_payload["update_task_payload"])
    response_data = response.json()
    print(response_data)
    response_time = response.elapsed.total_seconds()
    print(response_time)
    assert response_time <= FrameworkConstant.MAX_RESPONSE_TIME_UPDATE_TASK

    status_code = response.status_code
    print(status_code)
    assert FrameworkConstant.STATUS_CODE_SUCCESS == status_code
    Logger.info("Task updated successfully.")

    Logger.info("Deleting task.")
    response = requests.delete(EndpointConstant.ENDPOINT_DELETE_TASK_ID.format(task_id))
    response_data = response.json()
    print(response_data)
    response_time = response.elapsed.total_seconds()
    print(response_time)
    assert response_time <= FrameworkConstant.MAX_RESPONSE_TIME_DELETE_TASK

    ststus_code = response.status_code
    print(ststus_code)
    assert task_id == response_data["deleted_task_id"]
    assert FrameworkConstant.STATUS_CODE_SUCCESS == ststus_code
    Logger.info("Task deleted successfully.")

    Logger.info("Validating whether task is deleted or not.")
    response_deleted_task = requests.get(EndpointConstant.ENDPOINT_GET_TASK.format(task_id))
    response_deleted_data = response_deleted_task.json()
    print(response_deleted_data)
    response_time = response_deleted_task.elapsed.total_seconds()
    print(response_time)
    assert response_time <= FrameworkConstant.MAX_RESPONSE_TIME_GET_TASK
    
    ststus_code = response_deleted_task.status_code
    print(ststus_code)
    assert FrameworkConstant.STATUS_CODE_NOT_FOUND == ststus_code
    Logger.info("Task deleted and not found.")

    