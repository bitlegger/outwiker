# -*- coding: UTF-8 -*-

import wx
import wx.lib.newevent
import wx.adv

from outwiker.gui.controls.hyperlink import (HyperLinkCtrl,
                                             EVT_HYPERLINK_LEFT,
                                             EVT_HYPERLINK_RIGHT,
                                             EVT_HYPERLINK_MIDDLE)

TagLeftClickEvent, EVT_TAG_LEFT_CLICK = wx.lib.newevent.NewEvent()
TagMiddleClickEvent, EVT_TAG_MIDDLE_CLICK = wx.lib.newevent.NewEvent()


class TagLabel(HyperLinkCtrl):
    """
    Класс для представления одной метки
    """
    def __init__(self, parent, title):
        super(TagLabel, self).__init__(
            parent,
            label=title,
            style=wx.adv.HL_ALIGN_CENTRE | wx.BORDER_NONE)

        self.__propagationLevel = 10
        self.AutoBrowse(False)
        self.DoPopup(False)
        self.ReportErrors(False)
        self.EnableRollover(True)
        self.SetUnderlines(False, False, False)

        self.__minFontSize = 8
        self.__maxFontSize = 15
        self.__normalBackColor = wx.Colour(255, 255, 255)

        self.__normalFontColor = wx.Colour(0, 0, 0)
        self.__markedFontColor = wx.Colour(0, 0, 0)
        self.__markedBackColor = wx.Colour(250, 255, 36)

        self.__normalHoverFontColor = wx.Colour(255, 0, 0)
        self.__markedHoverFontColor = wx.Colour(255, 0, 0)

        self.__isMarked = False
        self.updateColors()
        self.Bind(EVT_HYPERLINK_LEFT, self.__onMouseLeftDown)
        self.Bind(EVT_HYPERLINK_RIGHT, self.__onMouseRightDown)
        self.Bind(EVT_HYPERLINK_MIDDLE, self.__onMouseMiddleDown)

    @property
    def normalFontColor(self):
        return self.__normalFontColor

    @normalFontColor.setter
    def normalFontColor(self, value):
        self.__normalFontColor = value
        self.updateColors()

    @property
    def normalBackColor(self):
        return self.__normalBackColor

    @normalBackColor.setter
    def normalBackColor(self, value):
        self.__normalBackColor = value
        self.updateColors()

    @property
    def markedFontColor(self):
        return self.__markedFontColor

    @markedFontColor.setter
    def markedFontColor(self, value):
        self.__markedFontColor = value
        self.updateColors()

    @property
    def markedBackColor(self):
        return self.__markedBackColor

    @markedBackColor.setter
    def markedBackColor(self, value):
        self.__markedBackColor = value
        self.updateColors()

    @property
    def normalHoverFontColor(self):
        return self.__normalHoverFontColor

    @normalHoverFontColor.setter
    def normalHoverFontColor(self, value):
        self.__normalHoverFontColor = value
        self.updateColors()

    @property
    def markedHoverFontColor(self):
        return self.__markedHoverFontColor

    @markedHoverFontColor.setter
    def markedHoverFontColor(self, value):
        self.__markedHoverFontColor = value
        self.updateColors()

    def updateColors(self):
        if self.__isMarked:
            self.SetBackgroundColour(self.__markedBackColor)
            self.SetColours(self.__markedFontColor,
                            self.__markedFontColor,
                            self.__markedHoverFontColor)
        else:
            self.SetBackgroundColour(self.__normalBackColor)
            self.SetColours(self.__normalFontColor,
                            self.__normalFontColor,
                            self.__normalHoverFontColor)

        self.UpdateLink()

    def __onMouseLeftDown(self, event):
        self.__sendTagEvent(TagLeftClickEvent)

    def __onMouseRightDown(self, event):
        pass

    def __onMouseMiddleDown(self, event):
        self.__sendTagEvent(TagMiddleClickEvent)

    def __sendTagEvent(self, eventType):
        newevent = eventType(text=self.GetLabel())
        newevent.ResumePropagation(self.__propagationLevel)
        wx.PostEvent(self.GetParent(), newevent)

    def setRatio(self, ratio):
        """
        Установить коэффициент, показывающий относительный размер метки.
        Коэффициент должен быть в интервале [0; 1]
        """
        fontsize = int(self.__minFontSize + ratio *
                       (self.__maxFontSize - self.__minFontSize))

        font = wx.Font(fontsize,
                       wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_NORMAL,
                       underline=False)

        self.SetFont(font)
        self.InvalidateBestSize()
        self.SetSize(self.GetBestSize())

    def mark(self, marked=True):
        self.__isMarked = marked
        self.updateColors()

    @property
    def isMarked(self):
        return self.__isMarked
