__author__ = 'Yu Zhu'
__version__= '1.2'


from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from PIL import Image, ImageTk
import os

class App(object):
    def __init__(self, master):

        self.pnum = 22                  # Number of the points
        self.pNames = ["Left Brow Left Corner", "Left Brow Right Corner",
                       "Left Eye Left Corner", "Left Eye Top center",
                       "Left Eye Right Corner", "Left Eye Bottom Center",
                       "Left Eye Center", "Right Brow Left Corner",
                       "Right Brow Right Corner", "Right Eye Left Corner",
                       "Right Eye Top center", "Right Eye Right Corner",
                       "Right Eye Bottom Center", "Right Eye Center",
                       "Nose Left", "Nose Center", "Nose Right",
                       "Mouth Left Corner", "Mouth Upper Lip Center",
                       "Mouth Right Corner", "Mouth Bottom Lip Center",
                       "Mouth Center"]  # Names of the points
        self.pPos = [[0, 0]]*self.pnum  # Point coordinates for single image
        self.outputdir = os.getcwd()    # Output dir: Save the points positions
        self.filepath = ""              # Input dir: Image folder
        self.filelist = []              # File names in the selected image folder
        self.pointsAll = []             # List of dict: each dict in the list saves points positions for each image
        self.linesAll = []              # List of list: each list in the list saves the marks shown in each image
        self.currentIndex = 0           # Current Image Index selected from the file list
        self.currentPoint = 0           # Current Point Index for labeling
        self.imgformatstr = '*.jpg'      # Load Image format
        self.entrylist = []             # List of Entry widget for the Setting->PointsNames

        self.imgSizeX = 500                  # image size for canvas show (bigger than the real image size)
        self.imgSizeY = 500
        self.winSizeX = 500                  # canvas size on the window
        self.winSizeY = 500

        #########  Menu Widget  ########
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.selectfolder)
        filemenu.add_command(label="Save", command=self.savePoints)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Point Number & Names",command=self.setpoints)
        editmenu.add_command(label="Output Folder", command=self.setoutputFolder)
        menubar.add_cascade(label="Setting", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="How to use",command=self.howtouse)
        helpmenu.add_command(label="About...", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        master.config(menu=menubar)


        ########  GUI Frames  ########
        frame1 = Frame(master)
        frame1.pack()

        # Face Image Frame: level 2
        frame_img0 = Frame(frame1)
        frame_img0.pack(side=LEFT, fill=BOTH, expand=YES, padx=10, pady=20)
        # Face label Frame: level 3
        frame_imglab = Frame(frame_img0)
        frame_imglab.pack(fill=BOTH, expand=YES)
        # Face canvas Frame: level 3
        frame_imgcanvas = Frame(frame_img0)
        frame_imgcanvas.pack(pady=5, fill=BOTH, expand=YES)
        # Face button Frame: level 3
        frame_imgbtn = Frame(frame_img0)
        frame_imgbtn.pack(fill=BOTH, expand=YES)


        # Right part Frame: level 2
        frame_right = Frame(frame1)
        frame_right.pack(side=LEFT,fill=BOTH, expand=YES, padx=10, pady=20)
        # Folder select Frame: level 3
        frame_ff = Frame(frame_right)
        frame_ff.pack(side=TOP,anchor=W)
        # List Box Frame
        frame_flb = Frame(frame_right)
        frame_flb.pack(side=TOP, fill=Y, expand=YES, anchor=W)
        # Message Frame
        frame_msg = Frame(frame_right)
        frame_msg.pack(side=TOP, anchor=W)

        frame_msg_lt = Frame(frame_msg)
        frame_msg_lt.pack(side=BOTTOM, anchor=W)

        frame_msg_txt = Frame(frame_msg_lt)
        frame_msg_txt.pack(side=RIGHT, anchor=W)





        ################# GUI Left Part Widgets ###################

        # Button: Previous image
        self.btn_prev = Button(frame_imgbtn, text="Previous", command=self.previmg)
        self.btn_prev.pack(side=LEFT, fill=X, expand=YES)
        # Button: Load the image
        self.btn_savelab = Button(frame_imgbtn, text="Save Labels", command=self.savelab)
        self.btn_savelab.pack(side=LEFT, fill=X, expand=YES)
        # Button: Next image
        self.btn_prev = Button(frame_imgbtn, text="Next", command=self.nextimg)
        self.btn_prev.pack(side=LEFT, fill=X, expand=YES)



        # Labels: Current Image Info
        self.str_imgNum = StringVar()
        self.str_imgNum.set("Image Num: 00/00")
        self.str_imgName = StringVar()
        self.str_imgName.set("Image Name: ")
        self.imgLab1 = Label(frame_imglab, textvariable=self.str_imgName)
        self.imgLab1.pack(side=LEFT, anchor=W)
        self.imgLab2 = Label(frame_imglab, textvariable=self.str_imgNum)
        self.imgLab2.pack(side=RIGHT, anchor=E)

        # Canvas: Show the Facial image
        self.vscrollbar = Scrollbar(frame_imgcanvas, orient=VERTICAL)
        self.vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.hscrollbar = Scrollbar(frame_imgcanvas, orient=HORIZONTAL)
        self.hscrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)
        self.img = Canvas(frame_imgcanvas, width=self.winSizeX, height=self.winSizeY, background="white", scrollregion=(0, 0, self.imgSizeX, self.imgSizeY), yscrollcommand=self.vscrollbar.set, xscrollcommand=self.hscrollbar.set)
        self.vscrollbar.config(command=self.img.yview)
        self.hscrollbar.config(command=self.img.xview)
        self.img.configure(cursor='crosshair')
        self.img.pack(side=LEFT, anchor=NW)
        self.img.bind('<Button-1>', self.clickPoint1)
        self.img.bind('<Button-3>', self.clickPoint2)


        ################# Right Frame Widgets ###################

        # Button & Entry: Select Input Image Folder
        self.pathLab = Label(frame_ff, text="Image Folder:")
        self.pathLab.pack(side=TOP, anchor=W)
        self.entry_path = Entry(frame_ff, width=22)
        self.entry_path.insert(0, self.filepath)
        self.entry_path.pack(side=LEFT)
        self.btn_path = Button(frame_ff, text="Select...", command=self.selectfolder)
        self.btn_path.pack(side=LEFT, padx=3)

        #List box: Show point names
        self.lb = Listbox(frame_flb, name='lb', selectmode=SINGLE, width=40, font=("COURIER", 9))
        self.lb.pack(side=LEFT, fill=BOTH, expand=YES, pady=3)
        self.scrollBar = Scrollbar(frame_flb)
        self.scrollBar.pack(side=RIGHT, fill=Y, expand=YES, pady=3)
        self.scrollBar.config(command=self.lb.yview)
        self.lb.config(yscrollcommand=self.scrollBar.set)
        #Used for debug only
        #Show items in List Box
        #self.pointPos = dict(zip(pNames, pPos))
        #for key in pNames:
        #    lt = key + ":    (" + str(self.pointPos[key][0]) + " ," + str(self.pointPos[key][1]) + ")"
        #    self.lb.insert(END, lt)
        #for k, v in self.pointPos.items():
        #    lt = k + ":    (" + str(v[0]) + " ," + str(v[1]) + ")"
        #    self.lb.insert(END, lt)
        self.loadPoints()
        self.lb.bind('<<ListboxSelect>>', self.onselect)

        # Button: clear Point
        self.btn_prev = Button(frame_msg, text="Clear Labeled Points", command=self.clearPoints)
        self.btn_prev.pack(side=TOP, fill=X, expand=YES)


        # Label: Show Output Dir
        self.opathLab_n = Label(frame_msg_lt, text="Output folder:", justify=LEFT)
        self.opathLab_n.pack(side=LEFT, anchor=W)

        self.outp=StringVar()
        self.outp.set(self.outputdir)

        self.opathLab = Text(frame_msg_txt, width=20, height=1, wrap=NONE)
        scrl = Scrollbar(frame_msg_txt, orient=HORIZONTAL, command=self.opathLab.xview)
        self.opathLab.config(xscrollcommand=scrl.set)
        scrl.pack(side="bottom", fill="x", expand=False)
        self.opathLab.insert(END, self.outp.get())
        self.opathLab.configure(state='disabled')
        self.opathLab.pack(side=TOP, anchor=W, expand=True)




    """List Box callback func:
     If current points is already labeled, change the mark color, change the current point index"""
    def onselect(self, event):
        # Note here that Tkinter passes an event object to onselect()
        w = event.widget

        if w.curselection():
            index = int(w.curselection()[0])
            value = w.get(index)
            if self.pNames[index] in self.linesAll[self.currentIndex].keys():

                l0 = self.linesAll[self.currentIndex][self.pNames[self.currentPoint]]
                self.img.itemconfig(l0[0], fill="red")
                self.img.itemconfig(l0[1], fill="red")

                self.currentPoint = index  # Change the current point index

                l = self.linesAll[self.currentIndex][self.pNames[index]]
                self.img.itemconfig(l[0], fill="blue")
                self.img.itemconfig(l[1], fill="blue")

                #print 'You selected item %d: "%s"' % (index, value)

    """ Save the current labeled points: JSON Format is used """
    def savePoints(self):
        if len(self.filelist) == 0:
            showwarning("No Image Folder Selected!", "No Image Folder Selected. Cannot Save!")
            self.btn_path.focus_set()
        else:
            filename = os.path.basename(self.filelist[self.currentIndex])[0:-4]
            #print "saving to " + filename
            import json
            file_obj = open(os.path.join(self.outputdir, filename+'.txt'), 'w')
            if file_obj:
                jsonstr = json.dumps(self.pointsAll[self.currentIndex])
                file_obj.write(jsonstr)
                file_obj.close()
                self.nextimg()
            else:
                showwarning("Saving Error", "Labels cannot be saved!")

    """Read point locations from file"""
    def readPoints(self):
        if len(self.filelist) > 0:
            filename = os.path.basename(self.filelist[self.currentIndex])[0:-4]
            if os.path.exists(os.path.join(self.outputdir, filename+'.txt')):
                import json
                file_obj = open(os.path.join(self.outputdir, filename+'.txt'), 'r')
                if file_obj:
                    jsondata = json.load(file_obj)
                    if set(jsondata.keys())==set(self.pNames):
                        self.pointsAll[self.currentIndex] = jsondata  #may have error
                else:
                    showwarning("Loading Error", "Output file exists but labels cannot be loaded!")
                file_obj.close()
            else:
                self.pointsAll[self.currentIndex] = dict(zip(self.pNames, self.pPos))



    """ Show Message to confirm saving """
    def savelab(self):
        if askyesno("Save the points", "Save these labels?", icon=QUESTION):
            self.savePoints()

    """ Right click Event Callback: Draw point """
    def clickPoint1(self, event):

        selection = self.lb.curselection()
        if not selection:
            if askyesno("All points are drawn", "Save the labeling?", icon=QUESTION):
                self.savePoints()
            else:
                self.lb.select_set(self.pnum-1)
        else:
            #print "Mouse Position: (%s, %s)" % (event.x, event.y)
            #print "Scroll.fraction()",  self.vscrollbar.fraction(event.x, event.y)
            #print "scroll get", self.vscrollbar.get()

            #Important: Get the offset of mouse position according to the scroll bar position and image size.
            offset_y = int(self.img["scrollregion"].split()[3]) * self.vscrollbar.get()[0]
            offset_y = int(offset_y)
            offset_x = int(self.img["scrollregion"].split()[2]) * self.hscrollbar.get()[0]
            offset_x = int(offset_x)
            #print "offset:", offset_x,offset_y

            if self.linesAll[self.currentIndex]:
                # recolor the previous point
                l0 = self.linesAll[self.currentIndex][self.pNames[self.currentPoint]]
                self.img.itemconfig(l0[0], fill="red")
                self.img.itemconfig(l0[1], fill="red")

            index = int(self.lb.curselection()[0])
            self.currentPoint = index

            # if current selection point exists
            if self.pNames[index] in self.linesAll[self.currentIndex].keys():
                self.img.delete(self.linesAll[self.currentIndex][self.pNames[index]][0])
                self.img.delete(self.linesAll[self.currentIndex][self.pNames[index]][1])

            c1 = self.img.create_line(event.x-4+offset_x, event.y+offset_y, event.x+4+offset_x, event.y+offset_y, width=2, fill='green')
            c2 = self.img.create_line(event.x+offset_x, event.y+offset_y-4, event.x+offset_x, event.y+offset_y+4, width=2, fill='green')

            #self.points.append([event.x, event.y])
            #self.lines.append([c1, c2])
            #save points
            self.pointsAll[self.currentIndex][self.pNames[index]] = [event.x+offset_x, event.y+offset_y]
            self.linesAll[self.currentIndex][self.pNames[index]] = [c1, c2]

            self.lb.delete(index)
            self.lb.insert(index, self.pNames[index].ljust(30) + "(" + str(event.x+offset_x) + ", " + str(event.y+offset_y) + ")")
            #print self.pNames[index], len(self.pNames[index])
            self.lb.select_set(index+1)
            if index+1 == self.pnum:
                if askyesno("All points are drawn", "Save the labeling?", icon=QUESTION):
                    self.savePoints()
                else:
                    self.lb.select_set(self.pnum-1)

    """ Left click Event Callback: Delete point """
    def clickPoint2(self, event):
        if self.currentPoint == -1:
            showwarning("No Points", "No points on the image!")
        else:
            #print "current p", self.currentPoint
            self.pointsAll[self.currentIndex][self.pNames[self.currentPoint]] = [0, 0]
            [c1, c2] = self.linesAll[self.currentIndex][self.pNames[self.currentPoint]]
            self.img.delete(c1)
            self.img.delete(c2)
            self.lb.selection_clear(0, END)
            self.lb.delete(self.currentPoint)
            self.lb.insert(self.currentPoint, self.pNames[self.currentPoint].ljust(30) + "(0, 0)")
            self.lb.select_set(self.currentPoint)
            self.currentPoint -= 1


    """Btn callback: clear points"""
    def clearPoints(self):
        self.pointsAll[self.currentIndex] = dict(zip(self.pNames, self.pPos))
        self.loadimg()
        self.loadPoints()

    """ Menu settings: set output folder """
    def setoutputFolder(self):
        filepath = askdirectory()
        if filepath:
            self.outputdir = filepath
            self.outp.set(self.outputdir)
            self.opathLab.configure(state='normal')
            self.opathLab.delete(1.0, END)
            self.opathLab.insert(END, self.outp.get())
            self.opathLab.configure(state='disabled')
            self.loadimg()
            self.readPoints()
            self.loadPoints()

    """ Menu settings: set point num and names """
    def setpoints(self):
        if askquestion(title="Reset the Points...", message="Reset Points Num and Names? \n \n" + "Current Points #: " + str(self.pnum) + "\n" + "Point Names: \n   " + "\n   ".join(self.pNames), type=YESNOCANCEL) == YES:
            self.top = Toplevel()
            self.top.title("Set Number of Points: ")

            frame1 = Frame(self.top)
            frame1.pack(side=TOP, fill=BOTH, expand=YES, padx=10, pady=20)

            lab = Label(frame1, text="Number of Points: ")
            lab.pack(side=LEFT)

            self.npentry = Entry(frame1, width=5)
            self.npentry.pack()
            self.npentry.focus_set()

            frame2 = Frame(self.top)
            frame2.pack(side=TOP, fill=BOTH, expand=YES, padx=10, pady=20)

            button = Button(frame2, text="OK", command=self.setpointsdetail)
            button.pack()

    """Menu Settings: Set the points names"""
    def setpointsdetail(self):
        self.pnum = int(self.npentry.get())
        #print self.pnum
        self.top.destroy()

        self.top2 = Toplevel()
        self.top2.title("Set Point Names:")

        frame1 = Frame(self.top2)
        frame1.pack(side=TOP, fill=BOTH, expand=YES, padx=10, pady=20)

        lab = Label(frame1,text="Name of Points: ")
        lab.pack(side=LEFT)

        frame2 = Frame(self.top2)
        frame2.pack(side=TOP, fill=BOTH, expand=YES, padx=10, pady=10)

        self.entrylist=[]
        for i in range(self.pnum):
            e = Entry(frame2, width=10)
            e.pack()
            self.entrylist.append(e)

        self.entrylist[0].focus_set()

        frame2 = Frame(self.top2)
        frame2.pack(side=TOP, fill=BOTH, expand=YES, padx=10, pady=20)

        button = Button(frame2, text="OK", command=self.detailcallback)
        button.pack()

    """Save the point names into pNames"""
    def detailcallback(self):
        self.pNames = [self.entrylist[i].get() for i in range(len(self.entrylist))]
        self.top2.destroy()

    """Select the image folder"""
    def selectfolder(self):
        filepath = askdirectory()
        if filepath:
            self.entry_path.delete(0, END)
            self.entry_path.insert(0, filepath)
            self.filepath = self.entry_path.get()

            #init points
            if not os.path.exists(self.filepath):  # folder not exists
                showwarning("No folder Exists", "Please select file folder.")
            else:
                #load all images in the selected folder
                import glob
                self.filelist = glob.glob(os.path.join(self.filepath, '*.jpg'))
                if len(self.filelist) != 0:
                    #filename = self.filelist[self.currentIndex]
                    #init points
                    pointPos = dict(zip(self.pNames, self.pPos))
                    lines = dict(zip(self.pNames, []))
                    for i in range(len(self.filelist)):
                        self.pointsAll.append(pointPos.copy())  # Must use copy, otherwise points to the same dict object
                        self.linesAll.append(lines.copy())
                        #print self.pointsAll
                        #print len(self.pointsAll)

            #load first image
            self.currentIndex = 0
            self.loadimg()
            self.readPoints()
            self.loadPoints()


    """Button Callback: Previous Image"""
    def previmg(self):
        if len(self.filelist) == 0:
            showwarning("No Image Folder Selected!", "No Image Folder Selected. Cannot Save!")
            self.btn_path.focus_set()
        else:
            if self.currentIndex == 0:
                showwarning("No previous Image", "This is the 1st image!")
            else:
                self.currentIndex -= 1  # get previous image number
                filename = self.filelist[self.currentIndex]
                #change the label text
                self.str_imgNum.set("Image Num: " + str(self.currentIndex+1) + "/" + str(len(self.filelist)))
                self.str_imgName.set("Image Name: " + os.path.basename(filename))
                self.loadimg()
                self.loadPoints()

    """Button Callback: Next Image"""
    def nextimg(self):
        if len(self.filelist) == 0:
            showwarning("No Image Folder Selected!", "No Image Folder Selected. Cannot Save!")
            self.btn_path.focus_set()
        else:
            if self.currentIndex == len(self.filelist)-1:
                showwarning("No next Image", "This is the last image!")
            else:
                self.currentIndex += 1  # get next image number
                filename = self.filelist[self.currentIndex]
                #change the label text
                self.str_imgNum.set("Image Num: " + str(self.currentIndex+1) + "/" + str(len(self.filelist)))
                self.str_imgName.set("Image Name: " + os.path.basename(filename))
                self.loadimg()
                self.readPoints()
                self.loadPoints()

    """Load the stored points and draw marks on the image"""
    def loadPoints(self):
        if len(self.pointsAll) != 0:
            pointPos = self.pointsAll[self.currentIndex]
            #print "current index", self.currentIndex
            #print pointPos
            self.lb.delete(0, END)
            for key in self.pNames:
                lt = key.ljust(30) + "(" + str(pointPos[key][0]) + " ," + str(pointPos[key][1]) + ")"
                self.lb.insert(END, lt)

                c1 = self.img.create_line(pointPos[key][0]-4, pointPos[key][1], pointPos[key][0]+4, pointPos[key][1], width=2, fill='red')
                c2 = self.img.create_line(pointPos[key][0], pointPos[key][1]-4, pointPos[key][0], pointPos[key][1]+4, width=2, fill='red')
                self.linesAll[self.currentIndex][key] = [c1, c2]

            self.lb.select_set(0)

    """Show image on the canvas"""
    def loadimg(self):
        self.filepath = self.entry_path.get()
        #logging.info(self.entry_path.get())
        if not os.path.exists(self.filepath):  # folder not exists
            showwarning("No folder Exists", "Please select file folder.")
            self.btn_path.focus_set()
        else:
            #load all images in the selected folder
            import glob
            self.filelist = glob.glob(os.path.join(self.filepath, self.imgformatstr))
            if len(self.filelist) != 0:
                filename = self.filelist[self.currentIndex]
                #logging.warning(filename)

                self.str_imgNum.set("Image Num: " + str(self.currentIndex+1) + "/" + str(len(self.filelist)))
                self.str_imgName.set("Image Name: " + os.path.basename(filename))

                im = Image.open(filename)
                #print im.size, im.mode, im.format
                #print im.size[0]
                #im.show()
                photo = ImageTk.PhotoImage(im)
                #img = self.img.create_image(0,0, image=photo)
                self.img.delete(ALL)
                self.img.create_image(0, 0, anchor=NW, image=photo)
                self.img.image = photo
                self.img.configure(width=min(self.imgSizeX, im.size[0]), height=min(self.imgSizeY, im.size[1]))

                self.img.configure(scrollregion=(0, 0, im.size[0], im.size[1]))
                # reset the view
                self.img.xview_moveto(0)
                self.img.yview_moveto(0)

            else:
                showwarning("No image files in this folder", "Please select proper file folder.")

    """ Menu: show about message """
    def about(self):
        title = "About this software..."
        msg1 = """FACIAL LABELING APP
                  Version 1.3 """
        msg2 ="""
              Author: Yu Zhu
              Contact: yzhu4@mix.wvu.edu
              Affiliate: CSEE, West Virginia University, USA

              This software is used for labeling and saving facial points on facial images.
              For academic or personal purpose only.


                          Copyright. Yu Zhu. 2014."""
        self.topabout = Toplevel()
        self.topabout.title(title)

        frame1 = Frame(self.topabout)
        frame1.pack(side=TOP, fill=BOTH, expand=YES, padx=10, pady=20)

        lab1 = Label(frame1, text=msg1, font=("Purisa", 12), anchor=CENTER, justify=LEFT, pady=5)
        lab1.pack(side=TOP)

        lab2 = Label(frame1, text=msg2, font=("arial", 9), anchor=NW, justify=LEFT)
        lab2.pack(side=TOP)


        frame2 = Frame(self.topabout)
        frame2.pack(side=TOP, fill=BOTH, expand=YES, padx=10, pady=10)

        btn = Button(frame2, text="OK", command=self.topabout.destroy, width=60)
        btn.pack()
        btn.focus_set()

    """ Menu: show how to use """
    def howtouse(self):
        title = "How to Use..."
        msg1 ="""Facial Points Labeling Application"""
        msg2 ="""
        V1.3
        Yu Zhu, WVU, USA, 2014
        yzhu4@mix.wvu.edu"""
        msg3="""
        How to Use:

        1. Set the Output Folder
           (1)Go to Menu-->Setting-->Output Folder
           (2)Select the folder where the output files will be saved

        2. Set the Image Folder
           (1)Press Button "Select..." in the main window
                OR go to Menu-->File-->Open.
           (2)Select the images folder for labeling. The 1st image in the folder will be loaded.
           Note. In this version (v1.3), ONLY .jpg file is supported.

        3. Label the Facial Points
           (1)Click the image area to label the facial points.
           (2)The position (x,y) will be shown in the listbox for each point.
           (3)Select item in the listbox can label/modify each specific point.

        4. Save the Points
           (1)When all the points are labeled, pop-up window will show up.
              OR
                 Go to Menu-->File-->Save
              OR
                 Click "Save" button

           Note. The point positions are saved in JSON string format and output to .txt file.
                 The saving overwrites the previous output each time.

        5. Modify the Points
           (1)Select the item in the listbox and click the image area to modify the positions of that point.
           (2)Right click in the image area will delete the previous point that has been labeled.

        6. Clear the Labeled Points
           (1)Press the "Clear Labeled Points" button, all the points that labeled in this image will be clear and reset.

        7. Go to Next Image
           (1) Press Next button to label the next image in the folder.

        8. Go to Previous Image
           (1) Press Previous button to label the previous image in the folder.

        9. (Usually not required) Reset the default Number of Points & Point Names.
           If you need to change the default number of points and names for labeling:
           (1)Go to Menu-->Setting--> Point Number & Names.
           (2)The default settings are shown, select YES to reset.
           (3)Input the number of facial points for labeling.
           (4)Input the names of the points.


        """

        self.tophelp = Toplevel()
        self.tophelp.title(title)



        frame1 = Frame(self.tophelp)
        frame1.pack(side=TOP, fill=BOTH, expand=YES, padx=10, pady=10)


        lab1 = Label(frame1, text=msg1, font=("Purisa",12), anchor=CENTER, justify=LEFT, pady=10)
        lab1.pack(side=TOP)

        #lab2 = Label(frame1, text=msg2, font=("arial",9), anchor=NW, justify=LEFT, pady=15)
        #lab2.pack(side=TOP)

        scrollbar = Scrollbar(frame1)
        scrollbar.pack(side=RIGHT, fill=Y)
        #lab3 = Label(frame1, text=msg3, font=("arial",9), anchor=NW, justify=LEFT, bg='white',yscrollcommand=scrollbar.set)
        #lab3.pack(side=TOP)
        text = Text(frame1)
        text.configure(font=("arial", 9), bg="white",state="normal", yscrollcommand=scrollbar.set, pady=10)
        text.insert("1.0", msg3)
        text.pack()
        scrollbar.config(command=text.yview)

        frame2 = Frame(self.tophelp)
        frame2.pack(side=TOP, fill=BOTH, expand=YES, padx=10, pady=10)

        btn = Button(frame2, text="OK", command=self.tophelp.destroy, width=60)
        btn.pack()
        btn.focus_set()

"""Main function"""
if __name__ == "__main__":
    root = Tk()
    root.title("Facial Point Labeling")
    #root.geometry('600x500')
    app = App(root)
    root.mainloop()

