'''
Society is an econmicics game/simulator in which the player can control meny aspects of life within a "society" of
one hundered people. Consequences of a player's actions will be as real as possible.
Title: Society
Arthor: third-meow
Date:
'''

#print('\n\n')
import time
from random import uniform

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
		self.health = 0
		self.employment = 0
		self.avr_salary = 0
		self.population = []
		

		for p in range (0,self.people):
			if uniform(0,100) < unhealthy_chance:
				temp_health = False
			else:
				temp_health = True
			
			if uniform(0,100) < unemployment_chance:
				temp_employed = False
			else:
				temp_employed = True
				
			self.population.append(Person(temp_health,temp_employed,70))
		self.update_stats()
		print('Society created')
		print('\n')
	
	def info_dump(self):
		for p in self.population:
			#print every Person's health status,employment status and salery
			print(str(p.health)+(9-len(str(p.health)))*' '+str(p.employed)+(9-len(str(p.employed)))*' '+str(p.salary))
	
	def stat_dump(self):
		print('Health'+(14-len('Health'))*' '+'Employment'+(14-len('Employment'))*' '+'Average Salary')
		#print overall health, employment rate and average salery
		print(str(self.health)+(14-len(str(self.health)))*' '+str(self.employment)+(14-len(str(self.employment)))*' '+str(self.avr_salary))
	
	def update_stats(self):
		self.health = 0
		self.employment = 0
		self.avr_salary = 0		
		total_salary = 0
		for p in self.population:
			if p.health == True:
				self.health += 1
			if p.employed == True:
				self.employment += 1
				total_salary += p.salary
		self.avr_salary = total_salary/self.employment
		
	def calibrate_chances(self,debug=False):		#to be run in self.recalculate() after self.update_stats() but before if statments
		self.calibrated_get_sick_chance = get_sick_chance/self.health
		self.calibrated_get_better_chance = get_better_chance/(self.people-self.health)
		self.calibrated_lose_job_chance = lose_job_chance/self.employment
		self.calibrated_new_job_chance = new_job_chance/(self.people-self.employment)
		if debug == True:
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
	def recalculate(self):
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

			
		
class Person:
	def __init__(self,health,employed,salary):
		self.health = health
		self.employed = employed
		self.salary = salary  #can be from 10 to 200 (k)



mySociety = Society()

for i in range (0,100):
	mySociety.recalculate()	
	mySociety.recalculate()	
	mySociety.stat_dump()