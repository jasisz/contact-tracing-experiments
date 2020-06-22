# Copyright (c) 2017, Nordic Semiconductor ASA
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#    3. Neither the name of Nordic Semiconductor ASA nor the names of
#       its contributors may be used to endorse or promote products
#       derived from this software without specific prior written
#       permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL NORDIC
# SEMICONDUCTOR ASA OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import time, os, logging
from . import Logger

LINKTYPE_BLUETOOTH_LE_LL = 251
LINKTYPE_NORDIC_BLE = 157

MAGIC_NUMBER = 0xA1B2C3D4
VERSION_MAJOR = 2
VERSION_MINOR = 4
THISZONE = 0
SIGFIGS = 0
SNAPLEN = 0xFFFF
NETWORK = LINKTYPE_NORDIC_BLE


globalHeaderString = [
    ((MAGIC_NUMBER >> 0) & 0xFF),
    ((MAGIC_NUMBER >> 8) & 0xFF),
    ((MAGIC_NUMBER >> 16) & 0xFF),
    ((MAGIC_NUMBER >> 24) & 0xFF),
    ((VERSION_MAJOR >> 0) & 0xFF),
    ((VERSION_MAJOR >> 8) & 0xFF),
    ((VERSION_MINOR >> 0) & 0xFF),
    ((VERSION_MINOR >> 8) & 0xFF),
    ((THISZONE >> 0) & 0xFF),
    ((THISZONE >> 8) & 0xFF),
    ((THISZONE >> 16) & 0xFF),
    ((THISZONE >> 24) & 0xFF),
    ((SIGFIGS >> 0) & 0xFF),
    ((SIGFIGS >> 8) & 0xFF),
    ((SIGFIGS >> 16) & 0xFF),
    ((SIGFIGS >> 24) & 0xFF),
    ((SNAPLEN >> 0) & 0xFF),
    ((SNAPLEN >> 8) & 0xFF),
    ((SNAPLEN >> 16) & 0xFF),
    ((SNAPLEN >> 24) & 0xFF),
    ((NETWORK >> 0) & 0xFF),
    ((NETWORK >> 8) & 0xFF),
    ((NETWORK >> 16) & 0xFF),
    ((NETWORK >> 24) & 0xFF),
]

DEFAULT_CAPTURE_FILE_DIR = Logger.DEFAULT_LOG_FILE_DIR
DEFAULT_CAPTURE_FILE_NAME = "capture.pcap"


def get_capture_file_path(capture_file_path=None):
    default_path = os.path.join(DEFAULT_CAPTURE_FILE_DIR, DEFAULT_CAPTURE_FILE_NAME)
    if capture_file_path is None:
        return default_path
    if os.path.splitext(capture_file_path)[1] != ".pcap":
        return default_path
    return os.path.abspath(capture_file_path)


class CaptureFileHandler:
    def __init__(self, capture_file_path=None, clear=False):
        filename = get_capture_file_path(capture_file_path)
        if not os.path.isdir(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        self.filename = filename
        self.backupFilename = self.filename + ".1"
        if not os.path.isfile(self.filename):
            self.startNewFile()
        elif os.path.getsize(self.filename) > 20000000:
            self.doRollover()
        if clear:
            # clear file
            self.startNewFile()

    def startNewFile(self):
        with open(self.filename, "wb") as f:
            f.write(bytes(globalHeaderString))

    def doRollover(self):
        try:
            os.remove(self.backupFilename)
        except:
            logging.exception("capture file rollover remove backup failed")
        try:
            os.rename(self.filename, self.backupFilename)
            self.startNewFile()
        except:
            logging.exception("capture file rollover failed")

    def readLine(self, lineNum):
        line = ""
        with open(self.filename, "r") as f:
            f.seek(lineNum)
            line = f.readline()
        return line

    def readAll(self):
        text = ""
        with open(self.filename, "r") as f:
            text = f.read()
        return text

    def writeString(self, msgString):
        with open(self.filename, "ab") as f:
            f.write(msgString.encode("utf-8"))

    def writePacket(self, packet):
        packetList = [packet.boardId] + packet.getList()
        packetHeader = self.makePacketHeader(len(packetList), packet.time)
        self.writeString(toString(packetHeader + packetList))

    def makePacketHeader(self, length, timestamp):
        TS_SEC = int(timestamp)
        TS_USEC = int((timestamp - int(timestamp)) * 1_000_000)
        INCL_LENGTH = length
        ORIG_LENGTH = length

        headerString = [
            ((TS_SEC >> 0) & 0xFF),
            ((TS_SEC >> 8) & 0xFF),
            ((TS_SEC >> 16) & 0xFF),
            ((TS_SEC >> 24) & 0xFF),
            ((TS_USEC >> 0) & 0xFF),
            ((TS_USEC >> 8) & 0xFF),
            ((TS_USEC >> 16) & 0xFF),
            ((TS_USEC >> 24) & 0xFF),
            ((INCL_LENGTH >> 0) & 0xFF),
            ((INCL_LENGTH >> 8) & 0xFF),
            ((INCL_LENGTH >> 16) & 0xFF),
            ((INCL_LENGTH >> 24) & 0xFF),
            ((ORIG_LENGTH >> 0) & 0xFF),
            ((ORIG_LENGTH >> 8) & 0xFF),
            ((ORIG_LENGTH >> 16) & 0xFF),
            ((ORIG_LENGTH >> 24) & 0xFF),
        ]
        return headerString


def toString(myList):
    myString = ""
    for i in myList:
        try:
            myString += chr(i)
        except ValueError:
            logging.exception("byte: %d, list: %s" % (i, str(myList)))
        except:
            logging.exception("byte: %d, list: %s" % (i, str(myList)))
            raise
    return myString


def toList(myString):
    myList = []
    for c in myString:
        myList += [ord(c)]
    return myList
