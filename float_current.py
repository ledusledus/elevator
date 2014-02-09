# much of this is coming from sample app of wx floatcanvas.
import cStringIO

try:
    import numpy as N
    import numpy.random as RandomArray
    haveNumpy = True
    #print "Using numpy, version:", N.__version__
except ImportError:
            # numpy isn't there
            haveNumpy = False
            errorText = (
            "The FloatCanvas requires the numpy module, version 1.* \n\n"
            "You can get info about it at:\n"
            "http://numpy.scipy.org/\n\n"
            )
      
#---------------------------------------------------------------------------

def _ColorFromElevation(elevation):
    if elevation == -1:
        return "Red"
    return "Blue"

def BuildDrawFrame(): # this gets called when needed, rather than on import
    try:
        from floatcanvas import NavCanvas, FloatCanvas, Resources
    except ImportError: # if it's not there locally, try the wxPython lib.
        from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources
    import wx.lib.colourdb
    import time, random

    class DrawFrame(wx.Frame):

        """
        A frame used for the FloatCanvas Demo

        """


        def __init__(self,parent, id,title,position,size):
            wx.Frame.__init__(self,parent, id,title,position, size)

            ## Set up the MenuBar
            MenuBar = wx.MenuBar()

            file_menu = wx.Menu()
            item = file_menu.Append(-1, "&Close","Close this frame")
            self.Bind(wx.EVT_MENU, self.OnQuit, item)

            item = file_menu.Append(-1, "&Save File","Save the updated dxf")
            self.Bind(wx.EVT_MENU, self.OnSaveFILE, item)

            item = file_menu.Append(-1, "&Open File","Open vector file")
            self.Bind(wx.EVT_MENU, self.OnOpenFILE, item)

            MenuBar.Append(file_menu, "&File")
            
            draw_menu = wx.Menu()

            item = draw_menu.Append(-1, "&Hit Test","Run a test of the hit test code")
            self.Bind(wx.EVT_MENU, self.TestHitTest, item)

            MenuBar.Append(draw_menu, "&Tests")

            view_menu = wx.Menu()
            item = view_menu.Append(-1, "Zoom to &Fit","Zoom to fit the window")
            self.Bind(wx.EVT_MENU, self.ZoomToFit, item)
            MenuBar.Append(view_menu, "&View")

            help_menu = wx.Menu()
            item = help_menu.Append(-1, "&About",
                                    "More information About this program")
            self.Bind(wx.EVT_MENU, self.OnAbout, item)
            MenuBar.Append(help_menu, "&Help")

            self.SetMenuBar(MenuBar)

            self.CreateStatusBar()

            
            # Add the Canvas
            NC = NavCanvas.NavCanvas(self,
                                     Debug = 0,
                                     BackgroundColor = "DARK SLATE BLUE")

            self.Canvas = NC.Canvas # reference the contained FloatCanvas

            self.MsgWindow = wx.TextCtrl(self, wx.ID_ANY,
                                         "Look Here for output from events\n",
                                         style = (
                                                  wx.SUNKEN_BORDER)
                                         )
            self.MsgWindow.Bind(wx.EVT_TEXT, self.OnMsgUpdate)
            
            ##Create a sizer to manage the Canvas and message window
            MainSizer = wx.BoxSizer(wx.VERTICAL)
            MainSizer.Add(NC, 4, wx.EXPAND)
            MainSizer.Add(self.MsgWindow, 1, wx.EXPAND | wx.ALL, 5)

            self.SetSizer(MainSizer)
            self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

            self.EventsAreBound = False

            ## getting all the colors for random objects
            wx.lib.colourdb.updateColourDB()
            self.colors = wx.lib.colourdb.getColourList()

            self.lastline = None

            return None
        def OnMsgUpdate(self, object):
            if self.lastline != None:
                try:
                    self.elevations[self.lastline.line_idx] = float(self.MsgWindow.GetValue())
                except ValueError:
                    self.elevations[self.lastline.line_idx]

        def Log(self, text):
            self.MsgWindow.AppendText(text)
            if not text[-1] == "\n":
                self.MsgWindow.AppendText("\n")
            

        def BindAllMouseEvents(self):
            if not self.EventsAreBound:
                ## Here is how you catch FloatCanvas mouse events
                self.Canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.OnLeftDown) 
                self.Canvas.Bind(FloatCanvas.EVT_LEFT_UP, self.OnLeftUp)
                self.Canvas.Bind(FloatCanvas.EVT_LEFT_DCLICK, self.OnLeftDouble) 

                self.Canvas.Bind(FloatCanvas.EVT_MIDDLE_DOWN, self.OnMiddleDown) 
                self.Canvas.Bind(FloatCanvas.EVT_MIDDLE_UP, self.OnMiddleUp) 
                self.Canvas.Bind(FloatCanvas.EVT_MIDDLE_DCLICK, self.OnMiddleDouble) 

                self.Canvas.Bind(FloatCanvas.EVT_RIGHT_DOWN, self.OnRightDown) 
                self.Canvas.Bind(FloatCanvas.EVT_RIGHT_UP, self.OnRightUp) 
                self.Canvas.Bind(FloatCanvas.EVT_RIGHT_DCLICK, self.OnRightDouble) 

            self.EventsAreBound = True


        def UnBindAllMouseEvents(self):
            ## Here is how you unbind FloatCanvas mouse events
            self.Canvas.Unbind(FloatCanvas.EVT_LEFT_DOWN)
            self.Canvas.Unbind(FloatCanvas.EVT_LEFT_UP)
            self.Canvas.Unbind(FloatCanvas.EVT_LEFT_DCLICK)

            self.Canvas.Unbind(FloatCanvas.EVT_MIDDLE_DOWN)
            self.Canvas.Unbind(FloatCanvas.EVT_MIDDLE_UP)
            self.Canvas.Unbind(FloatCanvas.EVT_MIDDLE_DCLICK)

            self.Canvas.Unbind(FloatCanvas.EVT_RIGHT_DOWN)
            self.Canvas.Unbind(FloatCanvas.EVT_RIGHT_UP)
            self.Canvas.Unbind(FloatCanvas.EVT_RIGHT_DCLICK)

            self.EventsAreBound = False


        def PrintCoords(self,event):
            self.Log("coords are: %s"%(event.Coords,))
            self.Log("pixel coords are: %s\n"%(event.GetPosition(),))

        def DrawLines(self):
            for i in range(len(self.lines)):
                L = self.Canvas.AddLine(self.lines[i], LineWidth = 2, LineColor = _ColorFromElevation(self.elevations[i]))
                L.line_idx = len(self.lines)-1
                L.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.LineGotHit)
            self.Canvas.Draw(Force = True)
                
        def DrawDxf(self, path):
            from dxf_reader import DXFReader
            dxf = DXFReader("sample_export_from_ocad2.dxf")
            self.lines = []
            self.elevations = []
            for entity in dxf.lines():
                line = []
                el = -1
                for point in entity.points():
                    line.append(self.scaler.locate((point[0], point[1])))
                    lastpoint = point
                if len(point) > 2:
                    el = point[2] 
                self.lines.append(line)
                self.elevations.append(el)
            self.DrawLines()
        def DrawElv(self, path):
            lines = file(path, "rb").readlines();
            self.lines = []
            self.elevations = []
            for line in lines:
                splits = [float(i) for i in line.split(",")]
                self.elevations.append(splits[0])
                self.lines.append([])
                for i in range(1, len(splits), 2):
                    self.lines[-1].append((splits[i],splits[i+1]))
            self.DrawLines()
                

        def OnOpenFILE(self, event=None):
            import os
            dlg = wx.FileDialog(
                self, message="Open file ...", defaultDir=os.getcwd(), 
                defaultFile="", wildcard="*.dxf;*.elv", style=wx.FD_OPEN
                )
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                self.vector_file = path
                if len(path)>4 and path[-4:] == ".dxf":
                    self.DrawDxf(path)
                else: 
                    self.DrawElv(path)
        # make elv model
        def WriteElv(self, path, lines, elevations):
            f = file(path, "wt")
            for i in range(len(lines)):
                s = str(elevations[i])+","+",".join([str(point[0])+","+str(point[1]) for point in lines[i]])
                f.write(s+"\n")
            f.close()
                
        def OnSaveFILE(self, event=None):
            import os
            import dxf_writer
            dlg = wx.FileDialog(
                self, message="Save file as ...", defaultDir=os.getcwd(), 
                defaultFile="output.elv", wildcard="*.dxf;*.elv", style=wx.SAVE
                )
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                if path[-4:].lower() == ".dxf": #todo: make "isDxfFile" 
                    dxf_writer.WriteDXF(path, self.lines, self.elevations)
                if path[-4:].lower() == ".elv":
                    self.WriteElv(path, self.lines, self.elevations)


        def OnMove(self, event):
            """
            Updates the status bar with the world coordinates
            """
            self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))
            event.Skip()

        def OnAbout(self, event):
            dlg = wx.MessageDialog(self,
                                   "This is a small program to demonstrate\n"
                                   "the use of the FloatCanvas\n",
                                   "About Me",
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

        def ZoomToFit(self,event):
            self.Canvas.ZoomToBB()

        def Clear(self,event = None):
            self.UnBindAllMouseEvents()
            self.Canvas.InitAll()
            self.Canvas.Draw()

        def OnQuit(self,event):
            self.Close(True)

        def OnCloseWindow(self, event):
            self.Destroy()
 
        def ShowFrame(self):
            Object = self.MovingObject
            Range = self.Range
            if  self.TimeStep < self.NumTimeSteps:
                x,y = Object.XY
                if x > Range[1] or x < Range[0]:
                    self.dx = -self.dx
                if y > Range[1] or y < Range[0]:
                    self.dy = -self.dy
                Object.Move( (self.dx,self.dy) )
                Object.Text.Move( (self.dx,self.dy))
                self.Canvas.Draw()
                self.TimeStep += 1
                wx.GetApp().Yield(True)
            else:
                self.Timer.Stop()

        def MoveMe(self, Object):
            self.MovingObject = Object
            Range = self.Range
            self.dx = random.uniform(Range[0]/4,Range[1]/4)
            self.dy = random.uniform(Range[0]/4,Range[1]/4)
            #import time
            #start = time.time()
            self.NumTimeSteps = 200
            self.TimeStep = 1
            self.Timer.Start(self.FrameDelay)
            #print "Did %i frames in %f seconds"%(N, (time.time() - start) )

        def TestHitTest(self, event=None):
            wx.GetApp().Yield(True)

            self.UnBindAllMouseEvents()
            Canvas = self.Canvas

            Canvas.InitAll()

            #Add a Hit-able rectangle
            #h = 20
            FontSize = 8

            Point = (0, 0)

            imageFile = 'back.tif'
            data = open(imageFile, "rb").read()
            # convert to a data stream
            stream = cStringIO.StringIO(data)
            # show the bitmap, (5, 5) are upper left corner coordinates
            image = wx.ImageFromStream( stream )

            # would this become fast if we did not have a scaled bitmap?
            ORIGINAL_Y = 200
            BitMap = Canvas.AddScaledBitmap(image, (0, ORIGINAL_Y), Height=ORIGINAL_Y)

            x, y = 0, 0

            from tiff_size import GetTiffSize
            sizing = GetTiffSize(imageFile)
            from scaler import Scaler
            self.scaler = Scaler(sizing[4]-sizing[2], sizing[5]-sizing[3], sizing[2], sizing[3])
            self.scaler.set_scale_y(ORIGINAL_Y)

            self.Canvas.ZoomToBB()

        def LineGotHit(self, Object):
            if self.lastline!=None:
                self.lastline.SetLineColor(_ColorFromElevation(self.elevations[self.lastline.line_idx]))
            self.lastline = Object
            self.MsgWindow.ChangeValue(str(self.elevations[Object.line_idx]))
            Object.SetLineColor("Green")
            self.Canvas.Draw(Force = True)

        def RectMoveLeft(self,Object):
            self.MoveRects("left")

        def RectMoveRight(self,Object):
            self.MoveRects("right")

        def RectMoveUp(self,Object):
            self.MoveRects("up")

        def RectMoveDown(self,Object):
            self.MoveRects("down")

        def MoveRects(self, Dir):
            for Object in self.MovingRects:
                X,Y = Object.XY
                if Dir == "left": X -= 10
                elif Dir == "right": X += 10
                elif Dir == "up": Y += 10
                elif Dir == "down": Y -= 10
                Object.SetPoint((X,Y))
            self.Canvas.Draw()

        def PointSetGotHit(self, Object):
            self.Log(Object.Name + "Got Hit\n")

        def RectGotHit(self, Object):
            self.Log(Object.Name + "Got Hit\n")

        def RectGotHitRight(self, Object):
            self.Log(Object.Name + "Got Hit With Right\n")

        def ItemGotHit(self, Object):
            self.Log(Object.Name + "Got Hit with Left\n")

        def RectMouseOver(self, Object):
            self.Log("Mouse entered:" +  Object.Name)

        def RectMouseLeave(self, Object):
            self.Log("Mouse left " +  Object.Name)

        def RectGotHitLeft(self, Object):
            self.Log(Object.Name + "Got Hit with Left\n")

    return DrawFrame 


#---------------------------------------------------------------------------
      
if __name__ == "__main__":

    import wx
   
    if not haveNumpy:
        raise ImportError(errorText)
    StartUpDemo = "hit" # the default

    class DemoApp(wx.App):
        def __init__(self, *args, **kwargs):
            wx.App.__init__(self, *args, **kwargs)

        def OnInit(self):
            DrawFrame = BuildDrawFrame()
            frame = DrawFrame(None, -1, "FloatCanvas Demo App",wx.DefaultPosition,(700,700))
            self.SetTopWindow(frame)
            frame.Show()
            frame.TestHitTest()
            return True

    app = DemoApp(False)# put in True if you want output to go to it's own window.
    app.MainLoop()

