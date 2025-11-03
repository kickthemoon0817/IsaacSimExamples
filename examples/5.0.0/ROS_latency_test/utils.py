import time

import omni
import omni.kit.app
import omni.graph.core as og
import omni.replicator.core as rep

from isaacsim.core.api import World
from isaacsim.sensors.camera import Camera


# ROS2 imports
try:
    import rclpy
    from sensor_msgs.msg import Image
    ROS2_AVAILABLE = True
except ImportError:
    ROS2_AVAILABLE = False
    print("WARNING: ROS2 not available. Test will be limited.")

# Global ROS 2 state
_ros2_node_initialized = False
_ros2_node = None


def do_step(world_instance: World, render=True, steps=150):
    frame_count = 0

    start_time = time.time()
    for _ in range(steps):
        world_instance.step(render=render)
        frame_count += 1
    end_time = time.time()

    fps = frame_count / (end_time - start_time)

    return fps


def create_camera(
    idx,
    world_instance: World,
    width,
    height,
    use_omnigraph=False,
    use_python=False,
):
    try:
        camera = _create_camera(idx, width, height)
        if use_omnigraph:
            _create_publisher_ogn(idx, camera.prim_path, width, height)
        if use_python:
            _create_publisher_py(idx, camera, world_instance, width, height)
        return camera
    except Exception as e:
        print(f"Failed to create camera: {e}")
        return None


def _create_camera(idx, width, height):
    try:
        camera_prim_path = f"/World/Camera_{idx}"
        camera = Camera(camera_prim_path)
        camera.initialize()
        camera.set_resolution((width, height))
        return camera
    except Exception as e:
        print(f"Failed to create camera: {e}")
        return None


def _create_publisher_ogn(idx, camera_prim_path, width, height):
    # Create omnigraph with ROS1CameraHelper
    graph_path = f"/World/Camera_{idx}_Graph"
    (ros_camera_graph, _, _, _) = og.Controller.edit(
        {"graph_path": graph_path, "evaluator_name": "execution"},
        {
            og.Controller.Keys.CREATE_NODES: [
                ("OnTick", "omni.graph.action.OnPlaybackTick"),
                ("CreateRenderProduct", "isaacsim.core.nodes.IsaacCreateRenderProduct"),
                ("cameraHelper", "isaacsim.ros2.bridge.ROS2CameraHelper"),
            ],
            og.Controller.Keys.CONNECT: [
                ("OnTick.outputs:tick", "CreateRenderProduct.inputs:execIn"),
                ("CreateRenderProduct.outputs:execOut", "cameraHelper.inputs:execIn"),
                ("CreateRenderProduct.outputs:renderProductPath", "cameraHelper.inputs:renderProductPath"),
            ],
            og.Controller.Keys.SET_VALUES: [
                ("CreateRenderProduct.inputs:cameraPrim", [camera_prim_path]),
                ("CreateRenderProduct.inputs:height", height),
                ("CreateRenderProduct.inputs:width", width),
                ("cameraHelper.inputs:frameId", f"camera_{idx}"),
                ("cameraHelper.inputs:topicName", f"camera_{idx}/image_raw"),
                ("cameraHelper.inputs:type", "rgb"),
            ],
        },
    )

    return ros_camera_graph


def _create_publisher_py(
    idx,
    camera_instance: Camera,
    world_instance: World,
    width,
    height,
    *,
    publish_every_n: int = 1,  # decimate if needed: 1 = every frame
):
    # Create ROS 2 publisher
    if not ROS2_AVAILABLE:
        return None

    global _ros2_node_initialized, _ros2_node

    if not _ros2_node_initialized:
        rclpy.init(args=None)
        _ros2_node = rclpy.create_node("isaac_sim_camera_publisher")
        _ros2_node_initialized = True

    pub = _ros2_node.create_publisher(Image, f"camera_{idx}/image_raw", 10)

    # Reusable message object (avoid re-allocating each frame)
    msg = Image()
    msg.header.frame_id = f"camera_{idx}"
    msg.height = height
    msg.width = width
    msg.encoding = "rgb8"            # publish RGB8
    msg.is_bigendian = 0
    msg.step = width * 3

    # replicator
    render_product = rep.create.render_product(camera_instance.prim_path, (width, height))
    rgb_annotator = rep.annotators.get("LdrColor", device="cuda").augment("RgbaToRgb")
    rgb_annotator.attach(render_product)

    # Per-camera frame counter for decimation
    frame_counter = {"n": 0}

    def __publish_camera_image_py(_event):
        # Decimate if requested
        frame_counter["n"] += 1
        if frame_counter["n"] % publish_every_n != 0:
            return

        # current_frame = camera_instance.get_current_frame()
        # rgba = current_frame.get("rgba", None)
        # if rgba is None:
        #     return

        # # Ensure dtype and contiguity (avoid copies unless needed)
        # # Expected shape: (H, W, 4), dtype=uint8
        # if rgba.dtype != getattr(__import__("numpy"), "uint8"):
        #     rgba = rgba.astype("uint8", copy=False)
        # if not rgba.flags["C_CONTIGUOUS"]:
        #     # Only make contiguous if necessary
        #     rgba = __import__("numpy").ascontiguousarray(rgba)

        rgb = rgb_annotator.get_data()

        # Ensure proper dtype/contiguity and pack into bytes
        import numpy as _np

        # Convert Warp array to NumPy if needed
        if hasattr(rgb, 'numpy'):
            # This is a Warp array, convert to numpy
            rgb = rgb.numpy()

        # Ensure uint8 dtype
        if rgb.dtype != _np.uint8:
            rgb = rgb.astype(_np.uint8, copy=False)

        # Ensure C-contiguous layout
        if not rgb.flags['C_CONTIGUOUS']:
            rgb = _np.ascontiguousarray(rgb)

        # Update only the parts that change every frame
        msg.header.stamp = _ros2_node.get_clock().now().to_msg()
        msg.data = rgb.tobytes()

        try:
            pub.publish(msg)
        except Exception:
            # Avoid logging in the hot path; silently drop on shutdown.
            pass

    # Use a named function (slightly cheaper than creating a closure with captures)
    world_instance.add_render_callback(
        callback_name=f"camera_{idx}_publisher",
        callback_fn=__publish_camera_image_py,
    )
    return pub
