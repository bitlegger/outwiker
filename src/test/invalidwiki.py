#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты на загрузку вики с ошибками
"""

import os.path
import shutil
import unittest

from core.event import Event
from core.attachment import Attachment
from core.tree import RootWikiPage, WikiDocument
from pages.text.textpage import TextPageFactory
from pages.html.htmlpage import HtmlPageFactory


path = u"../test/invalidwiki"

class InvalidWikiTest (unittest.TestCase):
	def setUp (self):
		pass
		

	def testNotPage (self):
		"""
		Тест папок, которые не являются страницами
		"""
		wiki = WikiDocument.load (path)
		page = wiki[u"Просто папка"]
		self.assertEqual (page, None)

	
	def testEmptyAttaches (self):
		"""
		Тест страницы без папки с аттачами
		"""
		wiki = WikiDocument.load (path)
		page = wiki[u"Страница без аттачей"]
		self.assertEqual ( len (Attachment (page).attachmentFull), 0)

	
	def testEmptyAttaches2 (self):
		"""
		Попытка прикрепления файлов к странице без папки __attach
		"""
		filesPath = u"../test/samplefiles/"
		files = [u"accept.png", u"add.png", u"anchor.png"]
		attaches = [os.path.join (filesPath, fname) for fname in files]

		wiki = WikiDocument.load (path)
		Attachment (wiki[u"Страница без аттачей"]).attach (attaches)

		self.assertEqual (len (Attachment (wiki[u"Страница без аттачей"]).attachmentFull), 3)

		# Удалим прикрепленные файлы
		attachPath = Attachment (wiki[u"Страница без аттачей"]).getAttachPath()
		shutil.rmtree (attachPath)
	

	def testEmptyContent (self):
		"""
		Тест страницы без файла контента
		"""
		wiki = WikiDocument.load (path)
		page = wiki[u"Страница без контента"]
		self.assertEqual (page.content, "")
	

	def testInvalidPath (self):
		"""
		Тест попытки открытия несуществующей вики
		"""
		invalidpath = u"../testsss/invalidwiki"
		self.assertRaises (IOError, WikiDocument.load, invalidpath)
	


