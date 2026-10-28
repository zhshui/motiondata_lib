from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from motiondata_lib.importers.common import build_motion_clip
from motiondata_lib.types import MotionClip, MotionClipRef

if TYPE_CHECKING:
    from motiondata_lib.robot_profiles import RobotProfile

FORMAT_NAME = "supermimic"
REQUIRED = {"fps", "joint_names", "joint_pos", "body_names", "body_pos_w", "body_quat_w"}


def can_load(path: Path) -> bool:
    if path.suffix.lower() != ".npz":
        return False
    try:
        with np.load(path, allow_pickle=False) as data:
            return REQUIRED.issubset(data.files)
    except (OSError, ValueError):
        return False


def load_motion_clip(clip_ref: MotionClipRef, robot_profile: RobotProfile) -> MotionClip:
    with np.load(clip_ref.path, allow_pickle=False) as data:
        root = list(data["body_names"]).index(robot_profile.root_body)
        return build_motion_clip(
            clip_ref,
            framerate=float(data["fps"].item()),
            joint_names=data["joint_names"],
            joint_pos=data["joint_pos"],
            base_pos_w=data["body_pos_w"][:, root],
            base_quat_w=data["body_quat_w"][:, root],
        )


def export_trim(source: Path, output: Path, start: int, end: int) -> None:
    """Save an inclusive frame range, preserving all training arrays and metadata."""
    if source.resolve() == output.resolve():
        raise ValueError("Choose a new filename to preserve the original motion.")
    if output.exists():
        raise ValueError("Output already exists. Choose a new filename to preserve existing motions.")
    frame_keys = {"joint_pos", "joint_vel", "body_pos_w", "body_quat_w",
                  "body_lin_vel_w", "body_ang_vel_w"}
    with np.load(source, allow_pickle=False) as data:
        count = len(data["joint_pos"])
        if not 0 <= start <= end < count:
            raise ValueError("Invalid trim range")
        arrays = {key: data[key][start:end + 1] if key in frame_keys else data[key]
                  for key in data.files}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as handle:
        np.savez_compressed(handle, **arrays)
