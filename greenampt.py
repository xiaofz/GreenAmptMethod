from functools import partial
import numpy
import scipy.optimize
import matplotlib.pyplot as pp
import os, sys, math
import numpy as np


Rain = 0.5 ##cm/hr
Duration = 2#hour


#############################################################
K = 0.044             #Sautrated hydraulic conductivity, unit is cm/hr
InitialM = 0.25     #Initial moisture content
Saturated =0.5    #Saturated moisture content
SuctionH =22.4      #Matic pressure at the wetting front, unit is cm
#############################################################
t_window = 0, 5     #time range
f_window = 0.1, 1   #infiltration range

##############################################################
Fp = SuctionH*K*(Saturated-InitialM)/(Rain-K)    
#calculate the time to ponding at the surface(hr)
tp = Fp/Rain
print Fp, tp
vari = SuctionH*(Saturated-InitialM)

def z(t, f):
    return tp + vari/(f-K)- Fp/K + vari/K * numpy.log(Rain *(f-K)/((Rain-K)*f))-t

ts = []     #time    
fs = []     #infiltration rate
pfs = []
pts=[]
for t in numpy.linspace(*t_window, num=5*60):
    try:
        # A more efficient technique would use the last-found-y-value as a 
        # starting point
        f = scipy.optimize.brentq(partial(z, t), *f_window)
    except ValueError:
        # Should we not be able to find a solution in this window.
        pass
    else:
        ts.append(t)
        fs.append(f)




for i in range (0, len(fs)-1):
    pfs.append(min(Rain,fs[i]))
    
    pts.append(ts[i])
print pts

pp.title('Precipitation and infiltration rate') # title
pp.xlabel('Time (hrs)')                         # axis labels
pp.ylabel('Infiltration Rate/Rain Intensity, (cm/hr)')  # axis labels

plot1 = pp.plot(ts,fs,'R',label='Potential Infiltration Rate')
plot = pp.plot(pts,pfs,'B',label='Actual Infiltration Rate')

rainIntensity=np.array([0.5 for i in xrange(len(pts))])
plot2 = pp.plot(pts,rainIntensity,'y',label='Rain Intensity')

pp.legend(loc='upper right')
pp.xlim(*t_window)
pp.ylim(*f_window)
pp.show()
