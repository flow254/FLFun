# Practical 1: Ring Computation Walkthrough: Calculating an Average Across Nodes on SyftBox

Hello everyone,

Thank you for taking the time to walk through this practical. We will be exploring how to do a ring computation, specifically an average, across nodes on SyftBox.

_Ring Computation_: A sample application that performs computations in a ring, starting and ending at the first node.

Prerequisites:

We assume you have SyftBox already installed. If not, please install it using the steps highlighted in the [SyftBox documentation](https://syftbox-documentation.openmined.org/#install-syftbox).

Recommended:

_Ring Fundamentals in depth:_ Andrej Jovanović has created [a tutorial](https://syftbox.openmined.org/datasites/andrej@jovanovic.co.za/tutorial/create_your_ring.html) that covers how Ring works with SyftBox under the hood. Going through it will help understand how Ring computations work and how SyftBox orchestrates them. The code snippets are a great way to walk through what SyftBox is doing under the hood.

Since the tutorial was published, Ring’s code has gone through some changes, particularly in the `main.py` file which will be fundamental for this tutorial. Please see the updated, live version of the Ring code on SyftBox [here](https://github.com/OpenMined/ring/blob/main/main.py).

For this practical, we will be modifying Ring’s current code in `main.py` which computes the sum of the node’s secret values to calculate the average from the nodes. Here is the modified code snippet for `main.py`

```
import os, sys
from pathlib import Path
from syftbox.lib import Client
from utils import load_json, write_json, setup_folders
from typing import List

def load_ring_data(file_path: Path):
    ring_data = load_json(file_path)
    return ring_data["participants"], ring_data["data"], ring_data["current_index"]

def create_ring_data(participants: List[str], data: int, current_index: int):
    return {"participants": participants, "data": data, "current_index": current_index}

client = Client.load()
my_email: str = client.email

RING_APP_PATH = Path(os.path.abspath(__file__)).parent
RING_PIPELINE_FOLDER = client.api_data("ring")
RUNNING_FOLDER = RING_PIPELINE_FOLDER / "running"
DONE_FOLDER = RING_PIPELINE_FOLDER / "done"
SECRET_FILE = RING_APP_PATH / "secret.json"
DATA_TEMPLATE_FILE = RING_APP_PATH / "data.json"

my_secret = load_json(SECRET_FILE)["data"]
setup_folders(RUNNING_FOLDER, DONE_FOLDER, RING_PIPELINE_FOLDER, DATA_TEMPLATE_FILE, my_email)
pending_inputs_files = [RUNNING_FOLDER / file for file in RUNNING_FOLDER.glob("*.json")]

if len(pending_inputs_files) == 0:
    print("No data file found. As you were, soldier.")
    sys.exit(0)

file_path = pending_inputs_files[0]
print(f"Found input {file_path}! Let's get to work.")

try:
    ring_participants, data, current_index = load_ring_data(file_path)
except Exception:
    print("It seems something is not set. Skipping it for now")
    exit()
data += my_secret
next_index = current_index + 1

if next_index < len(ring_participants):
    next_person = ring_participants[next_index]
    new_ring_data = create_ring_data(ring_participants, data, next_index)
    receiver_ring_data = client.api_data("ring", datasite=next_person) / "running" / "data.json"
    write_json(receiver_ring_data, new_ring_data)
else:
    print(f"Terminating ring, writing back to {DONE_FOLDER}"
    #modify last data entry to be average of whole group
    data = data / len(ring_participants)
    final_ring_data = create_ring_data(ring_participants, data, current_index)
    write_json(DONE_FOLDER / "data.json", final_ring_data)

file_path.unlink()
print(f"Done processing {file_path}, removed from pending inputs")
```

#### _What happens in a nutshell:_

- Ring first loads the data of participants in the ring computation.
- It then creates an object of the ring data, used when performing the desired computation and iterating through the ring participants.
- Ring sets up the necessary file and folder structure to run the computations, then checks if there are any pending input files in the Running folder.
- If there are any pending input files, they are computed using the defined computation. In this case, the ring first computes the sum of all secrets across the ring participants. It starts with the leader of the ring _(current_index = 0)_, then passes on the computed sum to the next ring participant at _next_index_.
- Once all participants have completed the computation, the data returns to the first ring participant, that then computes the average.
- The average is then written to all participants, completing the computation.

![](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTgycm1uYXpzN205dmQ4aWg3MWozczB4bmE1Z2k0ZGU3MHYzbHV4aSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/zMrgi3bj97yKn44Z5a/giphy.gif)

Thanks for walking through this!
