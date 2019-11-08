import maya.cmds as mc

renderBall = mc.renderThumbnailUpdate(q=True)
if renderBall:
    mc.renderThumbnailUpdate(False)
    print ">> Render Thumbnail OFF"
else:
    mc.renderThumbnailUpdate(True)
    print ">> Render Thumbnail ON"