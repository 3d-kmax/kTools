import maya.cmds as mc
import os
import subprocess

projectFileName = mc.file( query=True, list=True )
UVFolder = projectFileName[0].split('/')
del UVFolder[-1]
del UVFolder[5]

UVFolder[5] = "tak_design"
UVFolder = '\\'.join(UVFolder)

subprocess.Popen(r'explorer /select,"%s"'%UVFolder)