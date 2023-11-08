"""
This is the External wrapper for handling Heterodyne Four Wave Mixing callbacks 

Generated By Matthew Larson on November 8th 2023
"""

import dearpygui.dearpygui as dpg 
def stageselecta(sender,data):
    """handle stage a selection for HFWM setup window
    """
    print(sender,"stage a returned: ", dpg.get_value(sender))

def stageselectb(sender,data):
    """handle stage b selection for HFWM setup window
    """
    print(sender,"stage b returned: ", dpg.get_value(sender))