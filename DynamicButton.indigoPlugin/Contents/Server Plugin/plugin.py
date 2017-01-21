#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2014, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

import indigo
import os, os.path
import sys
import time
from ghpu import GitHubPluginUpdater

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL.ExifTags import TAGS

from shutil import copyfile
from random import randint
from time import sleep
import datetime as dt


########################################
#Custom procedures
########################################


########################################
class Plugin(indigo.PluginBase):
########################################

	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = False
		self.updater = GitHubPluginUpdater(self)

	#########################################
	# Plugin startup and shutdown
	#########################################
	def startup(self):
		self.debugLog(u"startup called")

	def shutdown(self):
		self.debugLog(u"shutdown called")

	#########################################
	# Main Loop
	#########################################
	def runConcurrentThread(self):
		try:
			while True:
				for device in indigo.devices.iter("self"):
				
					#########################################
					# Variable Setup
					#########################################
				
					try:						
						### = device.pluginProps["###"]
					except:
						pass
					
					#########################################
					# Main Codde
					#########################################
					
		except self.StopThread:
			indigo.server.log("thread stopped")
			pass
	
	################################################################################
	# Plugin menus
	################################################################################
	def checkForUpdate(self):
		ActiveVersion = str(self.pluginVersion)
		CurrentVersion = str(self.updater.getVersion())
		if ActiveVersion == CurrentVersion:
			indigo.server.log("Running the most recent version of ????")
		else:
			indigo.server.log("The current version of ???? is " + str(CurrentVersion) + " and the running version " + str(ActiveVersion) + ".")
		
	def updatePlugin(self):
		ActiveVersion = str(self.pluginVersion)
		CurrentVersion = str(self.updater.getVersion())
		if ActiveVersion == CurrentVersion:
			indigo.server.log("Already running the most recent version of ????")
		else:
			indigo.server.log("The current version of ???? is " + str(CurrentVersion) + " and the running version " + str(ActiveVersion) + ".")
			self.updater.update()
	
	#########################################
	# Plugin Actions object callbacks
	#########################################
	def PhotoToggle(self, pluginAction):
		dev = indigo.devices[pluginAction.deviceId]
		state = dev.states["state"]
		
		if state == "Playing":
			indigo.server.log("Pause Photo Album")
			dev.updateStateOnServer("state", value="Paused")
		else:
			indigo.server.log("Play photo album")
			dev.updateStateOnServer("state", value="Playing")
