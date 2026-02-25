"""
Video Temporal Labeling Tool - GUI Application.

A wxPython-based GUI application for temporal video data labeling.
Supports labeling video segments with start/end frames and action types.

Author: Pengnan Fan (Modernized for Python 3.12)
Date: 2020-07-13 (Updated: 2026-02-25)
License: MIT
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import wx

from .service import Service

if TYPE_CHECKING:
    import numpy as np


class Layout(wx.Frame):
    """Main application window layout and UI components."""

    def __init__(
        self,
        parent: wx.Window | None = None,
        size: tuple[int, int] = (1000, 700),
        title: str = "Video Temporal Labeling Tool",
    ) -> None:
        """Initialize the main application window.

        Args:
            parent: Parent window (None for top-level window).
            size: Window size as (width, height).
            title: Window title.
        """
        super().__init__(parent=parent, size=size, title=title)
        self.service = Service(self)
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize all UI components and layout."""
        self.init_menu()

        # Set up dataset info inputs
        self.dataset_input = wx.TextCtrl(self)

        input_style = wx.ALIGN_CENTER | wx.ALL
        dataset_input_box = wx.BoxSizer()
        dataset_input_box.Add(
            wx.StaticText(self, label="Dataset Path"), 1, input_style, border=10
        )
        dataset_input_box.Add(self.dataset_input, 5, input_style, border=10)

        # Set up store path inputs
        self.store_input = wx.TextCtrl(self)
        store_input_box = wx.BoxSizer()
        store_input_box.Add(
            wx.StaticText(self, label="Store Path"), 1, input_style, border=10
        )
        store_input_box.Add(self.store_input, 5, input_style, border=10)

        # Set up input box (left)
        input_box_left_style = wx.EXPAND | wx.ALL
        input_box_left = wx.BoxSizer(wx.VERTICAL)
        input_box_left.Add(dataset_input_box, 1, input_box_left_style, border=2)
        input_box_left.Add(store_input_box, 1, input_box_left_style, border=2)

        # Set up input confirm button
        input_confirm = wx.Button(self, label="Confirm")
        input_confirm.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "confirm_input")
        )

        # Set up input box
        input_box_style = wx.ALIGN_CENTER | wx.ALL
        input_box = wx.BoxSizer()
        input_box.Add(input_box_left, 6, input_box_style, border=10)
        input_box.Add(input_confirm, 1, input_box_style, border=10)

        # Default image - use a fallback if resource file doesn't exist
        resource_path = Path(__file__).parent / "resource" / "test_frame.jpg"
        if resource_path.exists():
            img = wx.Image(str(resource_path), wx.BITMAP_TYPE_JPEG)
            img = wx.Bitmap(img)
        else:
            # Create a blank bitmap as fallback
            img = wx.Bitmap(640, 480)

        # Video info box
        video_info_static_box = wx.StaticBox(self, label="Video Information")
        video_info_static_box_sizer = wx.StaticBoxSizer(
            video_info_static_box, wx.VERTICAL
        )

        self.select_video = wx.Choice(self)
        self.select_video.Bind(
            wx.EVT_CHOICE, lambda x: self.service.button_event(x, "selectVideo")
        )
        video_box_style = wx.EXPAND | wx.ALL

        self.video_frame = wx.StaticText(self)

        video_grid_box = wx.FlexGridSizer(2, 2, 5, 5)
        video_grid_box.Add(wx.StaticText(self, label="Video: "), 1, video_box_style)
        video_grid_box.Add(self.select_video, 3, video_box_style)
        video_grid_box.Add(
            wx.StaticText(self, label="Current Frame: "), 1, video_box_style
        )
        video_grid_box.Add(self.video_frame, 1, video_box_style)

        video_info_static_box_sizer.Add(
            video_grid_box, 1, wx.EXPAND | wx.ALL, border=5
        )

        # Video control box
        prev_video = wx.Button(self, label="Previous")
        prev_video.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "prevVideo")
        )

        next_video = wx.Button(self, label="Next")
        next_video.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "nextVideo")
        )

        video_control_box = wx.StaticBox(self, label="Video Control")
        video_control_box_sizer = wx.StaticBoxSizer(
            video_control_box, wx.HORIZONTAL
        )
        video_control_style = wx.EXPAND | wx.ALL
        video_control_box_sizer.Add(prev_video, 1, video_control_style, border=5)
        video_control_box_sizer.Add(next_video, 1, video_control_style, border=5)

        # Label info box
        label_info_box = wx.StaticBox(self, label="Label Information")
        label_info_box_sizer = wx.StaticBoxSizer(label_info_box, wx.VERTICAL)

        label_info_grid_box = wx.GridSizer(2, 2, 5, 5)

        self.selected_start = wx.StaticText(self, label="0")
        self.selected_end = wx.StaticText(self, label="0")

        label_info_grid_box.Add(
            wx.StaticText(self, label="Selected Start Frame: "), video_box_style
        )
        label_info_grid_box.Add(self.selected_start, video_box_style)
        label_info_grid_box.Add(
            wx.StaticText(self, label="Selected End Frame: "), video_box_style
        )
        label_info_grid_box.Add(self.selected_end, video_box_style)

        label_info_box_sizer.Add(
            label_info_grid_box, 1, wx.EXPAND | wx.ALL, border=5
        )

        # Control box
        control_static_box = wx.StaticBox(self, label="Frame Control")
        control_static_box_sizer = wx.StaticBoxSizer(
            control_static_box, wx.VERTICAL
        )

        prev_n_frame = wx.Button(self, label="-FPI")
        prev_n_frame.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "prevNFrame")
        )

        prev_frame = wx.Button(self, label="-1")
        prev_frame.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "prevFrame")
        )

        next_frame = wx.Button(self, label="+1")
        next_frame.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "nextFrame")
        )

        next_n_frame = wx.Button(self, label="+FPI")
        next_n_frame.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "nextNFrame")
        )

        button_style = wx.EXPAND | wx.ALL

        control_grid_box = wx.GridSizer(2, 2, 5, 5)
        control_grid_box.Add(prev_frame, button_style)
        control_grid_box.Add(next_frame, button_style)
        control_grid_box.Add(prev_n_frame, button_style)
        control_grid_box.Add(next_n_frame, button_style)

        control_static_box_sizer.Add(
            control_grid_box, 1, wx.EXPAND, border=5
        )

        # Label box
        label_box = wx.StaticBox(self, label="Labelling Box")
        label_box_sizer = wx.StaticBoxSizer(label_box, wx.VERTICAL)

        select_start = wx.Button(self, label="Start")
        select_start.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "selectStart")
        )

        select_end = wx.Button(self, label="End")
        select_end.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "selectEnd")
        )

        # Select label box
        select_label_box = wx.BoxSizer()
        select_label_box.Add(select_start, 1, button_style, border=5)
        select_label_box.Add(select_end, 1, button_style, border=5)

        select_close = wx.Button(self, label="Close")
        select_close.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "selectClose")
        )

        select_mid = wx.Button(self, label="Mid")
        select_mid.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "selectMid")
        )

        select_far = wx.Button(self, label="Far")
        select_far.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "selectFar")
        )

        save_label = wx.Button(self, label="Save")
        save_label.Bind(
            wx.EVT_BUTTON, lambda e: self.service.button_event(e, "saveLabel")
        )

        select_type_box = wx.BoxSizer()
        select_type_box.Add(select_close, 1, button_style, border=5)
        select_type_box.Add(select_mid, 1, button_style, border=5)
        select_type_box.Add(select_far, 1, button_style, border=5)

        label_box_sizer.Add(select_label_box, 1, wx.EXPAND, border=5)
        label_box_sizer.Add(select_type_box, 1, wx.EXPAND, border=5)
        label_box_sizer.Add(
            save_label, 1, wx.EXPAND | wx.ALL, border=5
        )

        # Action type selection
        action_type_static_box = wx.StaticBox(self, label="Action Type")
        self.action_type_choice = wx.Choice(self)
        self.action_type_choice.Bind(
            wx.EVT_CHOICE,
            lambda x: self.service.button_event(x, "selectAction"),
        )
        self.action_type_choice.SetItems(["tripping", "faceoff"])
        self.action_type_choice.Selection = 0
        action_type_static_box_sizer = wx.StaticBoxSizer(action_type_static_box)
        action_type_static_box_sizer.Add(
            self.action_type_choice, 1, wx.EXPAND, border=5
        )

        # Info box
        info_box = wx.BoxSizer(wx.VERTICAL)
        info_box_style = wx.EXPAND
        info_box.Add(video_info_static_box_sizer, 2, info_box_style, border=5)
        info_box.Add(video_control_box_sizer, 2, info_box_style, border=5)
        info_box.Add(label_info_box_sizer, 2, info_box_style, border=5)
        info_box.Add(control_static_box_sizer, 2, info_box_style, border=5)
        info_box.Add(action_type_static_box_sizer, 1, info_box_style, border=5)
        info_box.Add(label_box_sizer, 3, info_box_style, border=5)

        # Display box
        self.display = wx.StaticBitmap(parent=self)
        self.display.SetBitmap(img)
        display_box_style = wx.ALIGN_CENTER | wx.ALL
        display_box = wx.BoxSizer()

        frame_box = wx.StaticBox(self, label="Video Frame")
        frame_box_sizer = wx.StaticBoxSizer(frame_box)
        frame_box_sizer.Add(self.display, 1, wx.EXPAND)

        display_box.Add(frame_box_sizer, 5, display_box_style, border=10)
        display_box.Add(info_box, 2, display_box_style, border=10)

        # Set up feedback message
        self.feedback_message = wx.StaticText(
            self, label="Welcome to Video Temporal Labeling Tool v2.0"
        )
        self.feedback_message.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
        )

        # Construct main layout
        my_style = wx.ALL | wx.ALIGN_CENTER
        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(self.feedback_message, 1, my_style, border=1)
        main_box.Add(input_box, 6, my_style, border=1)
        main_box.Add(display_box, 20, my_style, border=1)

        # Set main box in frame
        self.SetSizer(main_box)
        self.Centre()

        # Setup keyboard shortcuts
        self._setup_keyboard_shortcuts()

    def _setup_keyboard_shortcuts(self) -> None:
        """Setup global keyboard shortcuts for frame navigation.

        Shortcuts:
            Left Arrow:  Previous frame (-1)
            Right Arrow: Next frame (+1)
            Shift+Left:  Previous N frames (-FPI)
            Shift+Right: Next N frames (+FPI)
            S:           Select start frame
            E:           Select end frame
            Ctrl+S:      Save label
        """
        # Define accelerator entries
        accel_entries = [
            # Frame navigation
            (wx.ACCEL_NORMAL, wx.WXK_LEFT, 1001),    # Left arrow -> prev frame
            (wx.ACCEL_NORMAL, wx.WXK_RIGHT, 1002),   # Right arrow -> next frame
            (wx.ACCEL_SHIFT, wx.WXK_LEFT, 1003),     # Shift+Left -> prev N frames
            (wx.ACCEL_SHIFT, wx.WXK_RIGHT, 1004),    # Shift+Right -> next N frames
            # Label operations
            (wx.ACCEL_NORMAL, ord('S'), 1005),       # S -> select start
            (wx.ACCEL_NORMAL, ord('E'), 1006),       # E -> select end
            (wx.ACCEL_CTRL, ord('S'), 1007),         # Ctrl+S -> save
        ]

        accel_table = wx.AcceleratorTable(accel_entries)
        self.SetAcceleratorTable(accel_table)

        # Bind accelerator events
        self.Bind(wx.EVT_MENU, lambda e: self.service.button_event(e, "prevFrame"), id=1001)
        self.Bind(wx.EVT_MENU, lambda e: self.service.button_event(e, "nextFrame"), id=1002)
        self.Bind(wx.EVT_MENU, lambda e: self.service.button_event(e, "prevNFrame"), id=1003)
        self.Bind(wx.EVT_MENU, lambda e: self.service.button_event(e, "nextNFrame"), id=1004)
        self.Bind(wx.EVT_MENU, lambda e: self.service.button_event(e, "selectStart"), id=1005)
        self.Bind(wx.EVT_MENU, lambda e: self.service.button_event(e, "selectEnd"), id=1006)
        self.Bind(wx.EVT_MENU, lambda e: self.service.button_event(e, "saveLabel"), id=1007)

    def init_menu(self) -> None:
        """Initialize the menu bar with settings."""
        menu_bar = wx.MenuBar()

        file_menu = wx.Menu()

        # FPS selection menu
        fps_menu = wx.Menu()
        fps_menu.Append(
            wx.MenuItem(file_menu, id=11, text="5", kind=wx.ITEM_RADIO)
        )
        fps_menu.Append(
            wx.MenuItem(file_menu, id=12, text="10", kind=wx.ITEM_RADIO)
        )
        fps_menu.Append(
            wx.MenuItem(file_menu, id=13, text="15", kind=wx.ITEM_RADIO)
        )
        fps_menu.Append(
            wx.MenuItem(file_menu, id=14, text="20", kind=wx.ITEM_RADIO)
        )
        fps_menu.Append(
            wx.MenuItem(file_menu, id=15, text="30", kind=wx.ITEM_RADIO)
        )

        file_menu.Append(wx.ID_ANY, "Frame Per Interval", fps_menu)

        menu_bar.Append(file_menu, title="Setting")

        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.service.menu_event)

    def update_message(self, msg: str) -> None:
        """Display a success message.

        Args:
            msg: Message to display.
        """
        self.feedback_message.SetLabel(f"Message: {msg}")
        self.feedback_message.SetForegroundColour((0, 0, 0))

    def update_error(self, error: str) -> None:
        """Display an error message.

        Args:
            error: Error message to display.
        """
        self.feedback_message.SetLabel(f"Error: {error}")
        self.feedback_message.SetForegroundColour((255, 0, 0))

    def update_frame(
        self, cv2_frame: np.ndarray, frame_no: int
    ) -> None:
        """Update the displayed video frame.

        Args:
            cv2_frame: OpenCV frame data (BGR format).
            frame_no: Current frame number.
        """
        h, w = cv2_frame.shape[:2]
        self.display.SetBitmap(wx.Bitmap.FromBuffer(w, h, cv2_frame))
        self.video_frame.SetLabel(str(frame_no))

    def update_start_label(self, start: int) -> None:
        """Update the start frame label.

        Args:
            start: Start frame number.
        """
        self.selected_start.SetLabel(str(start))

    def update_end_label(self, end: int) -> None:
        """Update the end frame label.

        Args:
            end: End frame number.
        """
        self.selected_end.SetLabel(str(end))


class App(wx.App):
    """Main application class for displaying the UI."""

    def OnInit(self) -> bool:
        """Initialize and show the application window.

        Returns:
            True if initialization successful.
        """
        frame = Layout()
        frame.Show()
        return True


def main() -> None:
    """Application entry point."""
    try:
        app = App()
        app.MainLoop()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
