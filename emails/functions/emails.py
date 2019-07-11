import pandas as pd
import numpy as np
import re


def read_csv(filepath):
	df = pd.read_csv(filepath)

	return df.columns


def process_file(input_file, email_col):
	df = pd.read_csv(input_file)

	df['verified'] = df[email_col].apply(verify_email)

	df.to_csv("data/output.csv", index=False)

	return 1




def verify_email(email_str):
	pattern = r'''([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|"([]!#-[^-~ \t]|(\\[\t -~]))+")@[0-9A-Za-z]([0-9A-Za-z-]{0,61}[0-9A-Za-z])?(\.[0-9A-Za-z]([0-9A-Za-z-]{0,61}[0-9A-Za-z])?)+'''
	pattern = re.compile(pattern)

	if not re.match(pattern, email_str):
		return -1
	else:
		return 1