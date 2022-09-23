print("The dead zone is +- 15%, if more than one axe readings are past the dead zone, the ESCs will stop")
while True:

    XAxis = int(input("X Axe (Forward -ve/Backward +ve) value:\t", ))
    YAxis = int(input("Y Axe (Left -ve/Right +ve) value:\t", ))
    ZAxis = int(input("Z Axe (Up -ve/Down +ve) value:\t", ))
    WAxis = int(input("R Axe (Rotate left -ve/Rotate right +ve) value:\t", ))
    if (XAxis not in range(-15,15)) & (YAxis not in  range(-15,15)) & (WAxis not in range (-15,15))|(XAxis not in range(-15,15)) & (YAxis not in  range(-15,15))|(XAxis not in range(-15,15)) & (WAxis not in  range(-15,15))|(WAxis not in range(-15,15)) & (YAxis not in  range(-15,15)):
        state= "Input is past the deadzone in more than 1 axes\nAll ESCs stopped"
        print(state)
    else:
        if ZAxis in range(-15,15):
            state1 ="Vertical ESCs stopped '0'"
        elif ZAxis < -15:
            state1="Upwards '1'"
        elif ZAxis > 15:
            state1="Downwards '2'"
    
    
    
        if (XAxis in  range(-15,15)) & (YAxis in  range(-15,15)) & (WAxis in range (-15,15)):
            state2 = "Horizontal ESCs stopped '0'"
        elif (XAxis >= 15) & (YAxis in range(-15,15)) & (WAxis in range (-15,15)):
            state2 = "backward '2'"
        elif (XAxis <= -15) & (YAxis in range(-15,15)) & (WAxis in range (-15,15)):
            state2 = "forward '1'"
        elif (YAxis >= 15) & (XAxis in range(-15,15)) & (WAxis in range (-15,15)):
            state2 = "right '3'"
        elif (YAxis <= -15) & (XAxis in range(-15,15)) & (WAxis in range (-15,15)):
            state2 = "left '4'"
        elif (WAxis >= 15) & (YAxis in range(-15,15)) & (XAxis in range(-15,15)):
            state2 = "rotate right '5'"
        elif (WAxis <= -15) & (YAxis in range(-15,15)) & (XAxis in range(-15,15)):
            state2 = "rotate left '6'"
    
        print(f"{state1}\n{state2}")