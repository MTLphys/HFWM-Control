from zhinst.toolkit import Session
import time as t
import numpy as np 
def connect():
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
    return device,session
def polldata(device,session,inttime):
    """_summary_

    Args:
        device (_type_): _description_
        session (_type_): _description_
        inttime (_type_): _description_

    Returns:
        _type_: _description_
    """
    #print('poll start with delay of',inttime)
    device.demods[0].sample.subscribe()
    t.sleep(inttime)
    device.demods[0].sample.unsubscribe()
    #print('poll end')
    poll_result = session.poll()
    demod_sample = poll_result[device.demods[0].sample]
    return np.sqrt(demod_sample['x']**2+demod_sample['y']**2)
