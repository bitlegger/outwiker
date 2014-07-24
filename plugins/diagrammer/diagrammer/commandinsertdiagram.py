# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command


class CommandInsertDiagram (Command):
    """
    Команда (:diagram:) для википарсера
    """
    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)


    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"diagram"


    def execute (self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        params_dict = Command.parseParams (params)

        return u"Plugin Command Result"