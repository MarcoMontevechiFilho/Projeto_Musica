import funcoes as f
import random as r
from midiutil import MIDIFile

#ap.5 = apogiatura na quinta
#ap.3 = apogiatura na terça



class blues_arvore:
	def __init__(self):
		#a = r.choices(["Cb","C","C#","Db","D","D#","Eb","E","E#","Fb","F","F#","Gb","G","G#","Ab","A","A#","Bb","B","B#"])
		#self.tonica = f.notas[a]
		self.compassos = r.choices([8,12,16,20,24],[0,1,0,0,0]) #por enquanto, vou trabalhar com a forma básica 12 compassos
		progressao = []
		progressao.append(r.choices(["1","1maj7"],[0.9,0.1])[0])
		if progressao[0]=="1":
			progressao.append(r.choices(["1","4","7m7b5-37b9"],[0.7,0.2,0.1])[0]) 
		elif progressao[0]=="1maj7":
			progressao.append(r.choices(["7m7b5-37b9","4","1"],[0.8,0.1,0.1])[0])

		if progressao == ["1","1"] or progressao==["1","4"]:
			progressao.append(r.choices(["1","4","6m-2"],[0.94,0.03,0.03])[0])
		elif progressao[1] == ["7m7b5-37b9"]:
			progressao.append(r.choices(["6m-2","1","4"],[0.94,0.03,0.03])[0])
		elif progressao[0] == "1maj7" and progressao[1] != "7m7b5-37b9":
			progressao.append(r.choices(["1","6m-2"],[0.5,0.5])[0])


class cadeia_de_markov:
	def __init__(self,estados,probabilidades,alternancia="nao"):
		self.estados = estados
		self.alternancia = alternancia
		self.probabilidades = probabilidades
	

class blues_markov: #blues em cadeia de markov 
	def __init__(self, tonica=1, modo = 1):
		self.compassos = r.choices([8,12,16,20,24],[0,1,0,0,0]) #por enquanto, vou trabalhar com a forma básica 12 compassos
		progressao = r.choices(["blues basico"])[0] #vou adicionando variações conforme for terminando as anteriores
		prog = []
# Criando o vetor de interesse prog
		self.prog = f.escolha_progressao("blues")
		if tonica == 1:
			tonica = r.choices(list(f.notas))[0]	
		self.tonica = tonica
		if modo==1:
			modo = r.choices(list(f.dic_modos),[(1/3),(1/3),(1/3),0,0,0,0,0,0,0])[0]
		self.modo = modo
		self.escala = f.escala(self.tonica,self.modo)

		#marcação
#Criando o vetor de interesse chords
		chords = []
		contador = -1
		for i in self.prog:
			contador = contador+1  
			if contador == 0:       #se for a primeira interação, apenas escolhe entre menor e menor com apogiatura
				c = r.choices(["menor", "ap.5 menor"],[0.8,0.2])[0]
				chords.append(c)
				continue
			if i == "4":		#para o blues hexatonico, corrige o deslocamento da quarta
				i = "3"
			u=f.modos_da_triade(int(self.escala[int(i)-1]),self.tonica,self.modo)
			if "menor" in u and "diminuto" in u and "suspenso" in u and "suspenso diminuto" in u and len(u)==4:
				if "maior" in chords[len(chords)-1]:
					c = r.choices(["menor","diminuto","ap.5 menor"],[0.5,0.1,0.4])[0]
				elif "menor" in chords[len(chords)-1]:
					c = r.choices(["menor","diminuto","ap.5 menor"],[0.4,0.3,0.3])[0]
				elif "diminuto" in chords[len(chords)-1]:
					c = r.choices(["menor","diminuto","ap.5 menor"],[0.6,0.05,0.35])[0]
				elif "aumentado" in chords[len(chords)-1]:
					c = r.choices(["menor","diminuto","ap.5 menor"],[0.6,0.1,0.3])[0]
				elif chords[len(chords)-1] == "suspenso":
					c = r.choices(["menor","diminuto","ap.5 menor"],[0.5,0.1,0.4])[0]
			elif "maior" in u and "menor" in u and "suspenso" in u and len(u)==3:
				if "maior" in chords[len(chords)-1]:
					c = r.choices(["menor", "maior", "ap.3 menor"],[0.4,0.1,0.5])[0]
				elif "menor" in chords[len(chords)-1]:
					c = r.choices(["menor", "maior", "ap.3 menor"],[0.2,0.3,0.5])[0]
				elif "diminuto" in chords[len(chords)-1]:
					c = r.choices(["menor", "maior", "ap.3 menor"],[0.8,0.1,0.1])[0]
				elif "aumentado" in chords[len(chords)-1]:
					c = r.choices(["menor", "maior", "ap.3 menor"],[0.1,0.4,0.5])[0]
				elif chords[len(chords)-1] == "suspenso":
					c = r.choices(["menor", "maior", "ap.3 menor"],[0.8,0.1,0.1])[0]
			elif "suspenso" in u and len(u)==1:
				c = "suspenso"
			elif "suspenso diminuto" in u and len(u)==1:
				c = "suspenso diminuto"
			elif "suspenso aumentado" in u and len(u)==1:
				c = "suspenso aumentado"
			elif "suspenso" in u and "suspenso aumentado" in u and len(u)==2:
				if "maior" in chords[len(chords)-1]:
					c = r.choices(["suspenso", "suspenso aumentado"],[0.6,0.4])[0]
				elif "menor" in chords[len(chords)-1]:
					c = r.choices(["suspenso", "suspenso aumentado"],[0.9,0.1])[0]
				elif "diminuto" in chords[len(chords)-1]:
					c = r.choices(["suspenso", "suspenso aumentado"],[0.95,0.05])[0]
				elif "aumentado" in chords[len(chords)-1]:
					c = r.choices(["suspenso","suspenso aumentado"],[0.3,0.7])[0]
				elif chords[len(chords)-1] == "suspenso":
					c = r.choices(["suspenso","suspenso aumentado"],[0.3,0.7])[0]
			chords.append(c)
		self.chords = chords
#Criando o vetor de interesse acordes
		acordes = []
		w=0
		for i in self.prog:
			if i =="4":
				i = "3"
			if chords[w][:2]!="ap":
				a = f.triade(int(self.escala[int(i)-1])-24,chords[w])
			elif chords[w][:2]=="ap":
				a = f.triade(int(self.escala[int(i)-1])-24,chords[w][5:])
				if chords[w][:4]=="ap.3":
					a[1]=str(a[1])+"a"
				elif chords[w][:4]=="ap.5":
					a[2]=str(a[2])+"a"
			if f.pertence_a_tonalidade(a[0]+f.setim["maior"],self.tonica,self.modo)==True:
				a.append(a[0]+f.setim["maior"])
				acordes.append(a)
			else:
				if f.pertence_a_tonalidade(a[0]+f.setim["menor"],self.tonica,self.modo)==True:
					a.append(a[0]+f.setim["menor"])
					acordes.append(a)
				else:
					if f.pertence_a_tonalidade(a[0]+f.setim["diminuto"],self.tonica,self.modo)==True:
						a.append(a[0]+f.setim["diminuto"])
						acordes.append(a)
					else:
						if f.pertence_a_tonalidade(a[0]+f.setim["aumentado"],self.tonica,self.modo)==True:
							a.append(a[0]+f.setim["aumentado"])
							acordes.append(a)
			w=w+1

		self.acordes = acordes
#Criando o vetor de interesse voicings
		voicings = f.criar_voicing()
		xv = []
		for i in range(0,len(voicings)):
			xv.append(voicings[i])

		alterar_grupos = r.choices(["sim","nao"],[0.5,0.5])[0]
		if alterar_grupos=="sim":
			completamente = r.choices(["sim","nao"],[0.5,0.5])[0]
			if completamente=="nao":
				novo_voicing = []
				for i in range(0,len(voicings)-1):
					novo_voicing.append(voicings[i])
				novo_voicing1 = r.choices(["caminhante","poly","2-4","7-3"],[0.7,0.1,0.1,0.1])[0]
				novo_voicing2 = r.choices(["caminhante","poly","2-4","7-3"],[0.7,0.1,0.1,0.1])[0]
				novo_voicing3=[novo_voicing1,novo_voicing2]
				novo_voicing.append(novo_voicing3)
				self.voicings=voicings+voicings+novo_voicing
			elif completamente=="sim":
				novo_voicing = f.criar_voicing()
				self.voicings=voicings+voicings+novo_voicing
		elif alterar_grupos == "nao":
			self.voicings=voicings+voicings+voicings

# Criando o vetor de interesse baixo
		self.baixo = f.criar_baixo()
		alterar_grupos = r.choices(["sim","nao"],[0.5,0.5])[0]
		if alterar_grupos=="sim":
			completamente = r.choices(["sim","nao"],[0.5,0.5])[0]
			if completamente=="nao":
				novo_baixo = []
				for i in range(0,len(self.baixo)-2):
					novo_baixo.append(self.baixo[i])
				novo_baixo1 = r.choices(["1","153","135","153a","135a"],[0.4,0.2,0.2,0.1,0.1])[0]
				novo_baixo2 = r.choices(["1","153","135"],[0.4,0.3,0.3])[0]
				novo_baixo.append(novo_baixo1)
				novo_baixo.append(novo_baixo2)
				self.baixo = self.baixo+self.baixo+novo_baixo
			elif completamente=="sim":
				novo_baixo = f.criar_baixo()
				self.baixo=self.baixo+self.baixo+novo_baixo
		elif alterar_grupos == "nao":
			self.baixo=self.baixo+self.baixo+self.baixo

#criando o vetor de interesse linha de bateria

		self.linha_de_bateria=f.gerar_linha_de_bateria_2()


#Criando os vetores de interesse melodia e durações
		#melod = f.gerar_melodia_blues_hexatonico(self.tonica)
		#self.duracoes_melodia = melod["tempo"]
		#self.notas_melodia = melod["notas"]
		self.notas_melodia=[]
		self.duracoes_melodia=[]
		for i in range(0,12):
			a = f.gerar_melodia_blues_hexatonico(self.tonica,tonica_acorde=self.prog[i])
			self.notas_melodia=self.notas_melodia+a["notas"]
			self.duracoes_melodia=self.duracoes_melodia+a["tempo"]



			

#escrevendo e gravando o arquivo
	def escrever(self, nome_da_musica):  


		track = 0
		channel = 0
		if self.chords[0][:2]!="ap":
			time = 0
		elif self.chords[0][:2]=="ap":
			time = 4
		duration = 4
		#tempo = 140
		volume = 100
		self.apogi1 = r.choices([1,2],[0.7,0.3])[0]
		if self.apogi1 == 1:
			tempo = r.choices([140,150,160],[0.9/5,0.1,(4*0.9/5)])[0]
		elif self.apogi1 == 2:
			tempo = r.choices([140,150,160],[4*0.9/5,0.1,0.9/5])[0]
		MyMIDI = MIDIFile(1)
		MyMIDI.addTempo(track,time,tempo)

		for i in range(0,len(self.acordes)):
			vetor_mod_baixo = ["nao","nao","nao","nao","nao","nao","nao","nao","nao","nao","nao","nao"]
			for w in range(0,len(self.acordes)):
				if self.acordes[w][0]-12 < 28:
					self.acordes[w][0] = self.acordes[w][0]+12
					vetor_mod_baixo[w] = ["sim"]
			if self.chords[i][:2]=="ap":
				for k in range(0,len(self.acordes[i])):
					if type(self.acordes[i][k])==str:
						conv = int(self.acordes[i][k][:len(self.acordes[i][k])-1])
						if self.apogi1==1:
							MyMIDI.addNote(track,channel,conv-1,time+4*i-0.5,0.5,volume)
							MyMIDI.addNote(track,channel,conv,time+4*i,2,volume)

							MyMIDI.addNote(track,channel,conv-1,time+4*i+1.5,0.5,volume)
							MyMIDI.addNote(track,channel,conv,time+4*i+2,2,volume)
						elif self.apogi1==2:
							MyMIDI.addNote(track,channel,conv-1,time+4*i-0.5,0.5,volume)
							MyMIDI.addNote(track,channel,conv,time+4*i,2,volume)
							MyMIDI.addNote(track,channel,conv-2,time+4*i,2,volume)

							MyMIDI.addNote(track,channel,conv-1,time+4*i+1.5,0.5,volume)
							MyMIDI.addNote(track,channel,conv,time+4*i+2,2,volume)
							MyMIDI.addNote(track,channel,conv-2,time+4*i+2,2,volume)
					elif type(self.acordes[i][k])==int:
						if k != 0:
							MyMIDI.addNote(track,channel,self.acordes[i][k],time+4*i-0.5,2.5,volume)
						elif k == 0:
							if self.baixo[i] == "1":
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+2,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+3,1,volume)
							elif self.baixo[i] == "135":
								if self.prog[i] == "1":
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(3-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(7-12),time+4*i+3,1,volume)
								elif self.prog[i] == "4":
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(5-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(7-12),time+4*i+3,1,volume)
								elif self.prog[i] == "5":
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(3-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(5-12),time+4*i+3,1,volume)
							elif self.baixo[i] == "153":
								if self.prog[i] == "1":
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(7-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(3-12),time+4*i+3,1,volume)
								elif self.prog[i] == "4":
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(7-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(5-12),time+4*i+3,1,volume)
								elif self.prog[i] == "5":
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(5-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(3-12),time+4*i+3,1,volume)
							elif self.baixo[i] == "153a":
								if i == 11:
									MyMIDI.addNote(track,channel+1,self.acordes[0][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[0][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[0][k]+(7-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[0][k]+(3-12),time+4*i+3,1,volume)
								elif i < 11:
									if self.prog[i+1] == "1":
										MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(7-12),time+4*i+2,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(3-12),time+4*i+3,1,volume)
									elif self.prog[i+1] == "4":
										MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(7-12),time+4*i+2,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(5-12),time+4*i+3,1,volume)
									elif self.prog[i+1] == "5":
										MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(5-12),time+4*i+2,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(3-12),time+4*i+3,1,volume)

							elif self.baixo[i] == "135a":
								if i == 1:
									MyMIDI.addNote(track,channel+1,self.acordes[0][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[0][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[0][k]+(3-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[0][k]+(7-12),time+4*i+3,1,volume)
								elif i < 11:
									if self.prog[i+1] == "1":
										MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(3-12),time+4*i+2,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(7-12),time+4*i+3,1,volume)
									elif self.prog[i+1] == "4":
										MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(5-12),time+4*i+2,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(7-12),time+4*i+3,1,volume)
									elif self.prog[i+1] == "5":
										MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(3-12),time+4*i+2,1,volume)
										MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(5-12),time+4*i+3,1,volume)



			elif self.chords[i][:2]!="ap":
				for k in range(0,len(self.acordes[i])):
					if k == 0:
						if self.baixo[i] == "1":
							MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
							MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
							MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+2,1,volume)
							MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+3,1,volume)
						elif self.baixo[i] == "135":
							if self.prog[i] == "1":
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(3-12),time+4*i+2,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(7-12),time+4*i+3,1,volume)
							elif self.prog[i] == "4":
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(5-12),time+4*i+2,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(7-12),time+4*i+3,1,volume)
							elif self.prog[i] == "5":
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(3-12),time+4*i+2,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(5-12),time+4*i+3,1,volume)
								
						elif self.baixo[i] == "153":
							if self.prog[i] == "1":
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(7-12),time+4*i+2,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(3-12),time+4*i+3,1,volume)
							elif self.prog[i] == "4":
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(7-12),time+4*i+2,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(5-12),time+4*i+3,1,volume)
							elif self.prog[i] == "5":
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(5-12),time+4*i+2,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[i][k]+(3-12),time+4*i+3,1,volume)
						elif self.baixo[i] == "135a":
							if i == 11:
								MyMIDI.addNote(track,channel+1,self.acordes[0][k]-12,time+4*i,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[0][k]-12,time+4*i+1,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[0][k]+(3-12),time+4*i+2,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[0][k]+(7-12),time+4*i+3,1,volume)
							elif i < 11:
								if self.prog[i+1] == "1":
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(3-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(7-12),time+4*i+3,1,volume)
								elif self.prog[i+1] == "4":
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(5-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(7-12),time+4*i+3,1,volume)
								elif self.prog[i+1] == "5":
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(3-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(5-12),time+4*i+3,1,volume)
						elif self.baixo[i] == "153a":
							if i == 11:
								MyMIDI.addNote(track,channel+1,self.acordes[0][k]-12,time+4*i,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[0][k]-12,time+4*i+1,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[0][k]+(7-12),time+4*i+2,1,volume)
								MyMIDI.addNote(track,channel+1,self.acordes[0][k]+(3-12),time+4*i+3,1,volume)
							elif i < 11:
								if self.prog[i+1] == "1":
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(7-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(3-12),time+4*i+3,1,volume)
								elif self.prog[i+1] == "4":
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(7-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(5-12),time+4*i+3,1,volume)
								elif self.prog[i+1] == "5":
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i][k]-12,time+4*i+1,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(5-12),time+4*i+2,1,volume)
									MyMIDI.addNote(track,channel+1,self.acordes[i+1][k]+(3-12),time+4*i+3,1,volume)

					elif k != 0:
						MyMIDI.addNote(track,channel,self.acordes[i][k],time+4*i,2,volume)

						MyMIDI.addNote(track,channel,self.acordes[i][k],time+4*i+2,2,volume)
			for w in range(0,len(self.acordes)):
				if vetor_mod_baixo[w] == "sim":
					self.acordes[w][0] = self.acordes[w][0]-12
					vetor_mod_baixo[w] = "nao"
		
			#for w in range(0,len(self.linha_de_bateria[i])):
				#if type(self.linha_de_bateria[i][w]) == str:
					#if self.linha_de_bateria[i][w] == "n":
						#continue
					#else:
						#MyMIDI.addNote(track,9,int(self.linha_de_bateria[i][w]),time+4*i+w,0.5,volume)
						#MyMIDI.addNote(track,9,int(self.linha_de_bateria[i][w]),time+4*i+w+0.5,0.5,volume)
				#elif type(self.linha_de_bateria[i][w]) == int:
					#MyMIDI.addNote(track,9,self.linha_de_bateria[i][w],time+4*i+w,1,volume)


		for i in range(0,len(self.linha_de_bateria)):
			if type(self.linha_de_bateria[i])==int:
				MyMIDI.addNote(track,9,self.linha_de_bateria[i],time+0.5*i,0.5,volume)
			elif type(self.linha_de_bateria[i])==list:
				for k in range(0,len(self.linha_de_bateria[i])):
					MyMIDI.addNote(track,9,self.linha_de_bateria[i][k],time+0.5*i,0.5,volume)

		contador_de_tempo = 0
		self.trocar_instrumento = r.choices(["nenhum","guitarra","acordeao"],[0.5,0.25,0.25])[0]
		for i in range(0,len(self.notas_melodia)):
			vetor_soma = []
			for k in range(0,i):
				vetor_soma.append(self.duracoes_melodia[k])
			if sum(vetor_soma) <16:
				canal_melod = 0
			elif sum(vetor_soma) >= 16 and sum(vetor_soma) < 32:
				canal_melod = 2
			elif sum(vetor_soma) >= 32:
				canal_melod = 0
			
			if self.trocar_instrumento == "nenhum":
				canal_melod = 0

			#MyMIDI.addNote(track,0,self.notas_melodia[i],time+0.5*i,self.duracoes_melodia[i],volume)
			if type(self.notas_melodia[i])==int:
				variavel_dispensavel = self.notas_melodia[i]
			elif type(self.notas_melodia[i])==list:
				variavel_dispensavel = self.notas_melodia[i][0]
			if f.qualnota(variavel_dispensavel) == f.qualnota(self.escala[3]):
				trocar = r.choices(["sim","nao"],[0.5,0.5])[0]
				if trocar == "sim":
					if self.apogi1 == 1:
						if type(self.notas_melodia[i])==int:
							dur = self.duracoes_melodia[i]
							MyMIDI.addNote(track,canal_melod,self.notas_melodia[i],time+contador_de_tempo,dur/4,volume)
							MyMIDI.addNote(track,canal_melod,self.notas_melodia[i]+1,time+contador_de_tempo+dur/4,self.duracoes_melodia[i]+dur*(3/4),volume)
						elif type(self.notas_melodia[i])==list:
							dur = self.duracoes_melodia[i]
							MyMIDI.addNote(track,0,self.notas_melodia[i][1],time+contador_de_tempo,dur,volume)
							MyMIDI.addNote(track,canal_melod,self.notas_melodia[i][0],time+contador_de_tempo,dur/4,volume)
							MyMIDI.addNote(track,canal_melod,self.notas_melodia[i][0]+1,time+contador_de_tempo+dur/4,self.duracoes_melodia[i]+dur*(3/4),volume)
					elif self.apogi1 == 2:
						if type(self.notas_melodia[i])==int:
							dur = self.duracoes_melodia[i]
							MyMIDI.addNote(track,canal_melod,self.notas_melodia[i],time+contador_de_tempo,dur/4,volume)
							MyMIDI.addNote(track,canal_melod,self.notas_melodia[i]+1,time+contador_de_tempo+dur/4,self.duracoes_melodia[i]+dur*(3/4),volume)
							MyMIDI.addNote(track,canal_melod,self.notas_melodia[i]-1,time+contador_de_tempo+dur/4,self.duracoes_melodia[i]+dur*(3/4),volume)
						elif type(self.notas_melodia[i])==list:
							dur = self.duracoes_melodia[i]
							MyMIDI.addNote(track,0,self.notas_melodia[i][1],time+contador_de_tempo,dur,volume)
							MyMIDI.addNote(track,canal_melod,self.notas_melodia[i][0],time+contador_de_tempo,dur/4,volume)
							MyMIDI.addNote(track,canal_melod,self.notas_melodia[i][0]+1,time+contador_de_tempo+dur/4,self.duracoes_melodia[i]+dur*(3/4),volume)
							MyMIDI.addNote(track,canal_melod,self.notas_melodia[i][0]-1,time+contador_de_tempo+dur/4,self.duracoes_melodia[i]+dur*(3/4),volume)


					contador_de_tempo=self.duracoes_melodia[i]+contador_de_tempo
				elif trocar == "nao":
					if type(self.notas_melodia[i])==int:
						MyMIDI.addNote(track,canal_melod,self.notas_melodia[i],time+contador_de_tempo,self.duracoes_melodia[i],volume)
						contador_de_tempo=self.duracoes_melodia[i]+contador_de_tempo
					elif type(self.notas_melodia[i])==list:
						MyMIDI.addNote(track,canal_melod,self.notas_melodia[i][0],time+contador_de_tempo,self.duracoes_melodia[i],volume)
						MyMIDI.addNote(track,0,self.notas_melodia[i][1],time+contador_de_tempo,self.duracoes_melodia[i],volume)
						contador_de_tempo=self.duracoes_melodia[i]+contador_de_tempo
			else:
				if type(self.notas_melodia[i])==int:
					MyMIDI.addNote(track,canal_melod,self.notas_melodia[i],time+contador_de_tempo,self.duracoes_melodia[i],volume)
					contador_de_tempo=self.duracoes_melodia[i]+contador_de_tempo
				elif type(self.notas_melodia[i])==list:
					MyMIDI.addNote(track,canal_melod,self.notas_melodia[i][0],time+contador_de_tempo,self.duracoes_melodia[i],volume)
					MyMIDI.addNote(track,0,self.notas_melodia[i][1],time+contador_de_tempo,self.duracoes_melodia[i],volume)
					contador_de_tempo=self.duracoes_melodia[i]+contador_de_tempo

		MyMIDI.addProgramChange(0, 0,0,0)
		MyMIDI.addProgramChange(0, 1,0,34)
		if self.trocar_instrumento == "guitarra":
			MyMIDI.addProgramChange(0,2,0,25)
		elif self.trocar_instrumento == "acordeao":
			MyMIDI.addProgramChange(0,2,0,22)

		with open(nome_da_musica+".mid","wb") as output_file:
			MyMIDI.writeFile(output_file)


		arq = open(nome_da_musica+".txt","w+")
		t1 = str(self.tonica)
		t2 = str(self.modo)
		t3 = str(self.prog)
		t4 = str(self.chords)
		t5 = str(self.voicings)
		t6 = str(self.baixo)
		t7 = str(self.linha_de_bateria)
		t9 = str(self.acordes)
		t10 = str(self.notas_melodia)
		t11 = str(self.duracoes_melodia)
		arq.write("Tonica:" + t1)
		arq.write("\n")
		arq.write("Modo:" + t2)
		arq.write("\n")
		arq.write("Progressão:" + t3)
		arq.write("\n")
		arq.write("Modos:" + t4)
		arq.write("\n")
		arq.write("Voicings:" + t5)
		arq.write("\n")
		arq.write("Baixo:" + t6)
		arq.write("\n")
		arq.write("Bateria: " +t7)
		arq.write("\n")
		arq.write("Numeros dos acordes: " +t9)
		arq.write("\n")
		arq.write("Melodia: " +t10)
		arq.write("\n")
		arq.write("Duracoes_melodia: " +t11)
		arq.close()

