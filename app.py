import wx
import service


class Layout(wx.Frame):
    def __init__(self, parent=None, size=(1200, 750), title="Video Temporal Labeling Tool"):
        wx.Frame.__init__(self, parent=parent, size=size, title=title)
        self.service = service.Service(self)

        self.initUI()

    def initUI(self):
        self.initMenu()

        # set up dataset info inputs
        self.datasetInput = wx.TextCtrl(self)

        inputStyle = wx.ALIGN_CENTER | wx.ALL
        datasetInputBox = wx.BoxSizer()
        datasetInputBox.Add(wx.StaticText(self, label="Dataset Path"), 1, inputStyle, border=10)
        datasetInputBox.Add(self.datasetInput, 5, inputStyle, border=10)

        # set up store path inputs
        self.storeInput = wx.TextCtrl(self)
        storeInputBox = wx.BoxSizer()
        storeInputBox.Add(wx.StaticText(self, label="Store Path"), 1, inputStyle, border=10)
        storeInputBox.Add(self.storeInput, 5, inputStyle, border=10)

        # set up input box (left)
        inputBoxLeftStyle = wx.EXPAND | wx.ALL
        inputBoxLeft = wx.BoxSizer(wx.VERTICAL)
        inputBoxLeft.Add(datasetInputBox, 1, inputBoxLeftStyle, border=2)
        inputBoxLeft.Add(storeInputBox, 1, inputBoxLeftStyle, border=2)

        # set up input confirm button
        inputConfirm = wx.Button(self, label="Confirm")
        inputConfirm.Bind(wx.EVT_BUTTON, lambda e: self.service.button_event(e, "confirm_input"))

        # set up input box
        inputBoxStyle = wx.ALIGN_CENTER | wx.ALL
        inputBox = wx.BoxSizer()
        inputBox.Add(inputBoxLeft, 6, inputBoxStyle, border=10)
        inputBox.Add(inputConfirm, 1, inputBoxStyle, border=10)

        # default image
        img = wx.Image("./resource/test_frame.jpg", wx.BITMAP_TYPE_JPEG)
        img = wx.Bitmap(img)

        # video infos box
        videoInfoStaticBox = wx.StaticBox(self, label='Video Information')
        videoInfoStaticBoxSizer = wx.StaticBoxSizer(videoInfoStaticBox, wx.VERTICAL)

        self.selectVideo = wx.Choice(self)
        self.selectVideo.Bind(wx.EVT_CHOICE, lambda x: self.service.button_event(x, "selectVideo"))
        videoBoxStyle = wx.EXPAND | wx.ALL

        self.videoFrame = wx.StaticText(self)

        videoGridBox = wx.FlexGridSizer(2, 2, 5, 5)
        videoGridBox.Add(wx.StaticText(self, label="Video: "), 1, videoBoxStyle)
        videoGridBox.Add(self.selectVideo, 3, videoBoxStyle)
        videoGridBox.Add(wx.StaticText(self, label="Current Frame: "), 1, videoBoxStyle)
        videoGridBox.Add(self.videoFrame, 1, videoBoxStyle)

        videoInfoStaticBoxSizer.Add(videoGridBox, 1, wx.EXPAND | wx.ALL, border=5)

        # video control box
        prevVideo = wx.Button(self, label="Previous")
        prevVideo.Bind(wx.EVT_BUTTON, lambda e: self.service.button_event(e, "prevVideo"))

        nextVideo = wx.Button(self, label="Next")
        nextVideo.Bind(wx.EVT_BUTTON, lambda e: self.service.button_event(e, "nextVideo"))

        videoControlBox = wx.StaticBox(self, label="Video Control")
        videoControlBoxSizer = wx.StaticBoxSizer(videoControlBox, wx.HORIZONTAL)
        videoControlStyle = wx.EXPAND | wx.ALL
        videoControlBoxSizer.Add(prevVideo, 1, videoControlStyle, border=5)
        videoControlBoxSizer.Add(nextVideo, 1, videoControlStyle, border=5)

        # label info box
        labelInfoBox = wx.StaticBox(self, label="Label Information")
        labelInfoBoxSizer = wx.StaticBoxSizer(labelInfoBox, wx.VERTICAL)

        labelInfoGirdBox = wx.GridSizer(2, 2, 5, 5)

        self.selectedStart = wx.StaticText(self, label='0')
        self.selectedEnd = wx.StaticText(self, label='0')

        labelInfoGirdBox.Add(wx.StaticText(self, label="Selected Start Frame: "), videoBoxStyle)
        labelInfoGirdBox.Add(self.selectedStart, videoBoxStyle)
        labelInfoGirdBox.Add(wx.StaticText(self, label="Selected End Frame: "), videoBoxStyle)
        labelInfoGirdBox.Add(self.selectedEnd, videoBoxStyle)

        labelInfoBoxSizer.Add(labelInfoGirdBox, 1, wx.EXPAND | wx.ALL, border=5)

        # control box
        controlStaticBox = wx.StaticBox(self, label="Frame Control")
        controlStaticBoxSizer = wx.StaticBoxSizer(controlStaticBox, wx.VERTICAL)

        prevNFrame = wx.Button(self, label="-FPS")
        prevNFrame.Bind(wx.EVT_BUTTON, lambda e: self.service.button_event(e, "prevNFrame"))

        prevFrame = wx.Button(self, label="-1")
        prevFrame.Bind(wx.EVT_BUTTON, lambda e: self.service.button_event(e, "prevFrame"))

        nextFrame = wx.Button(self, label="+1")
        nextFrame.Bind(wx.EVT_BUTTON, lambda e: self.service.button_event(e, "nextFrame"))

        nextNFrame = wx.Button(self, label="+FPS")
        nextNFrame.Bind(wx.EVT_BUTTON, lambda e: self.service.button_event(e, "nextNFrame"))

        buttonStyle = wx.EXPAND | wx.ALL

        controlGridBox = wx.GridSizer(2, 2, 5, 5)
        controlGridBox.Add(prevFrame, buttonStyle)
        controlGridBox.Add(nextFrame, buttonStyle)
        controlGridBox.Add(prevNFrame, buttonStyle)
        controlGridBox.Add(nextNFrame, buttonStyle)

        controlStaticBoxSizer.Add(controlGridBox, 1, wx.EXPAND, border=5)

        # label box
        labelBox = wx.StaticBox(self, label="Labelling Box")
        labelBoxSizer = wx.StaticBoxSizer(labelBox, wx.VERTICAL)

        selectStart = wx.Button(self, label="Start")
        selectStart.Bind(wx.EVT_BUTTON, lambda e: self.service.button_event(e, "selectStart"))

        selectEnd = wx.Button(self, label="End")
        selectEnd.Bind(wx.EVT_BUTTON, lambda e: self.service.button_event(e, "selectEnd"))

        # select label box
        selectLabelBox = wx.BoxSizer()
        selectLabelBox.Add(selectStart, 1, buttonStyle, border=5)
        selectLabelBox.Add(selectEnd, 1, buttonStyle, border=5)

        selectClose = wx.Button(self, label="Close")
        selectClose.Bind(wx.EVT_BUTTON, lambda e: self.service.button_event(e, "selectClose"))

        selectMid = wx.Button(self, label="Mid")
        selectMid.Bind(wx.EVT_BUTTON, lambda e: self.service.button_event(e, "selectMid"))

        selectFar = wx.Button(self, label="Far")
        selectFar.Bind(wx.EVT_BUTTON, lambda e: self.service.button_event(e, "selectFar"))

        selectTypeBox = wx.BoxSizer()
        selectTypeBox.Add(selectClose, 1, buttonStyle, border=5)
        selectTypeBox.Add(selectMid, 1, buttonStyle, border=5)
        selectTypeBox.Add(selectFar, 1, buttonStyle, border=5)

        labelBoxSizer.Add(selectLabelBox, 1, wx.EXPAND, border=5)
        labelBoxSizer.Add(selectTypeBox, 1, wx.EXPAND, border=5)


        # info box
        infoBox = wx.BoxSizer(wx.VERTICAL)
        infoBoxStyle = wx.EXPAND
        infoBox.Add(videoInfoStaticBoxSizer, 2, infoBoxStyle, border=5)
        infoBox.Add(videoControlBoxSizer, 2, infoBoxStyle, border=5)
        infoBox.Add(labelInfoBoxSizer, 2, infoBoxStyle, border=5)
        infoBox.Add(controlStaticBoxSizer, 2, infoBoxStyle, border=5)
        infoBox.Add(labelBoxSizer, 3, infoBoxStyle, border=5)

        # display box
        self.display = wx.StaticBitmap(parent=self)
        self.display.SetBitmap(img)
        displayBoxStyle = wx.ALIGN_CENTER | wx.ALL
        displayBox = wx.BoxSizer()

        frameBox = wx.StaticBox(self, label="Video Frame")
        frameBoxSizer = wx.StaticBoxSizer(frameBox)
        frameBoxSizer.Add(self.display, 1, wx.EXPAND)

        displayBox.Add(frameBoxSizer, 5, displayBoxStyle, border=10)
        displayBox.Add(infoBox, 2, displayBoxStyle, border=10)

        # set up feedback message
        self.feedbackMessage = wx.StaticText(self, label="Welcome to use Video Temporal Labelling Tool v1.1")
        self.feedbackMessage.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL))

        # construct main layout
        myStyle = wx.ALL | wx.ALIGN_CENTER
        mainBox = wx.BoxSizer(wx.VERTICAL)
        mainBox.Add(self.feedbackMessage, 1, myStyle, border=1)
        mainBox.Add(inputBox, 6, myStyle, border=1)
        mainBox.Add(displayBox, 20, myStyle, border=1)

        # set main box in frame
        self.SetSizer(mainBox)
        self.Centre()


    def initMenu(self):
        menuBar = wx.MenuBar()

        fileMenu = wx.Menu()

        # fps selection menu
        fpsMenu = wx.Menu()
        fpsMenu.Append(wx.MenuItem(fileMenu, id=11, text="5", kind=wx.ITEM_RADIO))
        fpsMenu.Append(wx.MenuItem(fileMenu, id=12, text="10", kind=wx.ITEM_RADIO))
        fpsMenu.Append(wx.MenuItem(fileMenu, id=13, text="15", kind=wx.ITEM_RADIO))
        fpsMenu.Append(wx.MenuItem(fileMenu, id=14, text="20", kind=wx.ITEM_RADIO))
        fpsMenu.Append(wx.MenuItem(fileMenu, id=15, text="30", kind=wx.ITEM_RADIO))

        fileMenu.Append(wx.ID_ANY, "FPS", fpsMenu)

        menuBar.Append(fileMenu, title="Setting")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.service.menu_event)

    def updateMessage(self, msg):
        self.feedbackMessage.SetLabel("Message: "+msg)
        self.feedbackMessage.SetForegroundColour((0,0,0))

    def updateError(self, error):
        self.feedbackMessage.SetLabel("Error: "+error)
        self.feedbackMessage.SetForegroundColour((255,0,0))

    def updateFrame(self, cv2_frame, no):
        h, w = cv2_frame.shape[:2]
        self.display.SetBitmap(wx.Bitmap.FromBuffer(w, h, cv2_frame))
        self.videoFrame.SetLabel(str(no))

    def updateStartLabel(self, start):
        self.selectedStart.SetLabel(str(start))

    def updateEndLabel(self, end):
        self.selectedEnd.SetLabel(str(end))



class App(wx.App):
    """
        This is only for displaying the UI
    """

    def OnInit(self):
        a = Layout()
        a.Show()
        return True


if __name__ == '__main__':
    try:
        debug = App()
        debug.MainLoop()
    except:
        exit(0)
