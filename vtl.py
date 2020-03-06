import cv2
from cv2 import VideoCapture as vc
import wx
import os
import os.path as osp
import shutil
import pandas as pd
from pandas import DataFrame as df


class APP(wx.App):

    def OnInit(self):
        self.fps = None
        self.store_path = None
        self.data_path = None
        self.selected_video = None
        self.frames = list()
        self.raw_video = None
        self.next_to_read_frame_idx = 0
        self.frame_idx = 0
        self.total_frames = 0
        self.scale_factor = 5

        self.window = wx.Frame(None, title="Video Temporal Labeling Tool", size=(500, 400))
        self.panel = wx.Panel(self.window)
        self.warning = wx.StaticText(self.panel, label="Warning: ", pos=(10,10), size=(1000,25))
        self.warning.SetForegroundColour((255,0,0))

        self.warning.Show(False)
        self.help_text_bt = wx.Button(self.panel, label='Confirm', pos=(1100,40), size=(60,25))
        self.help_text_bt.Bind(wx.EVT_BUTTON, self.confirm_store_path)
        self.help_text_store_path = wx.StaticText(self.panel, label="Absolute Store Path: ", pos=(10,45), size=(110,25))
        self.store_path_text = wx.TextCtrl(self.panel, pos=(125,40), style=wx.TE_LEFT, size=(950,25))
        self.help_data_path = wx.StaticText(self.panel, label="Absolute Data Path: ", pos=(10,80), size=(110,25))
        self.data_path_text = wx.TextCtrl(self.panel, pos=(125,75), style=wx.TE_LEFT, size=(950,25))
        self.data_path_bt = wx.Button(self.panel, label='Confirm', pos=(1100,75), size=(60,25))
        self.data_path_bt.Bind(wx.EVT_BUTTON, self.confirm_data_path)
        self.help_video_data_choice = wx.StaticText(self.panel, label="Videos: ", pos=(10, 110), size=(75, 25))
        self.video_data_choice = wx.Choice(self.panel, pos=(125,110), size=(500, 25))
        self.video_data_bt = wx.Button(self.panel, label="Confirm", pos=(650,110), size=(60,25))
        self.video_data_bt.Bind(wx.EVT_BUTTON, self.confirm_video_choice)
        self.help_fps = wx.StaticText(self.panel, label="FPS: ", pos=(10, 150), size=(50, 25))
        self.fps_text = wx.TextCtrl(self.panel, pos=(125,145), size=(100, 25))
        self.fps_bt = wx.Button(self.panel, label="Confirm", pos=(250, 145), size=(60, 25))
        self.fps_bt.Bind(wx.EVT_BUTTON, self.confirm_fps)
        self.gallery = [
            wx.StaticBitmap(self.panel, -1, pos=(10,250)), wx.StaticBitmap(self.panel, -1, pos=(360,250)), wx.StaticBitmap(self.panel, -1, pos=(710,250)),
            wx.StaticBitmap(self.panel, -1, pos=(10,425)), wx.StaticBitmap(self.panel, -1, pos=(360,425)), wx.StaticBitmap(self.panel, -1, pos=(710,425)),
            wx.StaticBitmap(self.panel, -1, pos=(10,600)), wx.StaticBitmap(self.panel, -1, pos=(360,600)), wx.StaticBitmap(self.panel, -1, pos=(710,600))
                        ]
        self.description = [
            wx.StaticText(self.panel, pos=(10,400)), wx.StaticText(self.panel, pos=(360,400)), wx.StaticText(self.panel, pos=(710,400)),
            wx.StaticText(self.panel, pos=(10,575)), wx.StaticText(self.panel, pos=(360,575)), wx.StaticText(self.panel, pos=(710,575)),
            wx.StaticText(self.panel, pos=(10,750)), wx.StaticText(self.panel, pos=(360,750)), wx.StaticText(self.panel, pos=(710,750)),
        ]

        self.previous_bt = wx.Button(self.panel, label='Previous', pos=(10, 200), size=(75, 25))
        self.next_bt = wx.Button(self.panel, label='Next', pos=(110, 200), size=(75, 25))
        self.previous_bt.Bind(wx.EVT_BUTTON, self.previous_window)
        self.next_bt.Bind(wx.EVT_BUTTON, self.next_window)

        self.help_start_frame_input = wx.StaticText(self.panel, label="Start Frame: ", pos=(1000, 250), size=(75,25))
        self.start_frame_input = wx.TextCtrl(self.panel, pos=(1075, 245), size=(75, 25))

        self.help_end_frame_input = wx.StaticText(self.panel, label="End Frame: ", pos=(1000, 300), size=(75,25))
        self.end_frame_input = wx.TextCtrl(self.panel, pos=(1075, 295), size=(75, 25))

        self.label_confirm_bt = wx.Button(self.panel, label="Confirm", pos=(1180, 270), size=(75, 25))
        self.label_confirm_bt.Bind(wx.EVT_BUTTON, self.labelling)
        self.label_confirm_bt.Disable()

        self.window.Show()
        self.window.Maximize()
        return True

    def labelling(self, e):
        self.warning.Show(False)
        start = self.start_frame_input.GetValue()
        end = self.end_frame_input.GetValue()
        if start.isdigit() and end.isdigit() and int(start)<int(end) and int(start)>=0 and int(end)>=0:
            self.warning.SetForegroundColour((0,0,0))
            new_data = df({"video":[self.selected_video],"start_frame":[int(start)],"end_frame":[int(end)]})
            result_path = osp.join(self.store_path, osp.basename(self.data_path).replace(" ", "_")+"_labels.csv")
            if osp.exists(result_path):
                old_data = pd.read_csv(result_path)
                new_data = pd.concat([old_data, new_data], axis=0, sort=False)
            new_data.to_csv(result_path, index=False)
            self.warning.SetLabel("Action [start_frame: {}, end_frame: {}] has been recorded".format(start, end))
            self.warning.Show(True)
        else:
            self.warning.SetLabel("Warning: INVALID Frame Number.")
            self.warning.SetForegroundColour((255,0,0))
            self.warning.Show(True)

        self.window.Refresh()

    def confirm_store_path(self, e):
        self.warning.Show(False)
        self.store_path = self.store_path_text.GetValue()
        if not osp.exists(self.store_path):
            self.store_path_text.SetForegroundColour((0,0,0))
            self.warning.SetLabel("Warning: INVALID Store Path.")
            self.warning.SetForegroundColour((255,0,0))
            self.warning.Show(True)
            self.store_path = None
            self.label_confirm_bt.Disable()
        else:
            self.store_path_text.SetForegroundColour((0,255,0))
            self.warning.SetForegroundColour((0,0,0))
            self.warning.SetLabel("Store Path Set as: "+self.store_path)
            self.warning.Show(True)
            if self.data_path is not None:
                self.label_confirm_bt.Enable()

        self.window.Refresh()

    def confirm_data_path(self, e):
        self.warning.Show(False)
        self.data_path = osp.abspath(self.data_path_text.GetValue())
        if not osp.exists(self.data_path):
            self.data_path_text.SetForegroundColour((0,0,0))
            self.warning.SetLabel("Warning: INVALID Data Path.")
            self.warning.SetForegroundColour((255,0,0))
            self.warning.Show(True)
            self.data_path = None
            self.label_confirm_bt.Disable()
        else:
            self.data_path_text.SetForegroundColour((0,255,0))
            self.videos = list(filter(lambda x: x[-4:] in ['.avi', '.wav', '.mp4'], os.listdir(self.data_path)))
            self.video_data_choice.SetItems(self.videos)
            self.warning.SetForegroundColour((0,0,0))
            self.warning.SetLabel("Data Path Set as: "+self.data_path)
            self.warning.Show(True)
            if self.store_path is not None:
                self.label_confirm_bt.Enable()

        self.window.Refresh()

    def confirm_fps(self, e):
        self.warning.Show(False)
        if not self.fps_text.GetValue().isdigit():
            self.warning.SetLabel("Warning: INVALID FPS.")
            self.warning.SetForegroundColour((255,0,0))
            self.warning.Show(True)
        else:
            self.fps = int(self.fps_text.GetValue())
            self.warning.SetForegroundColour((0,0,0))
            self.warning.SetLabel("FPS Set as: "+str(self.fps))
            self.warning.Show(True)

        self.window.Refresh()

    def confirm_video_choice(self, e):
        self.warning.Show(False)
        id = self.video_data_choice.GetCurrentSelection()
        if id < 0 or self.data_path is None or self.store_path is None or self.fps is None:
            self.warning.SetLabel("Warning: No video is selected.")
            self.warning.SetForegroundColour((255,0,0))
            self.warning.Show(True)
        else:
            self.selected_video = self.videos[id]
            self.warning.SetLabel("Processing Video: "+osp.join(self.data_path, self.selected_video))
            self.warning.Show(True)
            self.window.Refresh()
            # Load the videos

            self.raw_video = vc(osp.join(self.data_path, self.selected_video))
            self.load_video_frame()
            self.raw_video.release()

            self.warning.SetForegroundColour((0,0,0))
            self.warning.SetLabel("Video is Ready: "+osp.join(self.data_path, self.selected_video))
            self.update()


        self.window.Refresh()

    def update(self):
        self.warning.Show(False)

        if self.frames is None:
            self.warning.SetLabel("Warning: No available frames")
            self.warning.SetForegroundColour((255,0,0))
            self.warning.Show(True)
        else:
            num_update = 0
            for frame, display, caption in zip(self.frames[self.frame_idx:], self.gallery, self.description):
                img = wx.Image(osp.join(self.data_path, self.selected_video.split('.')[0], frame), wx.BITMAP_TYPE_ANY)
                img = img.Scale(img.GetWidth()/self.scale_factor, img.GetHeight()/self.scale_factor)
                caption.SetLabel("Frame#: "+frame.split('.')[0].split('_')[-1])
                caption.Show(True)
                display.SetBitmap(wx.BitmapFromImage(img))
                display.Show(True)
                num_update+=1

            for display, caption in zip(self.gallery[num_update:], self.description[num_update:]):
                display.Show(False)
                caption.Show(False)

        self.window.Refresh()

    def next_window(self, e):
        self.frame_idx+=9
        if self.frame_idx < self.total_frames:
            self.update()
        else:
            self.frame_idx-=9
        self.window.Layout()

    def previous_window(self, e):
        self.frame_idx-=9
        if self.frame_idx >= 0:
            self.update()
        else:
            self.frame_idx+=9
        self.window.Layout()

    def load_video_frame(self):
        if self.raw_video is None:
            return

        temp_frame_folder = osp.join(self.data_path, self.selected_video.split('.')[0])

        if osp.exists(temp_frame_folder):
            shutil.rmtree(temp_frame_folder)

        os.makedirs(temp_frame_folder, 0x0777)

        self.sampling_freq = int(self.raw_video.get(cv2.CAP_PROP_FPS)/self.fps)

        idx = 0
        success, frame = self.raw_video.read()

        while success:
            if idx%self.sampling_freq == 0:
                savename = self.selected_video.split('.')[0]+"_frame_"+str(idx)+".jpg"
                cv2.imwrite(osp.join(temp_frame_folder, savename), frame)

            idx+=1
            success, frame = self.raw_video.read()

        self.frames = os.listdir(temp_frame_folder)
        self.frames.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
        self.frame_idx = 0
        self.total_frames = len(self.frames)


if __name__ == '__main__':
    try:
        app = APP()
        app.MainLoop()
    except:
        exit(0)
