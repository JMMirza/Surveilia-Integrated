# Surveilia-Integrated
This repository contain my FYP project, which is real time anomaly detection. We have used TSM-Model for this which is implemented on PyTorch and for Graphical User Interface we have used PyQt5. So the basic Libaries required for that are:
"import datetime
import sys
import os
import urllib.request
import xlrd
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
import os"
