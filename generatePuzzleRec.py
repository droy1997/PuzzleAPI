import random
import math
import argparse

operators = ['+','-','*','/']

def divisors(number):
	list_div = []
	for i in range(2, math.floor(number/2)):
		if number%i == 0:
			list_div.append(str(i))
	return list_div

def split_number(number,step, operators):
	if step>=1:
		operator = random.choice(operators)
		if (operator == '*' or operator == '/') and step!=1:
			operator = random.choice(['+','-'])
		if operator == '*' and number>3:
			divisors_list = divisors(number)
			if len(divisors_list) == 0:
				return str(number)
			else:
				num1 = int(random.choice(divisors_list))
				num2 = int(number/num1)
				return str(num2) + " x " + str(num1)
		elif operator == "/" and number>=2:
			num1 = random.randint(2,number)
			num2 = number*num1
			return str(num2) + " / " + str(num1)
		elif operator == "+" and int(number/(step+1)) > 1:
			num1 = random.randint(1, int(number/(step+1)))
			num2 = number - num1
			if step == 1:
				return str(num1) + " + " + str(num2)
			else:
				return str(num1) + " + " + split_number(num2,step-1)
		elif operator == "-":
			num1 = random.randint(number+1, 2*number)
			num2 = num1 - number
			if step == 1:
				return str(num1) + " - " + str(num2)
			else:
				return split_number(num1,step-1) + " - " + str(num2)
		else:
			return str(number)
	else:
		return str(number)

def generate_options(ans_range, correct_answer, no_options):
	opt_list = [str(correct_answer)]
	while no_options>1:
		option = random.randint(int(ans_range[0]), int(ans_range[1]))
		if str(option) not in opt_list:
			opt_list.append(str(option))
			no_options-=1
	random.shuffle(opt_list)
	idx = opt_list.index(str(correct_answer))
	return opt_list, idx

def generate_puzzle(ans_range,operators, ques_operators=1,ans_operators=0,options=4):
	data = dict()
	num = random.randint(int(ans_range[0]),int(ans_range[1]))
	ques_str = split_number(num, ques_operators, operators)
	while ques_str == str(num):
		ques_str = split_number(num, ques_operators, operators)
	ques_str+= " = _"
	
	if ans_operators==0:
		ans_list, correct_idx = generate_options(ans_range, num, options)
		data["question"] = ques_str
		data["options"] = ans_list
		data["answer"] = correct_idx
	return data

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--operators',action='store',type=str)
	parser.add_argument('--ans_range',action='store',type=str)
	parser.add_argument('--ques_operators',action='store',default=1,type=int)
	parser.add_argument('--ans_operators',action='store',default=0,type=int)
	parser.add_argument('--options',action='store',default=4,type=int)
	parser.add_argument('--iter',action='store',default=1,type=int)
	args = parser.parse_args()
	
	operators = args.operators.split(',')
	ans_range = args.ans_range.split(',')
	for i in range(args.iter):
		num = random.randint(int(ans_range[0]),int(ans_range[1]))
		ques_str = split_number(num, args.ques_operators, args.operators)
		if args.ans_operators == 0:
			ques_str= ques_str + " = _"
			ans_list, correct_idx = generate_options(ans_range, num, args.options)
			print(ques_str +"\t\t"+ str(ans_list)+ "\t"+str(correct_idx))
			
