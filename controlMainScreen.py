import datetime
import sys
import os
import urllib.request
import xlrd
import pandas as pd
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw, QtWidgets, QtCore
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import QUrl, QDir, QTimer, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog, QStyle
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from surveiliaFrontEnd import Ui_surveiliaFrontEnd
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtWidgets import QFileDialog, QStyle
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import sys
import cv2
import numpy as np
import argparse
from PIL import Image
import torchvision
import torch.nn.parallel
import torch.optim
from tsm_model.ops.models import TSN
from tsm_model.ops.transforms import *
from torch.nn import functional as F
import os
from threading import Thread
import time
import csv
import glob
import os


class ControlMainWindow(qtw.QMainWindow, Ui_surveiliaFrontEnd):
    counter = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.logic = 0
        self.camSignal = 0
        self.mainStackedWidget.setCurrentIndex(0)
        self.menuStackedWidget.setCurrentIndex(0)

        ####################### MAIN STACKED WIDGET ###############################################
        # self.login1_pushButton.clicked.connect(lambda: self.mainStackedWidget.setCurrentIndex(1))
        self.logout_toolButton.clicked.connect(
            lambda: self.mainStackedWidget.setCurrentIndex(2)
        )
        self.loginAgain_pushButton_3.clicked.connect(
            lambda: self.mainStackedWidget.setCurrentIndex(0)
        )

        ######################## MENU STACKED WIDGET ##############################################
        self.logo_toolButton.clicked.connect(
            lambda: self.menuStackedWidget.setCurrentIndex(0)
        )
        self.getStarted_pushButton_2.clicked.connect(
            lambda: self.menuStackedWidget.setCurrentIndex(1)
        )
        self.camera_toolButton.clicked.connect(
            lambda: self.menuStackedWidget.setCurrentIndex(1)
        )
        self.alarm_toolButton.clicked.connect(
            lambda: self.menuStackedWidget.setCurrentIndex(2)
        )
        self.storage_toolButton.clicked.connect(
            lambda: self.menuStackedWidget.setCurrentIndex(3)
        )
        self.account_toolButton.clicked.connect(
            lambda: self.menuStackedWidget.setCurrentIndex(4)
        )
        self.users_toolButton.clicked.connect(
            lambda: self.menuStackedWidget.setCurrentIndex(5)
        )
        self.userAdd_pushButton.clicked.connect(
            lambda: self.menuStackedWidget.setCurrentIndex(6)
        )
        self.language_toolButton.clicked.connect(
            lambda: self.menuStackedWidget.setCurrentIndex(8)
        )

        ##########################CAMERA PAGE####################################################
        self.cam02_pushButton.hide()
        self.cam03_pushButton.hide()
        self.cam04_pushButton.hide()
        self.cam05_pushButton.hide()
        self.cam06_pushButton.hide()

        self.display_2.hide()
        self.display_3.hide()
        self.display_4.hide()
        self.display_5.hide()
        self.display_6.hide()

        self.addNew_pushButton.clicked.connect(self.addNewCamera)
        self.cancel_pushButton_3.clicked.connect(self.close)
        self.flag = 0

        self.cam01_pushButton.clicked.connect(self.cam1clicked)
        self.cam02_pushButton.clicked.connect(self.cam2clicked)
        self.cam03_pushButton.clicked.connect(self.cam3clicked)
        self.cam04_pushButton.clicked.connect(self.cam4clicked)
        self.cam05_pushButton.clicked.connect(self.cam5clicked)
        self.cam06_pushButton.clicked.connect(self.cam6clicked)

        ##########################PAGE 7####################################################
        self.openDir_pushButton.clicked.connect(self.openFile)
        self.addIPCam_pushButton.clicked.connect(self.openIPcam)
        self.openWebcam_pushButton.clicked.connect(self.openWebcam)
        self.cancel_PushButton.clicked.connect(
            lambda: self.menuStackedWidget.setCurrentIndex(1)
        )

        self.english_radioButton.toggled.connect(self.changeLanguagetoEnglish)
        self.urdu_radioButton.toggled.connect(self.changeLanguagetoUrdu)
        self.logout_toolButton.clicked.connect(self.changeLanguagetoEnglish)
        ######################## OPEN AND PLAY VIDEO ###############################################
        # create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # pass the widget where the video will be displayed
        # self.mediaPlayer.setVideoOutput(self.videoDisplay_widget1)

        #######################LOGIN###########################################
        self.login1_pushButton.clicked.connect(self.Login)
        self.alarm_toolButton.clicked.connect(self.anomaly_tableDetail)

    # Record Anaomlous event to a file
    def getStatsOfAbnormalActivity(self, cameraID):
        x = datetime.datetime.now()
        with open("./appData/Details.csv", mode="a") as csv_file:
            fieldnames = ["CameraID", "Event", "Date", "Time"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if csv_file.tell() == 0:
                writer.writeheader()
            date = str(x.strftime("%A") + "/" + str(x.date()))
            time = str(x.strftime("%H:%M:%S"))

            writer.writerow(
                {"CameraID": cameraID, "Event": "Abnormal", "Date": date, "Time": time}
            )

    ######################READ CSV FILE TO DISPLAY DATA IN QTABLEWIDGET###################

    def anomaly_tableDetail(self):
        self.menuStackedWidget.setCurrentIndex(2)
        read_file = pd.read_csv(r"./appData/Details.csv")
        read_file.to_excel(r"./appData/Details.xlsx", index=None, header=True)

        self.anomaly_details = xlrd.open_workbook("./appData/Details.xlsx")
        self.sheet = self.anomaly_details.sheet_by_index(0)
        self.data = [
            [self.sheet.cell_value(r, c) for c in range(self.sheet.ncols)]
            for r in range(self.sheet.nrows)
        ]
        # print(self.data)
        self.alarm_tableWidget.setColumnCount(4)
        self.alarm_tableWidget.setRowCount(
            self.sheet.nrows - 1
        )  # same no.of rows as of csv file
        for row, columnvalues in enumerate(self.data):
            for column, value in enumerate(columnvalues):
                self.item = QtWidgets.QTableWidgetItem(
                    str(value)
                )  # str is to also display the integer values
                self.alarm_tableWidget.setItem(row - 1, column, self.item)
                # to set the elements read only
                self.item.setFlags(QtCore.Qt.ItemIsEnabled)

    def tsmmodel(self, f, check):

        # os.environ[""] = "0"

        emptyString = ""

        print()
        print("======>>>>> Loading model ... Please wait ...")

        # just adding some comments to check git
        def parse_shift_option_from_log_name(log_name):
            if "shift" in log_name:
                strings = log_name.split("_")
                for i, s in enumerate(strings):
                    if "shift" in s:
                        break
                return True, int(strings[i].replace("shift", "")), strings[i + 1]
            else:
                return False, None, None

        # args = parser.parse_args()

        this_weights = "tsm_model/checkpoint/TSM_ucfcrime_RGB_mobilenetv2_shift8_blockres_avg_segment8_e50/ckpt.best.pth.tar"
        # this_weights = 'checkpoint/TSM_ucfcrime_RGB_resnet50_shift8_blockres_avg_segment8_e25/ckpt.best.pth.tar'
        is_shift, shift_div, shift_place = parse_shift_option_from_log_name(
            this_weights
        )
        modality = "RGB"
        if "RGB" in this_weights:
            modality = "RGB"

        # Get dataset categories.
        categories = ["Normal Activity", "Abnormal Activity"]
        num_class = len(categories)
        # this_arch = 'resnet50'
        this_arch = "mobilenetv2"

        net = TSN(
            num_class,
            1,
            modality,
            base_model=this_arch,
            consensus_type="avg",
            img_feature_dim="225",
            # pretrain=args.pretrain,
            is_shift=is_shift,
            shift_div=shift_div,
            shift_place=shift_place,
            non_local="_nl" in this_weights,
        )

        checkpoint = torch.load(this_weights, map_location=torch.device("cpu"))
        # checkpoint = torch.load(this_weights)

        checkpoint = checkpoint["state_dict"]

        # base_dict = {('base_model.' + k).replace('base_model.fc', 'new_fc'): v for k, v in list(checkpoint.items())}
        base_dict = {".".join(k.split(".")[1:]): v for k, v in list(checkpoint.items())}
        replace_dict = {
            "base_model.classifier.weight": "new_fc.weight",
            "base_model.classifier.bias": "new_fc.bias",
        }
        for k, v in replace_dict.items():
            if k in base_dict:
                base_dict[v] = base_dict.pop(k)

        net.load_state_dict(base_dict)
        # net.cuda().eval()
        net.eval()
        transform = torchvision.transforms.Compose(
            [
                Stack(roll=(this_arch in ["BNInception", "InceptionV3"])),
                ToTorchFormatTensor(
                    div=(this_arch not in ["BNInception", "InceptionV3"])
                ),
                GroupNormalize(net.input_mean, net.input_std),
            ]
        )
        try:
            os.makedirs("./appData/Anoamly_Clips")
            os.makedirs("./appData/Anoamly_Images")
        except OSError as e:
            pass

        print("loading Video...")
        if f == emptyString:
            print("cam")
            cap = cv2.VideoCapture(cv2.CAP_DSHOW)
        else:
            print("cam")
            cap = cv2.VideoCapture(f)

        i_frame = -1
        count = 0
        print("Ready!")
        writer = None
        c = 0

        while cap.isOpened():
            count += 1
            i_frame += 1
            ret, img = cap.read()  # (480, 640, 3) 0 ~ 255

            # release everything when job is finished

            if ret:
                if (
                    i_frame % 3 == 0
                ):  # skip every other frame to obtain a suitable frame rate
                    t1 = time.time()

                    img_tran = transform([Image.fromarray(img).convert("RGB")])

                    input = img_tran.view(
                        -1, 3, img_tran.size(1), img_tran.size(2)
                    ).unsqueeze(0)

                    with torch.no_grad():
                        logits = net(input)

                        h_x = torch.mean(F.softmax(logits, 1), dim=0).data

                        print(h_x)

                        pr, li = h_x.sort(0, True)

                        probs = pr.tolist()

                        idx = li.tolist()

                        t2 = time.time()
                        print(count, "-", categories[idx[0]], "Prob: ", probs[0])

                        current_time = t2 - t1
                dim = (420, 420)
                img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                height, width, _ = img.shape
                # height, width, _ = img.shape

                # label = np.ones([height // 10, width, 3]).astype("uint8") + 255

                if categories[idx[0]] == "Abnormal Activity":
                    R = 255
                    G = 0
                    print("\007")
                    Abnormality = True
                    c += 1
                else:
                    R = 0
                    G = 255
                    Abnormality = False

                cv2.putText(
                    img,
                    "Stream: " + str(check) + " " + categories[idx[0]],
                    (20, int(height / 16)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, int(G), int(R)),
                    2,
                )

                cv2.putText(
                    img,
                    "Accuracy: {:.2f}%".format(probs[0] * 100, "%"),
                    (20, int(height / 9)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, int(G), int(R)),
                    2,
                )
                cv2.putText(
                    img,
                    "FPS: {:.1f} Frame/s".format(1 / current_time),
                    (250, int(height / 9)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                )
                if writer is None:
                    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                    (H, W) = img.shape[:2]
                    path = "./appData/Anoamly_Clips/"
                    name = len(glob.glob(path + "*.avi"))

                    getVidName = path + "Abnormal_Event_{}_Cam_{}.avi".format(
                        name + 1, check
                    )
                    writer = cv2.VideoWriter(getVidName, fourcc, 30.0, (W, H), True)

                # Saving Anaomlous Event Image and Clip
                if Abnormality:
                    writer.write(img)
                    # record stat every two seconds if exists
                    if c % 60 == 0:
                        self.getStatsOfAbnormalActivity(check)
                        # if tempThres > 0.75:

                        path = "./appData/Anoamly_Images/"
                        index = len(glob.glob(path + "*.jpg"))
                        # imageName = getFileName(path+'.jpg')
                        imageName = path + "Abnormal_Event_{}_Cam_{}.jpg".format(
                            index + 1, check
                        )
                        cv2.imwrite(imageName, img)

                    # image_frame = np.concatenate((img, label), axis=0)

                if ret == True:
                    if check == 1:
                        dim = (self.display_1.width(), self.display_1.height())
                        img1 = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                        height, width, _ = img1.shape
                        bytesPerLine = 3 * width
                        img1 = qtg.QImage(
                            img1.data,
                            width,
                            height,
                            bytesPerLine,
                            qtg.QImage.Format_RGB888,
                        ).rgbSwapped()
                        self.display_1.setPixmap(qtg.QPixmap.fromImage(img1))

                    elif check == 2:
                        dim = (self.display_1.width(), self.display_1.height())
                        img2 = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                        height, width, _ = img2.shape
                        bytesPerLine = 3 * width
                        img2 = qtg.QImage(
                            img2.data,
                            width,
                            height,
                            bytesPerLine,
                            qtg.QImage.Format_RGB888,
                        ).rgbSwapped()
                        self.display_2.setPixmap(qtg.QPixmap.fromImage(img2))
                        # self.camSignal = 0

                    elif check == 3:
                        dim = (self.display_1.width(), self.display_1.height())
                        img3 = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                        height, width, _ = img3.shape
                        bytesPerLine = 3 * width
                        img3 = qtg.QImage(
                            img3.data,
                            width,
                            height,
                            bytesPerLine,
                            qtg.QImage.Format_RGB888,
                        ).rgbSwapped()
                        self.display_3.setPixmap(qtg.QPixmap.fromImage(img3))
                        # self.camSignal = 0

                    elif check == 4:
                        dim = (self.display_1.width(), self.display_1.height())
                        img4 = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                        height, width, _ = img4.shape
                        bytesPerLine = 3 * width
                        img4 = qtg.QImage(
                            img4.data,
                            width,
                            height,
                            bytesPerLine,
                            qtg.QImage.Format_RGB888,
                        ).rgbSwapped()
                        self.display_4.setPixmap(qtg.QPixmap.fromImage(img4))
                        # self.camSignal = 0

                    elif check == 5:
                        dim = (self.display_1.width(), self.display_1.height())
                        img5 = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                        height, width, _ = img5.shape
                        bytesPerLine = 3 * width
                        img5 = qtg.QImage(
                            img5.data,
                            width,
                            height,
                            bytesPerLine,
                            qtg.QImage.Format_RGB888,
                        ).rgbSwapped()
                        self.display_5.setPixmap(qtg.QPixmap.fromImage(img5))
                        # self.camSignal = 0

                    elif check == 6:
                        dim = (self.display_1.width(), self.display_1.height())
                        img6 = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                        height, width, _ = img6.shape
                        bytesPerLine = 3 * width
                        img6 = qtg.QImage(
                            img6.data,
                            width,
                            height,
                            bytesPerLine,
                            qtg.QImage.Format_RGB888,
                        ).rgbSwapped()
                        self.display_6.setPixmap(qtg.QPixmap.fromImage(img6))
                        # self.camSignal = 0
                else:
                    print("Else not found")

            else:
                cap.release()
                cv2.destroyAllWindows()

    def Login(self):

        self.excel = xlrd.open_workbook("UsersList.xlsx")
        self.sheet1 = self.excel.sheet_by_index(0)

        for row in range(self.sheet1.nrows):

            cellID = str(self.sheet1.cell(row, 0))
            cellID = cellID.lstrip(":'text")  # to get data before text
            cellID = cellID.rstrip("'")

            cellUserName = str(self.sheet1.cell(row, 1))
            cellUserName = cellUserName.lstrip(":'text")
            cellUserName = cellUserName.rstrip("'")

            cellPassword = str(self.sheet1.cell_value(row, 2))
            cellPassword = cellPassword.lstrip(":'text")
            cellPassword = cellPassword.rstrip("'")

            Name = str(self.username1_field.text())
            Password = str(self.password1_field.text())

            if cellUserName == Name:
                print("HERE")
                if Password == cellPassword:
                    print("login successful")
                    self.mainStackedWidget.setCurrentIndex(1)
                    break
                else:
                    print("INVALID USERNAME OR PASSWORD")

            else:
                print("still in else")

    def cam1clicked(self):
        self.camSignal = 1
        self.menuStackedWidget.setCurrentIndex(7)

    def cam2clicked(self):
        self.camSignal = 2
        self.menuStackedWidget.setCurrentIndex(7)

    def cam3clicked(self):
        self.camSignal = 3
        self.menuStackedWidget.setCurrentIndex(7)

    def cam4clicked(self):
        self.camSignal = 4
        self.menuStackedWidget.setCurrentIndex(7)

    def cam5clicked(self):
        self.camSignal = 5
        self.menuStackedWidget.setCurrentIndex(7)

    def cam6clicked(self):
        self.camSignal = 6
        self.menuStackedWidget.setCurrentIndex(7)

    # METHOD TO OPEN THE IP CAM THROUGH IP ADDRESS
    def openIPcam(self):
        self.input = 0
        url = str(self.addIPCam_field.text())
        self.menuStackedWidget.setCurrentIndex(1)
        t = Thread(target=self.tsmmodel, args=(url, self.camSignal))
        t.start()
        cv2.waitKey(10)

    # cv2.waitKey(10)

    # METHOD TO OPEN WEB CAM
    @pyqtSlot()
    def openWebcam(self):
        self.input = 0
        self.logic = 1
        cap = 0
        self.menuStackedWidget.setCurrentIndex(1)
        t1 = Thread(target=self.tsmmodel, args=(cap, self.camSignal))
        t1.start()
        # release everything when job is finished

    # METHOD TO DISPLAY VIDEO(IMAGE BY IMAGE) IN THE BOX
    """def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        pix = qtg.QPixmap.fromImage(img)
        # pix = pix.scaled(self.display_1.width(), self.display_1.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        pix = pix.scaled(
            600, 450, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        if self.camSignal == 1:

            self.display_1.setPixmap(pix)
            # self.camSignal = 0

        elif self.camSignal == 2:
            self.display_2.setPixmap(pix)
            # self.camSignal = 0

        elif self.camSignal == 3:
            # pix = pix.scaled(self.display_3.width(), self.display_3.height(), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
            self.display_3.setPixmap(pix)
            # self.camSignal = 0

        elif self.camSignal == 4:
            # pix = pix.scaled(self.display_4.width(), self.display_4.height(), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
            self.display_4.setPixmap(pix)
            # self.camSignal = 0

        elif self.camSignal == 5:
            # pix = pix.scaled(self.display_5.width(), self.display_5.height(), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
            self.display_5.setPixmap(pix)
            # self.camSignal = 0

        elif self.camSignal == 6:
            # pix = pix.scaled(self.display_6.width(), self.display_6.height(), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
            self.display_6.setPixmap(pix)
            # self.camSignal = 0"""

    # METHOD TO OPEN FILE DIALOG
    def openFile(self):
        self.input = 0
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Video", "", "Video Files (*.mp4 *.flv *.ts *.mts *.avi *.wmv)"
        )
        t2 = Thread(target=self.tsmmodel, args=(fileName, self.camSignal))

        if fileName != "":
            # self.displayImage(fileName, 1)
            t2.start()
        else:
            print("NO FILE FOUND")
        # display_1.play()
        self.menuStackedWidget.setCurrentIndex(1)

    # METHOD TO ADD NEW CAMERAS
    def addNewCamera(self):
        if self.cam02_pushButton.isHidden():
            self.cam02_pushButton.show()
            self.display_2.show()
        elif self.cam03_pushButton.isHidden():
            self.cam03_pushButton.show()
            self.display_3.show()
        elif self.cam04_pushButton.isHidden():
            self.cam04_pushButton.show()
            self.display_4.show()
        elif self.cam05_pushButton.isHidden():
            self.cam05_pushButton.show()
            self.display_5.show()
        elif self.cam06_pushButton.isHidden():
            self.cam06_pushButton.show()
            self.display_6.show()
        else:
            self.addNew_pushButton.setEnabled(False)
            self.addNew_pushButton.setStyleSheet("background-color: light grey ;\n")

            ############################TRANSLATE INTO URDU######################################
            # METHOD TO CHANGE LANGUAGE

    def changeLanguagetoUrdu(self):
        # self.title1_label.setText("سرویلیا")
        self.title_label.setText("سرویلیا")

        self.camera_toolButton.setText("کیمرہ")
        self.storage_toolButton.setText("اسٹوریج")
        self.logout_toolButton.setText("لاگ آوٹ")
        self.users_toolButton.setText("صارفین")
        self.language_toolButton.setText("زبان")
        self.logo_toolButton.setText("لاگ آوٹ")
        self.alarm_toolButton.setText("الارم لاگ")
        self.account_toolButton.setText("اکاؤنٹ")
        self.title_label.setText("سرویلیا")
        self.welcome_label.setText("سرویلیا میں خوش آمدید")
        self.getStarted_pushButton_2.setText("آو شروع کریں")
        self.cameras_label.setText("کیمرے")
        self.cam01_pushButton.setText("کیمرہ_01")
        self.cam03_pushButton.setText("کیمرہ_03")
        self.cam02_pushButton.setText("کیمرہ_02")
        self.cam04_pushButton.setText("کیمرہ_04")
        self.cam05_pushButton.setText("کیمرہ_05")
        self.cam06_pushButton.setText("کیمرہ_06")
        self.addNew_pushButton.setText("نیا شامل کریں")
        self.showAll_pushButton.setText("سب دکھائیں")
        self.alarmHistory_label.setText("الارم کی حسٹری")

        self.alarm_tableWidget.horizontalHeaderItem(0).setText(" ID کیمرہ ")
        self.alarm_tableWidget.horizontalHeaderItem(1).setText("وقت")
        self.alarm_tableWidget.horizontalHeaderItem(2).setText("الارم کی تفصیل")
        self.alarm_tableWidget.horizontalHeaderItem(3).setText("اناملی کلپ")
        self.storage_label.setText("اسٹوریج")
        self.show_label.setText("دکھائیں        ")
        self.anomalyClip_checkBox.setText("اناملی کلپ")
        self.cameraFeed_checkBox.setText("کیمرا فیڈ")

        self.storage_tableWidget.horizontalHeaderItem(0).setText("فائل کا نام")
        self.storage_tableWidget.horizontalHeaderItem(1).setText("تاریخ")
        self.storage_tableWidget.horizontalHeaderItem(2).setText("سائز")
        self.accountInfo_label.setText("اکاؤنٹ کی معلومات")
        self.username_label.setText("صارف نام")
        self.username_lineEdit.setText("Ifrah Tehleel")
        self.password_label.setText("پاس ورڈ")
        self.password_lineEdit.setText("Ifrah")
        self.contactInfo_label.setText("رابطہ کی معلومات")
        self.contactInfo_lineEdit.setText("+923014474797")
        self.address_label.setText("پتہ")
        self.edit_pushButton.setText("ترمیم کریں")
        self.userInfo_label.setText("صارفین کی معلومات")
        self.userAdd_pushButton.setText("شامل کریں")
        self.userDelete_pushButton.setText("حذف کریں")

        self.user_tableWidget.horizontalHeaderItem(0).setText("نام")
        self.user_tableWidget.horizontalHeaderItem(1).setText("پاس ورڈ")
        self.user_tableWidget.horizontalHeaderItem(2).setText("رابطہ کی معلومات")
        self.user_tableWidget.horizontalHeaderItem(3).setText("پتہ")
        self.addUser_label.setText("نیا صارف شامل کریں")
        self.aUsername_label.setText("صارف نام")
        self.aPassword_label.setText("پاس ورڈ")
        self.aContactInfo_label.setText("رابطہ کی معلومات")
        self.aAddress_label.setText("پتہ")
        self.aEdit_pushButton.setText("نیا صارف شامل کریں")
        """
        self.label.setText("IP ایڈریس کا استعمال کرتے ہوئے کیمرا شامل کریں")
        self.addIPCam_field.setText("IP ایڈریس یہاں داخل کریں")
        self.addIPCam_pushButton.setText("شامل کریں")
        self.label_2.setText("ڈائریکٹری سے فائل کے ذریعہ ویڈیو شامل کریں")
        self.openDir_pushButton.setText("کھولیں")
        self.label_3.setText("ویب کیم کا استعمال کرتے ہوئے شامل کریں")
        self.openWebcam_pushButton.setText("ویب کیم کھولیں")
        self.cancel_PushButton.setText("منسوخ کریں")
        """
        self.english_radioButton.setText("English")
        self.chooseLanguage_label.setText("زبان کا انتخاب کریں:")
        self.urdu_radioButton.setText("Urdu")
        self.title3_label.setText("سرویلیا")
        self.cancel_pushButton_3.setText("منسوخ کریں")
        self.loginAgain_pushButton_3.setText("دوبارہ لاگ ان")
        self.loggedOut_label_3.setText("آپ لاگ آؤٹ ہوچکے ہیں")

        ##########################TRANSLATE INTO ENGLISH###################################

    def changeLanguagetoEnglish(self):

        self.camera_toolButton.setText("Camera")
        self.storage_toolButton.setText("Storage")
        self.logout_toolButton.setText("Logout")
        self.users_toolButton.setText("Users")
        self.language_toolButton.setText("Language")
        self.logo_toolButton.setText("Logout")
        self.alarm_toolButton.setText("Alarm Log")
        self.account_toolButton.setText("Account")
        self.title_label.setText("SURVEILIA")
        self.welcome_label.setText("Welcome to SURVEILIA")
        self.getStarted_pushButton_2.setText("GET STARTED")
        self.cameras_label.setText("CAMERAS")
        self.cam01_pushButton.setText("CAMERA_01")
        self.cam03_pushButton.setText("CAMERA_03")
        self.cam02_pushButton.setText("CAMERA_02")
        self.cam04_pushButton.setText("CAMERA_04")
        self.cam05_pushButton.setText("CAMERA_05")
        self.cam06_pushButton.setText("CAMERA_06")
        self.addNew_pushButton.setText("ADD NEW")
        self.showAll_pushButton.setText("SHOW ALL")
        self.alarmHistory_label.setText("ALARM HISTORY")

        self.alarm_tableWidget.horizontalHeaderItem(0).setText("Camera ID")
        self.alarm_tableWidget.horizontalHeaderItem(1).setText("Time")
        self.alarm_tableWidget.horizontalHeaderItem(2).setText("Alarm Description")
        self.alarm_tableWidget.horizontalHeaderItem(3).setText("Anomaly Clip")
        self.storage_label.setText("STORAGE")
        self.show_label.setText("           Show:")
        self.anomalyClip_checkBox.setText("Anomaly Clip")
        self.cameraFeed_checkBox.setText("Camera Feed")

        self.storage_tableWidget.horizontalHeaderItem(0).setText("Filename")
        self.storage_tableWidget.horizontalHeaderItem(1).setText("Date")
        self.storage_tableWidget.horizontalHeaderItem(2).setText("Size")
        self.accountInfo_label.setText("ACCOUNT INFORMATION")
        self.username_label.setText("Username:")
        self.username_lineEdit.setText("Ifrah Tehleel")
        self.password_label.setText("Password:")
        self.password_lineEdit.setText("Ifrah")
        self.contactInfo_label.setText("Contact Info:")
        self.contactInfo_lineEdit.setText("+923014474797")
        self.address_label.setText("Address:")
        self.edit_pushButton.setText("EDIT")
        self.userInfo_label.setText("  USERS INFORMATION")
        self.userAdd_pushButton.setText("ADD")
        self.userDelete_pushButton.setText("DELETE")

        self.user_tableWidget.horizontalHeaderItem(0).setText("Name")
        self.user_tableWidget.horizontalHeaderItem(1).setText("Password")
        self.user_tableWidget.horizontalHeaderItem(2).setText("Contact Info")
        self.user_tableWidget.horizontalHeaderItem(3).setText("Address")
        self.addUser_label.setText("ADD NEW USER")
        self.aUsername_label.setText("Username:")
        self.aPassword_label.setText("Password:")
        self.aContactInfo_label.setText("Contact Info:")
        self.aAddress_label.setText("Address:")
        self.aEdit_pushButton.setText("ADD USER")

        self.english_radioButton.setText("English")
        self.chooseLanguage_label.setText("Choose Language:")
        self.urdu_radioButton.setText("Urdu")
        self.title3_label.setText("SURVEILIA")
        self.cancel_pushButton_3.setText("CANCEL")
        self.loginAgain_pushButton_3.setText("LOGIN AGAIN")
        self.loggedOut_label_3.setText("You have been logged out!")


if __name__ == "__main__":
    app = qtw.QApplication([])
    widget = ControlMainWindow()
    widget.show()
    # sys.exit(app.exec_())
    app.exec_()
