from __future__ import division
import matplotlib.pyplot as plt

class stream:
	def __init__ (self,name, supply_temp,target_temp, heat_capacity, dT):
		self.name = name
		self.supply_temp = supply_temp
		self.target_temp = target_temp
		self.heat_capacity = heat_capacity
		self.dT=dT
		self.cp = []

		#Determine Cold/Hot
		if (self.supply_temp < self.target_temp):
			self.hot_cold = "cold"
		else:
			self.hot_cold = "hot"

		#Capacity changer
		if (self.hot_cold == "cold"):
			self.heat_capacity = self.heat_capacity*-1


		#From Cold/Hot create shifts
		if (self.hot_cold == "cold"):
			self.supply_shift = self.supply_temp + (self.dT/2)
			self.target_shift = self.target_temp + (self.dT/2)
		else:
			self.supply_shift = self.supply_temp - (self.dT/2)
			self.target_shift = self.target_temp - (self.dT/2)

	def getHeatCapacity(self):
		return int(self.heat_capacity)

class column:
	def __init__(self,name, fixed_temp, heat, reb_cond,dT):
		self.name = name
		self.fixed_temp = fixed_temp
		self.heat = heat
		self.reb_cond = reb_cond
		self.dT = dT

		#Determines if Column is a condenser or reboiler
		if self.reb_cond == 'reb':
			self.interface_temp = fixed_temp + self.dT
			self.heat = self.heat*-1
			self.shifted_column_temp=self.fixed_temp + self.dT/2
		elif self.reb_cond == 'cond':
			self.interface_temp = fixed_temp - self.dT
			self.shifted_column_temp=self.fixed_temp - self.dT/2


	#Look into integrating column into the process class.


#Process Class for processing columns and streams
class process:
	def __init__(self, l):
		self.l = l

		#Lists for Streams and Columns
		self.stream_list=[]
		self.column_list = []

		self.temps = []

		#Seperates the Streams from the Columns
		for i in range(0,len(self.l)):
			if isinstance(self.l[i] , column):
				self.column_list.append(self.l[i])
			elif isinstance(self.l[i] , stream):
				self.stream_list.append(self.l[i])
		
		#Unique Temperatures
		for i in self.stream_list:
			self.temps.append(i.target_shift)
			self.temps.append(i.supply_shift)
		self.temps = list(set(self.temps))
		self.temps = sorted(self.temps)
		self.temps.reverse()

		#Temperature Change
		self.temp_change = []
		counter = 0
		while (counter < len(self.temps)-1):
			self.temp_change.append(self.temps[counter]-self.temps[counter+1])
			counter = counter + 1

	def mcp(self):
		self.sum_cp=[0] * len(self.temp_change) #cold-hot

		#Running through stream Lists (User inputs)
		for i in self.stream_list:

			
			if i.hot_cold == "cold":
				s = set(range(int(i.supply_shift),int(i.target_shift)+1))
			else:
				s = set(range(int(i.target_shift),int(i.supply_shift)+1))

			#Creates subset temp changes (Shift Temperatures)
			for j in range(0,len(self.temps)-1):

				#Cretes Subset
				small_subset = set(range(int(self.temps[j+1]),int(self.temps[j])+1))

				#Subset Function
				if small_subset.issubset(s):
					self.sum_cp[j]=self.sum_cp[j]+i.heat_capacity
				else:
					pass

		for i in range (0, len(self.sum_cp)):
			self.sum_cp[i]=round(self.sum_cp[i],3)

		#Creating dH Change in Enthalpy
		self.dH=[0] * len(self.temp_change) #cold-hot
		for i in range (0, len(self.sum_cp)):
			self.dH[i] = self.temp_change[i]*self.sum_cp[i]

	#Generating Cascades
	def cascade(self):
		#INfeasible Cascade
		self.in_feas_cascade = [0]
		counter = 0
		for i in self.dH:
			self.in_feas_cascade.append(self.in_feas_cascade[counter]+i)
			counter = counter + 1
		
		#Used to DETERMINE smallest value and pinch
		self.minimum_value = min(self.in_feas_cascade)

		if self.minimum_value<0:
			self.minimum_value= self.minimum_value*-1
		
		#Feasible Cascade
		self.feas_cascade = self.in_feas_cascade

		for i in range(0,len(self.feas_cascade)):
			#INFEASIBLE CHANGES HERE FOR SOME REASON...
			#Determine the reason for the change
			self.feas_cascade[i] = self.feas_cascade[i] + self.minimum_value

	#Return which temp is the pinch
	def pinch(self):
		self.pinch = 0
		for i in range (1,len(self.in_feas_cascade)):
			if self.in_feas_cascade[self.pinch]>self.in_feas_cascade[i]:
				self.pinch = i


	def column_int(self):
		#temps with columns
		self.integrated_temp_profiles = []

		for i in self.temps:
			self.integrated_temp_profiles.append(i)

		#Creating unique Temperature profiles
		for i in self.column_list:
			self.integrated_temp_profiles.append(i.shifted_column_temp)
			self.integrated_temp_profiles.append(i.shifted_column_temp)
			if i=="cond":
				print "Condenser Temp: ", i.shifted_column_temp, "Condenser Work: ", i.heat, "kW"
			else:
				print "Reboiler Temp: ", i.shifted_column_temp, "Reboiler Temp: ", i.heat, "kW"

		self.integrated_temp_profiles.sort()
		self.integrated_temp_profiles.reverse()

		#Temperature Change
		self.temp_change_column = []
		counter = 0
		while (counter < len(self.integrated_temp_profiles)-1):
			self.temp_change_column.append(self.integrated_temp_profiles[counter]-self.integrated_temp_profiles[counter+1])
			counter = counter + 1

		#Sum of Cp's ARRAY with Columns
		self.sum_cp_columns=[0] * len(self.temp_change_column) #cold-hot

		print '_'*100
		#Printing out Column Information and adding 
		print '\nTemps including Column', self.integrated_temp_profiles
		print 'Temps Change w/ Columns ', self.temp_change_column

		print '_'*100

		for i in self.stream_list:
			if i.hot_cold == "cold":
				s = set(range(int(i.supply_shift),int(i.target_shift)+1))
			else:
				s = set(range(int(i.target_shift),int(i.supply_shift)+1))

			#Creates subset temp changes (Shift Column Temperatures)
			for j in range(0,len(self.temp_change_column)):

				#Cretes Subset
				small_subset = set(range(int(self.integrated_temp_profiles[j+1]),int(self.integrated_temp_profiles[j])+1))
				small_subset = set(sorted(small_subset))
				#Subset Function
				if len(small_subset) == 1:
					pass
				if small_subset.issubset(s):
					self.sum_cp_columns[j]=self.sum_cp_columns[j]+i.heat_capacity
				else:
					pass


		print "\nSum of Cp: ", self.sum_cp_columns

		for i in range (0, len(self.sum_cp_columns)):
			self.sum_cp_columns[i]=round(self.sum_cp_columns[i],3)

		#Creating dH Change in Enthalpy
		self.dH_column=[0] * len(self.temp_change_column) #cold-hot
		for i in range (0, len(self.sum_cp_columns)):
			self.dH_column[i] = self.temp_change_column[i]*self.sum_cp_columns[i]

		print self.dH_column

		#Finding the Zeros where the columns are...
		for i in range(0,self.dH_column):
			if self.dH_column[i] == 0;
			





	def final(self):
		print "_"*100
		print "Temperatures Ranges: ", self.temps
		print "Temperatures Change: ", self.temp_change
		print "\nSummation mCp (Net): ", self.sum_cp
		print "Delta Enthalpy dH:   ", self.dH



		self.min_HOT_Utility = self.feas_cascade[0]
		self.min_COLD_Utility = self.feas_cascade[-1]
		print '\nFeasibile Heat Cascade:     ', self.feas_cascade

		print "\n"
		print "\tMin Hot  Utility:  ", int(self.min_HOT_Utility), "kW"
		print "\tMin Cold Utility:  ", int(self.min_COLD_Utility), "kW"
		print "\tPinch Temperature: ", int(self.temps[self.pinch]), "C\n"
		print "_"*100

	def comp_curve(self):
		
		#Grand Composite Curve (Subplot 1)
		plt.subplot(2, 2, 1)
		x_points = self.feas_cascade
		y_points = self.temps

		plt.plot(x_points, y_points, 'ob-')
		plt.title('Grand Composite')
		plt.xlabel('Net Heat Flow (kW)')
		plt.ylabel('Shifterd Temps (C)')




		#Grid Diagrams (Subplot 2)
		plt.subplot(2, 2, 2)
		plt.grid(True)

		plt.plot(0,0)

		
		for i in self.stream_list:

			x = [int(i.supply_shift),int(i.target_shift)]
			y = [i.name,i.name]
			if (i.hot_cold == "cold"):
				plt.plot(x,y,color='b')
			else:
				plt.plot(x,y,color='r')
			plt.plot(0,i.name+1)
			plt.quiver(i.supply_shift,i.name,i.target_shift,i.name)

		
		plt.title('Grid Diagrams')
		plt.xlabel('Temperatures (C)')
		plt.ylabel('Stream #')

		#Composite Curve (Subplot 3)
		plt.subplot(2, 2, 3)
		x_points = []
		y_points = []

		plt.plot(x_points, y_points, 'xb-')
		plt.title('Hot & Cold Actual Composite Curve')
		plt.xlabel('Heat Flow (kW)')
		plt.ylabel('Actual Temps (C)')

		#Shifted Composite Curve (Subplot 4)
		plt.subplot(2, 2,4)
		x_points = []
		y_points = []

		plt.plot(x_points, y_points, 'xb-')
		plt.title('Shifted Composite Curve')
		plt.xlabel('Heat Flow (kW)')
		plt.ylabel('Shifterd Temps (C)')
		plt.tight_layout()
		
		plt.show()

