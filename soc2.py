'''
Society is an econmicics game/simulator in which the player can control meny aspects of life within a "society" of
one hundered people. Consequences of a player's actions will be as real as possible.
Title: Society
Arthor: third-meow
Date:
'''
# ## #
'''
Goals	
	intro infomation!
	include tax low wage cut off
	include math for find living costs
	include "cash on hand" vairable for finding money after living costs and tax
	karma stat
	homeless stat
	city wide crime?
	city wide "activitys"
	buildings could include
		dairy
		park
		bank
		lawers
		roads
		police stations (combats crime levels and karma?)
		truck depot
		state houseing
	buildings could unlock other buildings
	infrastuctor
	random events!
		earthquakes
		fires
		sudden lack of money
		changes of federal law requirements
		criminal activity in town
		state lawsuits
	people in society demanding/requesting stuff
		enviromentalists
		commuters
		anti-tax avoiders
		sick people
		homeless people
	end objectives
		prove to govenment you are stable by not dying for X days/years
'''
#print('\n')

import time
from math import floor
from random import uniform

FORMATGAP = 20					#FORMATGAP is used for formating output to keep numbers under their labels

#chance variables
unhealthy_chance = 10.0 		#the higher this is(out of 100) the more people will be unhealthy.
unemployment_chance = 10.0 		#the higher this is(out of 100) the more unemployed Society will be.

get_sick_chance = 1.0 		#the higher this is the more likly a person will get sick.
get_better_chance = 1.0 	#the higher this is the more likly a sick person will get better.
new_job_chance = 1.0 		#the higher this is the more likly a unemployed person will get a job.
lose_job_chance = 1.0 		#the higher this is the more likly a person is to lose their job.
pay_rise_chance = 1.0		#the higher this is the more likly a person will get a pay rise
pay_cut_chance = 1.0		#the higher this is the more likly a person will get a pay cut
class Society:
	def __init__(self):
		
		self.people = 100			#number of people is society
		self.population = []		#holds instances of class "person"
		
		self.health = 0				#number of healthy people is society
		self.employment = 0			#number of employed people is society
		self.avr_salary = 0			#average salary of the people in society
		self.avr_savings = 0		#average savings of the people in society
		
		self.avalible_buildings = []		#list of buildings player could build
		self.avalible_buildings.append(['Small Hospital',1000,1.2,+13,+15])			#format of these inner lists is [name, cost, maintaining cost(per day), societal heath benift, societal employment benifit]
		self.avalible_buildings.append(['Large Hospital',3000,2.1,+19,+20])
		self.avalible_buildings.append(['Library',50,0,+10])
		
		self.buildings = []			#list of built buildings
		
		self.income_tax = 10 		#income_tax is how much of each citizen's salary they pay for tax per year
		self.gov_funds = 20			#the govenments savings
		self.gov_costs = 0.5		#dayliy cost of govenment
		
		self.days = 0				#days so far
		self.years = 0				#years so far
		
		self.rst = False			#allows game to be reset
		self.ext = False			#allows game to exit
		
		for p in range(self.people):
			if uniform(0,100) < unhealthy_chance:
				temp_health = False
			else:
				temp_health = True
			
			if uniform(0,100) < unemployment_chance:
				temp_employed = False
			else:
				temp_employed = True
			temp_salary = uniform(10,200)
				
			self.population.append(Person(temp_health,temp_employed,temp_salary))		#create instances of class "person" with random health status, employment status & random salary
		self.update_stats()
		self.days = 0				#begin gameplay with day 0
	
	def reset(self):				#allows for self.rst to be "seen" outside self
		return self.rst	
	def exit(self):					#allows for self.ext to be "seen" outside self
		return self.ext
	def update_stats(self):
		self.days+=1  			#every recalculate() is one day passing
		if self.days == 365: 	# if 365 days have past, 1 year has past and so we:
			self.years+=1			# update the year count +1
			self.days = -1			# & set days to negitive 1 because the next day should be 1 year 0 days
		
		self.health = 0
		self.employment = 0
		
		self.avr_salary = 0			#set all statistics about society to 0 (we are about to update them)
		total_salary = 0
		
		self.avr_savings = 0
		total_savings = 0
		
		for p in self.population:			#for loop where p represents a instance of person from our list
			total_savings += p.savings		#total savings is used to calculate average savings
			
			if p.health == True:
				self.health += 1			#this will keep track of how meny healthy people there are in our population
			
			if p.employed == True:
				self.employment += 1		#this will keep track of how meny employed people there are in our population
				total_salary += p.salary	#total salary is used to calculate average salary
		
				self.gov_funds = (self.gov_funds + ((p.salary/100)*(self.income_tax/365))) 				#add each person's income tax to govement funds 
				p.savings = p.savings + (p.salary - ((p.salary/100)*(self.income_tax/365)))/365			#add remaining money to person's savings
		self.avr_salary = total_salary/self.employment		#calculate average salary
		self.avr_savings = total_savings/self.people		#calculate average savings
		self.gov_funds -= self.gov_costs					#take govement costs off govement funds
	
	def calibrate_chances(self,debug=False):		#to be run in self.recalculate() after self.update_stats() but before if statments
		
		try:
			self.calibrated_get_sick_chance = get_sick_chance/self.health
		except ZeroDivisionError:
			self.calibrated_get_sick_chance = 100
		try:
			self.calibrated_get_better_chance = get_better_chance/(self.people-self.health)
		except ZeroDivisionError:
			self.calibrated_get_better_chance = 100
		try:
			self.calibrated_lose_job_chance = lose_job_chance/self.employment
		except ZeroDivisionError:
			self.calibrated_lose_job_chance = 100
		try:
			self.calibrated_new_job_chance = new_job_chance/(self.people-self.employment)
		except ZeroDivisionError:
			self.calibrated_new_job_chance = 100
			
		if debug:
			print('self.calibrated_get_sick_chance')
			print(self.calibrated_get_sick_chance)
			print('self.calibrated_get_better_chance')
			print(self.calibrated_get_better_chance)
			print('self.calibrated_lose_job_chance')
			print(self.calibrated_lose_job_chance)
			print('self.calibrated_new_job_chance')
			print(self.calibrated_new_job_chance)
			print('back to non-calibrated values')
			print('getsick')
			print(self.calibrated_get_sick_chance*self.health)
			print('getbetter')
			print(self.calibrated_get_better_chance*(self.people-self.health))
			print('losejob')
			print(self.calibrated_lose_job_chance*self.employment)
			print('newjob')
			print(self.calibrated_new_job_chance*(self.people-self.employment))
	
	def recalculate(self, printout=False):
		self.update_stats()
		self.calibrate_chances()
	
		for p in self.population:
			if p.health == True:
				if uniform(0,100) < self.calibrated_get_sick_chance:
					p.health = False
			else:
				if uniform(0,100) < self.calibrated_get_better_chance:
					p.health = True
					
			if p.employed == True:
				if uniform(0,100) < self.calibrated_lose_job_chance:
					p.employed = False
			else:
				if uniform(0,100) < self.calibrated_new_job_chance:
					p.employed = True
					
			if p.employed == True:
				if uniform(0,100) > pay_rise_chance:
					p.salary = p.salary/0.95
			
				if uniform(0,100) > pay_cut_chance:
					p.salary = p.salary*0.95
		if printout:
			self.dashboard()
	
	def dashboard(self):
		dash_labels=[]
		dash_values=[]
		
		dash_labels.append('Days')
		dash_labels.append((6-len('Days')) * ' ')
		dash_labels.append('Years')
		dash_labels.append((8-len('Years')) *' ')
		dash_labels.append('Health')
		dash_labels.append((9-len('Health')) * ' ')
		dash_labels.append('Employment')
		dash_labels.append((13-len('Employment')) * ' ')
		dash_labels.append('Average Salary')
		dash_labels.append((17-len('Average Salary')) * ' ')
		dash_labels.append('Income Tax(%)')
		dash_labels.append((16-len('Income Tax(%)')) * ' ')
		dash_labels.append('Gov Funds')
		dash_labels.append((12-len('Gov Funds')) * ' ')
		dash_labels.append('Average Savings')
		
		dash_values.append(str(self.days))
		dash_values.append((6-len(str(self.days))) * ' ')
		dash_values.append(str(self.years))
		dash_values.append((8-len(str(self.years))) * ' ')
		dash_values.append(str(self.health))
		dash_values.append((9-len(str(self.health))) * ' ')
		dash_values.append(str(self.employment))
		dash_values.append((13-len(str(self.employment))) * ' ')
		dash_values.append(str(floor(self.avr_salary)))
		dash_values.append((17-len(str(floor(self.avr_salary)))) * ' ')
		dash_values.append(str(self.income_tax))
		dash_values.append((16-len(str(self.income_tax))) * ' ')
		dash_values.append(str(floor(self.gov_funds)))
		dash_values.append((12-len(str(floor(self.gov_funds)))) * ' ')
		dash_values.append(str(floor(self.avr_savings*100)/100))
		dash_values.append('\n')
		
		print("".join(dash_labels))
		print("".join(dash_values))
		
	def action(self):
		while True:
			self.dashboard()
			
			usr_sig = input('Action> ')
			if  usr_sig == 'n' or usr_sig == 'N':		# n = next day
				break
			elif usr_sig == 'x' or usr_sig == 'X':		# x = reset/exit
				usr_reset_sig = input('Do you want to reset(r), exit(x) or continue(c)>')
				if usr_reset_sig == 'r' or usr_reset_sig =='R':
					self.rst = True
					break
				elif usr_reset_sig == 'x' or usr_reset_sig == 'X':
					self.ext = True
					break
				elif usr_reset_sig == 'c' or usr_reset_sig == 'C':
					pass
				else:
					pass
			elif usr_sig == 't' or usr_sig == 'T':		# t = tax change
				self.income_tax = int(input('Income tax(%)> '))
			elif usr_sig == 'e' or usr_sig == 'E':		# e = employ
				self.build()
			elif usr_sig == 'w' or usr_sig == 'W':		# w = wait
				wait_for = int(input('Days>'))
				for i in range (wait_for):
					self.recalculate()
			else:
				break
	def build(self):
		print('Built Buildings')
		print('Index'+(14-len('Index'))*' '+'Building'+(28-len('Building'))*' '+'Cost')
		
		for i in range(len(self.buildings)):
			print(str(i)+(14-len(str(i)))*' '+self.buildings[i][0]+(28-len(self.buildings[i][0]))*' '+str(self.buildings[i][1]))
		print('\n')
		
		
		print('Avalible Buildings')
		print('Index'+(14-len('Index'))*' '+'Building'+(28-len('Building'))*' '+'Cost')
		
		for i in range(len(self.avalible_buildings)):
			print(str(i)+(14-len(str(i)))*' '+self.avalible_buildings[i][0]+(28-len(self.avalible_buildings[i][0]))*' '+str(self.avalible_buildings[i][1]))
		print('\n')
		
		
		usr_sig = input('Build(b) or exit(x)>')
		if usr_sig == 'b' or usr_sig == 'B':
			
			usr_build_sig = input('Build(index number)>')
			if self.gov_funds > self.avalible_buildings[int(usr_build_sig)][1]:
				self.gov_funds -= self.avalible_buildings[int(usr_build_sig)][1]
				self.gov_costs += self.avalible_buildings[int(usr_build_sig)][2]
				
				self.buildings.append(self.avalible_buildings[int(usr_build_sig)])
			else:
				print('Not enough funds \n')
				time.sleep(1)
		else:
			pass
		
		
class Person:
	def __init__(self,health,employed,salary):
		self.health = health
		self.employed = employed
		self.salary = salary  #can be from 10K to 200K
		self.savings = 0


while True:
	mySociety = Society()
	while mySociety.reset() == False:
		mySociety.recalculate()
		mySociety.action()
		if mySociety.exit():
			quit()