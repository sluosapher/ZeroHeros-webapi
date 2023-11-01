import json
from collections import deque
import os
from fastapi import FastAPI
import uvicorn

# FILEPATH for queue file
queue_file = "/Users/sluo/development/techspark-webapi/queue.txt"

class QueueManager:
    def __init__(self):
        # Create an empty deque to represent the queue
        self.queue = deque()


        # if queue_file does not exist, create it
        if not os.path.exists(queue_file):
            print(f"Creating queue file: {queue_file}")
            open(queue_file, "w").close()
        else:
            # Read the current queue from the queue file
            with open(queue_file, "r") as f:
                queue_contents = f.read()
            # Split the queue contents into individual JSON strings
            json_data_points = queue_contents.split("\n")
            # Add each JSON string to the deque
            for json_data_point in json_data_points:
                if json_data_point != "":
                    self.queue.append(json_data_point)
    
    # Function to add a data point to the queue
    def add_data_point(self, data_point):
        # Convert the data point to a JSON string
        json_data_point = json.dumps(data_point)
        # Append the JSON string to the deque
        self.queue.append(json_data_point)

        # convert queue to a list of JSON strings
        # json_data_points = list(self.queue)

        # Write the updated deque to the queue file
        with open(queue_file, "w") as f:
            f.write("\n".join(self.queue))
            f.close()

    # Function to pop a data point from the queue
    def pop_data_point(self):
        # Pop a JSON string from the deque
        json_data_point = self.queue.popleft()
        # Convert the JSON string to a data point
        data_point = json.loads(json_data_point)

        # Write the updated queue to the queue file
        with open(queue_file, "w") as f:
            f.write("\n".join(self.queue))

        return data_point

# Create a FastAPI instance
app = FastAPI()

# Create a QueueManager instance
queue_manager = QueueManager()

# Define a GET endpoint to pop a data point from the queue and return it
@app.get("/detections")
async def get_data_point():
    try:
        data_point = queue_manager.pop_data_point()
    except IndexError:
        data_point = {}
    # data_point = queue_manager.pop_data_point()
    return data_point

# Define a POST endpoint to add a data point to the queue
@app.post("/detections")
async def add_data_point(data_point: dict):
    queue_manager.add_data_point(data_point)
    return {"message": "Data point added to queue."}

  

if __name__ == "__main__":
    uvicorn.run("webapi:app", host="0.0.0.0", port=8000, reload=True)