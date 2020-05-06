import os as os
from PIL import Image,ImageDraw,ImageFont,ImageChops as PIL
import PIL.ImageOps
import time as time
import math as math
import shutil as shutil

class export():

    def __init__(self, setup):

        self.setup = setup

    def findAllFBXFiles(self, absPath):

        files = os.listdir(absPath)
        fbxFiles = [file for file in files if file.endswith('.fbx')]

        fbxFiles.sort(key=str.lower)
        return fbxFiles


    def findOutputDirectory(self, absPath):

        self.runSetup = False;

        while True:
            try:
                with open("{}/programFiles/defaultDirectory.txt".format(absPath), "r") as file:
                    directory = file.read()
                    break
            except:
                with open("{}/programFiles/defaultDirectory.txt".format(absPath), "a+") as file:
                    self.runSetup = True;
                    file.write("{}/Default output/".format(absPath))

        return directory

    def writeOutputDirectory(self, directoryToWrite, absPath):

        if directoryToWrite != "":

            with open("{}/programFiles/defaultDirectory.txt".format(absPath), "w") as file:
                file.write("{}{}".format(directoryToWrite,"/"))
                directory = "{}{}".format(directoryToWrite,"/")

        else:
            directory = self.findOutputDirectory(absPath)

        return directory


    def deleteTempFolder(self, appFolder):
        shutil.rmtree("{}/programFiles/temp/".format(appFolder))


    def finalExport(self, guiClass, appFolder, setup):

        def doImageEditing(doWall, doName, doOverlay, wall):

            ## Brunt of the workload here.
            def drawText(iterations, position, offset, text, outlineColour, textColour, font):

                for x in range(iterations):
                    draw.text((position[0] + math.sin(x) * offset, position[1] + math.cos(x) * offset ), text, outlineColour, font=font)

                draw.text((position[0], position[1]), text, textColour,font=font)


            if doOverlay:
                
                imgIcon = PIL.Image.open("{}/programFiles/temp/icon.png".format(appFolder))
                imgOverlay = PIL.Image.open("{}/programFiles/temp/main_BC.png".format(appFolder))

                print(imgIcon.mode)
                print(imgOverlay.mode)

                imgOverlay = imgOverlay.convert("RGBA")

                imgOverlay = imgOverlay.resize((512, 512), Image.ANTIALIAS)

                img = PIL.ImageChops.multiply(imgIcon, imgOverlay)

            else:
                img = PIL.Image.open("{}/programFiles/temp/icon.png".format(appFolder))

            draw = PIL.ImageDraw.Draw(img)

            if doWall:

                fontToUse = PIL.ImageFont.truetype("{}/programFiles/Eagle-Bold.otf".format(appFolder), 45)
                drawText(64, (20, 400), 2, wall, (0,0,0), (255,255,255), fontToUse)


            if doName:

                name = guiClass.iconTextName.get()

                fontSize = int(round(-0.4 * len(name) + 40, 0))

                if fontSize < 1:

                    fontSize = 1


                fontToUse = PIL.ImageFont.truetype("{}/programFiles/Eagle-Bold.otf".format(appFolder), fontSize)
                drawText(64, (20, 450), 2, guiClass.iconTextName.get(), (0,0,0), (255,255,255), fontToUse)
            
            img.save("{}/programFiles/temp/icon.png".format(appFolder))



        def rnInvert(doInvert, material, directory):

            if doInvert:
                rnMap = PIL.Image.open(directory)

                rnMap = rnMap.convert("L")
                rnMap = PIL.ImageOps.invert(rnMap)

                rnMap.save("{}/programFiles/temp/{}_RN.png".format(appFolder, material))

            elif doInvert == False:

                rnMap = PIL.Image.open(directory)
                rnMap.save("{}/programFiles/temp/{}_RN.png".format(appFolder, material))

        def exportZippingHandler(fbxFile, doWallText, doNameText, doIconOverlay):


            zipName = os.path.splitext(fbxFile)[0]

            if os.path.isfile("{}/programFiles/models/icons/{}.png".format(appFolder, zipName)):

                shutil.copy("{}/programFiles/models/icons/{}.png".format(appFolder, zipName, ".png"), "{}/programFiles/temp/icon.png".format(appFolder))

            else:

                shutil.copy("{}/programFiles/models/icons/default.png".format(appFolder), "{}/programFiles/temp/icon.png".format(appFolder))

            doImageEditing(doWallText, doNameText, doIconOverlay, zipName)

            shutil.copy("{}/programFiles/models/fbx/{}".format(appFolder, fbxFile), "{}/programFiles/temp/{}".format(appFolder, fbxFile))


            shutil.make_archive("{}{}".format(setup.outputDirectory, zipName), "zip", "{}/programFiles/temp/".format(appFolder))

            os.remove("{}/programFiles/temp/{}".format(appFolder, fbxFile))
            os.remove("{}/programFiles/temp/icon.png".format(appFolder))


        def outputImageFilesToMasterDirectory(directoryList, prefixList, materialName):

            for x in range(len(prefixList)):

                if directoryList[x] != "No File Selected" and prefixList[x] != "":

                    if prefixList[x] == "_RN":
                        rnInvert(guiClass.invertRoughnessVar.get(), materialName, directoryList[x])

                    elif prefixList[x] == "_MT" or prefixList[x] == "_SM" or prefixList[x] == "_SP":
                        img = PIL.Image.open(directoryList[x]).convert("L")
                        img.save("{}/programFiles/temp/{}{}.png".format(appFolder, materialName, prefixList[x]))

                    else:

                        if prefixList[x] == "_BC":

                            img = PIL.Image.open(directoryList[x])

                            if img.size[0] > 1024 or img.size[1] > 1024:

                                raise ValueError("BCMapTooBig")

                        shutil.copy(directoryList[x], "{}/programFiles/temp/{}{}.png".format(appFolder, materialName, prefixList[x]))
                else:

                    if prefixList[x] == "_BC":
                        raise ValueError("BCMapMissing")


        def getPrefixes():

            self.normalPrefix = ""
            self.workflow = ("", "")
            self.flexiPrefixes = ["", "", "", ""]
            self.advancedPrefixes = ["_AO", "_CA", "_EM", ""]

            if guiClass.useNormal.get() == True:

                self.normalPrefix = "_NM"

                if guiClass.useAltNormal.get() == True:

                    self.normalPrefix = "_NG"


            if guiClass.textureMode.get() == "Metalness/Roughness":

                self.workflow = ("_MT", "_RN")

            elif guiClass.textureMode.get() == "Metalness/Smoothness":

                self.workflow = ("_MT", "_SM")

            elif guiClass.textureMode.get() == "Specular/Smoothness":

                self.workflow = ("_SP", "_SM")


            for x in range(guiClass.flexiScale.get()):

                self.flexiPrefixes[x] = "_F{}".format(x+1)


        self.exportStack = []

        try:
            os.makedirs("{}/programFiles/temp/".format(appFolder))
        except OSError:
            pass

        for x in range(len(guiClass.exportCBList)): 

            if guiClass.exportCBList[x].buttonVar.get() == 1:

                self.exportStack.append(self.setup.foundFiles[x])

        if len(self.exportStack) < 1:
            raise ValueError("NoObjectInExport")


        getPrefixes()

        self.mainPrefixes = ("_BC", self.normalPrefix, self.workflow[0], self.workflow[1])

        outputImageFilesToMasterDirectory(self.setup.mainMaterialDirs, self.mainPrefixes, "main")
        outputImageFilesToMasterDirectory(self.setup.trimMaterialDirs, self.mainPrefixes, "trim")
        outputImageFilesToMasterDirectory(self.setup.mainFlexiColourDirs, self.flexiPrefixes, "main")
        outputImageFilesToMasterDirectory(self.setup.trimFlexiColourDirs, self.flexiPrefixes, "trim")
        outputImageFilesToMasterDirectory(self.setup.mainAdvancedDirs, self.advancedPrefixes, "main")
        outputImageFilesToMasterDirectory(self.setup.trimAdvancedDirs, self.advancedPrefixes, "trim")
        
        useWallText = False
        useNameText = False
        useOverlay = False

        name = guiClass.iconTextName.get()

        if len(name) > 32:
            raise ValueError("ProjectNameTooBig")

        if guiClass.iconUseWallText.get() == 1:
            useWallText = True

        if guiClass.iconUseNameText.get() == 1:
            useNameText = True

        if guiClass.iconOverlayBCTexture.get() == 1:
            useOverlay = True


        for file in range(len(self.exportStack)):
            exportZippingHandler(self.exportStack[file], useWallText, useNameText, useOverlay)

        os.startfile(self.setup.outputDirectory)




    

