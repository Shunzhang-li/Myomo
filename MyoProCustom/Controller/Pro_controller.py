"""
Instance of Pro_Controller
1. Be able to take in EMG data points and output motor speend command
2. Be able to change controller parameters
"""
    
import numpy as np

class Pro_controller:

    
    def __init__(self):
        self.thresholds = [-10,10]   # Tricep Bicep Thresholds. Bicep is positive
        self.Kp = [5,5]              # Tricep Bicep Gain.
        self.motorspeed = 15         # motor speed in rpm. set one rotation for 4 seconds  


    #TODO: set get methods, and cap parameters  

    def set_Bicep_thresholds(self,th):
        self.threholds[1] = th

    def get_Bicep_thresholds(self):
        return self.threholds[1] 

    def set_Tricep_thresholds(self,th):
        self.threholds[0] = -th
    
    def get_Tricep_thresholds(self):
        return self.threholds[0]

    def set_Bicep_gain(self,gain):
        self.Kp[1] = gain

    def get_Bicep_gain(self):
        return self.Kp[1]

    def set_Tricep_gain(self,gain):
        self.Kp[0] = gain
    
    def get_Tricep_gain(self):
        return self.Kp[0]    

    def set_motorspeed(self,speed):
        self.motorspeed = speed

    def get_motorspeed(self):
        return self.motorspeed

    def tear_down(self):
        pass

    """
    Primary function of the class
    Input EMG (Tri, Bi) data point
    Output Motor cmd
    """    

    def motorcmd_update(self,EMG):
        if len(EMG) != 2:
            return None
        try:
            tri = EMG[0]
            bi = EMG[1]
            efforts = -tri*self.Kp[0]+bi*self.Kp[1]     #muscle efforts Bicep - Tricep
            cmd = 0                                     #assume within non-effort range
            if efforts >= self.threholds[1] or efforts <= self.thresholds[0]:   #when effort is significant
                cmd = efforts/math.abs(efforts)*self.motorspeed
            return cmd
        except:
            return None
        



#def main():


#if __name__ == '__main__':
