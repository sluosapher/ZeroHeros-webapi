import json
from fastapi.testclient import TestClient
from webapi import app
from webapi import QueueManager


client = TestClient(app)

def test_add_data_point(id:int):
    data_point = {
        "detection id": id,
        "agent id": "abc123",
        "summary": "Test summary",
        "recommended action": {
            "action": "block",
            "user name": "testuser",
            "resource name": "testresource"
        },
        "command history": {
            "sequence no": 1,
            "command line": "test command"
        }
    }
    response = client.post("/detections", json=data_point)
    print(f"test_add_data_point: {response.json()}")
    assert response.status_code == 200
    assert response.json() == {"message": "Data point added to queue."}

def test_get_data_point():
    response = client.get("/detections")
    assert response.status_code == 200
    data_point = json.loads(response.content)
    print(f"test_get_data_point: {data_point}")
    assert "agent id" in data_point
    assert "summary" in data_point
    assert "recommended action" in data_point
    assert "command history" in data_point

# Create a test client for the FastAPI instance
# client = TestClient(app)

# def test_add_and_pop_data_point():
#     queue_manager = QueueManager()
#     # Add the test data point to the queue
#     queue_manager.add_data_point(test_data_point)
#     queue_manager.add_data_point(test_data_point)
#     # print(f"input test data: {test_data_point}")
#     # # Pop the data point from the queue
#     # popped_data_point = pop_data_point()
#     # print(f"output test data: {popped_data_point}")

# # a test function to add data to the queue
# # def test_add_data_point():
# #     # Add the test data point to the queue
# #     add_data_point(test_data_point)


if __name__ == "__main__":
    # test_add_data_point(1)
    # test_add_data_point(2)
    # test_add_data_point(3)
    test_get_data_point()