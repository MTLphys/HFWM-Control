from zhinst.toolkit import Session
import time as t
import numpy as np 
def connect():
    session = Session("localhost",hf2=True)
    avbdev = session.devices.visible()
    print(avbdev[0])
    device = session.connect_device(avbdev[0])
    device.demods[0].enable(1)
    return device,session
def polldata(device,session,inttime):
    #print('poll start with delay of',inttime)
    device.demods[0].sample.subscribe()
    t.sleep(inttime)
    device.demods[0].sample.unsubscribe()
    #print('poll end')
    poll_result = session.poll()
    demod_sample = poll_result[device.demods[0].sample]
    return np.sqrt(demod_sample['x']**2+demod_sample['y']**2)
