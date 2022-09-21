import functions as f, variables as v, classes as c;


if __name__=='__main__':
	f.initialize();
	while True:
			statement = f.takeCommand().lower();
			if statement != "null":
				# If the keyword is not spoken - comprehend what command is nessesary
				if v.active:
					f.comprehend(statement);
					f.toggleActive(False);
				else:
					# If the keyword is spoken - activate the AI
					if v.keyword in statement:
						v.statusWindow.configure(bg=v.statusbar_Listening);
						f.toggleActive(True);
						statement = statement.replace(v.keyword, '');
						# If the statement is still going - comprehend what command is nessesary
						if(len(statement)>5):
							f.comprehend(statement);
							f.toggleActive(False);
			continue;