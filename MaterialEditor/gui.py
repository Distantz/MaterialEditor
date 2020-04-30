import tkinter as tk
import PIL as PIL
import os as os
from tkinter import messagebox
from tkinter import ttk
import webbrowser

class Gui():

    def __init__(self, setup, handle, exporter):

        ## Define colour pallete

        self.PalleteRed = "#db6565"
        self.PalleteLightGrey = "#dbdbdb"
        self.PalleteDarkGrey = "#bfbfbf"

        ## Tkinter Window Setup
        self.root = tk.Tk()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        default_width = 750
        default_height = 750

        self.root.geometry("{}x{}+{}+{}".format(default_width, default_height, int(screen_width / 2 - (default_width / 2)), int(screen_height / 2 - (default_height / 2))))

        self.root.iconbitmap(setup.programFolder + '//programFiles//icon.ico')

        self.root.title("Material Editor {}".format("v1.0"))


        ## Class referal variables
        self.setup = setup

        self.exporter = exporter

        self.onEvent = handle


        ## Directory lists for Image Selections

        self.setup.mainMaterialDirs = ["No File Selected", "No File Selected", "No File Selected", "No File Selected"]
        self.setup.trimMaterialDirs = ["No File Selected", "No File Selected", "No File Selected", "No File Selected"]
        self.setup.mainFlexiColourDirs = ["No File Selected", "No File Selected", "No File Selected", "No File Selected"]
        self.setup.trimFlexiColourDirs = ["No File Selected", "No File Selected", "No File Selected", "No File Selected"]
        self.setup.mainAdvancedDirs = ["No File Selected", "No File Selected", "No File Selected", "No File Selected"]
        self.setup.trimAdvancedDirs = ["No File Selected", "No File Selected", "No File Selected", "No File Selected"]


        ## Call GUI setup
        self.createMenu()
        self.createFrames()
        self.createWidgets()
        self.createBinds()

        if (self.exporter.runSetup):

            self.createStartupPopup()

    def createMenu(self):

        menubar = tk.Menu(self.root)

        programmenu = tk.Menu(menubar, tearoff=0)
        programmenu.add_command(label="Set output directory", command = lambda: self.onEvent.onPickOutputDirectory())
        programmenu.add_command(label="Open output directory", command = lambda: os.startfile(self.setup.outputDirectory))
        menubar.add_cascade(label="Settings", menu=programmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Online Documentation", command=lambda: webbrowser.open('https://www.youtube.com/channel/UCqg5Sh3Z8joVlll6drGufTg', new=2))
        helpmenu.add_command(label="Local Documentation", command=lambda: os.system("notepad.exe " + "{}/README.txt".format(self.setup.programFolder)))
        helpmenu.add_separator()
        helpmenu.add_command(label=("Material Editor {} {}".format("v1.0", "- Distantz 2020")))
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.root.config(menu=menubar)


    ## Creates all frames used within the program
    def createFrames(self):

        ## Define tab container (which contains all main UI frames)
        self.tabContainer = ttk.Notebook(self.root)
        self.tabContainer.grid(row=0, column=0, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)


        ## Creates all the frames used in the Texture Options tab (First tab)
        def textureOptions():

            self.exportOptionsMasterFrame = tk.Frame(self.tabContainer, highlightthickness=1, highlightbackground="black")

            self.workflowOptionsFrame = tk.Frame(self.exportOptionsMasterFrame, highlightthickness=0, highlightbackground="black")
            self.advancedOptionsFrame = tk.Frame(self.exportOptionsMasterFrame, highlightthickness=0, highlightbackground="black")
            self.exportOptionStretch = tk.Frame(self.exportOptionsMasterFrame, highlightthickness=0, highlightbackground="black", background=self.PalleteDarkGrey)
            self.projectNameFrame = tk.Frame(self.advancedOptionsFrame, highlightthickness=0, highlightbackground="black")

            self.tabContainer.add(self.exportOptionsMasterFrame, text="Export options", sticky="nsew")

            self.workflowOptionsFrame.grid(row=0, column=0, sticky="nsew")
            self.advancedOptionsFrame.grid(row=1, column=0, sticky="nsew", pady=(10,0))
            self.exportOptionStretch.grid(row=2, column=0, sticky="nsew")
            self.projectNameFrame.grid(row=2, column=0, columnspan=2, sticky="nsew")

            self.projectNameFrame.grid_columnconfigure(2, weight=1)

            self.exportOptionsMasterFrame.columnconfigure(0, weight=1)
            self.exportOptionsMasterFrame.grid_rowconfigure(0)
            self.exportOptionsMasterFrame.grid_rowconfigure(1, minsize=150)
            self.exportOptionsMasterFrame.grid_rowconfigure(2, weight=1, minsize=150)

            ## Flexicolour frame, defined under the texture options frame
            self.flexiColourOptionFrame = tk.Frame(self.workflowOptionsFrame, highlightthickness=1, highlightbackground="black")
            self.flexiColourOptionFrame.grid(row=2, column=1, sticky="nsew", rowspan=2)


        ## Creates all the frames used in the Image Selection tab (Second tab)
        def imageSelect():

            self.imageSelectFrame = tk.Frame(self.tabContainer, highlightthickness=1, highlightbackground="black")
            self.tabContainer.add(self.imageSelectFrame, text="Texture Maps")


        ## Creates all the frames used in the Export tab (Third tab)
        def export():

            self.exportFrame = tk.Frame(self.tabContainer, highlightthickness=1, highlightbackground="black")

            self.exportFrame.grid_columnconfigure(0, weight=1)
            self.exportFrame.grid_rowconfigure(0, weight=1)

            self.exportSelectFrame = tk.Frame(self.exportFrame)
            self.exportSelectFrame.grid(row=0, column=0, sticky="nsew")

            self.exportSelectorFrame = tk.Frame(self.exportSelectFrame)
            self.exportSelectorFrame.grid(row=0, column=0, sticky="nesw")

            self.exportSelectFrame.grid_columnconfigure(0, weight=1)
            self.exportSelectFrame.grid_rowconfigure(0, weight=1, minsize=50)
            self.exportSelectFrame.grid_rowconfigure(1, minsize=50)

            self.exportSelectorFrame.grid_rowconfigure(0, weight=1, minsize=100)
            self.exportSelectorFrame.grid_columnconfigure(0, weight=1)
            self.exportSelectorFrame.grid_columnconfigure(1, minsize=25)

            self.exportSelectorOptionFrame = tk.LabelFrame(self.exportSelectFrame, text="Export options")
            self.exportSelectorOptionFrame.grid(row=1, column=0, sticky="nsew")

            self.exportSelectorOptionFrame.columnconfigure(3, weight=1, minsize=60)

            self.tabContainer.add(self.exportFrame, text="Export")

        
        ## Runs the creation definitions for all frames
        textureOptions()
        imageSelect()
        export()



    ## Creates all widgets in the program
    def createWidgets(self):

        ## Creates all widgets used in the Texture Options tab
        def textureOptions():

            ## Workflow options frame
            ## ---------------------
            ## Workflow options label
            self.workflowLabel = tk.Label(self.workflowOptionsFrame, text="Workflow Settings:")
            self.workflowLabel.grid(row=0, column=0, sticky="nsw")

            ## Configure master frame
            self.workflowOptionsFrame.grid_rowconfigure(0, weight=1)
            self.workflowOptionsFrame.grid_columnconfigure(0, weight=1, uniform="exportOptionsGroup")
            self.workflowOptionsFrame.grid_columnconfigure(1, weight=1, uniform="exportOptionsGroup")
            
            ## Create the two workflow lists
            txt = ["Metalness/Roughness", "Metalness/Smoothness", "Specular/Smoothness"]
            self.workflows = ["Metalness:", "Roughness:", "Metalness:", "Smoothness:", "Specular:", "Smoothness:"]

            ## Define all Tkinter variables used
            self.textureMode = tk.StringVar(None, txt[0])
            self.useNormal = tk.BooleanVar()
            self.useAltNormal = tk.BooleanVar()

            ## Create and place the 3 workflow RadioButtons
            self.cbList = []

            for x in range(3):

                self.cbList.append(tk.Radiobutton(self.workflowOptionsFrame, text=txt[x], variable=self.textureMode, value=txt[x], state="active"))

                self.workflowOptionsFrame.grid_rowconfigure(x+1, weight=1)
                self.cbList[x].grid(row=x+1, column=0, sticky="nsw")

            ## Normal button tickbox
            self.normalTickbox = tk.Checkbutton(self.workflowOptionsFrame, text="Use Normal Map", variable=self.useNormal)
            self.normalTickbox.grid(row=0, column=1, sticky="nsw")

            ## Alt Normal button tickbox
            self.altNormalTickbox = tk.Checkbutton(self.workflowOptionsFrame, text="Use Normal Map Variant", variable=self.useAltNormal, state="disabled")
            self.altNormalTickbox.grid(row=1, column=1, sticky="nsw")

            ## Flexicolour slider label
            flexiLabel = tk.Label(self.flexiColourOptionFrame, text="Flexicolor:")
            flexiLabel.grid(row=0, column=0, sticky="nsew")

            ## Flexicolour slider
            self.flexiScale = tk.Scale(self.flexiColourOptionFrame, from_=0, to=4, resolution=1, orient="horizontal")
            self.flexiScale.grid(row=0, column=1, sticky="nsew")


            ## Advanced options frame
            ## ----------------------
            ## Advanced options label
            self.advancedOptionsLabel = tk.Label(self.advancedOptionsFrame, text="Advanced options:")
            self.advancedOptionsLabel.grid(row=0, column=0, sticky="nsw")

            ## Configure master frame
            self.advancedOptionsFrame.grid_columnconfigure(0, weight=1, uniform="exportOptionsGroup")
            self.advancedOptionsFrame.grid_columnconfigure(1, weight=1, uniform="exportOptionsGroup")

            ## Define tkinter variables
            self.invertRoughnessVar = tk.BooleanVar()
            self.iconUseWallText = tk.BooleanVar()
            self.iconUseNameText = tk.BooleanVar()
            self.iconOverlayBCTexture = tk.BooleanVar()
            self.iconTextName = tk.StringVar()

            ## Roughness map inverter
            self.roughnessMapInverter = tk.Checkbutton(self.advancedOptionsFrame, text="Invert Roughness map", variable = self.invertRoughnessVar)
            self.roughnessMapInverter.grid(row=0, column=1, sticky="nsw")

            ## Icon wall text checkbox
            self.iconBCTextureCheckbutton = tk.Checkbutton(self.advancedOptionsFrame, text="Overlay BC texture onto icon", variable = self.iconOverlayBCTexture)
            self.iconBCTextureCheckbutton.grid(row=1, column=0, sticky="nsw")

            ## Icon wall text checkbox
            self.iconWallTextCheckbutton = tk.Checkbutton(self.advancedOptionsFrame, text="Add wall name to icon", variable = self.iconUseWallText)
            self.iconWallTextCheckbutton.grid(row=1, column=1, sticky="nsw")

            ## Icon name text checkbox
            self.iconNameTextCheckbutton = tk.Checkbutton(self.projectNameFrame, text="Add project name to icon", variable = self.iconUseNameText)
            self.iconNameTextCheckbutton.grid(row=0, column=0, sticky="nesw")

            ## Icon name text label
            self.iconNameTextLabel = tk.Label(self.projectNameFrame, text="Project name:")
            self.iconNameTextLabel.grid(row=0, column=1, sticky="nesw", padx=(10, 5))

            ## Icon Text Entry Widget
            self.iconTextEntry = tk.Entry(self.projectNameFrame, textvariable=self.iconTextName)
            self.iconTextEntry.grid(row=0, column=2, sticky="nsew", padx=(5, 10))

            ## Advanced main image frame
            self.advancedMainImageSelector = self.imageTextureFrameClass(self, self.advancedOptionsFrame, "Main advanced textures", ("AO:", "Emissive:", "Cavity:", "To be added...:"), self.setup.mainAdvancedDirs, (4,0))
            self.advancedMainImageSelector.masterFrame.grid(row=4, column=0, columnspan=2, pady=(10,5))
            self.advancedMainImageSelector.masterFrame.configure(highlightthickness=0)
            self.advancedMainImageSelector.configure(3, True)

            ## Advanced trim image frame
            self.advancedTrimImageSelector = self.imageTextureFrameClass(self, self.advancedOptionsFrame, "Trim advanced textures", ("AO:", "Emissive:", "Cavity:", "To be added...:"), self.setup.trimAdvancedDirs, (5,0))
            self.advancedTrimImageSelector.masterFrame.grid(row=5, column=0, columnspan=2, pady=(5,10))
            self.advancedTrimImageSelector.masterFrame.configure(highlightthickness=0)
            self.advancedTrimImageSelector.configure(3, True)


        def imageTextures():

            self.mainMaterialSelector = self.imageTextureFrameClass(self, self.imageSelectFrame, "Main textures", ("Base Colour:", "Normal:", "Metalness:", "Roughness:"), self.setup.mainMaterialDirs, (0,0))
            self.trimMaterialSelector = self.imageTextureFrameClass(self, self.imageSelectFrame, "Trim textures", ("Base Colour:", "Normal:", "Metalness:", "Roughness:"), self.setup.trimMaterialDirs, (2,0))
            self.mainFlexiColourSelector = self.imageTextureFrameClass(self, self.imageSelectFrame, "Main Flexicolour textures", ("Flexicolor 1:", "Flexicolor 2:", "Flexicolor 3:", "Flexicolor 4:"), self.setup.mainFlexiColourDirs, (4,0))
            self.trimFlexiColourSelector = self.imageTextureFrameClass(self, self.imageSelectFrame, "Trim Flexicolour textures", ("Flexicolor 1:", "Flexicolor 2:", "Flexicolor 3:", "Flexicolor 4:"), self.setup.trimFlexiColourDirs, (6,0))

            self.separator1 = tk.Frame(self.imageSelectFrame, bg=self.PalleteDarkGrey)
            self.separator2 = tk.Frame(self.imageSelectFrame, bg=self.PalleteDarkGrey)
            self.separator3 = tk.Frame(self.imageSelectFrame, bg=self.PalleteDarkGrey)
            self.separator4 = tk.Frame(self.imageSelectFrame, bg=self.PalleteDarkGrey)

            self.separator1.grid(row=1, column=0, sticky="nsew")
            self.separator2.grid(row=3, column=0, sticky="nsew")
            self.separator3.grid(row=5, column=0, sticky="nsew")
            self.separator4.grid(row=7, column=0, sticky="nsew")
            
            self.imageSelectFrame.grid_columnconfigure(0, weight=1)
            self.imageSelectFrame.grid_rowconfigure(1, minsize=30)
            self.imageSelectFrame.grid_rowconfigure(3, minsize=30)
            self.imageSelectFrame.grid_rowconfigure(5, minsize=30)
            self.imageSelectFrame.grid_rowconfigure(7, weight=1, minsize=30)

            self.mainFlexiColourSelector.configure(0, False)
            self.trimFlexiColourSelector.configure(0, False)


        def export():

            class checkButton():

                def __init__(self, guiClass, parent, text):

                    self.buttonVar = tk.IntVar()
                    self.button = tk.Checkbutton(guiClass.exportOptionCanvas,text=text, variable=self.buttonVar)


            self.exportOptionCanvas = tk.Canvas(self.exportSelectorFrame, scrollregion=(0, 0, 5000, 5000), bd=0, highlightthickness=0)
            self.exportScroll = tk.Scrollbar(self.exportSelectorFrame, orient=tk.VERTICAL, command=self.exportOptionCanvas.yview)

            self.exportCBList = []

            for x in range(len(self.setup.foundFiles)):

                self.exportCBList.append(checkButton(self, self.exportOptionCanvas, self.setup.foundFiles[x]))
                self.exportCBList[x].button.grid(row=x, column = 0, sticky="nsw")

                w = self.exportOptionCanvas.create_window(0, x*20 + 20, window=self.exportCBList[x].button, anchor=tk.W)

            self.exportOptionCanvas.grid(row=0, column=0, sticky="nsew")
            self.exportScroll.grid(row=0, column=1, sticky="nse")

            self.exportOptionCanvas.configure(yscrollcommand = self.exportScroll.set)
            self.exportOptionCanvas.configure(scrollregion=self.exportOptionCanvas.bbox("all"))

            self.optionSelectAllButton = tk.Button(self.exportSelectorOptionFrame, text="Select All", command=lambda: self.onEvent.onExportSelectionButton(self, "select"), bg=self.PalleteLightGrey)
            self.optionDeSelectAllButton = tk.Button(self.exportSelectorOptionFrame, text="Deselect All", command=lambda: self.onEvent.onExportSelectionButton(self, "deselect"), bg=self.PalleteLightGrey)
            self.optionInverseAllButton = tk.Button(self.exportSelectorOptionFrame, text="Inverse Selection", command=lambda: self.onEvent.onExportSelectionButton(self, "inverse"), bg=self.PalleteLightGrey)
            self.optionExportButton = tk.Button(self.exportSelectorOptionFrame, text="EXPORT", command=lambda: self.onEvent.onExport(self, self.setup), bg=self.PalleteRed)

            self.optionSelectAllButton.grid(row=0, column=0, sticky="nsew", padx=(5,5))
            self.optionDeSelectAllButton.grid(row=0, column=1, sticky="nsew", padx=(5,5))
            self.optionInverseAllButton.grid(row=0, column=2, sticky="nsew", padx=(5,5))
            self.optionExportButton.grid(row=0, column=3, sticky="nse", padx=(5,5))

            self.exportOptionCanvas.update()


        textureOptions()
        imageTextures()
        export()

    
    def createBinds(self):

        ## Disable at setup all image selectors that are not enabled by default
        self.mainMaterialSelector.configure(1, True)
        self.trimMaterialSelector.configure(1, True)

        for x in range(4):
            self.mainFlexiColourSelector.configure(x, True)
            self.trimFlexiColourSelector.configure(x, True)


        self.cbList[0].configure(command = lambda: self.onEvent.onWorkflowChange(self, 0))
        self.cbList[1].configure(command = lambda: self.onEvent.onWorkflowChange(self, 1))
        self.cbList[2].configure(command = lambda: self.onEvent.onWorkflowChange(self, 2))

        def onUpdate(event):
            self.onEvent.onSliderUpdate(self)

        self.flexiScale.bind("<ButtonRelease-1>", onUpdate)

        self.normalTickbox.configure(command = lambda: self.onEvent.onNormalMapClick(self))


    def createStartupPopup(self):

        self.root.state("iconic")
        openDocumentation = messagebox.askquestion(title = "Material Editor", message = "Thank you for downloading the Material Editor! \n \n Would you like to read the starting documentation?")

        if openDocumentation == "yes":

            os.system("notepad.exe " + "{}/README.txt".format(self.setup.programFolder))
            self.root.state("normal")

        else:

            self.root.wm_state("normal")









    ## This class is for creating 2x2 image frames. This is only called when the GUI is being set up or a specific image frame needs to be configured
    class imageTextureFrameClass():

        '''
        Places a 2x2 image selection box at a given point.
        '''

        def __init__(self, guiClass, root, frameName, labels = ("0", "1", "2", "3"), directoryList=("0", "1", "2", "3"), offset=(0,0)):

            self.children = list()

            self.masterFrame = tk.LabelFrame(root, text=frameName, highlightthickness=1, highlightbackground="black")

            self.masterFrame.grid_columnconfigure(0, weight=1, uniform="group1")
            self.masterFrame.grid_columnconfigure(1, weight=1, uniform="group1")

            self.masterFrame.grid_rowconfigure(0, weight=1)
            self.masterFrame.grid_rowconfigure(1, weight=1)

            for widget in range(4):
                self.children.append(self.singleImageTexture(self, guiClass, labels, directoryList, widget))
                pass

            self.children[0].frame.grid(row=0, column=0, sticky="news")
            self.children[1].frame.grid(row=0, column=1, sticky="news")
            self.children[2].frame.grid(row=1, column=0, sticky="news")
            self.children[3].frame.grid(row=1, column=1, sticky="news")

            self.masterFrame.grid(row = offset[0], column = offset[1], sticky="nsew")

        def configure(self, widget, disabled):

            """
            Configures a selection box within the 2x2 grid.

            Parameters
            ----------
            widget : int
                An integer that specifies the widget object
            disabled : bool
                A bool, whether the entire frame should be disabled
            """

            if disabled:
                state = "disable"

            else:
                state = "normal"

            for child in self.children[widget].frame.winfo_children():
                child.configure(state=state)



        class singleImageTexture():

            def __init__(self, master, guiClass, name, dirVar, widget):

                self.frame = tk.Frame(master.masterFrame)

                self.selector = tk.Button(self.frame, text=dirVar[widget], command=lambda: guiClass.onEvent.onFileManager(guiClass, master, widget, dirVar, "pick"), bg=guiClass.PalleteLightGrey)
                self.label = tk.Label(self.frame, text=name[widget])
                self.remover = tk.Button(self.frame, text="Remove", command=lambda: guiClass.onEvent.onFileManager(guiClass, master, widget, dirVar, "remove"), bg=guiClass.PalleteRed)

                self.frame.rowconfigure(0, weight=1, minsize=20)
                self.frame.rowconfigure(1, weight=1, minsize=20)
                 
                self.frame.columnconfigure(0, weight=1, minsize=60)
                self.frame.columnconfigure(1, weight=1, minsize=30)
                self.frame.columnconfigure(2, weight=1, minsize=30)

                self.label.grid(row=0, column=0, sticky="nws", padx=(2, 2), pady=(2,2))
                self.remover.grid(row=0, column=2, sticky="nes", padx=(2, 2), pady=(2,2))
                self.selector.grid(row=1, column=0, sticky="nsew", columnspan=3, padx=(2, 2), pady=(2,2))