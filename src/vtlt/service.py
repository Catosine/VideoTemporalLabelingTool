"""
Video Temporal Labeling Tool - Service Module.

This module contains the Service class that handles business logic
triggered by UI interactions.

Author: Pengnan Fan (Modernized for Python 3.12)
Date: 2020-07-13 (Updated: 2026-02-25)
License: MIT
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import cv2
import pandas as pd
from pandas import DataFrame

if TYPE_CHECKING:
    import wx

    from .app import Layout


class Service:
    """Service class handling video labeling business logic."""

    def __init__(self, ui: Layout) -> None:
        """Initialize the service with UI reference.

        Args:
            ui: Reference to the main UI layout.
        """
        self.ui = ui
        self.dataset_path: Path | None = None
        self.store_path: Path | None = None
        self.fps: int = 5
        self.video_lists: list[str] = []
        self.curr_video: int = 0
        self.cap: cv2.VideoCapture | None = None
        self.tot_frame: int = 0
        self.curr_frame: int = 0
        self.label_start: int = 0
        self.label_end: int = 0
        self.shot_type: str | None = None
        self.action_type: str = "tripping"

    def update_input_info(self, data_path: str, store_path: str) -> None:
        """Update dataset and store paths from user input.

        Args:
            data_path: Path to the video dataset directory.
            store_path: Path to the output directory for labels.
        """
        data_path_obj = Path(data_path)
        if data_path_obj.exists():
            self.dataset_path = data_path_obj
            self.ui.update_message("Dataset path is updated")
        else:
            self.ui.update_error(f"Invalid dataset path: {data_path}")
            return

        store_path_obj = Path(store_path)
        if store_path_obj.exists():
            self.store_path = store_path_obj
            self.ui.update_message("Store path is updated")
        else:
            self.ui.update_error(f"Invalid store path: {store_path}")
            return

        self.update_video_lists()

    def get_selected_video(self, evt: wx.Event) -> str:
        """Get the selected video name from choice event.

        Args:
            evt: wx Choice event.

        Returns:
            Selected video filename.
        """
        return evt.GetString()

    def update_video_lists(self) -> None:
        """Scan dataset directory and update video list."""
        if self.dataset_path and self.dataset_path.exists():
            video_extensions = {".avi", ".wav", ".mp4", ".mkv", ".mov"}
            self.video_lists = sorted([
                f for f in os.listdir(self.dataset_path)
                if Path(f).suffix.lower() in video_extensions
            ])
            self.ui.select_video.SetItems(self.video_lists)
        else:
            self.ui.update_error("Please enter a valid dataset path.")

    def load_video(self) -> None:
        """Load the current video and initialize playback state."""
        tot_video = len(self.video_lists)
        if tot_video == 0:
            self.ui.update_error("No videos found in dataset")
            return

        self.curr_video = min(self.curr_video, tot_video - 1)
        self.curr_video = max(self.curr_video, 0)
        self.ui.select_video.Selection = self.curr_video

        video_path = self.dataset_path / self.video_lists[self.curr_video]
        self.cap = cv2.VideoCapture(str(video_path))
        self.tot_frame = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.curr_frame = 0
        self.label_start = 0
        self.label_end = 0
        self.ui.update_start_label(0)
        self.ui.update_end_label(0)
        self.shot_type = None
        self.ui.video_frame.SetLabel("0")
        self.update_frame_n()
        self.ui.update_message(
            f"Select video: {self.video_lists[self.curr_video]}"
        )

    def update_frame_n(self) -> None:
        """Update the current frame display based on curr_frame."""
        if self.cap is None:
            return

        self.curr_frame = min(self.curr_frame, self.tot_frame - 1)
        self.curr_frame = max(self.curr_frame, 0)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.curr_frame)
        ret, frame = self.cap.read()
        if ret:
            self.ui.update_frame(
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                self.curr_frame
            )
        else:
            self.ui.update_error(
                f"This is an empty video: {self.video_lists[self.curr_video]}"
            )

    def button_event(self, e: wx.Event, evt_id: str) -> None:
        """Handle button click events.

        Args:
            e: wx event object.
            evt_id: Event identifier string.
        """
        if evt_id == "prevVideo":
            self.curr_video -= 1
            self.load_video()
        elif evt_id == "prevNFrame":
            self.curr_frame -= self.fps
            self.update_frame_n()
        elif evt_id == "prevFrame":
            self.curr_frame -= 1
            self.update_frame_n()
        elif evt_id == "nextFrame":
            self.curr_frame += 1
            self.update_frame_n()
        elif evt_id == "nextNFrame":
            self.curr_frame += self.fps
            self.update_frame_n()
        elif evt_id == "nextVideo":
            self.curr_video += 1
            self.load_video()
        elif evt_id == "confirm_input":
            self.update_input_info(
                self.ui.dataset_input.GetValue(),
                self.ui.store_input.GetValue()
            )
        elif evt_id == "selectStart":
            self.label_start = self.curr_frame
            self.ui.update_start_label(int(self.curr_frame))
            self.ui.update_message(
                f"Select frame {self.curr_frame} as start of labeling"
            )
        elif evt_id == "selectEnd":
            self.label_end = self.curr_frame
            self.ui.update_end_label(int(self.curr_frame))
            self.ui.update_message(
                f"Select frame {self.curr_frame} as end of labeling"
            )
        elif evt_id == "selectVideo":
            self.curr_video = self.ui.select_video.Selection
            self.load_video()
        elif evt_id == "selectClose":
            self.store_label("close")
        elif evt_id == "selectMid":
            self.store_label("mid")
        elif evt_id == "selectFar":
            self.store_label("far")
        elif evt_id == "saveLabel":
            self.save_label()
        elif evt_id == "selectAction":
            self.action_type = e.GetString()
            self.ui.update_message(
                f"Action Type: {self.action_type} is selected."
            )
        else:
            self.ui.update_error("Unsupported Button")

        self.ui.Refresh()

    def update_fps(self, fps: int) -> None:
        """Update frames per interval setting.

        Args:
            fps: Frames per interval value.
        """
        self.fps = fps
        self.ui.update_message(f"FPS is updated as: {fps}")

    def menu_event(self, event: wx.Event) -> None:
        """Handle menu selection events.

        Args:
            event: wx menu event.
        """
        menu_id = event.GetId()
        fps_map = {
            11: 5,
            12: 10,
            13: 15,
            14: 20,
            15: 30,
        }
        if menu_id in fps_map:
            self.update_fps(fps_map[menu_id])
        else:
            raise NotImplementedError(f"Menu ID {menu_id} not implemented")

    def read_label(self) -> DataFrame | None:
        """Read and validate the current label selection.

        Returns:
            DataFrame with label data if valid, None otherwise.
        """
        if self.label_start < self.label_end:
            label = DataFrame({
                "video": [self.video_lists[self.curr_video]],
                "start_frame": [self.label_start],
                "end_frame": [self.label_end],
                "type": [self.shot_type],
                "action": [self.action_type]
            })
            msg = f"{self.action_type.upper()} action [{self.label_start}, {self.label_end}] is recorded"
            if self.shot_type:
                msg += f" as {self.shot_type} shot"
            self.ui.update_message(msg)
            return label
        else:
            self.ui.update_error(
                f"Action [{self.label_start},{self.label_end}] is NOT recorded: "
                "start should be less than end"
            )
            return None

    def store_label(self, label_type: str | None = None) -> None:
        """Store the shot type for current label.

        Args:
            label_type: Type of shot (close, mid, far).
        """
        self.shot_type = label_type
        self.ui.update_message(f"Action type is selected as {label_type}")

    def save_label(self) -> None:
        """Save the current label to CSV file."""
        label = self.read_label()
        if label is not None and self.store_path and self.dataset_path:
            result_path = (
                self.store_path /
                f"{self.dataset_path.name.replace(' ', '_')}_labels.csv"
            )
            if result_path.exists():
                old_data = pd.read_csv(result_path)
                label = pd.concat([old_data, label], axis=0, ignore_index=True)
            label.to_csv(result_path, index=False)
        else:
            self.ui.update_error("No action selected")
