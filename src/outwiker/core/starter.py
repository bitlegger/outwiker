# -*- coding: UTF-8 -*-

import logging
import sys

from outwiker.core.commands import openWiki, findPage
from outwiker.core.commandline import CommandLine, CommandLineException
from outwiker.core.commands import getCurrentVersion
from outwiker.core.defines import APP_DATA_DISABLE_MINIMIZING, APP_DATA_DEBUG
from outwiker.gui.guiconfig import GeneralGuiConfig


logger = logging.getLogger('outwiker.core.starter')


class StarterExit(BaseException):
    """
    Исключение бросается, если нужно прервать выполнение программы
    """
    pass


class Starter(object):
    """
    Класс для выполнения команд из командной строки (не для разбора параметров)
    и начального открытия вики
    """
    def __init__(self, application):
        self._application = application
        self._commandLine = self.__parseCommandLine(sys.argv[1:])

    def processGUI(self):
        """
        Выполнить команды после создания GUI
        """
        # Открытие дерева с заметками
        if self._commandLine is None or self._commandLine.wikipath is None:
            self.__openRecentWiki()
        else:
            logger.debug('Open wiki {}'.format(self._commandLine.wikipath))
            openWiki(self._commandLine.wikipath, self._commandLine.readonly)

        if self._commandLine is not None:
            page = findPage(self._application, self._commandLine.page_id)
            if self._application.wikiroot is not None and page is not None:
                self._application.selectedPage = page

    def processConsole(self):
        """
        Выполнить команды командной строки до создания интерфейса
        """
        if self._commandLine is not None:
            self.__processConsoleCommands()

    def __parseCommandLine(self, args):
        cl = None

        if len(args) > 0:
            cl = CommandLine()
            try:
                cl.parseParams(args)
            except CommandLineException:
                print(cl.format_help())
                raise StarterExit

        return cl

    def __processConsoleCommands(self):
        # Вывод справки
        if self._commandLine.help:
            print(self._commandLine.format_help())
            raise StarterExit

        # Вывод информации о версии
        if self._commandLine.version:
            print(r"""OutWiker {ver}""".format(ver=str(getCurrentVersion())))
            raise StarterExit

        self._application.sharedData[APP_DATA_DISABLE_MINIMIZING] = self._commandLine.disableMinimizing
        self._application.sharedData[APP_DATA_DEBUG] = self._commandLine.debug

    def __openRecentWiki(self):
        """
        Открыть последнюю вики, если установлена соответствующая опция
        """
        openRecent = GeneralGuiConfig(self._application.config).autoopen.value

        if openRecent and len(self._application.recentWiki) > 0:
            logger.debug('Open recently used wiki')
            openWiki(self._application.recentWiki[0])
