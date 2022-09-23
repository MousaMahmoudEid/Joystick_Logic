#Models from PyQt5 library needed for ui functions loading in python code
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit
#Model needed to invoke timer function and load ui file
from PyQt5.QtCore import QTimer
from PyQt5 import uic
import numpy as np
#Libraries needed to deal with system directories, joystick and delay functions
import sys
import time
#Must use functions to operate the joystick


#Class to use our UI file created by qt designer 
class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("NoJoystickGUI.ui",self)
        self.show() # show the ui 
        #timer function to update readings every 10ms
        self.MotionButton.clicked.connect(self.JoystickBar)


#The function invoked to get readings as what postion is the joystick on right now
    def JoystickBar(self):

    #Joystick values configuration
        valueX = self.XAxe.text() #Forward (+ve) & backward (-ve) axe
        valueY = self.YAxe.text() #Right (+ve) & left (-ve) axe
        valueZ = self.ZAxe.text() #up (+ve) & down (-ve) axe
        valueW = self.WAxe.text() #Rotate right (+ve) & rotate left (-ve) axe

        XAxis = int(float(valueX))
        YAxis = int(float(valueY))
        ZAxis = int(float(valueZ))
        WAxis = int(float(valueW))

        #Using this list to get value of each axe with specified index
        HorizontalAxisList = [XAxis, YAxis, WAxis]
        #Using this array to get index of each element in it
        Array = np.array([XAxis, YAxis, WAxis])
        Max = np.argmax(Array) #Returns index of max positive number
        MaxAxeValue = HorizontalAxisList[Max] #Uses the index to get the real value from the HorizontalAxisList
        Min = np.argmin(Array) #Returns index of max negative number (Max negative as in -99 > -5, Not the typical math stuff)
        MinAxeValue = HorizontalAxisList[Min] #Uses the index to get the real value from the HorizontalAxisList


    #State 1: Direction
        
    #State 1: PWM 
        #print("ZAxis",abs(ZAxis))
        state1_pwm = abs(ZAxis)
        
    #logic test for up and down actions
        if (ZAxis in range (-15,15)):
            #print("Stop '0'")
            state1 = 0
            #We can also do self."Name of progress bar".setValue(abs(ZAxis)) if we want to tell pilot about dead zone
            self.UpBar.setValue(0)
            self.DownBar.setValue(0)
        elif ZAxis >= 15 :
            #print("up '1' ")
            state1 = 1
            self.UpBar.setValue(abs(ZAxis))
            self.DownBar.setValue(0)
        elif ZAxis <= -15:
            #print("down '2' ")
            state1 = 2
            self.UpBar.setValue(0)
            self.DownBar.setValue(abs(ZAxis))




    #State 2: Direction
        
    #State 2 PWM 
        if MaxAxeValue > abs(MinAxeValue):
            if MaxAxeValue == XAxis:
                #print("XAxis",XAxis)
                state2_pwm = XAxis
            elif MaxAxeValue == YAxis:
                #print("YAxis",YAxis)
                state2_pwm = YAxis
            elif MaxAxeValue == WAxis:
                #print("WAxis",WAxis)
                state2_pwm = WAxis
        elif MaxAxeValue < abs(MinAxeValue):
            if MinAxeValue == XAxis:
                #print("XAxis",abs(XAxis))
                state2_pwm = abs(XAxis)
            elif MinAxeValue == YAxis:
                #print("YAxis", abs(YAxis))
                state2_pwm = abs(YAxis)
            elif MinAxeValue == WAxis:
                #print("WAxis", abs(WAxis))
                state2_pwm = abs(WAxis)
        print(state2_pwm)
        
    #logic test for forward, backward, right, left, rotate right and rotate left actions 
    #Note for rotate right and rotate left we will use ForwardBar alongside either RightBar or LeftBar as indicator for rotation
        if (XAxis in  range(-15,15)) & (YAxis in  range(-15,15)) & (WAxis in range (-15,15)):
            #print("stop '0'")
            state2 = 0
            self.ForwardBar.setValue(0)
            self.BackwardBar.setValue(0)
            self.RightBar.setValue(0)
            self.LeftBar.setValue(0)
                    
    
        elif (XAxis >= 15) & (YAxis in range(-15,15)) & (WAxis in range (-15,15)):
            #print("forward '1'")
            state2 = 1
            self.ForwardBar.setValue(abs(XAxis))
            self.BackwardBar.setValue(0)
            self.RightBar.setValue(0)
            self.LeftBar.setValue(0)

        elif (XAxis <= -15) & (YAxis in range(-15,15)) & (WAxis in range (-15,15)):
            #print("backward '2'")
            state2 = 2
            self.ForwardBar.setValue(0)
            self.BackwardBar.setValue(abs(YAxis))
            self.RightBar.setValue(0)
            self.LeftBar.setValue(0) 

        elif (YAxis >= 15) & (XAxis in range(-15,15)) & (WAxis in range (-15,15)):
            #print("right '3'")
            state2 = 3
            self.ForwardBar.setValue(0)
            self.BackwardBar.setValue(0)
            self.RightBar.setValue(abs(YAxis))
            self.LeftBar.setValue(0)     

        elif (YAxis <= -15) & (XAxis in range(-15,15)) & (WAxis in range (-15,15)):
            #print("left '4'")
            state2 = 4
            self.ForwardBar.setValue(0)
            self.BackwardBar.setValue(0)
            self.RightBar.setValue(0)
            self.LeftBar.setValue(abs(YAxis))       

        elif (WAxis >= 15) & (YAxis in range(-15,15)) & (XAxis in range(-15,15)):
            #print("rotate right '5'")
            state2 = 5
            self.ForwardBar.setValue(abs(WAxis))
            self.BackwardBar.setValue(0)
            self.RightBar.setValue(abs(WAxis))
            self.LeftBar.setValue(0)     

        elif (WAxis <= -15) & (YAxis in range(-15,15)) & (XAxis in range(-15,15)):
            #print("rotate left '6'")
            state2 = 6
            self.ForwardBar.setValue(abs(WAxis))
            self.BackwardBar.setValue(0)
            self.RightBar.setValue(0)
            self.LeftBar.setValue(abs(WAxis))
            
    #logic Error handling for horizontal motion in case all horzontal motion axis gone above dead zone(Take highest axe value and move)
        else:
            if MaxAxeValue > abs(MinAxeValue):
                if MaxAxeValue == XAxis:
                    #print("Forward '1'")
                    state2 = 1
                    self.ForwardBar.setValue(abs(XAxis))
                    self.BackwardBar.setValue(0)
                    self.RightBar.setValue(0)
                    self.LeftBar.setValue(0)
                    
                elif MaxAxeValue == YAxis:
                    #print("Right '3'")
                    state2 = 3
                    self.ForwardBar.setValue(0)
                    self.BackwardBar.setValue(0)
                    self.RightBar.setValue(abs(YAxis))
                    self.LeftBar.setValue(0)

                elif MaxAxeValue == WAxis:
                    #print("Rotate Right '5'")
                    state2 = 5
                    self.ForwardBar.setValue(abs(WAxis))
                    self.BackwardBar.setValue(0)
                    self.RightBar.setValue(abs(WAxis))
                    self.LeftBar.setValue(0)

            elif MaxAxeValue < abs(MinAxeValue):
                
                if MinAxeValue == XAxis:
                    #print("Backward '2'")
                    state2 = 2
                    self.ForwardBar.setValue(0)
                    self.BackwardBar.setValue(abs(XAxis))
                    self.RightBar.setValue(0)
                    self.LeftBar.setValue(0)

                elif MinAxeValue == YAxis:
                    #print("Left '4'")
                    state2 = 4
                    self.ForwardBar.setValue(0)
                    self.BackwardBar.setValue(0)
                    self.RightBar.setValue(0)
                    self.LeftBar.setValue(abs(YAxis))

                elif MinAxeValue == WAxis:
                    #print("Rotate Left '6'")
                    state2 = 6
                    self.ForwardBar.setValue(abs(WAxis))
                    self.BackwardBar.setValue(0)
                    self.RightBar.setValue(0)
                    self.LeftBar.setValue(abs(WAxis))


        #Displaying all data on the GUI
        NewState1 = str(state1)
        NewState1_pwm = str(state1_pwm)
        NewState2 = str(state2)
        NewState2_pwm = str(state2_pwm)
        answer= NewState1 + "|" + NewState1_pwm + "|" + NewState2 + "|" + NewState2_pwm
        self.JoystickMotion.setText(answer)
        
#The following lines must be places with the same order as explained here so that the program doesn't instantly close       
app = QApplication(sys.argv)
window = UI()
app.exec_()
