import cv2
import wx
import os
import os.path as osp

class APP(wx.App):

    def OnInit(self):
        self.fps = 5
        self.store_path = "~/"
        self.data_path = "~/"
        self.selected_video = None

        self.window = wx.Frame(None, title="Video Temporal Labeling Tool", size=(500, 400))
        self.panel = wx.Panel(self.window)
        self.warning = wx.StaticText(self.panel, label="Warning: ", pos=(10,10), size=(1000,25))
        self.warning.SetForegroundColour((255,0,0))
        self.warning.Show(False)
        self.help_text_bt = wx.Button(self.panel, label='Confirm', pos=(1100,40), size=(60,25))
        self.help_text_bt.Bind(wx.EVT_BUTTON, self.confirm_store_path)
        self.help_text_store_path = wx.StaticText(self.panel, label="Absolute Store Path: ", pos=(10,45), size=(110,25))
        self.store_path_text = wx.TextCtrl(self.panel, value=self.store_path, pos=(125,40), style=wx.TE_LEFT, size=(950,25))
        self.help_data_path = wx.StaticText(self.panel, label="Absolute Data Path: ", pos=(10,80), size=(110,25))
        self.data_path_text = wx.TextCtrl(self.panel, value=self.data_path, pos=(125,75), style=wx.TE_LEFT, size=(950,25))
        self.data_path_bt = wx.Button(self.panel, label='Confirm', pos=(1100,75), size=(60,25))
        self.data_path_bt.Bind(wx.EVT_BUTTON, self.confirm_data_path)
        self.help_video_data_choice = wx.StaticText(self.panel, label="Videos: ", pos=(10, 110), size=(75, 25))
        self.video_data_choice = wx.Choice(self.panel, pos=(125,110), size=(500, 25))
        self.video_data_bt = wx.Button(self.panel, label="Confirm", pos=(650,110), size=(60,25))
        self.video_data_bt.Bind(wx.EVT_BUTTON, self.confirm_video_choice)
        self.help_fps = wx.StaticText(self.panel, label="FPS: ", pos=(10, 150), size=(50, 25))
        self.fps_text = wx.TextCtrl(self.panel, value=str(self.fps), pos=(125,145), size=(100, 25))
        self.fps_bt = wx.Button(self.panel, label="Confirm", pos=(250, 145), size=(60, 25))
        self.fps_bt.Bind(wx.EVT_BUTTON, self.confirm_fps)

        self.previous_bt = wx.Button(self.panel, label='Previous', pos=(10, 200), size=(75, 25))

        self.window.Show()
        self.window.Maximize()
        return True

    def confirm_store_path(self, e):
        self.warning.Show(False)
        self.store_path = self.store_path_text.GetValue()
        if not osp.exists(self.store_path):
            self.warning.SetLabel("Warning: INVALID Store Path.")
            self.warning.SetForegroundColour((255,0,0))
            self.warning.Show(True)
        else:
            self.warning.SetForegroundColour((0,0,0))
            self.warning.SetLabel("Store Path Set as: "+self.store_path)
            self.warning.Show(True)

    def confirm_data_path(self, e):
        self.warning.Show(False)
        self.data_path = osp.abspath(self.data_path_text.GetValue())
        if not osp.exists(self.data_path):
            self.warning.SetLabel("Warning: INVALID Data Path.")
            self.warning.SetForegroundColour((255,0,0))
            self.warning.Show(True)
        else:
            self.videos = list(filter(lambda x: x[-4:] in ['.avi', '.wav', '.mp4'], os.listdir(self.data_path)))
            self.video_data_choice.SetItems(self.videos)
            self.warning.SetForegroundColour((0,0,0))
            self.warning.SetLabel("Data Path Set as: "+self.data_path)
            self.warning.Show(True)
            self.window.Refresh()

    def confirm_fps(self, e):
        self.warning.Show(False)
        self.fps = self.fps_text.GetValue()
        if not self.fps.isdigit():
            self.warning.SetLabel("Warning: INVALID FPS.")
            self.warning.SetForegroundColour((255,0,0))
            self.warning.Show(True)
        else:
            self.warning.SetForegroundColour((0,0,0))
            self.warning.SetLabel("FPS Set as: "+self.fps)
            self.warning.Show(True)
            self.window.Refresh()

    def confirm_video_choice(self, e):
        self.warning.Show(False)
        id = self.video_data_choice.GetCurrentSelection()
        if id < 0:
            self.warning.SetLabel("Warning: No video selected")
            self.warning.SetForegroundColour((255,0,0))
            self.warning.Show(True)
        else:
            self.selected_video = self.videos[id]
            self.warning.SetForegroundColour((0,0,0))
            self.warning.SetLabel("Video Selected: "+osp.join(self.data_path, self.selected_video))
            self.warning.Show(True)
            # Load the videos


if __name__ == '__main__':
    app = APP()
    app.MainLoop()
