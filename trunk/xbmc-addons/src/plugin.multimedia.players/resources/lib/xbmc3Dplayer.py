# -*- coding: utf-8 -*-

#import libraries
import subprocess
import string, urllib
import sys
import re
import os, stat
import xbmc, xbmcgui
import pLog, connection

__scriptID__   = sys.modules[ "__main__" ].__scriptID__
_ = sys.modules[ "__main__" ].__language__

_log = pLog.pLog()

TAB_INPUTS = {_(50080): 'separate-left-right',
              _(50081): 'separate-right-left',
              _(50082): 'top-bottom',
              _(50083): 'top-bottom-half',
              _(50084): 'bottom-top',
              _(50085): 'bottom-top-half',
              _(50086): 'left-right',
              _(50087): 'left-right-half',
              _(50088): 'right-left',
              _(50089): 'right-left-half',
              _(50090): 'even-odd-rows',
              _(50091): 'odd-even-rows'}

TAB_OUTPUTS = {_(50100): 'hdmi-frame-pack',
               _(50101): 'even-odd-rows',
               _(50102): 'even-odd-columns',
               _(50103): 'checkerboard',
               _(50104): 'red-cyan-monochrome',
               _(50105): 'red-cyan-half-color',
               _(50106): 'red-cyan-full-color',
               _(50107): 'red-cyan-dubois',
               _(50108): 'green-magenta-monochrome',
               _(50109): 'green-magenta-half-color',
               _(50110): 'green-magenta-full-color',
               _(50111): 'green-magenta-dubois',
               _(50112): 'amber-blue-monochrome',
               _(50113): 'amber-blue-half-color',
               _(50114): 'amber-blue-full-color',
               _(50115): 'amber-blue-dubois',
               _(50116): 'red-green-monochrome',
               _(50117): 'red-blue-monochrome',
               _(50118): 'equalizer',
               _(50119): 'equalizer-3d',
               _(50120): 'stereo',
               _(50121): 'left',
               _(50122): 'right',
               _(50123): 'top-bottom',
               _(50124): 'top-bottom-half',
               _(50125): 'left-right',
               _(50126): 'left-right-half'}

TAB_OUT_SET = {'HDMI': 'hdmi-frame-pack',
               'Rows': 'even-odd-rows',
               'Columns': 'even-odd-columns',
               'Checkerboard': 'checkerboard',
               _(50104): 'red-cyan-monochrome',
               _(50105): 'red-cyan-half-color',
               _(50106): 'red-cyan-full-color',
               _(50107): 'red-cyan-dubois',
               _(50108): 'green-magenta-monochrome',
               _(50109): 'green-magenta-half-color',
               _(50110): 'green-magenta-full-color',
               _(50111): 'green-magenta-dubois',
               _(50112): 'amber-blue-monochrome',
               _(50113): 'amber-blue-half-color',
               _(50114): 'amber-blue-full-color',
               _(50115): 'amber-blue-dubois',
               _(50116): 'red-green-monochrome',
               _(50117): 'red-blue-monochrome',
               _(50118): 'equalizer',
               _(50119): 'equalizer-3d',
               _(50120): 'stereo',
               'Left': 'left',
               'Right': 'right',
               'Over/Under [Top/Bottom]': 'top-bottom',
               'HALF Over/Under (HALF Top/Bottom)': 'top-bottom-half',
               'Side-By-Side': 'left-right',
               'HALF Side-By-Side': 'left-right-half'}


class StereoscopicPlayer:
    def __init__(self):
        _log.info('Starting') #@UndefinedVariable
        self.conn = connection.Connection()
        #self.settings = settings.StereoscopicSettings()
    
    
    def player3D(self, prefs):
        try:
            if prefs['switcher'] == 'false' and prefs['switcherexp'] == 'true':
                playerFile = open(os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/xbmc3Dplayer', 'w')
            commandFile = os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/cmd.tmp'
            #os.remove(commandFile)
            #numAudio = str(self.getAudioLanguage(mediaTab, prefs['audio']))
            numAudio = '1'
            #numSubtitle = str(self.getSubtitleLanguage(mediaTab, prefs['subtitle']))
            numSubtitle = '0'
            lircfile = os.getenv("HOME") + '/.lircrc'
            opt = ''
            lircOpt = ''
            if prefs['output'] == 'even-odd-rows':
                opt = '-S'
            if os.path.isfile(lircfile):
                lircOpt = '--lirc-config=' + lircfile
            if prefs['input'] != 'None':
                appRun = 'None'
                cmdfile = open(commandFile, 'w')
                cmdtext = ""
                if prefs['file1'] != 'None' and prefs['file2'] == 'None':
                    appRun = prefs['prog'] + ' --input=' + prefs['input'] + ' ' + prefs['file1'] + ' --output=' + prefs['output'] + ' --audio=' + numAudio + ' --subtitle=' + numSubtitle + ' --subtitle-size=' + prefs['subsize'] + ' --subtitle-encoding=' + prefs['subenc'] + ' --subtitle-color=' + prefs['subcolor'] + ' --subtitle-parallax=' + prefs['subparallax'] + ' ' + lircOpt +  ' ' + opt + ' -f -n'
                    cmdtext = 'toggle-fullscreen\nset-quality 1\nset-stereo-layout ' + prefs['input'] + '\nset-stereo-mode ' + prefs['output'] + '\nset-audio-stream ' + numAudio + '\nset-subtitle-stream ' + numSubtitle + '\nset-subtitle-size ' + prefs['subsize'] + '\nset-subtitle-encoding ' + prefs['subenc'] + '\nset-subtitle-color ' + prefs['subcolor'] + '\nopen ' + prefs['file1'].replace(' ', '%20').replace('"', '') + '\nplay'
                elif prefs['input'] == 'separate-left-right' and prefs['file1'] != 'None' and prefs['file2'] != 'None':
                    appRun = prefs['prog'] + ' --input=' + prefs['input'] + ' ' + prefs['file1'] + ' ' + prefs['file2'] + ' --output=' + prefs['output'] + ' --audio=' + numAudio + ' --subtitle=' + numSubtitle + ' --subtitle-size=' + prefs['subsize'] + ' --subtitle-encoding=' + prefs['subenc'] + ' --subtitle-color=' + prefs['subcolor'] + ' --subtitle-parallax=' + prefs['subparallax'] + ' ' + lircOpt + ' -f  -n'
                    cmdtext = 'toggle-fullscreen\nset-quality 1\nset-stereo-layout ' + prefs['input'] + '\nset-stereo-mode ' + prefs['output'] + '\nset-audio-stream ' + numAudio + '\nset-subtitle-stream ' + numSubtitle + '\nset-subtitle-size ' + prefs['subsize'] + '\nset-subtitle-encoding ' + prefs['subenc'] + '\nset-subtitle-color ' + prefs['subcolor'] + '\nopen ' + prefs['file1'].replace(' ', '%20').replace('"', '') + ' ' + prefs['file2'].replace(' ', '%20').replace('"', '') + '\nplay'
                elif prefs['input'] == 'separate-right-left' and prefs['file1'] != 'None' and prefs['file2'] != 'None':
                    appRun = prefs['prog'] + ' --input=' + prefs['input'] + ' ' + prefs['file1'] + ' ' + prefs['file2'] + ' --output=' + prefs['output'] + ' --audio=' + numAudio + ' --subtitle=' + numSubtitle + ' --subtitle-size=' + prefs['subsize'] + ' --subtitle-encoding=' + prefs['subenc'] + ' --subtitle-color=' + prefs['subcolor'] + ' --subtitle-parallax=' + prefs['subparallax'] + ' ' + lircOpt + ' -f  -n'
                    cmdtext = 'toggle-fullscreen\nset-quality 1\nset-stereo-layout ' + prefs['input'] + '\nset-stereo-mode ' + prefs['output'] + '\nset-audio-stream ' + numAudio + '\nset-subtitle-stream ' + numSubtitle + '\nset-subtitle-size ' + prefs['subsize'] + '\nset-subtitle-encoding ' + prefs['subenc'] + '\nset-subtitle-color ' + prefs['subcolor'] + '\nopen ' + prefs['file1'].replace(' ', '%20').replace('"', '') + ' ' + prefs['file2'].replace(' ', '%20').replace('"', '') + '\nplay'
                cmdfile.write(cmdtext)
                cmdfile.close()
                #appRun = prefs['prog'] + ' --read-commands ' + cmdfile
                #Jebie sie cos i bez "strace" nie dziala
                #appRun = appMovie + ' --input=' + formStreamInput + ' ' + movie + ' --output=' + formStreamOutput + ' --audio=' + numAudio + ' --subtitle=' + numSubtitle + ' --subtitle-size=' + subSize + ' --subtitle-encoding=' + subCode + ' --subtitle-color=' + subColor + ' --subtitle-parallax=' + subParallax + ' ' + lircOpt + ' -f ' + opt + ' -n|/usr/bin/strace -o /dev/null -p `/bin/ps ax|/bin/grep -v "' + appMovie + '"|/bin/grep -v grep|/bin/awk \'{print $1}\'`'
                #playerFile.write('#!/bin/sh\n')
                if prefs['switcher'] == 'false' and prefs['switcherexp'] == 'true':
                    playerFile.write(appRun)
                    playerFile.close()
                    os.chmod(os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/xbmc3Dplayer', stat.S_IRWXU)
                elif prefs['switcher'] == 'true' and prefs['switcherexp'] == 'false':
                    #subprocess.call(appRun, shell=True)
                    xbmc.executebuiltin('LIRC.Stop')
                    xbmc.executebuiltin('Hide')
                    os.system(appRun)
                    xbmc.executebuiltin('Restore')
                    xbmc.executebuiltin('LIRC.Start')
                _log.info('Starting command: ' + appRun)
        except OSError, e:
            #ekg.printf(subprocess.sys.stderr, "Błąd wykonania:", e)
            return 1


    def getFileName(self, movie):
        fileName = movie
        pref = "/"
        if "/" in movie:
            pref = "/"
        elif "\\" in movie:
            pref = "\\"
        tabFile = movie.split(pref)
        fileName = tabFile[len(tabFile) - 1]
        return fileName


    def getPathFileName(self, movie):
        separate = ''
        path = ''
        if '\\' in movie:
            tab = movie.split('\\')
            separate = '\\'
        elif '/' in movie:
            tab = movie.split('/')
            separate = '/'
        if len(tab) > 0:
            for i in range(len(tab - 1)):
                if i == 0:
                    if tab[i].startswith('http:'):
                        path += tab[i] + separate
                    else:
                        path += separate + tab[i] + separate
                else:
                    path += tab[i] + separate
        _log.info('Ściażka absolutna: ' + path)
        return path
    
    
    def isLeftEye(self, movie):
        matchEye = re.match(r'^.*([Ll][Ee][Ff][Tt]).*$', self.getFileName(movie), re.M|re.I)
        if matchEye:
            return True
        else:
            return False
      

    def isRightEye(self, movie):
        matchEye = re.match(r'^.*([Rr][Ii][Gg][Hh][Tt]).*$', self.getFileName(movie), re.M|re.I)
        if matchEye:
            return True
        else:
            return False
      

    def movieDir(self, movie):
        outDir = ''
        tab = movie.split('/')
        if len(tab) > 0:
            ntab = len(tab) - 1
            for i in range(ntab):
                outDir += tab[i] + '/'
                outDir = outDir.replace('"', '')
        return outDir    
	
    
    def isStereo(self, table):
        videos = []
        for line in table:
            if 'ID_VIDEO_ID' in line:
                videos.append(line)
            if len(videos) > 1:
                return True


    def getMovieName(self, movie):
        TAB_EYE = { 
                     "LEFT": "RIGHT",
                     "left": "right",
                     "Left": "Right",
                     "LEft": "RIght",
                     "LEFt": "RIGht",
                     "lEFT": "rIGHT",
                     "leFT": "riGHT",
                     "lefT": "rigHT",
                     "left": "righT",
                     "Right": "Left",
                     "RIght": "LEft",
                     "RIGht": "LEFt",
                     "RIGHT": "LEFT",
                     "rIGHT": "lEFT",
                     "riGHT": "leFT",
                     "rigHT": "lefT",
                     "righT": "left",
                     "right": "left"
                    }
        name = self.getFileName(movie)
        newName = ""
        for k,v in TAB_EYE.items():
            if k in name:
                newName = name.replace(k, v)
        movie = movie.replace(name, newName)
        return movie
                

    def getEyeFirst(self, table):
        inputForm = 'separate-left-right'
        eye = []
        for line in table:
            if 'ID_VID_' in line:
                eye.append(line)
                if len(eye) > 1:
                    exprL = re.match(r'^.*([Ll][Ee][Ff][Tt]).*$', str(eye[0]), re.M|re.I)
                    exprR = re.match(r'^.*([Rr][Ii][Gg][Hh][Tt]).*$', str(eye[0]), re.M|re.I)
                    if exprL:
                        inputForm = 'separate-left-right'
                        #_log.info('Set separate: left-right')
                    elif exprR:
                        inputForm = 'separate-right-left'
                else:
                    inputForm = ''
                    #_log.info('Set separate: right-left')
        return inputForm	


    def getAudioLanguage(self, table, lang):
        language = 1
        numLang = []
        for line in table:
            if 'ID_AUDIO_ID' in line:
                numLang.append(line)
        for i in range(len(numLang)):
            for line in table:
                if 'ID_AID_' + str(i) + '_LANG' in line:
                    lineTab = line.split('=')
                    llang = lineTab[1].split("\n")
                    #_log.info('Language: ' + line + ', ' + llang[0] + ', ' + str(lang.find(llang[0])))
                    if lang.rfind(llang[0]) == 0:
                        #_log.info('Language2: ' + line + ', ' + lineTab[1] + '=' + lang)
                        language = i + 1
        return language
  

    def getSubtitleLanguage(self, table, lang):
        language = 0
        numLang = []
        _log.info('lang: ' + lang)
        for line in table:
            if 'ID_SUBTITLE_ID' in line:
                numLang.append(line)
        for i in range(len(numLang)):
            for line in table:
                if 'ID_SID_' + str(i) + '_LANG' in line:
                    lineTab = line.split('=')
                    llang = lineTab[1].split("\n")
                    #_log.info('Language: ' + line + ', ' + llang[0] + ', ' + str(lang.find(llang[0])))
                    if lang.rfind(llang[0]) == 0:
                        #_log.info('Language2: ' + line + ', ' + lineTab[1] + '=' + lang)
                        language = i + 1
        return language


    def playStereo(self, prefs):
        pathMovie = '"' + prefs['file1'] + '"'
        _log.info('Generating informations of 3D movie: ' + pathMovie)
        if self.isRightEye(pathMovie) or self.isLeftEye(pathMovie):
            _log.info('Prepare to display movie from 2 files')
            prefs['file2'] = self.getMovieName(pathMovie)
            if self.isLeftEye(pathMovie):
                prefs['input'] = self.getInputFormat(_(50080))
            elif self.isRightEye(pathMovie):
                prefs['input'] = self.getInputFormat(_(50081))
        elif prefs['input'] == 'None':
            menu = self.setInputTable()
            dialog = xbmcgui.Dialog()
            choice = dialog.select(_(55020), menu)
            for i in range(len(menu)):
                if choice == i:
                    prefs['input'] = self.getInputFormat(menu[i])
        else:
            prefs['input'] = 'mono'
        self.player3D(prefs)
  

    def getOutputFormat(self, key):
        out = 'even-odd-rows'
        #for k,v in TAB_OUTPUTS.items():
        for k,v in TAB_OUT_SET.items():
            if key == k:
                out = v
                break
        return out


    def getInputFormat(self, key):
        out = 'mono'
        for k,v in TAB_INPUTS.items():
            if key == k:
                out = v
                break
        return out
    
    
    def setInputTable(self):
        tab = []
        #return TAB_INPUTS
        for k,v in TAB_INPUTS.items():
            tab.append(k)
        tab.sort()
        return tab
    
  