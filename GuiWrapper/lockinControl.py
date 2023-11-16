from zhinst.toolkit import Session
import time as t
import numpy as np 
import sys 
this = sys.modules[__name__]
this.samplingrate = 5400
def connect(int_time):
    """Connect to any available device 

    Returns:
        device: The access port of a give device 
        Session: The scope of the devices which holds data etc
    """
    session = Session("localhost",hf2=True)
    avbdev = session.devices.visible()
    print(avbdev[0])
    device = session.connect_device(avbdev[0])
    device.demods[0].enable(1)
    sample_nodes = [
                    device.demods[0].sample.x,
                    device.demods[0].sample.y
                    ]  
    TOTAL_DURATION = int_time
    this.samplingrate = device.demods[0].rate()
    SAMPLES = this.samplingrate*TOTAL_DURATION
    daq_module = session.modules.daq
    daq_module.device(device)
    daq_module.type(0) #continuous acquisition mode
    daq_module.grid.mode(2)
    daq_module.duration(TOTAL_DURATION)
    for node in sample_nodes:
        daq_module.subscribe(node)
    daq_module.count(1)
    daq_module.grid.cols(SAMPLES)
    return device,session,daq_module
def daqdata(device,session,daq_module,inttime):
    """_summary_

    Args:
        device (_type_): _description_
        session (_type_): _description_
        daq_module (_type_): _description_
        inttime (_type_): _description_

    Returns:
        _type_: _description_
    """
    sample_nodes = [
                    device.demods[0].sample.x,
                    device.demods[0].sample.y
                    ]  
    daq_module.execute()
    while not daq_module.raw_module.finished():
        t.sleep(inttime)
    result = daq_module.read(raw=False,clk_rate=device.clockbase())
    data = np.sqrt(result[sample_nodes[0]][0].value[0]**2+result[sample_nodes[1]][0].value[0]**2)
    #print('poll end')
    return data
