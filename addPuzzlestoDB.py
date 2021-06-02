from generatePuzzleRec import generate_puzzle
from pymongo import MongoClient
import argparse

difficulty_mat = {'trivial': '0', 'very easy': '1', 'easy': '2', 'medium':'3', 'hard': '4', 'very hard': '5', 'impossible':'6'}
agegroup_mat = {'6-7': 5, '8': 4, '9-10':3,'11-12': 2, '13-14':1, '15+':0}

def calc_difficulty(difficulty):
	octal_list = ['0' for i in range(6)]
	for key in difficulty.keys():
		octal_list[agegroup_mat[key]] = difficulty_mat[difficulty[key]]
	octal_str = ''
	for bit in octal_list:
		octal_str+=bit
	print(octal_str)
	return int(octal_str)

def add_puzzle_to_db(data):
	client = MongoClient("mongodb://localhost:5000")
	database = "GameTest"
	collection = "puzzles"
	cursor = client[database]	
	collection = cursor[collection]
	response = collection.insert_many(generate_puzzle_data(data) for i in range(data['iteration']))
	client.close()
	print(response)

def generate_puzzle_data(data):
	dictionary = dict()
	dictionary['type'] = data['type']
	dictionary['difficulty'] = calc_difficulty(data['difficulty']) if type(data['difficulty']) is dict else data['difficulty'] 	
	dictionary.update(generate_puzzle(data['range'], data['operator']))
	return dictionary

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--type',action='store', default = "math",type=str)
	parser.add_argument('--range',action='store',type=str)
	parser.add_argument('--operators',action='store',default=0,type=str)
	parser.add_argument('--iter',action='store',default=50,type=int)
	parser.add_argument('--difficulty',action='store',type=int)
	args = parser.parse_args()
	data = dict()
	data['type'] = args.type
#	data['difficulty'] = {"6-7": "very easy", "8": "easy"}
	data['difficulty'] = args.difficulty
	data['range'] = list(map(int, args.range.split(',')))
	data['operator'] =  args.operators.split(',')
	data['iteration'] = args.iter
	add_puzzle_to_db(data)
	
