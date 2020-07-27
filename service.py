"""
    @author Pengnan Fan
    @date Jul 13, 2020

    This is a helping file storing service triggered by interaction with UI

"""
import os
import os.path as osp
import cv2
import pandas as pd
from pandas import DataFrame as df

class Service:
    def __init__(self, ui):
        self.ui = ui
        self.dataset_path = None
        self.store_path = None
        self.fps = 5
        self.videoLists = list()
        self.currVideo = None
        self.cap = None
        self.totFrame = 0
        self.currFrame = 0
        self.labelStart = 0
        self.labelEnd = 0
        self.type = None
        self.actionType = "tripping"

    def updateInputInfo(self, data_path, store_path):
        if osp.exists(data_path):
            self.dataset_path = data_path
            self.ui.updateMessage("Dataset path is updated")
        else:
            self.ui.updateError("Invalid dataset path: {}".format(data_path))
            return

        if osp.exists(store_path):
            self.store_path = store_path
            self.ui.updateMessage("Store path is updated")
        else:
            self.ui.updateError("Invalid store path: {}".format(store_path))

        self.updateVideoLists()


    def getSelectedVideo(self, evt):
        return evt.GetString()


    def updateVideoLists(self):

        if osp.exists(self.dataset_path):
            self.videoLists = sorted(list(filter(lambda x: x[-4:] in ['.avi', '.wav', '.mp4'], os.listdir(self.dataset_path))))
            self.ui.selectVideo.SetItems(self.videoLists)
        else:
            self.ui.updateError("Please enter a valid dataset path.")

    def loadVideo(self):
        totVideo = len(self.videoLists)
        self.currVideo = totVideo if self.currVideo > totVideo else self.currVideo
        self.currVideo = 0 if self.currVideo < 0 else self.currVideo
        self.ui.selectVideo.Selection = self.currVideo
        self.cap = cv2.VideoCapture(osp.join(self.dataset_path, self.videoLists[self.currVideo]))
        self.totFrame = int(self.cap.get(7))
        self.currFrame = 0
        self.labelStart = 0
        self.labelEnd = 0
        self.ui.updateStartLabel(0)
        self.ui.updateEndLabel(0)
        self.type = None
        self.ui.videoFrame.SetLabel("0")
        self.updateFrameN()
        self.ui.updateMessage("Select video: {}".format(self.videoLists[self.currVideo]))

    def updateFrameN(self):
        if self.cap:
            self.currFrame = self.totFrame if self.currFrame > self.totFrame else self.currFrame
            self.currFrame = 0 if self.currFrame < 0 else self.currFrame
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.currFrame)
            ret, frame = self.cap.read()
            if ret:
                self.ui.updateFrame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), self.currFrame)
            else:
                self.ui.updateError("This is an empty video: {}".format(self.currVideo))

    def button_event(self, e, evt_id):
        # print(evt_id)
        if evt_id == "prevVideo":
            self.currVideo -= 1
            self.loadVideo()
        elif evt_id == "prevNFrame":
            self.currFrame -= self.fps
            self.updateFrameN()
        elif evt_id == "prevFrame":
            self.currFrame -= 1
            self.updateFrameN()
        elif evt_id == "start":
            self.ui.updateMessage("Select start")
        elif evt_id == "end":
            self.ui.updateMessage("Select end")
        elif evt_id == "nextFrame":
            self.currFrame += 1
            self.updateFrameN()
        elif evt_id == "nextNFrame":
            self.currFrame += self.fps
            self.updateFrameN()
        elif evt_id == "nextVideo":
            self.currVideo += 1
            self.loadVideo()
        elif evt_id == "confirm_input":
            self.updateInputInfo(self.ui.datasetInput.GetValue(), self.ui.storeInput.GetValue())
        elif evt_id == "selectStart":
            self.labelStart = self.currFrame
            self.ui.updateStartLabel(int(self.currFrame))
            self.ui.updateMessage("Select frame {} as start of labeling".format(self.currFrame))
        elif evt_id == "selectEnd":
            self.labelEnd = self.currFrame
            self.ui.updateEndLabel(int(self.currFrame))
            self.ui.updateMessage("Select frame {} as end of labeling".format(self.currFrame))
        elif evt_id == "selectVideo":
            self.currVideo = self.ui.selectVideo.Selection
            self.loadVideo()
        elif evt_id == "selectClose":
            self.storeLabel("close")
        elif evt_id == "selectMid":
            self.storeLabel("mid")
        elif evt_id == "selectFar":
            self.storeLabel("far")
        elif evt_id == "saveLabel":
            self.saveLabel()
        elif evt_id == "selectAction":
            self.actionType = e.GetString()
            self.ui.updateMessage("Action Type: {} is selected.".format(self.actionType))
        else:
            self.ui.updateError("Unsupported Button")

        self.ui.Refresh()

    def updateFPS(self, fps):
        self.fps = fps
        self.ui.updateMessage("FPS is updated as: {}".format(fps))

    def menu_event(self, event):
        id = event.GetId()
        if id == 11:
            self.updateFPS(5)
        elif id == 12:
            self.updateFPS(10)
        elif id == 13:
            self.updateFPS(15)
        elif id == 14:
            self.updateFPS(20)
        elif id == 15:
            self.updateFPS(30)
        else:
            raise NotImplemented

    def readLabel(self):
        if self.labelStart < self.labelEnd:
            label = df({"video":[self.videoLists[self.currVideo]],"start_frame":[self.labelStart],"end_frame":[self.labelEnd],"type":[self.type],"action":[self.actionType]})
            msg = "{} action [{}, {}] is recorded".format(self.actionType.upper(), self.labelStart, self.labelEnd)
            if self.type:
                msg += " as {} shot".format(self.type)
            self.ui.updateMessage(msg)
            return label
        else:
            self.ui.updateError("Action [{},{}] is NOT recorded: start should be less than end".format(self.labelStart, self.labelEnd))
            return None

    def storeLabel(self, type=None):
        self.type = type
        self.ui.updateMessage("Action type is selected as {}".format(type))

    def saveLabel(self):
        label = self.readLabel()
        if label is not None:
            result_path = osp.join(self.store_path, osp.basename(self.dataset_path).replace(" ", "_")+"_labels.csv")
            if osp.exists(result_path):
                old_data = pd.read_csv(result_path)
                label = pd.concat([old_data, label], axis=0, sort=False)
            label.to_csv(result_path, index=False)
        else:
            self.ui.updateError("No action selected")
