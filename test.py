from stream_process import stream, process, column
import matplotlib.pyplot as plt
import numpy as np

def plotting(x,y):
	plt.subplot(2, 2, 1)
	plt.grid(True)

	plt.plot(x, y, '*b-')
	plt.axis([0,60,0,3500])
	plt.title('Grid Diagrams')
	plt.xlabel('dT min')
	plt.ylabel('QH')


	plt.subplot(2, 2, 2)
	z = []
	cc = []
	for i in x:
		cc.append(25*10**6/(np.power(i,0.05)))
	print '\t\t\t',cc
	for i in y:
		z.append(i*10800)
	plt.plot(x, z, '*b-')
	plt.plot(x, cc, '*b-')
	plt.title('Grid Diagrams')
	plt.xlabel('dT min')
	plt.ylabel('$/year')


	plt.subplot(2, 2, 3)
	s = []
	for i in range(0,len(y)):
		s.append(z[i]+cc[i])

	plt.grid(True)
	plt.plot(x, s, '*b-')
	plt.xlabel('dT min')
	plt.ylabel('Summation')
	plt.show()

def main():

	Qh_arr = []
	dT_array = []


	'''
	#Streams
	stream1 = stream(1,20,135,2,dT)
	stream2 = stream(2,170,60,3,dT)
	stream3 = stream(3,80,140,4,dT)
	stream4 = stream(4,150,30,1.5,dT)

	#Columns
	reb_1 = column('Reboiler_1',150,20,'reb',dT)
	cond_1 = column('Condensor_1',140,20,'cond',dT)
	cond_2 = column('Condensor 2',104.5,186.8,'cond',dT)

	streams = [stream1, stream2, stream3, stream4,reb_1,cond_1,cond_2]
	

	'''
	for i in range (2,50):
		dT = i
		#stream# = (name, suppy_temp,target_temp, heat_capacity,dT)
		stream1 = stream(1,35.5,450.0,2.439,dT)
		stream2 = stream(2,450.0,40.0,2.4417,dT)
		stream3 = stream(3,40.0,75.0,1.2314,dT)
		stream4 = stream(4,35.5,20.0,0.5226,dT)
		stream5 = stream(5,104.5,35.0,0.5252,dT)
		stream6 = stream(6,129.9,80.3,1.1503,dT)
		stream7 = stream(7,183.2,80.0,3.25872,dT)
		stream8 = stream(8,249.3,25.0,.1177,dT)
		stream9 = stream(9,80.0,25.0,.12727,dT)

		
		reb_1 = column('Reboiler 1',129.91,95.0,'reb',dT)
		cond_1 = column('Condensor 1',35.51,35.7,'cond',dT)
		reb_2 = column('Reboiler 2',150.31,286.5,'reb',dT)
		cond_2 = column('Condensor 2',104.51,186.8,'cond',dT)
		reb_3 = column('Reboiler 3',249.3,2832,'reb',dT)
		cond_3 = column('Condensor 3',183.21,2552.7,'cond',dT)

		#combine streams into one array
		streams = [stream1, stream2, stream3, stream4, stream5, stream6, stream7, stream8, stream9,cond_3,reb_3,cond_1, cond_2, reb_1, reb_2] #reb_1,cond_1,cond_2,reb_2,reb_3,cond_3


		#Process stream array in the "process" class
		p = process(streams,dT)

		#Calculates mCp
		p.mcp()

		#Determines the infeasible and feasible heat cascade
		p.cascade()

		#Determines the single pinch
		p.pinch()

		#Prints Nessasary Info about the streams
		p.final()
		
		#integrates columns (Has to be after the feasible unintegrated cascade is determined)
		z = p.column_int()

		#Shows above and below values for kW needed
		#p.network()
		
		#Plots the All three composite curves and Grid Diagrams
		#p.comp_curve()

		Qh_arr.append(z)
		dT_array.append(i)

	plotting(dT_array,Qh_arr)



main()

