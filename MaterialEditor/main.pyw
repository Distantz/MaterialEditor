import gui as gui
import os as os
import eventHandler as event
import export as export
import tkinter as tk
from tkinter import messagebox


class Setup():

    def __init__(self):

        self.programFolder = os.path.dirname(os.path.abspath(__file__))

        self.handle = event.eventHandler(self)
        self.exporter = export.export(self)

        self.foundFiles = self.exporter.findAllFBXFiles(self.programFolder + "/programFiles/models/fbx/")

        self.outputDirectory = self.exporter.findOutputDirectory(self.programFolder)

        guiClass = gui.Gui(self, self.handle, self.exporter)
        guiClass.root.mainloop()

setup = Setup()