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
	include UI
'''
#print('\n')

import time
from math import floor
from random import uniform

FORMATGAP = 20

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
		
		self.people = 100
		self.population = []
		
		self.health = 0
		self.employment = 0
		self.avr_salary = 0
		self.avr_savings = 0
		
		self.income_tax = 10 #income_tax is how much of each citizen's salary they pay for tax per year
		self.gov_funds = 0
		self.gov_costs = 0
		
		self.days = 0
		self.years = 0
		
		
		for p in range (0,self.people):
			if uniform(0,100) < unhealthy_chance:
				temp_health = False
			else:
				temp_health = True
			
			if uniform(0,100) < unemployment_chance:
				temp_employed = False
			else:
				temp_employed = True
			temp_salary = uniform(10,200)
				
			self.population.append(Person(temp_health,temp_employed,temp_salary))
		self.update_stats()
		self.days = 0
		#print('Society created')
			
	def info_dump(self):
		for p in self.population:
			#print every Person's health status,employment status and salery
			print(str(p.health)+(9-len(str(p.health)))*' '+str(p.employed)+(9-len(str(p.employed)))*' '+str(p.salary))
	
	def stat_dump(self):
		
		#print days & years so far
		print('Days'+(FORMATGAP-len('Days'))*' '+'Years')
		print(str(self.days)+(FORMATGAP-len(str(self.days)))*' '+str(self.years)+'\n')
	
		#print overall health, employment rate and average salery
		print('Health'+(FORMATGAP-len('Health'))*' '+'Employment'+(FORMATGAP-len('Employment'))*' '+'Average Salary')
		print(str(self.health)+(FORMATGAP-len(str(self.health)))*' '+str(self.employment)+(FORMATGAP-len(str(self.employment)))*' '+str(self.avr_salary)+'\n')
	
		#print tax rate, gov_funds, avrerage savings
		print('Income Tax(%)'+(FORMATGAP-len('Income Tax(%)'))*' '+'Gov Funds'+(FORMATGAP-len('Gov Funds'))*' '+'Average savings')
		print(str(self.income_tax)+(FORMATGAP-len(str(self.income_tax)))*' '+str(self.gov_funds)+(FORMATGAP-len(str(self.gov_funds)))*' '+str(self.avr_savings)+'\n')
	
	def update_stats(self):
		self.days+=1  		#every recalculate() is one day passing
		if self.days == 365: 	# if 365 days have past 1 year has past and :
			self.years+=1		# we update the year count +1
			self.days = -1		# we set days to negitive 1 because the next day should be 1 year 0 days
		
		self.health = 0
		self.employment = 0
		
		self.avr_salary = 0	
		total_salary = 0
		
		self.avr_savings = 0
		total_savings = 0
		
		for p in self.population:
			total_savings += p.savings
			
			if p.health == True:
				self.health += 1
			
			if p.employed == True:
				self.employment += 1
				total_salary += p.salary
		
				self.gov_funds = (self.gov_funds + ((p.salary / 100)*(self.income_tax/365))) - self.gov_costs
				p.savings = p.savings + (p.salary - ((p.salary / 100)*(self.income_tax/365)))/365
		self.avr_salary = total_salary/self.employment
		self.avr_savings = total_savings/self.people
	
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
	
	def recalculate(self, debug=False):
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
		if debug:
			self.stat_dump()
	
	def dashboard(self):
		self.dash_labels=[]
		self.dash_values=[]
		
		self.dash_labels.append('Days')
		self.dash_labels.append((6-len('Days')) * ' ')
		self.dash_labels.append('Years')
		self.dash_labels.append((8-len('Years')) *' ')
		self.dash_labels.append('Health')
		self.dash_labels.append((9-len('Health')) * ' ')
		self.dash_labels.append('Employment')
		self.dash_labels.append((13-len('Employment')) * ' ')
		self.dash_labels.append('Average Salary')
		self.dash_labels.append((17-len('Average Salary')) * ' ')
		self.dash_labels.append('Income Tax(%)')
		self.dash_labels.append((16-len('Income Tax(%)')) * ' ')
		self.dash_labels.append('Gov Funds')
		self.dash_labels.append((12-len('Gov Funds')) * ' ')
		self.dash_labels.append('Average Savings')
		
		self.dash_values.append(str(self.days))
		self.dash_values.append((6-len(str(self.days))) * ' ')
		self.dash_values.append(str(self.years))
		self.dash_values.append((8-len(str(self.years))) * ' ')
		self.dash_values.append(str(self.health))
		self.dash_values.append((9-len(str(self.health))) * ' ')
		self.dash_values.append(str(self.employment))
		self.dash_values.append((13-len(str(self.employment))) * ' ')
		self.dash_values.append(str(floor(self.avr_salary)))
		self.dash_values.append((17-len(str(floor(self.avr_salary)))) * ' ')
		self.dash_values.append(str(self.income_tax))
		self.dash_values.append((16-len(str(self.income_tax))) * ' ')
		self.dash_values.append(str(floor(self.gov_funds*100)/100))
		self.dash_values.append((12-len(str(floor(self.gov_funds)))) * ' ')
		self.dash_values.append(str(floor(self.avr_savings*100)/100))
		self.dash_values.append('\n')
		
		print("".join(self.dash_labels))
		print("".join(self.dash_values))
		
		#print days, years, overall health, employment rate, average salery,  avrerage savings, tax rate, gov_funds, tax rate, gov_funds, avrerage savings
		#print('Days'+(6-len('Days'))*' '+'Years'+(8-len('Years'))*' '+'Health'+(9-len('Health'))*' '+'Employment'+(13-len('Employment'))*' '+'Average Salary'+(17-len('Average Salary'))*' '+'Income Tax(%)'+(16-len('Income Tax(%)'))*' '+'Gov Funds'+(12-len('Gov Funds'))*' '+'Average Savings')
		#print(str(self.days)+(6-len(str(self.days)))*' '+str(self.years)+(8-len(str(self.years)))*' '+str(self.health)+(9-len(str(self.health)))*' '+str(self.employment)+(13-len(str(self.employment)))*' '+str(floor(self.avr_salary))+(17-len(str(floor(self.avr_salary))))*' '+str(self.income_tax)+(16-len(str(self.income_tax)))*' '+str(floor(self.gov_funds))+(12-len(str(floor(self.gov_funds))))*' '+str(floor(self.avr_savings))+'\n')
class Person:
	def __init__(self,health,employed,salary):
		self.health = health
		self.employed = employed
		self.salary = salary  #can be from 10 to 200 (k)
		self.savings = 0
		
mySociety = Society()
mySociety.recalculate()
mySociety.dashboard()