from stream_process import stream, process

#dT Min
dT = 10

#stream# = (name, suppy_temp,target_temp, heat_capacity,dT)
stream1 = stream(1,60,180,3,dT)
stream2 = stream(2,180,40,2,dT)
stream3 = stream(3,30,105,2.6,dT)
stream4 = stream(4,150,40,4,dT)

#combine streams into an array
streams = [stream1, stream2, stream3, stream4]

#Process stream array using the "process" class
p = process(streams)

#Calculates mCp
p.mcp()

#Determines the infeasible and feasible heat cascade
p.cascade()

#Determines the single pinch
p.pinch()

#Prints Nessasary Info about the streams
p.final()

#Plots the All three composite curves and Grid Diagrams
p.comp_curve()

'''
Output
____________________________________________________________________________________________________
Temperatures Ranges:  [185.0, 175.0, 145.0, 110.0, 65.0, 35.0]
Temperatures Change:  [10.0, 30.0, 35.0, 45.0, 30.0]
Summation mCp (Net):  [-3.0, -1.0, 3.0, 0.4, 3.4]
Delta Enthalpy dH:    [-30.0, -30.0, 105.0, 18.0, 102.0]

INfeasibile Heat Cascade:  [60.0, 30.0, 0.0, 105.0, 123.0, 225.0]
FEasibile Heat Cascade:      [60.0, 30.0, 0.0, 105.0, 123.0, 225.0]


	Min Hot  Utility:   60 kW
	Min Cold Utility:   225 kW
	Pinch Temperature:  145 C

____________________________________________________________________________________________________
'''



