# -*- coding: utf-8 -*-

import pLog, Parser


log = pLog.pLog()

class tvpvod:
    mode = 0
    def __init__(self):
        log.info("Starting TVP.VOD")
        self.parser = Parser.Parser()

    def handleService(self):
        params = self.parser.getParams()
