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

def canvas(x,y):
	img = Image.new('RGBA',(x, y))
	return img	

def box(img,x,y,h,w,r,g,b,t):
	draw = ImageDraw.Draw(img)
	draw.rectangle(((x,y),(h,w)), fill=(r,g,b,t), outline=None)
	return img

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

	def didDeviceCommPropertyChange(self, origDev, newDev):
		return False

	def deviceStartComm(self, dev):
		Directory = dev.pluginProps["Directory"]
		#Main Dir Test
		DirTest = os.path.isdir(Directory)		
		if DirTest is False:
			indigo.server.log("Button directory not found.")
			os.makedirs(Directory)
			indigo.server.log("Created: " + Directory)

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
					
					#try:
					ButtonName = device.name
					ButtonFile = ButtonName.replace(" ", "_") + ".png"
					Directory = device.pluginProps["Directory"]
					
					ButtonCoordX = int(device.pluginProps["ButtonCoordX"])
					ButtonCoordY = int(device.pluginProps["ButtonCoordY"])
					
					CanvasX = int(device.pluginProps["CanvasX"])
					CanvasY = int(device.pluginProps["CanvasY"])
					CanvasR = int(device.pluginProps["CanvasR"])
					CanvasG = int(device.pluginProps["CanvasG"])
					CanvasB = int(device.pluginProps["CanvasB"])
					CanvasT = int(device.pluginProps["CanvasT"])
					
					ButtonX = int(device.pluginProps["ButtonX"])
					ButtonY = int(device.pluginProps["ButtonY"])
					ButtonR = int(device.pluginProps["ButtonR"])
					ButtonG = int(device.pluginProps["ButtonG"])
					ButtonB = int(device.pluginProps["ButtonB"])
					ButtonT = int(device.pluginProps["ButtonT"])

					GrowY = device.pluginProps["growy"]					
					GrowX = device.pluginProps["growx"]
					
					#except:
						#pass
					
					#########################################
					# Main Code
					#########################################
					
					#indigo.server.log("creating image " + GrowY)
					##Create Canvas
					img = canvas(CanvasX,CanvasY)
					img = box(img,0,0,CanvasX,CanvasY,CanvasR,CanvasG,CanvasB,CanvasT)
					
					##Left and right movement
					if GrowX == "growleft":
						Bx = CanvasX
					elif GrowX == "growright":
						Bx = 0
					elif ButtonCoordX < 0:
						Bx = ButtonX
						ButtonCoordX = 1
					elif ButtonCoordX >= (CanvasX-ButtonX):
						ButtonCoordX = CanvasX
						Bx = CanvasX - ButtonX
					else:
						Bx = ButtonCoordX + ButtonX
					
					##Up and down movement
					if GrowY == "growup":
						By = CanvasY
					elif GrowY == "growdown":
						By = 0
					elif ButtonCoordY < 0:
						By = ButtonY
						ButtonCoordY = 1
					elif ButtonCoordY >= (CanvasY-ButtonY):
						ButtonCoordY = CanvasY
						By = CanvasY - ButtonY
					else:
						By = ButtonCoordY + ButtonY
					
					img = box(img,ButtonCoordX,ButtonCoordY,Bx,By,ButtonR,ButtonG,ButtonB,ButtonT)
					img.save(Directory + ButtonFile,quality=15,optimize=True)
					
					self.sleep(.25)
					
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
			indigo.server.log("Running the most recent version of Dynamic Button")
		else:
			indigo.server.log("The current version of Dynamic Button is " + str(CurrentVersion) + " and the running version " + str(ActiveVersion) + ".")
		
	def updatePlugin(self):
		ActiveVersion = str(self.pluginVersion)
		CurrentVersion = str(self.updater.getVersion())
		if ActiveVersion == CurrentVersion:
			indigo.server.log("Already running the most recent version of Dynamic Button")
		else:
			indigo.server.log("The current version of Dynamic Button is " + str(CurrentVersion) + " and the running version " + str(ActiveVersion) + ".")
			self.updater.update()
	
	#########################################
	# Plugin Actions object callbacks
	#########################################
	def toggle(self, pluginAction):
		dev = indigo.devices[pluginAction.deviceId]
		state = dev.states["state"]
		
		if state == "on":
			dev.updateStateOnServer("state", value="off")
		else:
			dev.updateStateOnServer("state", value="on")
			
	def MoveButton(self, pluginAction):
		dev = indigo.devices[pluginAction.deviceId]
		
		CanvasX = int(dev.pluginProps["CanvasX"])
		CanvasY = int(dev.pluginProps["CanvasY"])
		ButtonCoordX = int(dev.pluginProps["ButtonCoordX"])
		ButtonCoordY = int(dev.pluginProps["ButtonCoordY"])
		
		growud = dev.pluginProps["growy"]					
		growlr = dev.pluginProps["growx"]
		
		percentpixel = pluginAction.props["percentpixel"]
		relativeto = pluginAction.props["relative"]
		usevariables = pluginAction.props["usevariables"]
		
		if usevariables == False:
			MoveX = float(pluginAction.props["MoveX"])
			MoveY = float(pluginAction.props["MoveY"])
		else:
			try:
				varMoveX = int(pluginAction.props["MoveX"])
				MoveX = float(indigo.variables[varMoveX].value)
			except:
				MoveX = 0
				
			try:
				varMoveY = int(pluginAction.props["MoveY"])
				MoveY = float(indigo.variables[varMoveY].value)	
			except:
				MoveY = 0

		## Move button via % change
		if percentpixel == "percent":

			if relativeto == "current":
				NewCoordx = ButtonCoordX + (CanvasX * float(MoveX/100))
				NewCoordy = ButtonCoordY + (CanvasY * float(MoveY/100))					
			else:
				if MoveX <= 0:
					NewCoordx = ButtonCoordX
				else:
					NewCoordx = (CanvasX * float((MoveX/100)))
					
				if MoveY <= 0:
					NewCoordy = ButtonCoordY
				else:
					NewCoordy = (CanvasY * float((MoveY/100)))
				
		## Move button via pixel change
		else:
			if relativeto == "current":
				NewCoordx = ButtonCoordX + MoveX
				NewCoordy = ButtonCoordY + MoveY
			else:
				if MoveX <= 0:
					NewCoordx = ButtonCoordX
				else:
					NewCoordx = MoveX
					
				if MoveY <= 0:
					NewCoordy = ButtonCoordY
				else:
					NewCoordy = MoveY
		
		if NewCoordx < 0:
			NewCoordx = 0
		elif NewCoordx > CanvasX:
			NewCoordx = CanvasX
			
		if NewCoordy < 0:
			NewCoordy = 0
		elif NewCoordy > CanvasY:
			NewCoordy = CanvasY
			
		if growud == "growup":
			NewCoordy = CanvasY - NewCoordy
				
		if growlr == "growleft":
		 	NewCoordx = CanvasX - NewCoordx

		localPropsCopy = dev.pluginProps
		localPropsCopy["ButtonCoordY"] = str(int(NewCoordy))
		dev.replacePluginPropsOnServer(localPropsCopy)
		localPropsCopy["ButtonCoordX"] = str(int(NewCoordx))
		dev.replacePluginPropsOnServer(localPropsCopy)
	
	def ButtonColor(self, pluginAction):
		dev = indigo.devices[pluginAction.deviceId]
		
		usevariables = pluginAction.props["usevariables"]
		
		if usevariables == False:
			ButtonR = pluginAction.props["buttonr"]
			ButtonG = pluginAction.props["buttong"]
			ButtonB = pluginAction.props["buttonb"]
			ButtonT = pluginAction.props["buttont"]
		else:
			try:
				ButtonR = indigo.variables[int(pluginAction.props["buttonr"])].value
			except:
				ButtonR = 0
			try:
				ButtonG = indigo.variables[int(pluginAction.props["buttong"])].value
			except:
				ButtonG = 0
			try:
				ButtonB = indigo.variables[int(pluginAction.props["buttonb"])].value
			except:
				ButtonB = 0
			try:
				ButtonT = indigo.variables[int(pluginAction.props["buttont"])].value
			except:
				ButtonT = 0
		
		localPropsCopy = dev.pluginProps
		localPropsCopy["ButtonR"] = ButtonR
		dev.replacePluginPropsOnServer(localPropsCopy)
		localPropsCopy["ButtonG"] = ButtonG
		dev.replacePluginPropsOnServer(localPropsCopy)
		localPropsCopy["ButtonB"] = ButtonB
		dev.replacePluginPropsOnServer(localPropsCopy)
		localPropsCopy["ButtonT"] = ButtonT
		dev.replacePluginPropsOnServer(localPropsCopy)
		
	def CanvasColor(self, pluginAction):
		dev = indigo.devices[pluginAction.deviceId]
		
		usevariables = pluginAction.props["usevariables"]
		
		if usevariables == False:
			CanvasR = pluginAction.props["canvasr"]
			CanvasG = pluginAction.props["canvasg"]
			CanvasB = pluginAction.props["canvasb"]
			CanvasT = pluginAction.props["canvast"]
		else:
			try:
				CanvasR = indigo.variables[int(pluginAction.props["canvasr"])].value
			except:
				CanvasR = 0
			try:
				CanvasG = indigo.variables[int(pluginAction.props["canvasg"])].value
			except:
				CanvasG = 0
			try:
				CanvasB = indigo.variables[int(pluginAction.props["canvasb"])].value
			except:
				CanvasB = 0
			try:
				CanvasT = indigo.variables[int(pluginAction.props["canvast"])].value
			except:
				CanvasT = 0
		
		localPropsCopy = dev.pluginProps
		localPropsCopy["CanvasR"] = CanvasR
		dev.replacePluginPropsOnServer(localPropsCopy)
		localPropsCopy["CanvasG"] = CanvasG
		dev.replacePluginPropsOnServer(localPropsCopy)
		localPropsCopy["CanvasB"] = CanvasB
		dev.replacePluginPropsOnServer(localPropsCopy)
		localPropsCopy["CanvasT"] = CanvasT
		dev.replacePluginPropsOnServer(localPropsCopy)

	
		
		