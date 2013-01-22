# -*- coding: utf-8 -*-
import re, os, sys, StringIO
from threading import Thread
import elementtree.ElementTree as ET
import xbmcaddon
import pLog

log = pLog.pLog()

scriptID = sys.modules[ "__main__" ].scriptID
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

dbg = ptv.getSetting('default_debug')


class SMTH:
    def __init__(self):
        self.conta
        self.failed = 0
        self.StreamIndex = 0
        

class Manifest:
    def __init__(self):
        #self.version = self.getVersion(manifest)
        #self.parser = ET.XMLParser(encoding="utf-8")
        pass
    
    def getVersion(self, manifest):
        if dbg == 'true':
            log.info('SMTH - getVersion() -> xml: ' + str(manifest))
        #parser = ET.XMLParser(encoding="utf-8")
        #elems = ET.parse(manifest, parser = parser).getroot()
        elems = ET.parse(manifest).getroot()
        return elems.attrib['MajorVersion']
    
    def getQualityLevel(self, manifest):
        video_quality = []
        audio_quality = []
        video_value = {}
        audio_value = {}
        #parser = ET.XMLParser(encoding="utf-8")
        #elems = ET.parse(manifest, parser = parser).getroot()
        elems = ET.parse(manifest).getroot()
        streams = elems.findall('.//StreamIndex')
        for i,s in enumerate(streams):
            stream_type = s.attrib["Type"]
            if stream_type == 'video':
                url_name = s.attrib["Url"]
                qualities = s.findall("QualityLevel")
                for i,q in enumerate(qualities):
                    bitrate = q.attrib["Bitrate"]
                    fourcc = q.attrib["FourCC"]
                    width = "0"
                    height = "0"
                    if self.getVersion(manifest) == "1":
                        width = q.attrib["Width"]
                        height = q.attrib["Height"]
                    elif self.getVersion(manifest) == "2":
                        width = q.attrib["MaxWidth"]
                        height = q.attrib["MaxHeight"]
                    video_value = { 
                              'bitrate': bitrate,
                              'fourcc': fourcc,
                              'width': width,
                              'height': height,
                              'url_name': url_name
                            }
                    video_quality.append(video_value)
            elif stream_type == 'audio':
                url_name = s.attrib["Url"]
                lang = 'None'
                subtype = 'None'
                if self.getVersion(manifest) == "1":
                    lang = 'None'
                elif self.getVersion(manifest) == "2":
                    lang = s.attrib["Language"]
                qualities = s.findall("QualityLevel")
                for i,q in enumerate(qualities):
                    bitrate = q.attrib["Bitrate"]
                    channels = 'None'
                    bits_per_sample = 'None'
                    sample_rate = 'None'
                    if self.getVersion(manifest) == "2":
                        channels = q.attrib["Channels"]
                        bits_per_sample = q.attrib["BitsPerSample"]
                        sample_rate = q.attrib["SamplingRate"]
                    audio_value = {
                               'bitrate': bitrate,
                               'language': lang,
                               'subtype': subtype,
                               'url_name': url_name,
                               'channels': channels,
                               'bits_per_sample': bits_per_sample,
                               'sample_rate': sample_rate
                        }
                    audio_quality.append(audio_value)
        return { 'video': video_quality, 'audio': audio_quality }

    def createChooseMenuTab(self, tab):
        out = []
        for i in range(len(tab)):
            #video: 1. H264, 1280x720 @ 2750000 bps
            #audio: 1. Polish - AACL 44100Hz 16bits 2ch @ 64000 bps
            a = i + 1
            item = str(a) + ". "
            try:
                if tab[i]['language'] != 'None':
                    item += tab[i]['language'].capitalize() + " - "
            except:
                pass
            try:
                if tab[i]['fourcc'] != 'None':
                    item += tab[i]['fourcc'] + ", "
            except:
                pass
            try:
                if tab[i]['subtype'] != 'None':
                    item += tab[i]['subtype'] + " "
            except:
                pass
            try:
                if tab[i]['width'] != 'None' and tab[i]['height'] != 'None':
                    item += tab[i]['width'] + "x" + tab[i]['height']
            except:
                pass
            try:
                if tab[i]['channels'] != 'None' and tab[i]['bits_per_sample'] != 'None' and tab[i]['sample_rate'] != 'None':
                    item += tab[i]['sample_rate'] + "Hz, " + tab[i]['bits_per_sample'] + "bits, " + tab[i]['channels'] + "ch"
            except:
                pass
            if tab[i]['bitrate'] != 'None':
                item += " @ " + tab[i]['bitrate'] + " bps"
            out.append(item)
        return out

    def getValueFromMenuTab(self, key, tab):
        value = {}
        for i in range(len(tab)):
            if key == i:
                value = tab[i]
                break
        return value
    
    
class Download(Thread):
    def __init__(self):
        Thread.__init__(self)
