#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import os

class Paths():
    _ydlname = ''
    _ydlpath = ''
    _ydllocation = ''

    def __init__(self):
        if (os.name == 'nt'):
            self._ydlname = 'youtube-dl.exe'
            self._ydlpath = os.environ['APPDATA'] + '\\ydlss'
            self._ydllocation = self._ydlpath + '\\' + self._ydlname
        else:
            self._ydlname = 'youtube-dl'
            self._ydlpath = os.path.expanduser('~') + '/.config/ydlss'
            self._ydllocation = self._ydlpath + '/' + self._ydlname

    def getYdlName(self):
        return self._ydlname

    def getYdlPath(self):
        return self._ydlpath

    def getYdlLocation(self):
        return self._ydllocation
