import maya.cmds as mc

iconSize = 32
path = "E:/kTools/icons/"

print "kShelf"


class kShelfTool():

    def __init__(self):
        print "__init__"
        self.wsCN = "kShelf"
        if mc.workspaceControl(self.wsCN, q=True, exists=True):
            print ">>> le workspace : " + self.wsCN + " existe deja !!!"
            mc.deleteUI(self.wsCN, control=True)
        else:
            print ">>> le workspace : " + self.wsCN + " n'existe pas !!"

    def createkShelfUI():
        print "createUI"
        mc.columnLayout()
        mc.button("coucou")
        mc.button("annuler")
        '''                        
        allButtons = [("bt_kMaxToolBar", "kMaxTool32.png", "kMaxTool32b.png", "Launch kMaxTools"),
                      ("bt_kMod", "kMaxMod32.png", "kMaxMod32.png", "Launch kMod Left bar")]
                        ("bt_kMaxShelfTop","kMaxShelfTop32.png","kMaxShelfTop32.png","Launch kMaxShelfTop"),
                        ("bt_outlinerView","outliner.png","outliner.png","Outliner/Persp"),
                        ("bt_singlePerspView","singlePerspLayout2016_32.png","singlePerspLayout2016_32.png","Single Perspective View"),
                        ("bt_fourView","fourViewLayout2016_32.png","fourViewLayout2016_32.png","Four View"),
                        ("bt_new","new.png","new.png","Create a New Scene"),
                        ("bt_classicOpen","open.png","open.png","Open a Scene"),
                        ("bt_classicSave","save.png","save.png","Save the current Scene"),
                        ("bt_savePlus","save+.png","save+.png","Incremental Save"),
                        ("bt_classicSaveAs","saveAs.png","saveAs.png","Save the current scene under a new name or export all")]
        mc.rowColumnLayout(numberOfRows=1, rowHeight=(1, iconSize))
        for btnName, btnImg, btnHighImg, btnAnno in allButtons:
            mc.iconTextButton(style='iconOnly', image1=path + btnImg, highlightImage=path + btnHighImg,
                              annotation=btnAnno, width=iconSize)  # command=btnCommand
        '''

    def build(self):
        print "build"
        mc.workspaceControl(self.wsCN, floating=True, retain=True, uiScript="self.createkShelfUI()")
        #mc.workspaceControl(self.wsCN, edit=True, initialHeight=iconSize, dockToControl=("Shelf", "top"))



kShelfTool().build()
