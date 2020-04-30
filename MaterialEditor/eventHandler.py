import tkinter as tk
import threading
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import messagebox

class eventHandler():
    
    def __init__(self, setup):

        self.setup = setup

    def onExport(self, guiClass, setup):

        try:
            self.setup.exporter.finalExport(guiClass, self.setup.programFolder, self.setup)

        except IOError:
            messagebox.showerror(title="Export cancelled", message="Error: IOError \n\n Do you have permission to create zips in this directory, or have an exported zip open?")

        except Exception as BCMapProblemError:
            messagebox.showerror(title="Export cancelled", message="Error: BCMapProblemError \n\n A Base Colour map is either missing, or is larger in one dimension than 1024.")

        self.setup.exporter.deleteTempFolder(self.setup.programFolder)

    def onPickOutputDirectory(self):

        self.setup.outputDirectory = self.setup.exporter.writeOutputDirectory(askdirectory(), self.setup.programFolder)


    def onNormalMapClick(self, guiClass):

        if guiClass.useNormal.get():

            guiClass.mainMaterialSelector.configure(1, False)
            guiClass.trimMaterialSelector.configure(1, False)

            guiClass.altNormalTickbox.configure(state="normal")

        else:

            guiClass.mainMaterialSelector.configure(1, True)
            guiClass.trimMaterialSelector.configure(1, True)
            guiClass.altNormalTickbox.configure(state="disabled")
            guiClass.altNormalTickbox.deselect()


    def onWorkflowChange(self, guiClass, workflow):

        if workflow != 0:

            guiClass.roughnessMapInverter.configure(state="disabled")
            guiClass.roughnessMapInverter.deselect()

        else:

            guiClass.roughnessMapInverter.configure(state="normal")

        guiClass.mainMaterialSelector.children[2].label.configure(text=guiClass.workflows[workflow * 2])
        guiClass.mainMaterialSelector.children[3].label.configure(text=guiClass.workflows[workflow * 2 + 1])

        guiClass.trimMaterialSelector.children[2].label.configure(text=guiClass.workflows[workflow * 2])
        guiClass.trimMaterialSelector.children[3].label.configure(text=guiClass.workflows[workflow * 2 + 1])


    def onFileManager(self, guiClass, master, widget, directoryList, mode):

        if mode == "pick":
            tempFileDir = askopenfilename(title="Pick texture", initialdir=directoryList[widget], filetypes = (("png files","*.png"),("jpeg files","*.jpg"),("All files","*.*")))
            directoryList[widget] = (tempFileDir) if len(tempFileDir) != 0 else directoryList[widget]


        elif mode == "remove":
            directoryList[widget] = "No File Selected"
        
        tmp = directoryList[widget].split("/")[-1]
        master.children[widget].selector.configure(text=tmp)


    def onSliderUpdate(self, guiClass):

        slideValue = guiClass.flexiScale.get()

        guiClass.mainFlexiColourSelector.configure(0, False)
        guiClass.mainFlexiColourSelector.configure(1, False)
        guiClass.mainFlexiColourSelector.configure(2, False)
        guiClass.mainFlexiColourSelector.configure(3, False)

        guiClass.trimFlexiColourSelector.configure(0, False)
        guiClass.trimFlexiColourSelector.configure(1, False)
        guiClass.trimFlexiColourSelector.configure(2, False)
        guiClass.trimFlexiColourSelector.configure(3, False)

        for x in range(4, slideValue, -1):
            
            guiClass.mainFlexiColourSelector.configure(x - 1, True)
            guiClass.trimFlexiColourSelector.configure(x - 1, True)

    def onExportSelectionButton(self, guiClass, mode):

        if mode == "inverse":

            for x in range(len(guiClass.exportCBList)):

                if guiClass.exportCBList[x].buttonVar.get() == 0:

                    guiClass.exportCBList[x].buttonVar.set(1)

                else:

                    guiClass.exportCBList[x].buttonVar.set(0)


        elif mode == "select":

            for x in range(len(guiClass.exportCBList)):

               guiClass.exportCBList[x].buttonVar.set(1)


        elif mode == "deselect":

            for x in range(len(guiClass.exportCBList)):

               guiClass.exportCBList[x].buttonVar.set(0)
            


