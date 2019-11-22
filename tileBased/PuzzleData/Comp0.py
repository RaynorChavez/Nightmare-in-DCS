import pickle
import os

CompName = 'Comp0'

PuzzleSolved = False

PuzzleLines = [ 'Test Line 1',
				'      Test Line 2',
				'          Test Line 3',
				':',
				'Test Line 5'
				]


PuzzleAnswer = [4,3,2,1,0]


def SaveMyState(screentext):
	with open('Comp0.pickle', 'wb') as f:
		pickle.dump(screentext, f)

def LoadMyMemories():
	screentext = []
	if os.path.exists("Comp0.pickle"):
		if os.path.getsize('Comp0.pickle') > 0:
			with open('Comp0.pickle', 'rb') as f:
				screentext = pickle.load(f)
	#print('screentext',screentext)
	return screentext
