from dataclasses import dataclass, field
from typing import Any, List, Literal, Optional, Union
from uuid import UUID, uuid4

from robot_interface.models.geometry.joints import Joints
from robot_interface.models.geometry.pose import Pose
from robot_interface.models.geometry.position import Position
from robot_interface.models.mission.status import MissionStatus


@dataclass
class Task:
    """
    Base class for all tasks in a mission.
    """

    id: UUID = field(default_factory=uuid4, init=False)
    status: MissionStatus = field(default=MissionStatus.NotStarted, init=False)

    def __str__(self):
        def add_indent(text: str) -> str:
            return "".join("  " + line for line in text.splitlines(True))

        def robot_class_to_pretty_string(obj: Task) -> str:
            log_message: str = ""
            for attr in dir(obj):
                if callable(getattr(obj, attr)) or attr.startswith("__"):
                    continue

                value: Any = getattr(obj, attr)
                try:
                    package_name: Optional[str] = (
                        str(value.__class__).split("'")[1].split(".")[0]
                    )
                except (AttributeError, IndexError) as e:
                    package_name = None

                if package_name == "robot_interface":
                    log_message += (
                        "\n" + attr + ": " + robot_class_to_pretty_string(value)
                    )
                else:
                    log_message += "\n" + str(attr) + ": " + str(value)

            return add_indent(log_message)

        class_name: str = type(self).__name__
        return class_name + robot_class_to_pretty_string(self)


@dataclass
class InspectionTask(Task):
    """
    Base class for all inspection tasks which produce a result to be uploaded.
    """

    pass


@dataclass
class MotionTask(Task):
    """
    Base class for all tasks which should cause the robot to move, but not return a result.
    """

    pass


@dataclass
class DriveToPose(MotionTask):
    """
    Task which causes the robot to move to the given pose.
    """

    pose: Pose
    name: Literal["drive_to_pose"] = "drive_to_pose"
    depends_on: Optional[List[int]] = None


@dataclass
class DockingProcedure(MotionTask):
    """
    Task which causes the robot to dock or undock
    """

    behavior: Literal["dock, undock"]
    name: Literal["docking_procedure"] = "docking_procedure"


@dataclass
class TakeImage(InspectionTask):
    """
    Task which causes the robot to take an image towards the given coordinate.
    """

    target: Position
    name: Literal["take_image"] = "take_image"
    computed_joints: Optional[Joints] = None
    tag_id: Optional[str] = None
    depends_on: Optional[List[int]] = None


@dataclass
class TakeThermalImage(InspectionTask):
    """
    Task which causes the robot to take a thermal image towards the given coordinate.
    """

    target: Position
    name: Literal["take_thermal_image"] = "take_thermal_image"
    computed_joints: Optional[Joints] = None
    tag_id: Optional[str] = None
    depends_on: Optional[List[int]] = None


TASKS = Union[DriveToPose, DockingProcedure, TakeImage, TakeThermalImage]
