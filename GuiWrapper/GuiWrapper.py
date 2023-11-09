"""
This is the External wrapper for handling the Graphical User Interface(GUI) 

Generated By Matthew Larson on November 8th 2023
"""

import dearpygui.dearpygui as dpg 
from hfwmSetup import *
from stageControl import *
import numpy as np 
import matplotlib.pyplot as plt

dpg.create_context()
dpg.create_viewport(title='Main Context',width=900,height=600)

#set up units and stages:
unitlist =['fs','ps','um','mm']
sunitlist=['fs/s','ps/s','um/s','mm/s']
stages   =['k1','k2','k3']
z = np.zeros(1)
#set up a storage location for figures
figurefile='figureplot.png'
#display a simple icon
dpg.set_viewport_small_icon("Icon.ico")
dpg.set_viewport_large_icon("Icon.ico")
#set up stage initialization window all callbacks in stageControl.py
with dpg.window(label='Stage Control Window',width=380,height=250):
    #setup control for stage initialization
    dpg.add_text('Stage Control')
    sstatus = dpg.add_text('Stage status:inactive')
    #stage monitor
    with dpg.group(horizontal=True):
        stage=dpg.add_combo(stages,label='Select Stage',width=50,default_value='k1')
        position = dpg.add_text('Current Position: Unknown')
    #stage zero/position
    with dpg.group(horizontal=True):
        dpg.add_button(label='Zero Stage',callback=zerostage,user_data=[position,sstatus])
        dpg.add_button(label='Get Position',callback=getposition,user_data=[position,sstatus])
        
    #translation control for stage positioning 
    with dpg.group(horizontal=True):    
        speed = dpg.add_input_double(label='Speed',default_value=6000,width=100)
        destination = dpg.add_input_double(label='Destination',width=100)
       
    #unit setting and motion 
    with dpg.group(horizontal=True): 
        units = dpg.add_combo(['fs','ps','um','mm'],label='units',
                              width=50,default_value='fs')
        sunits = dpg.add_combo(['fs/s','ps/s','um/s','mm/s'],label='speed units',
                               width=50,default_value='fs/s')
    #execute motion
    with dpg.group(horizontal=True):
        dpg.add_button(label='Move Stage',callback=movestage,user_data=[destination,position,stage,units,speed,sunits,sstatus])

with dpg.window(label="HFWM Data Monitor",pos=(0,250),width=880,height=300):
    x= np.linspace(-10,10)
    y= np.linspace(-10,10)
    X,Y = np.meshgrid(x,y)
    Z = X+Y
    plt.figure(figsize=(8.80,2.20),dpi=100)
    plt.imshow(Z)
    plt.savefig('defaultimage.png',dpi=100)
    
    width, height, channels, data = dpg.load_image("defaultimage.png")
    with dpg.texture_registry():
        texture_id = dpg.add_dynamic_texture(width, height, data)
    dpg.add_image(texture_id)
    pb =dpg.add_progress_bar()
    


#HFWM set up window all info in hfwmSetup.py
with dpg.window(label="HFWM Setup",pos=(380,0),width=500,height=250):
    #select stages
    with dpg.group(horizontal=True):
        stagea = dpg.add_combo(stages,label='Select Stage a',default_value='k1',width=100)
        stageb = dpg.add_combo(stages,label='Select Stage b',default_value='k2',width=100)
    #set stage speeds 
    with dpg.group(horizontal=True):
        speeda = dpg.add_input_double(label='Stage b speed',default_value=dpg.get_value(speed),
                                       width=100)
        speedb = dpg.add_input_double(label='Stage a speed',default_value=dpg.get_value(speed),
                                      width=100)

    with dpg.group(horizontal= True): 
        sunita = dpg.add_combo(sunitlist,label='stage a speed units',
                               width=50,default_value='fs/s')
        sunitb = dpg.add_combo(sunitlist,label='stage b speed units', 
                               width=50,default_value='fs/s')
    #set stage start point 
    with dpg.group(horizontal= True): 
        starta = dpg.add_input_double(label='Start a',default_value=0,
                                       width=100)
        startb = dpg.add_input_double(label='Start b',default_value=0,
                                       width=100)
    #set stage end point
    with dpg.group(horizontal= True): 
        enda = dpg.add_input_double(label='End a',default_value=dpg.get_value(destination),
                                       width=100)
        endb = dpg.add_input_double(label='End b',default_value=dpg.get_value(destination),
                                       width=100)
        inttime = dpg.add_input_double(label='Integration time [s]',default_value=.05,
                                       width=100)
    #set stage increment
    with dpg.group(horizontal= True): 
        stepsa = dpg.add_input_double(label='steps stage a',default_value=100,
                                       width=100)
        stepsb = dpg.add_input_double(label='steps stage b',default_value=100,
                                       width=100)
    #set stage speed units
    with dpg.group(horizontal= True): 
        unita = dpg.add_combo(unitlist,label='stage a units',
                               width=50,default_value='fs')
        unitb = dpg.add_combo(unitlist,label='stage b units', 
                               width=50,default_value='fs')
    #run 
    zvalues=np.zeros(1)
    runpackage = [ stagea,stageb, #[0,1]
                   speeda,speedb ,#[2,3]
                   sunita,sunitb ,#[4,5]
                   starta,startb ,#[6,7]
                   enda, endb,    #[8,9]
                   stepsa,stepsb, #[10,11]
                   unita,unitb,   #[12,13]
                   pb,texture_id, #[14,15]
                   zvalues,inttime] #[16,17]
    dpg.add_file_dialog(
        directory_selector=True, show=False, callback=savefile, tag="file_dialog_id",
        cancel_callback=savecanceled, width=700 ,height=400)
    with dpg.group(horizontal=True):               
        dpg.add_button(label='Run',callback=runHFWM,user_data=runpackage,width=100)#,userdata=runpackage,callback=runHFWM)
        dpg.add_button(label='Savecollection',callback=lambda:dpg.show_item('file_dialog_id'))

    


dpg.setup_dearpygui()
dpg.show_viewport()
#dpg.set_primary_window(window=0,value=True)
dpg.start_dearpygui()
dpg.destroy_context()