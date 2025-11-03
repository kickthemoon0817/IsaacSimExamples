import omni.kit.app


def enable_extensions():
    extension_manager = omni.kit.app.get_app().get_extension_manager()
    # For live
    extension_manager.set_extension_enabled_immediate("omni.kit.window.stage", True)
    extension_manager.set_extension_enabled_immediate("omni.kit.window.console", True)
    extension_manager.set_extension_enabled_immediate("omni.kit.viewport.window", True)
    extension_manager.set_extension_enabled_immediate("omni.kit.viewport.utility", True)
    extension_manager.set_extension_enabled_immediate("omni.kit.widget.graph", True)
    extension_manager.set_extension_enabled_immediate("omni.graph.core", True)
    extension_manager.set_extension_enabled_immediate("omni.graph.action", True)
    extension_manager.set_extension_enabled_immediate("omni.graph.action_nodes", True)
    extension_manager.set_extension_enabled_immediate("omni.graph.bundle.action", True)
    extension_manager.set_extension_enabled_immediate("omni.graph.window.core", True)
    extension_manager.set_extension_enabled_immediate("omni.graph.window.action", True)
    # For ROS2
    extension_manager.set_extension_enabled_immediate("isaacsim.ros2.bridge", True)

