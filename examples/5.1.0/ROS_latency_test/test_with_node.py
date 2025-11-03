from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from userExamples.ROS_latency_test.extension_loader import enable_extensions

enable_extensions()

from isaacsim.core.api import World

from userExamples.ROS_latency_test.utils import create_camera, do_step


world = World(
    physics_dt=1.0 / 60,
    rendering_dt=1.0 / 60,
    stage_units_in_meters=1.0
)

world.scene.add_default_ground_plane()

world.reset()

avg_frame_records = {}

# Warm up for stable measurements
avg_frame_time = do_step(world, render=True, steps=600)
avg_frame_records["warm_up"] = avg_frame_time

# Actual measurements
frame_avg = do_step(world, render=True, steps=600)
avg_frame_records["0"] = frame_avg

for i in range(10):
    create_camera(i, world, 1280, 720, use_omnigraph=True)
    frame_avg = do_step(world, render=True, steps=600)
    avg_frame_records[f"{i+1}"] = frame_avg

with open("./userExamples/ROS_latency_test/out/only_node.csv", "w") as f:
    for key, value in avg_frame_records.items():
        f.write(f"{key},{value}\n")

simulation_app.close()
