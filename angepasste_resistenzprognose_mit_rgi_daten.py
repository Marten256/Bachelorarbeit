import pandas as pd
from os import listdir
import os

#in Verzeichnis "Verzeichnis2+'Gene_list/'" müssen die Listen (.csv) hinterlegt sein, so wie sie auch auf GitHub benannt sind.

Verzeichnis = '/homes/marten/Schreibtisch/Coli2MARTEN/' #Verzeichnis in dem ein Ordner für jeden Stamm ist und die RGI Daten in der Form Ordnername.json und Ordnername.txt vorliegen
Verzeichnis2 = '/homes/marten/Schreibtisch/Test_rgi/' #Verzeichnis in dem Kombinierte Daten gespeichert werden sollen

if not os.path.exists(Verzeichnis2 + 'Combined'): #Verzeichnise werden erstellt
	os.makedirs(Verzeichnis2 + 'Combined')
if not os.path.exists(Verzeichnis2 + 'Combined/rgi'): 
	os.makedirs(Verzeichnis2 + 'Combined/rgi')
if not os.path.exists(Verzeichnis2 + 'Combined/rgi/Vergleich'): 
	os.makedirs(Verzeichnis2 + 'Combined/rgi/Vergleich')

#RGI Daten kompakter

liste = sorted(listdir(Verzeichnis)) 
for m in liste:
	df = pd.read_csv(Verzeichnis+m+'/'+m+'.txt', delimiter='	') #RGI Datei
	with open(Verzeichnis+m+'/rgi_gen_mode_class_mechanism_family_'+m+'.txt', 'w+') as fp:
		fp.write('Resistance Gene	Model_type	Drug Class	Resistance Mechanism	AMR Gene Family' + '\n')
		for i in range(0, len(df['Model_type'])):
			fp.write(df['Best_Hit_ARO'][i] + '	' + df['Model_type'][i] + '	' + df['Drug Class'][i] + '	' + df['Resistance Mechanism'][i] + '	' + df['AMR Gene Family'][i] + '\n')
			

#Genen, die ein Stamm besitzt, die Resistenzen zuordnen, sowie bestimmen, welche Efflux Pumpen vorliegen.

liste = sorted(listdir(Verzeichnis))
dg = pd.read_csv(Verzeichnis2+'Gene_list/resistance_genes+resistances+beta-lactamase.csv', delimiter='	', header = None)
dp = pd.read_csv(Verzeichnis2+'Gene_list/efflux_pumps+component+regulators+resistances.csv', delimiter='	')
for m in liste:
	df = pd.read_csv(Verzeichnis+m+'/rgi_gen_mode_class_mechanism_family_'+m+'.txt', delimiter='	')
	with open(Verzeichnis+m+'/genes_resistances_efflux_resistances_with_beta-lactamase.txt', 'w+') as fp:
		fp.write('Resistance Gene	Resistance	Beta-Lactamase?' + '\n')
		for i in range(0, len(dg)):
			if dg[0][i] in list(df['Resistance Gene']):
				fp.write(str(dg[0][i]) + '	' + str(dg[1][i]) + '	')
				if dg[2][i] == 'beta-lactamase':
					fp.write('Yes' + '\n')
				else:
					fp.write('\n')
		fp.write('\n' + 'Efflux Pump/Efflux Gene	Resistance	Regulators' + '\n')
		for i in range(0, len(dp)):
			a = str(dp['Components'][i]).split(';')
			b = 0
			for k in range(0, len(a)):
				if a[k] in list(df['Resistance Gene']):
					b = b+1
			c = str(dp['Regulators'][i]).split(';')
			d = []
			
			for k in range(0, len(c)):
				if c[k] in list(df['Resistance Gene']):
					d.append(c[k])
				else:
					for l in range(0, len(dp['Efflux pump'])):
						if c[k] == dp['Efflux pump'][l]:
							e = str(dp['Components'][l]).split(';')
							f = 0
							for n in range(0, len(e)):
								if e[n] in list(df['Resistance Gene']):
									f = f+1
							if f == len(e):
								g = str(c[k]) + '(' + str(dp['Components'][l]) + ')'
								d.append(g)
			if b == len(a):
				fp.write(str(dp['Efflux pump'][i]) + '	' + str(dp['Resistances'][i]) + '	')
				for k in range(0, len(d)):
					fp.write(str(d[k]))
					if k < len(d)-1:
						fp.write(';')
				fp.write('\n')
				

#Vergleich der Klinikdaten mit den Resistenzprognosen

liste = sorted(listdir(Verzeichnis))
for m in liste:
	df = pd.read_csv(Verzeichnis + m + '/Resistenzen_Kliniken_Langnamen_' + m + '.txt', delimiter='	')
	dg = pd.read_csv(Verzeichnis + m + '/genes_resistances_efflux_resistances_with_beta-lactamase.txt', delimiter='	')
	with open(Verzeichnis + m + '/Vergleich_Klinik_CARD_with_beta-lactamase_' + m + '.txt', 'w+') as fp:
		fp.write('RESISTANCE	Bestätigung/Fehler' + '\n')
		for i in range(0, len(df['RESISTANCE'])):
			if df['RESISTANCE'][i] == 'MEDIATE':
				b = i
			if df['RESISTANCE'][i] == 'SENSITIVE':
				c = i
		for i in range(0, b):
			d = 0
			y = 0
			e = df['RESISTANCE'][i]
			f = len(e)
			if e[f-1:] == ' ':
				e = e[:f-1]
			for k in range(0, len(dg['Resistance'])):
				a = str(dg['Resistance'][k]).split(';')
				if e in list(a):
					d = d+1
				if '-' in e:
					x = []
					x = e.split('-')
					if x[1] == 'sulfamethoxazole':
						if x[0] in list(a):
							d = d+1
						if x[1] in list(a):
							y = y+1
					else:
						if dg['Beta-Lactamase?'][k] != 'Yes':
							if x[0] in list(a):
								d = d+1
			if d == 0:
				fp.write(df['RESISTANCE'][i] + '	Resistenz wurde nicht bestätigt' + '\n')
			elif d != 0 and y != 0:
				fp.write(df['RESISTANCE'][i] + '	Resistenz durch ' + str(d) + '/' + str(y) + ' Gene bestätigt' + '\n')
			else:
				fp.write(df['RESISTANCE'][i] + '	Resistenz durch ' + str(d) + ' Gene bestätigt' + '\n')
				
		fp.write('\n' + 'MEDIATE	Bestätigung/Fehler' + '\n')
		for i in range(b+1, c):
			d = 0
			y = 0
			e = df['RESISTANCE'][i]
			f = len(e)
			if e[f-1:] == ' ':
				e = e[:f-1]
			for k in range(0, len(dg['Resistance'])):
				a = str(dg['Resistance'][k]).split(';')
				if e in list(a):
					d = d+1
				if '-' in e:
					x = []
					x = e.split('-')
					if x[1] == 'sulfamethoxazole':
						if x[0] in list(a):
							d = d+1
						if x[1] in list(a):
							y = y+1
					else:
						if dg['Beta-Lactamase?'][k] != 'Yes':
							if x[0] in list(a):
								d = d+1
			if d == 0:
				fp.write(df['RESISTANCE'][i] + '	mediäres Verhalten wurde nicht bestätigt' + '\n')
			elif d != 0 and y != 0:
				fp.write(df['RESISTANCE'][i] + '	mediäres Verhalten durch ' + str(d) + '/' + str(y) + ' Gene bestätigt' + '\n')
			else:
				fp.write(df['RESISTANCE'][i] + '	mediäres Verhalten durch ' + str(d) + ' Gene bestätigt' + '\n')
		fp.write('\n' + 'SENSITIVE	Bestätigung/Fehler' + '\n')
		for i in range(c+1, len(df['RESISTANCE'])):
			d = 0
			y = 0
			e = df['RESISTANCE'][i]
			f = len(e)
			if e[f-1:] == ' ':
				e = e[:f-1]
			for k in range(0, len(dg['Resistance'])):
				a = str(dg['Resistance'][k]).split(';')
				if e in list(a):
					d = d+1
				if '-' in e:
					x = []
					x = e.split('-')
					if x[1] == 'sulfamethoxazole':
						if x[0] in list(a):
							d = d+1
						if x[1] in list(a):
							y = y+1
					else:
						if dg['Beta-Lactamase?'][k] != 'Yes':
							if x[0] in list(a):
								d = d+1
			if d == 0:
				fp.write(df['RESISTANCE'][i] + '	sensitives Verhalten wurde bestätigt, kein Resistenz Gen vorhanden' + '\n')
			elif d != 0 and y != 0:
				fp.write(df['RESISTANCE'][i] + '	sensitivem Verhalten widersprechen ' + str(d) + '/' + str(y) + ' Gene' + '\n')
			else:
				fp.write(df['RESISTANCE'][i] + '	sensitivem Verhalten widersprechen ' + str(d) + ' Gene' + '\n')
	

#Zusammenfassen der Vergleiche mit den Klinikdaten zum ploten mit R			
				
liste = sorted(listdir(Verzeichnis))
a = []
b = []
x = []
with open(Verzeichnis2+'Combined/rgi/Vergleich/übereinstimmung_und_widerspruch_beim_vergleich_RGI2_Resistance_R.txt', 'w+') as fp:
	fp.write('RESISTANCE Antibiotics	Quantity	Übereinstimmung(1)/Wiederspruch(2)' + '\n')
	
	for m in liste:
		dg = pd.read_csv(Verzeichnis + m + '/Vergleich_Klinik_CARD_with_beta-lactamase_' + m +'.txt', delimiter='	')
		for i in range(0, len(dg)):
			if 'Resistenz durch ' in dg['Bestätigung/Fehler'][i]:
				c = 0
				for k in range(0, len(a)):
					if dg['RESISTANCE'][i] == a[k]:
						b[k] = b[k]+1
					else:
						c = c+1
				if c == len(a):
					a.append(dg['RESISTANCE'][i])
					b.append(1)
					x.append(0)
					
			if dg['Bestätigung/Fehler'][i]	== 'Resistenz wurde nicht bestätigt':
				c = 0
				for k in range(0, len(a)):
					if dg['RESISTANCE'][i] == a[k]:
						x[k] = x[k]+1
					else:
						c = c+1
				if c == len(a):
					a.append(dg['RESISTANCE'][i])
					x.append(1)
					b.append(0)
					
	for i in range(0, len(a)):
		fp.write(a[i] + '	' + str(b[i]) + '	' + 'True' + '\n' + a[i] + '	' + str(x[i]) + '	' + 'False' + '\n')
	
with open(Verzeichnis2+'Combined/rgi/Vergleich/übereinstimmung_und_widerspruch_beim_vergleich_RGI2_Mediate_R.txt', 'w+') as fp:
	fp.write('MEDIATE Antibiotics	Quantity	Übereinstimmung(1)/Wiederspruch(2)' + '\n')
	a = []
	b = []
	x = []
	for m in liste:
		dg = pd.read_csv(Verzeichnis + m + '/Vergleich_Klinik_CARD_with_beta-lactamase_' + m +'.txt', delimiter='	')
		for i in range(0, len(dg)):
			if 'mediäres Verhalten durch ' in dg['Bestätigung/Fehler'][i]:
				c = 0
				for k in range(0, len(a)):
					if dg['RESISTANCE'][i] == a[k]:
						b[k] = b[k]+1
					else:
						c = c+1
				if c == len(a):
					a.append(dg['RESISTANCE'][i])
					b.append(1)
					x.append(0)
					
			if dg['Bestätigung/Fehler'][i]	== 'mediäres Verhalten wurde nicht bestätigt':
				c = 0
				for k in range(0, len(a)):
					if dg['RESISTANCE'][i] == a[k]:
						x[k] = x[k]+1
					else:
						c = c+1
				if c == len(a):
					a.append(dg['RESISTANCE'][i])
					x.append(1)
					b.append(0)
				
	for i in range(0, len(a)):
		fp.write(a[i] + '	' + str(b[i]) + '	' + 'True' + '\n' + a[i] + '	' + str(x[i]) + '	' + 'False' + '\n')
	
with open(Verzeichnis2+'Combined/rgi/Vergleich/übereinstimmung_und_widerspruch_beim_vergleich_RGI2_Sensitive_R.txt', 'w+') as fp:
	fp.write('SENSITIVE Antibiotics	Quantity	Übereinstimmung(1)/Wiederspruch(2)' + '\n')
	a = []
	b = []
	x = []
	for m in liste:
		dg = pd.read_csv(Verzeichnis + m + '/Vergleich_Klinik_CARD_with_beta-lactamase_' + m +'.txt', delimiter='	')
		for i in range(0, len(dg)):
			if 'sensitives Verhalten wurde bestätigt, kein Resistenz Gen vorhanden' in dg['Bestätigung/Fehler'][i]:
				c = 0
				for k in range(0, len(a)):
					if dg['RESISTANCE'][i] == a[k]:
						b[k] = b[k]+1
					else:
						c = c+1
				if c == len(a):
					a.append(dg['RESISTANCE'][i])
					b.append(1)
					x.append(0)
					
			if 'sensitivem Verhalten widersprechen' in dg['Bestätigung/Fehler'][i]:
				c = 0
				for k in range(0, len(a)):
					if dg['RESISTANCE'][i] == a[k]:
						x[k] = x[k]+1
					else:
						c = c+1
				if c == len(a):
					a.append(dg['RESISTANCE'][i])
					x.append(1)
					b.append(0)
					
	for i in range(0, len(a)):
		fp.write(a[i] + '	' + str(b[i]) + '	' + 'True' + '\n' + a[i] + '	' + str(x[i]) + '	' + 'False' + '\n')
		
		
#Für die Zusammenfassung von Fällen mit resistenten und sensitiven Verhalten. Auch fürs ploten mit R		


liste = sorted(listdir(Verzeichnis))
a = []
b = []
x = []
with open(Verzeichnis2+'Combined/rgi/Vergleich/übereinstimmung_und_widerspruch_beim_vergleich_RGI2_Resistance_R_r_s_vergleich.txt', 'w+') as fp:
	fp.write('RESISTANCEorSENSITIV	Quantity	True/False positive/negative' + '\n')
	
	for m in liste:
		dg = pd.read_csv(Verzeichnis + m + '/Vergleich_Klinik_CARD_with_beta-lactamase_' + m +'.txt', delimiter='	')
		for i in range(0, len(dg)):
			if 'Resistenz durch ' in dg['Bestätigung/Fehler'][i]:
				c = 0
				for k in range(0, len(a)):
					if dg['RESISTANCE'][i] == a[k]:
						b[k] = b[k]+1
					else:
						c = c+1
				if c == len(a):
					a.append(dg['RESISTANCE'][i])
					b.append(1)
					x.append(0)
					
			if dg['Bestätigung/Fehler'][i]	== 'Resistenz wurde nicht bestätigt':
				c = 0
				for k in range(0, len(a)):
					if dg['RESISTANCE'][i] == a[k]:
						x[k] = x[k]+1
					else:
						c = c+1
				if c == len(a):
					a.append(dg['RESISTANCE'][i])
					x.append(1)
					b.append(0)
					
	for i in range(0, len(a)):
		fp.write(a[i] + '	' + str(b[i]) + '	' + 'True positive' + '\n' + a[i] + '	' + str(x[i]) + '	' + 'False negative' + '\n')
	
	
	a = []
	b = []
	x = []
	for m in liste:
		dg = pd.read_csv(Verzeichnis + m + '/Vergleich_Klinik_CARD_with_beta-lactamase_' + m +'.txt', delimiter='	')
		for i in range(0, len(dg)):
			if 'sensitives Verhalten wurde bestätigt, kein Resistenz Gen vorhanden' in dg['Bestätigung/Fehler'][i]:
				c = 0
				for k in range(0, len(a)):
					if dg['RESISTANCE'][i] == a[k]:
						b[k] = b[k]+1
					else:
						c = c+1
				if c == len(a):
					a.append(dg['RESISTANCE'][i])
					b.append(1)
					x.append(0)
					
			if 'sensitivem Verhalten widersprechen' in dg['Bestätigung/Fehler'][i]:
				c = 0
				for k in range(0, len(a)):
					if dg['RESISTANCE'][i] == a[k]:
						x[k] = x[k]+1
					else:
						c = c+1
				if c == len(a):
					a.append(dg['RESISTANCE'][i])
					x.append(1)
					b.append(0)
					
	for i in range(0, len(a)):
		fp.write(a[i] + '	' + str(b[i]) + '	' + 'True negative' + '\n' + a[i] + '	' + str(x[i]) + '	' + 'False positive' + '\n')
