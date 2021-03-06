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
	include tax low wage cut off
	include math for find living costs
	include "cash on hand" vairable for finding money after living costs and tax
	karma stat
	homeless stat
	city wide crime?
	city wide "activitys"
	buildings could include
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
print('\n')

import time
from math import floor
from random import uniform
import instruct

#chance variables
unhealthy_chance = 10.0 		#the higher this is(out of 100) the more people will be unhealthy.
unemployment_chance = 10.0 		#the higher this is(out of 100) the more unemployed Society will be.

get_sick_chance = 1.0 		#the higher this is the more likely a person will get sick.
get_better_chance = 1.0 	#the higher this is the more likely a sick person will get better.
new_job_chance = 1.0 		#the higher this is the more likely a unemployed person will get a job.
lose_job_chance = 1.0 		#the higher this is the more likely a person is to lose their job.
pay_rise_chance = 1.0		#the higher this is the more likely a person will get a pay rise
pay_cut_chance = 1.0		#the higher this is the more likely a person will get a pay cut
class Society:
	def __init__(self):
		
		self.people = 100			#number of people is society
		self.population = []		#holds instances of class "person"
		
		self.health = 0				#number of healthy people is society
		self.employment = 0			#number of employed people is society
		self.avr_salary = 0			#average salary of the people in society
		self.avr_savings = 0		#average savings of the people in society
		
		self.available_buildings = []		#list of buildings player could build
		self.available_buildings.append({'name':'Clinic','cost':1000,'cost/day':1.2,'health impact':+13,'employment impact':+15})			#available_buildings becomes a list of dictionarys with stats about the avalible buildings
		self.available_buildings.append({'name':'School','cost':300,'cost/day':2.1,'health impact':+2,'employment impact':+15})
		self.available_buildings.append({'name':'Library','cost':50,'cost/day':1.0,'health impact':0,'employment impact':+1})
		self.available_buildings.append({'name':'Park','cost':50,'cost/day':0.05,'health impact':+5,'employment impact':+1})
		self.available_buildings.append({'name':'Dairy','cost':25,'cost/day':0.5,'health impact':0,'employment impact':+5})
		
		self.buildings = []			#list of built buildings
		
		self.employment_offset = 0
		self.health_offset = 0
		self.salary_offset = 0
		
		
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

		    #create instances of class "person" with random health status, employment status & random salary	
			self.population.append(Person(temp_health,temp_employed,temp_salary))
		
		print(''.join(instruct.instructions))			#print instructions from instruct.py
		
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
				if uniform(0,100) < (self.calibrated_get_sick_chance + (self.health_offset/self.people)):
					p.health = False
			else:
				if uniform(0,100) < (self.calibrated_get_better_chance - (self.health_offset/self.people)):
					p.health = True
					
			if p.employed == True:
				if uniform(0,100) < (self.calibrated_lose_job_chance + (self.employment_offset/self.people)):
					p.employed = False
			else:
				if uniform(0,100) < (self.calibrated_new_job_chance - (self.employment_offset/self.people)):
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
		
		print(''.join(dash_labels))
		print(''.join(dash_values))
		
	
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
			elif usr_sig == 'DEV':
				command = input('COMMAND>')
				exec(command)
			else:
				break

	
	def build(self):
		print('Built Buildings')
		
		print(								#print the column titles
		'Index'									#index number for selcting building
		+(14-len('Index'))*' '					#spacer
		+'Building'								#building name
		+(18-len('Building'))*' '				#spacer
		+'Cost/day'								#cost per day
		+(18-len('Cost/day'))*' '				#spacer
		)
		
		for i in range(len(self.buildings)):
			
			print(													#print details of available buildings
			str(i)														#index number
			+(14-len(str(i)))*' '										#spacer	
			+self.buildings[i]['name']									#building name
			+(18-len(self.buildings[i]['name']))*' '					#spacer
			+str(self.buildings[i]['cost/day'])							#cost per day
			)
		print('\n')
		
		
		print('Available Buildings')
		print(								#print the column titles
		'Index'									#index number for selcting building
		+(14-len('Index'))*' '					#spacer
		+'Building'								#building name
		+(18-len('Building'))*' '				#spacer
		+'Cost'									#cost of building
		+(8-len('Cost'))*' '					#spacer
		+'Cost/day'								#cost per day
		+(18-len('Cost/day'))*' '				#spacer
		+'Effect(heath/employment)'				#effect of building on health and employment
		)
		
		for i in range(len(self.available_buildings)):
			
			print(													#print details of available buildings
			str(i)														#index number
			+(14-len(str(i)))*' '										#spacer	
			+self.available_buildings[i]['name']						#building name
			+(18-len(self.available_buildings[i]['name']))*' '			#spacer
			+str(self.available_buildings[i]['cost'])					#cost
			+(8-len(str(self.available_buildings[i]['cost'])))*' '		#spacer
			+str(self.available_buildings[i]['cost/day'])				#cost per day
			+(18-len(str(self.available_buildings[i]['cost/day'])))*' '	#spacer
			+'['														#open bracket for "effects"
			+str(self.available_buildings[i]['health impact'])			#health effect
			+'/'														#slash to separate effects
			+str(self.available_buildings[i]['employment impact'])		#emplyment effects
			+']'
			)
		print('\n')
		
		
		usr_sig = input('Build(b) or exit(x)>')
		if usr_sig == 'b' or usr_sig == 'B':
			
			usr_build_sig = int(input('Build(index number)>'))
			if self.gov_funds > self.available_buildings[usr_build_sig]['cost']:			#if you have enough money
				
				self.gov_funds -= self.available_buildings[usr_build_sig]['cost']				#take money from gov_funds
				self.gov_costs += self.available_buildings[usr_build_sig]['cost/day']				#add the amount building costs per day to gov_costs
				self.health_offset += self.available_buildings[usr_build_sig]['health impact']				#add building's health impact to self's health_offset
				self.employment_offset += self.available_buildings[usr_build_sig]['employment impact']			#add building's health impact to self's employment_offset
							
				self.buildings.append(self.available_buildings[int(usr_build_sig)])				#add building to self.buildings
			
			else:																			#if you dont have enough money
				print('Not enough funds \n')													#print "not enough funds"
				time.sleep(1)																	#wait 1 seconds
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
