#!/usr/bin/env python3

import sys
import os
import time
from typing import Union
import pathlib


class PlaysoundException(Exception):
    pass


def _playsoundWin(sound: Union[str, pathlib.Path], block=True) -> None:
    '''
    Utilizes windll.winmm. Tested and known to work with MP3 and Wave on
    Windows 10 with Python 3.8 and 3.9. Probably works with more file formats.

    Inspired by (but not copied from) Michael Gundlach <gundlach@gmail.com>'s mp3play:
    https://github.com/michaelgundlach/mp3play

    I never would have tried using windll.winmm without seeing his code.
    '''
    from ctypes import c_buffer, windll
    from random import random

    sound = str(sound)
    # sys.modules['__main__'] will not a have a __file__ attribute when run
    # from an interactive python console (such as IDLE or Jupyter Notebook)
    if hasattr(sys.modules['__main__'], "__file__"):
        sound = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), str(sound))

    def winCommand(*command):
        buf = c_buffer(255)
        command = ' '.join(command).encode(sys.getfilesystemencoding())
        errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
        if errorCode:
            errorBuffer = c_buffer(255)
            windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
            exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
                                '\n        ' + command.decode() +
                                '\n    ' + errorBuffer.value.decode())
            raise PlaysoundException(exceptionMessage)
        return buf.value

    alias = 'playsound_' + str(random())
    winCommand('open "' + sound + '" alias', alias)
    winCommand('set', alias, 'time format milliseconds')
    durationInMS = winCommand('status', alias, 'length')
    winCommand('play', alias, 'from 0 to', durationInMS.decode())

    if block:
        time.sleep(float(durationInMS) / 1000.0)

    winCommand('close', alias)


def _playsoundOSX(sound: Union[str, pathlib.Path], block=True) -> None:
    '''
    Utilizes AppKit.NSSound. Probably works with anything that has
    QuickTime support. Probably works on OS X 10.5 and newer. Probably
    works with all versions of Python.

    Inspired by (but not copied from) Aaron's Stack Overflow answer here:
    http://stackoverflow.com/a/34568298/901641

    I never would have tried using AppKit.NSSound without seeing his code.
    '''
    from AppKit import NSSound
    from Foundation import NSURL

    sound = str(sound)
    # sys.modules['__main__'] will not a have a __file__ attribute when run
    # from an interactive python console (such as IDLE or Jupyter Notebook)
    if hasattr(sys.modules['__main__'], "__file__"):
        sound = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), str(sound))

    if '://' not in sound:
        if not sound.startswith('/'):
            sound = os.getcwd() + '/' + sound
        sound = 'file://' + sound
        sound = sound.replace(' ', '%20')
    url = NSURL.URLWithString_(sound)
    nssound = NSSound.alloc().initWithContentsOfURL_byReference_(url, True)
    if not nssound:
        raise IOError('Unable to load sound named: ' + sound)
    nssound.play()

    if block:
        time.sleep(nssound.duration())


def _playsoundNix(sound: Union[str, pathlib.Path], block=True) -> None:
    sound = str(sound)
    # sys.modules['__main__'] will not a have a __file__ attribute when run
    # from an interactive python console (such as IDLE or Jupyter Notebook)
    if hasattr(sys.modules['__main__'], "__file__"):
        sound = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), str(sound))

    '''
    Play a sound using GStreamer.

    Inspired by this:
    https://gstreamer.freedesktop.org/documentation/tutorials/playback/playbin-usage.html
    '''
    if not block:
        raise NotImplementedError(
            "block=False cannot be used on this platform yet")

    # pathname2url escapes non-URL-safe characters
    from urllib.request import pathname2url

    import gi
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst

    Gst.init(None)

    playbin = Gst.ElementFactory.make('playbin', 'playbin')
    playbin.props.uri = sound if sound.startswith(('http://', 'https://')) \
        else 'file://' + pathname2url(os.path.abspath(sound))

    set_result = playbin.set_state(Gst.State.PLAYING)
    if set_result != Gst.StateChangeReturn.ASYNC:
        raise PlaysoundException(
            "playbin.set_state returned " + repr(set_result))

    # FIXME: use some other bus method than poll() with block=False
    # https://lazka.github.io/pgi-docs/#Gst-1.0/classes/Bus.html
    bus = playbin.get_bus()
    bus.poll(Gst.MessageType.EOS, Gst.CLOCK_TIME_NONE)
    playbin.set_state(Gst.State.NULL)


if sys.platform == 'win32':
    playsound = _playsoundWin
elif sys.platform == 'darwin':
    playsound = _playsoundOSX
else:
    playsound = _playsoundNix
