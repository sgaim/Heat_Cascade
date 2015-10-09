from Process_python import stream, process, column

#dT Min
dT = 10

#stream# = (name, suppy_temp,target_temp, heat_capacity,dT)
stream1 = stream(1,20,135,2,dT)
stream2 = stream(2,170,60,3,dT)
stream3 = stream(3,80,140,4,dT)
stream4 = stream(4,150,30,1.5,dT)


#Columns
reb_1 = column('Reboiler_1',150,20,'reb',dT)
cond_1 = column('Condensor_1',150,20,'cond',dT)


#If you would like to add more streams
'''
stream5 = stream(5,60,180,3,None,dT)
stream6 = stream(6,180,40,2,None,dT)
stream7 = stream(7,30,105,2.6,None,dT)
stream8 = stream(8,150,40,4,None,dT)
'''

#combine streams into one array
streams = [stream1, stream2, stream3, stream4,reb_1,cond_1]

#Process stream array in the "process" class
p = process(streams)

#Calculates mCp
p.mcp()

#Determines the infeasible and feasible heat cascade
p.cascade()

#Determines the single pinch
p.pinch()

#Prints Nessasary Info about the streams
p.final()

#integrates columns (Has to be after the feasible unintegrated cascade is determined)
p.column_in()


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



