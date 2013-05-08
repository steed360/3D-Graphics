# investigations with basic 3D graphics concepts

import wx
import numpy
import math

class TransformationMatrices:

  @classmethod
  def GetTrMatrixAroundX (cls,theta):

    cosTh  = math.cos (math.radians(theta))
    sinTh  = math.sin (math.radians(theta))
    return  numpy.matrix ([     1,      0,      0, 0, \
                                0,  cosTh, -sinTh, 0, \
                                0, sinTh,  cosTh, 0, \
                                0,      0,      0, 1 ]  ).reshape(4,4)

  @classmethod
  def GetTrMatrixAroundY (cls,theta):  

    cosTh  = math.cos (math.radians(theta))
    sinTh  = math.sin (math.radians(theta))
    return  numpy.matrix ([ cosTh,      0,  sinTh, 0, \
                                0,      1,      0, 0, \
                           -sinTh,      0,  cosTh, 0, \
                                 0,     0,      0, 1 ]  ).reshape(4,4)
 
  @classmethod  
  def GetTrMatrixAroundZ(cls,theta):

    cosTh  = math.cos (math.radians(theta))
    sinTh  = math.sin (math.radians(theta))
    return  numpy.matrix ([cosTh, -sinTh,  0, 0, \
                            sinTh,  cosTh,  0, 0, \
                            0,          0,  1, 0, \
                            0,          0,  0, 1 ]  ).reshape(4,4)

class ThreeDObject:

  def __init__ (self, lstPoints, centre):
    # points are xyz tuples
    self.lstPoints = lstPoints
    self.centre = centre
    self.setRotatePoint ("None")

  def setRotatePoint (self, rp):
    #rp is a 3*tuple
    self.rotatePoint = rp

  def setLstPoints (self, inlstPoints):
    self.lstPoints = inlstPoints

  def rotatePointOnAxis ( self,theta, xyzTuple, axis ):

    '''
    - theta - degrees (not radians)
    - xyzTuple - (x,y,z)
    - returns the transformed point as an x,y,z point
    '''

    if axis == 'X': trMatrix = TransformationMatrices.GetTrMatrixAroundX(theta)
    if axis == 'Y': trMatrix = TransformationMatrices.GetTrMatrixAroundY (theta)
    if axis == 'Z': trMatrix = TransformationMatrices.GetTrMatrixAroundZ (theta)

    # Translate the point to the centre of the object

    if self.rotatePoint != "None":
      currentRotatePoint = self.rotatePoint
    else:
      currentRotatePoint = self.centre

    centreOffset = ( xyzTuple[0] - currentRotatePoint[0], 
                     xyzTuple[1] - currentRotatePoint[1] , 
                     xyzTuple[2] - currentRotatePoint[2]  ) 

#    print "centre offset:" + str(centreOffset)
      
    resMatrix = trMatrix * \
               numpy.matrix \
               ( [ centreOffset[0], centreOffset[1], 
                  centreOffset[2], 1 ] ).reshape (4,1)
 

    # Re-translate rotated point back to correct offset relative to object centre
    resPoint = ( resMatrix [0,0] + currentRotatePoint[0] , 
                 resMatrix [1,0] + currentRotatePoint[1],              
                 resMatrix [2,0] + currentRotatePoint[2] )

#    print "Resulting point:" + str(resPoint)
    return resPoint

  def rotateOnAxis (self, theta, axis ):
    for i in range ( 0, len ( self.lstPoints) ):      
	      # remember points are tuples (x,y,z)
      self.lstPoints[i] = self.rotatePointOnAxis ( theta, self.lstPoints[i] , axis )


  def draw (self, canvas, strColour ):
#    print "3DObject.draw () should be overridden by subclasses"
    dc = canvas
    dc.SetPen(wx.Pen("BLACK", 5))

  def getProjectedListPoints (self, eyePos):
    # eye position is an x,y,z tuple

    projectedListPoints = []

    for i in range ( 0, len ( self.lstPoints) ):
      # remember points are tuples (x,y,z)
      projectedListPoints.append ( self.projectPoint ( self.lstPoints[i], eyePos ) ) 
    
    return projectedListPoints

  def projectPoint (self,  pTuple , cTuple    ):

    # c/pTuple (x,y,z)
    # c is a fixed point, basically where the point is viewed from
    # p is a point that need projecting

    cx = cTuple [0];  cy = cTuple [1]; cz = cTuple [2]
    px = pTuple [0];  py = pTuple [1]; pz = pTuple [2]

    distScreenFromEye = 2
    d2 = distScreenFromEye

    # find intercept ratio

    t =  ( -cz + d2 ) / float ( pz - cz ) 

    x = cx + (t * (px - cx ))
    y = cy + (t * (py - cy ))

#    print "Result: " + str (x) + " " + str (y)
    return  x ,y 

class ThreeDPolygon (ThreeDObject): 

  def __init__ ( self , centre, width, height, depth ):
    self.lstPoints = self.createPointsList ( centre, width, height, depth)
#    print "***"
#    print self.lstPoints
    self.centre = centre
 
  def createPointsList (self,centre, width, height, depth):
  
    l = []
    # bottom front left point
    bflp_X = centre[0] - float (width/2)
    bflp_Y = centre[1] - float (height/2)
    bflp_Z = centre[2] - float (depth/2)

    # Create front polygon
    l.append ( ( bflp_X,          bflp_Y,           bflp_Z ) )
    l.append ( ( bflp_X + width , bflp_Y,           bflp_Z ) )
    l.append ( ( bflp_X + width , bflp_Y + height , bflp_Z ) )
    l.append ( ( bflp_X ,         bflp_Y + height , bflp_Z ) )

    # Create rear polygon
    l.append ( ( bflp_X,          bflp_Y,           bflp_Z + depth ) )
    l.append ( ( bflp_X + width , bflp_Y,           bflp_Z + depth ) )
    l.append ( ( bflp_X + width , bflp_Y + height , bflp_Z + depth ) )
    l.append ( ( bflp_X ,         bflp_Y + height , bflp_Z + depth ) )

    return l

class ThreeDPolygon (ThreeDObject): 

  def __init__ ( self , centre, width, height, depth ):
    self.lstPoints = self.createPointsList ( centre, width, height, depth)
    self.centre = centre
    self.setRotatePoint ("None")
 
  def createPointsList (self,centre, width, height, depth):
  
    l = []
    # bottom front left point
    bflp_X = centre[0] - float (width/2)
    bflp_Y = centre[1] - float (height/2)
    bflp_Z = centre[2] - float (depth/2)

    # Create front polygon
    l.append ( ( bflp_X,          bflp_Y,           bflp_Z ) )
    l.append ( ( bflp_X + width , bflp_Y,           bflp_Z ) )
    l.append ( ( bflp_X + width , bflp_Y + height , bflp_Z ) )
    l.append ( ( bflp_X ,         bflp_Y + height , bflp_Z ) )

    # Create rear polygon
    l.append ( ( bflp_X,          bflp_Y,           bflp_Z + depth ) )
    l.append ( ( bflp_X + width , bflp_Y,           bflp_Z + depth ) )
    l.append ( ( bflp_X + width , bflp_Y + height , bflp_Z + depth ) )
    l.append ( ( bflp_X ,         bflp_Y + height , bflp_Z + depth ) )

    return l

  def setCentre (self, centre):
    self.centre = centre

  def draw (self, eyePos, canvas, strCol ):
    lst = self.getProjectedListPoints (eyePos)

#    print lst
    dc = canvas
    dc.SetPen(wx.Pen(strCol, 5))

    # front polygon
    dc.DrawLine ( lst[0][0], yCorr (lst[0][1]), lst[1][0], yCorr (lst[1][1]) )
    dc.DrawLine ( lst[1][0], yCorr (lst[1][1]), lst[2][0], yCorr (lst[2][1]) )
    dc.DrawLine ( lst[2][0], yCorr (lst[2][1]), lst[3][0], yCorr (lst[3][1]) )
    dc.DrawLine ( lst[3][0], yCorr (lst[3][1]), lst[0][0], yCorr (lst[0][1]) )
 
    # rear polygon
    dc.DrawLine ( lst[4][0], yCorr (lst[4][1]), lst[5][0], yCorr (lst[5][1]) )
    dc.DrawLine ( lst[5][0], yCorr (lst[5][1]), lst[6][0], yCorr (lst[6][1]) )
    dc.DrawLine ( lst[6][0], yCorr (lst[6][1]), lst[7][0], yCorr (lst[7][1]) )
    dc.DrawLine ( lst[7][0], yCorr (lst[7][1]), lst[4][0], yCorr (lst[4][1]) )
  
    # link front and back (bottom)
    dc.DrawLine ( lst[0][0], yCorr (lst[0][1]), lst[4][0], yCorr (lst[4][1]) )
    dc.DrawLine ( lst[1][0], yCorr (lst[1][1]), lst[5][0], yCorr (lst[5][1]) )

    # link front and back (top)
    dc.DrawLine ( lst[2][0], yCorr (lst[2][1]), lst[6][0], yCorr (lst[6][1]) )
    dc.DrawLine ( lst[3][0], yCorr (lst[3][1]), lst[7][0], yCorr (lst[7][1]) )

    # for debugging, plot a line from the centre to the left bl corner
#    projCentreTuple= self.projectPoint (self.centre, eyePos) 
#    dc.DrawLine ( projCentreTuple[0], yCorr (projCentreTuple[1]), lst[0][0], yCorr (lst[0][1]) )


class Composite3DShape (ThreeDObject):

  def __init__ ( self , centre ):
    self.shapes = []
    self.centre = centre

  def add (self, shape  ):
    self.shapes.append (shape)

  def draw (self, eyePos, canvas, strCol ):
    for s in self.shapes:
      s.draw(eyePos, canvas, strCol)

  def rotateOnAxis (self, theta, axis ):
    for s in self.shapes:
      s.rotateOnAxis ( theta, axis )

# y correction - y reverse axis
def yCorr (y):
  return 500 - y

def drawCircle (radius, canvas, strCol ):

  centre = (100,100)
  cX = centre[0]
  cY = centre[1]

  dc = canvas
  dc.SetPen(wx.Pen(strCol, 5))

  x1 =  0
  y1 =  math.sqrt ( math.pow (radius,2)  - math.pow(x1, 2) )  

  for x2 in range ( 1, radius + 1 , 1 ):

    y2 = math.sqrt ( math.pow (radius,2)  - math.pow(x2, 2) )
    dc.DrawLine ( cX+ x1 ,  yCorr ( cY + y1 ), cX + x2, yCorr (cY + y2) )
    dc.DrawLine ( cX+ x1 ,  yCorr ( cY - y1 ), cX + x2, yCorr (cY - y2) )
    dc.DrawLine ( cX- x1 ,  yCorr ( cY + y1 ), cX - x2, yCorr (cY + y2) )
    dc.DrawLine ( cX- x1 ,  yCorr ( cY - y1 ), cX - x2, yCorr (cY - y2) )

    y1 = y2
    x1 = x2

glCube   = ThreeDPolygon ( (200,200,400), 100, 100, 300)

glRightWing = ThreeDPolygon ( (350, 225,200), 200, 10, 30)
glLeftWing  = ThreeDPolygon ( (50 ,225 ,200), 200, 10, 30)
glTail      = ThreeDPolygon ( (200 , 300 , 300), 5, 100, 10)

glRightWing.setRotatePoint   ( (200,225,200) )
glLeftWing.setRotatePoint    ( (200,225,200) )
glTail.setRotatePoint ((200,200,400))

shape = Composite3DShape ( glCube.centre )
shape.add (glCube)
shape.add (glRightWing)
shape.add (glLeftWing)
shape.add (glTail)

eyePosition = (	200 , 300, -100)

def on_paint(event):
  dc = wx.PaintDC(event.GetEventObject())
  dc.Clear()
#  glCube.draw ( eyePosition, dc, 'GREEN' )
  shape.draw ( eyePosition, dc, 'GREEN')
  drawCircle ( 50, dc, 'GREEN')

def on_mouseClick (event):

  on_paint (event)

def on_KeyDown (event):
  if event.GetKeyCode () == wx.WXK_LEFT :
    shape.rotateOnAxis ( 5.0, 'Z' )
    on_paint (event)  

  if event.GetKeyCode () == wx.WXK_RIGHT :
    shape.rotateOnAxis ( -5.0, 'Z' )
    on_paint (event)  

  if event.GetKeyCode () == wx.WXK_UP:
    shape.rotateOnAxis ( 5.0, 'X' )
    on_paint (event)  

  if event.GetKeyCode () == wx.WXK_DOWN:
    shape.rotateOnAxis ( -5.0, 'X' )
    on_paint (event)  

app = wx.App(False)
frame = wx.Frame(None, title="Draw on Panel")
panel = wx.Panel(frame)
panel.Bind(wx.EVT_PAINT, on_paint)
panel.Bind(wx.EVT_LEFT_DOWN, on_mouseClick)

panel.SetFocusIgnoringChildren()
panel.Bind(wx.EVT_KEY_DOWN, on_KeyDown )

frame.Show(True)
app.MainLoop()

