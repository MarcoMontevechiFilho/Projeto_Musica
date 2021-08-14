notas = {"Cb":59, "C":60, "C#":61, "Db":61, "D":62, "D#":63, "Eb":63, "E":64, "E#":65, "Fb":64, "F":65, "F#":66, "Gb":66, "G":67, "G#":68, "Ab":68, "A":69, "A#":70, "Bb":70, "B":71, "B#":72}
setim = {"maior":11, "aumentado":12, "menor":10, "diminuto":9}
dic_modos = {"blues hexatonico":[3,2,1,1,3,2],"blues heptatonico":[2,1,2,1,3,1,2],"blues nonatonico":[2,1,1,1,2,2,1,1,1],"maior":[2,2,1,2,2,2,1], "menor":[2,1,2,2,1,2,2], "dorico":[2,1,2,2,2,1,2], "frigio":[1,2,2,2,1,2,2], "lidio":[2,2,2,1,2,2], "mixolidio":[2,2,1,2,2,1,2],"locrio":[1,2,2,1,2,2,2]}
modos_triades = {"maior":[4,7] , "aumentado":[4,8], "menor":[3,7], "diminuto":[3,6], "suspenso":[7], "sus diminuto":[6], "sus aumentado":[8]}
import random as r
#consertar blues menor
#blues maior = blues menor com penúltimo intervalo meio tom abaixo
#Resolver o problema do contraponto
#Transformar a ordem lexicográfica em uma cadeia de Markov

class cadeia_de_markov:
	def __init__(self,estados,probabilidades,alternancia="nao"):
		self.estados = estados
		self.alternancia = alternancia
		self.probabilidades = probabilidades

	

def markov(cadeia,estado,alterna=0):
	indice = cadeia.estados.index(estado)
	if cadeia.alternancia == "nao":
		prob = []
		for i in range(0,len(cadeia.probabilidades)):
			prob.append(cadeia.probabilidades[i][indice])
		resultado = r.choices(cadeia.estados,prob)[0]
	
	elif cadeia.alternancia == "sim":
		prob = []
		for i in range(0,len(cadeia.probabilidades[alterna-1])):
			prob.append(cadeia.probabilidades[alterna-1][i][indice])
		resultado = r.choices(cadeia.estados,prob)[0]
		
	return(resultado)
	


def nota(n, qual="todas"):  #traduz as notas em números MIDI
	if n == str(n):
		n = notas[n]
	i = []
	c = n
	while c < 128:
		i.append(c)
		c = c+12
	c = n-12
	while c >-1:
		i.append(c)
		c = c-12
	i.sort()
	if qual != "todas":
		o = i[qual]
		return(o)
	else:
		return(i)



def triade(n, modo = "maior"):   #forma um acorde de tríade com a nota desejada
	if type(n) == str:              
		#n = notas[n]
		n = nota(n) 
	if type(n) == int:             #caso n seja uma nota só
		if modo == "maior":
			t = [n, n+4, n+7]
		elif modo == "menor":
			t = [n, n+3, n+7]
		elif modo == "diminuto":
			t = [n, n+3, n+6]
		elif modo == "aumentado":
			t = [n,n+4,n+8]
		elif modo == "sus" or modo == "suspenso":
			t = [n,n+7]
		elif modo == "sus diminuto" or modo == "diminuto sus" or modo == "suspenso diminuto":
			t = [n,n+6]
		elif modo == "sus aumentado" or modo == "aumentado sus" or modo == "suspenso aumentado":
			t = [n,n+8]


	if type(n) == list:
		t = []            #caso n seja todas as notas com aquele nome
		if modo == "maior":
			for i in range(len(n)):
				t.append([n[i],n[i]+4,n[i]+7]) 
		elif modo =="menor":
			for i in range(len(n)):
				t.append([n[i],n[i]+3,n[i]+7])
		elif modo == "diminuto":
			for i in range(len(n)):
				t.append([n[i],n[i]+3,n[i]+6])
		elif modo == "aumentado":
			for i in range(len(n)):
				t.append([n[i],n[i]+4,n[i]+8])
		elif modo == "sus" or modo == "suspenso":
			for i in range(len(n)):
				t.append([n[i],n[i]+7])
		elif modo == "sus diminuto" or modo == "diminuto sus" or modo == "suspenso diminuto":
			for i in range(len(n)):
				t.append([n[i],n[i]+6])
		elif modo == "sus aumentado" or modo == "aumentado sus" or modo == "suspenso aumentado":
			for i in range(len(n)):
				t.append([n[i],n[i]+8])


	return(t)


def tetrade(n, mode = "maior", setima="maior"):
	setima = setim[setima]
	if type(n) == str:
		n = nota(n)
	if type(n) == int:
		u = triade(n, modo=mode)
		u.append(n+11+setima)
	if type(n) == list:
		u = triade(n, modo=mode)
		for i in range(0,len(u)):
			u[i].append(u[i][0]+setima)


	return(u)

def escala(tonic,modulus="maior"):
	if type(tonic)==str:
		tonic = notas[tonic]
		
	esc = tonalidade(tonic,modo=modulus,fim=tonic+12,inicio=tonic)
	return(esc)

def tonalidade(tonica, modo="maior", fim=127,inicio=0):  #cria um vetor de notas que estejam na tonalidade
	if type(tonica) == str:
		tonica = notas[tonica]
	modo = dic_modos[modo]

	n = tonica
	escala=[]

	while n != 1000:     #costrói um lista adicionando as notas acima da tonica central com base nos intervalos do modo
		for k in modo:
			if n < fim+1:
				escala.append(n)

			if n+k < fim+1:

				n = n+k
			else:
					n = 1000
	n = tonica
	modo.reverse()
	while n != -1000:   #adiciona as notas abaixo da tonica central considerando o modo
		for k in modo:
			if n-k > inicio-1:
				n = n-k
			else:
				n = -1000
			if n > inicio-1:
				escala.append(n)
				escala.sort()
	modo.reverse()
	return(escala)



def inverter_aux(chord, inversion=1): #função auxiliar da função inverter
	inv = chord
	c = 0
	while c != inversion:
		inv[c] = inv[c]+12
		c = c+1
	inv.sort()
	return(inv)

def inverter(acorde,inversao=1,sentido=1): #inverte um acorde
	inver = []
	if type(acorde)==str:
		acorde = triade(acorde)
	if type(acorde[0])==int:
		inver = inverter_aux(acorde,inversao)
	if type(acorde[0])==list:
		for i in range(0,len(acorde)):
			ap = inverter_aux(acorde[i],inversao)
			inver.append(ap)
	return(inver)

def qualnota(n): #traduz um número MIDI dizendo qual nota ele é
	vet = []
	n = nota(n)
	a = list(notas)
	for i in a:
		b = notas[i]
		for k in range(0,len(n)):
			if n[k] == b:
				vet.append(i)
	if len(vet)==2:
		x = vet[0]+" ou "+vet[1]
	elif len(vet)==1:
		x = vet[0]
	print("É a nota:", x)

	return(vet)


def qualnota_2(n): #traduz um número MIDI dizendo qual nota ele é
	vet = []
	n = nota(n)
	a = list(notas)
	for i in a:
		b = notas[i]
		for k in range(0,len(n)):
			if n[k] == b:
				vet.append(i)
	if len(vet)==2:
		x = vet[0]+" ou "+vet[1]
	elif len(vet)==1:
		x = str(vet[0])
	return(x)


def pertence_a_tonalidade_aux(pergunta,toni,mod="maior"): #funcao auxiliar da funcao pertence_a_tonalidade
	if type(toni)==str:
		toni = notas[toni]
	if type(toni)==int:
		a = tonalidade(toni,mod)
	if type(toni)==list:
		a = toni
	if type(pergunta)==str:
		pergunta=notas[pergunta]
	c = 0
	for i in range(0,len(a)):
		if a[i]==pergunta:
			c = c+1
	if c == 1:
		return(True)
	elif c ==0:
		return(False)
	elif c > 1 or c <0:
		return("Erro muito doido")

def pertence_a_tonalidade(perg,ton,mo="maior"): #verifica se perg pertence à tonalidade de tonica ton e modo mo
	if type(perg)==str or type(perg)==int:
		return(pertence_a_tonalidade_aux(perg,ton,mod=mo))
	elif type(perg)==list:
		c = 0
		for i in perg:
			if pertence_a_tonalidade_aux(i,ton,mod=mo)==True:
				c = c+1
		if c==len(perg):
			return(True)
		elif c !=len(perg):
			return(False)


def triades_da_tonalidade(tonica,modu="maior"): #dá um dicionário com as tríades pertencentes à tonalidade
	if type(tonica)==str:
		tonica=notas[tonica]
	b = ["menor","maior","diminuto","aumentado", "sus", "aumentado sus", "diminuto sus"]
	c = escala(tonica,modulus=modu)
	c.pop()
	triades_menores=[]
	triades_maiores=[]
	triades_diminutas=[]
	triades_aumentadas=[]
	triades_sus=[]
	triades_sus_aumentadas=[]
	triades_sus_diminutas=[]
	triades=[triades_menores,triades_maiores,triades_diminutas,triades_aumentadas,triades_sus,triades_sus_aumentadas,triades_sus_diminutas]

	for k in c:
		for i in range(0,len(b)):
			a = pertence_a_tonalidade(triade(k,b[i]),ton=tonica,mo=modu)
			if a==True:
				no = qualnota_2(k)
				triades[i].append(no)

	dic = {"triades menores":triades_menores,"triades maiores":triades_maiores,"triades diminutas":triades_diminutas, "triades aumentadas": triades_aumentadas, "triades suspensas": triades_sus, "triades suspensas aumentadas":triades_sus_aumentadas, "triades suspensas diminutas":triades_sus_diminutas}

	return(dic)

def modos_da_triade(to,tonal,m): #verifica quais modos da triade pertencem a tonalidade tonal de modo m
	if type(to)==str:
		to = notas[to]
	u = []
	for i in list(modos_triades):
		a = triade(to,i)
		if pertence_a_tonalidade(a,ton=tonal,mo=m) == True:
			if i == "maior":
				u.append("maior")
			elif i == "menor":
				u.append("menor")
			elif i == "diminuto":
				u.append("diminuto")
			elif i == "aumentado":
				u.append("aumentado")
			elif i == "suspenso":
				u.append("suspenso")
			elif i == "sus diminuto":
				u.append("suspenso diminuto")
			elif i == "sus aumentado":
				u.append("suspenso aumentado")

	return(u)

def criar_baixo():
	cadeia = cadeia_de_markov(["1","153","135","153a","135a"],[[0.4,0.2,0.2,0.2,0.2],[0.3,0.05,0.5,0.2,0.5],[0.15,0.5,0.05,0.5,0.2],[0.1,0.2,0.05,0.05,0.05],[0.05,0.05,0.2,0.05,0.05]])
	baixo = []
	baixo.append(r.choices(["1","153","135","153a","135a"],[0.8,0.05,0.05,0.05,0.05])[0])
	for i in range(0,3):
		baixo.append(markov(cadeia,baixo[i]))
	#for i in range(0,3):
		#if baixo[i] == "1":
			#baixo.append(r.choices(["1","153","135","153a","135a"],[0.4,0.3,0.15,0.1,0.05])[0])
		#elif baixo[i] == "153":
			#baixo.append(r.choices(["1","153","135","153a","135a"],[0.2,0.05,0.5,0.2,0.05])[0])
		#elif baixo[i] == "135":
		#	baixo.append(r.choices(["1","153","135","153a","135a"],[0.2,0.5,0.05,0.05,0.2])[0])
		#elif baixo[i] == "153a":
		#	baixo.append(r.choices(["1","153","135","153a","135a"],[0.2,0.2,0.5,0.05,0.05])[0])
		#elif baixo[i] == "135a":
		#	baixo.append(r.choices(["1","153","135","153a","135a"],[0.2,0.5,0.2,0.05,0.05])[0])
	return(baixo)

def criar_voicing():
	voicings = []
	voicings.append(r.choices(["7-3","2-4","poly"],[(1/3),(1/3),(1/3)]))
	
	if voicings[0][0] == "7-3":
		colocar = r.choices(["7-3","2-4","poly"],[0.7,0.15,0.15])[0]
		voicings[0].append(colocar)
	elif voicings[0][0] == "2-4":
		colocar = r.choices(["7-3","2-4","poly"],[0.15,0.7,0.15])[0]
		voicings[0].append(colocar)
	elif voicings[0][0] == "poly":
		colocar = r.choices(["7-3","2-4","poly"],[0.15,0.15,0.7])[0]
		voicings[0].append(colocar)
		
		

	for i in range(0,3):
		if voicings[i][0] == voicings[i][1]:
			copiar = r.choices(["sim","nao"],[0.75,0.25])[0]
		elif voicings[i][0] != voicings[i][1]:
			copiar = r.choices(["sim","nao"],[0.9,0.1])[0]
		if copiar == "sim":
			voicings.append(voicings[i])
		elif copiar == "nao":
			if voicings[i][0]=="7-3":
				if voicings[i][1]=="7-3":
					novo_voicing1=r.choices(["7-3","2-4","poly"],[0.2,0.4,0.4])
					novo_voicing2=r.choices(["7-3","2-4","poly"],[0.4,0.3,0.3])[0]
					novo_voicing1.append(novo_voicing2)
					voicings.append(novo_voicing1)
				elif voicings[i][1]=="2-4":
					novo_voicing1=r.choices(["7-3","2-4","poly"],[0.2,0.4,0.4])
					novo_voicing2=r.choices(["7-3","2-4","poly"],[0.4,0.2,0.4])[0]
					novo_voicing1.append(novo_voicing2)
					voicings.append(novo_voicing1)
				elif voicings[i][1]=="poly":
					novo_voicing1=r.choices(["7-3","2-4","poly"],[0.2,0.4,0.4])
					novo_voicing2=r.choices(["7-3","2-4","poly"],[0.4,0.4,0.2])[0]
					novo_voicing1.append(novo_voicing2)
					voicings.append(novo_voicing1)

			elif voicings[i][0]=="2-4":
				if voicings[i][1]=="7-3":
					novo_voicing1=r.choices(["7-3","2-4","poly"],[0.4,0.2,0.4])
					novo_voicing2=r.choices(["7-3","2-4","poly"],[0.2,0.4,0.4])[0]
					novo_voicing1.append(novo_voicing2)
					voicings.append(novo_voicing1)

				elif voicings[i][1]=="2-4":
					novo_voicing1=r.choices(["7-3","2-4","poly"],[0.4,0.2,0.4])
					novo_voicing2=r.choices(["7-3","2-4","poly"],[0.4,0.2,0.4])[0]
					novo_voicing1.append(novo_voicing2)
					voicings.append(novo_voicing1)

				elif voicings[i][1]=="poly":
					novo_voicing1=r.choices(["7-3","2-4","poly"],[0.4,0.2,0.4])
					novo_voicing2=r.choices(["7-3","2-4","poly"],[0.4,0.4,0.2])[0]
					novo_voicing1.append(novo_voicing2)
					voicings.append(novo_voicing1)

			elif voicings[i][0]=="poly":
				if voicings[i][1]=="7-3":
					novo_voicing1=r.choices(["7-3","2-4","poly"],[0.4,0.4,0.2])
					novo_voicing2=r.choices(["7-3","2-4","poly"],[0.2,0.4,0.4])[0]
					novo_voicing1.append(novo_voicing2)
					voicings.append(novo_voicing1)

				elif voicings[i][1]=="2-4":
					novo_voicing1=r.choices(["7-3","2-4","poly"],[0.4,0.4,0.2])
					novo_voicing2=r.choices(["7-3","2-4","poly"],[0.4,0.2,0.4])[0]
					novo_voicing1.append(novo_voicing2)
					voicings.append(novo_voicing1)

				elif voicings[i][1]=="poly":
					novo_voicing1=r.choices(["7-3","2-4","poly"],[0.4,0.4,0.2])
					novo_voicing2=r.choices(["7-3","2-4","poly"],[0.4,0.4,0.2])[0]
					novo_voicing1.append(novo_voicing2)
					voicings.append(novo_voicing1)
	return(voicings)

def escolha_progressao(tipo_de_musica):

	if tipo_de_musica == "blues":
		progressao = []
		progressao.append("1")
		cadeia = cadeia_de_markov(["1","4","5"],[[(5/7),(2/3),0],[(1/7),(1/3),1],[(1/7),0,0]])
		for i in range(0,11):
			progressao.append(markov(cadeia,progressao[i]))
		#for i in range(0,11):
				#if progressao[i]=="1":
					#a = r.choices(["1","4","5"],[(5/7),(1/7),(1/7)])[0] #verificar com a Gabi se eu fiz a conta certa
				#elif progressao[i]=="4":
					#a = r.choices(["1","4"],[(2/3),(1/3)])[0]
				#elif progressao[i]=="5":
					#a = "4"
				#progressao.append(a)
	return(progressao)

def gerar_linha_de_bateria(n = 4, m=4):
	linha1 = []
	linha1.append(r.choices([46,42,"46","42","n"],[0.6,0.2,0.1,0.05,0.05])[0])
	for i in range(0,n-1):
		if linha1[i] == 46:
			linha1.append(r.choices([46,42,"46","42","n"],[0.5, 0.1, 0.05, 0.05,0.3])[0])
		elif linha1[i] == 42:
			linha1.append(r.choices([46,42,"46","42","n"],[0.4,0.3,0.1,0.1,0.1])[0])
		elif linha1[i] == "42":
			linha1.append(r.choices([46,42,"46","42","n"],[0.2,0.4,0.25,0.1,0.05])[0])
		elif linha1[i] == "46":
			linha1.append(r.choices([46,42,"46","42","n"],[0.4,0.2,0.1,0.25,0.05])[0])
		elif linha1[i] == "n":
			linha1.append(r.choices([46,42,"46","42","n"],[0.4,0.2,0.075,0.25,0.025])[0])
	altera2 = r.choices(["sim","nao"],[0.1,0.9])[0]
	altera3 = r.choices(["sim","nao"],[0.1,0.9])[0]
	altera4 = r.choices(["sim","nao"],[0.1,0.9])[0]
	if altera2 == "sim":
		linha2 = []
		for i in range(0,len(linha1)):
			linha2.append(r.choices([linha1[i],46,42,"42","46"],[0.7,0.05,0.05,0.1,0.1])[0])
	elif altera2 == "nao":
		linha2 = linha1
	if altera3 == "sim":
		linha3 = []
		for i in range(0,len(linha1)):
			linha3.append(r.choices([linha1[i],46,42,"42","46"],[0.7,0.05,0.05,0.1,0.1])[0])
	elif altera3 == "nao":
		linha3 = linha1
	if altera4 == "sim":
		linha4 = []
		for i in range(0,len(linha1)):
			linha4.append(r.choices([linha1[i],46,42,"42","46"],[0.7,0.05,0.05,0.1,0.1])[0])
	elif altera4 == "nao":
		linha4 = linha1
	linha = [linha1,linha2,linha3,linha4]
	return(linha)

def gerar_linha_de_tambores(por_compasso=4,compassos=4):
	linha_tambor_1 = []
	linha_tambor_1.append(r.choices([35,36,38,40,"35","36","38","40","n"],[0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])[0])
	for i in range(0,por_compasso-1):
		if linha_tambor_1[i] == 35:
			linha_tambor_1.append(r.choices([35,36,38,40,"35","36","38","40","n"],[0.3,0.05,0.1,0.05,0.15,0.05,0.05,0.05,0.2])[0])
		elif linha_tambor_1[i] == 36:
			linha_tambor_1.append(r.choices([35,36,38,40,"35","36","38","40","n"],[0.05,0.3,0.05,0.15,0.05,0.05,0.1,0.05,0.2])[0])
		elif linha_tambor_1[i] == "35":
			linha_tambor_1.append(r.choices([35,36,38,40,"35","36","38","40","n"],[0.1,0.05,0.05,0.3,0.05,0.05,0.1,0.1,0.2])[0])
		elif linha_tambor_1[i] == "36":
			linha_tambor_1.append(r.choices([35,36,38,40,"35","36","38","40","n"],[0.05,0.1,0.1,0.1,0.05,0.05,0.1,0.25,0.2])[0])
		elif linha_tambor_1[i] == 38:
			linha_tambor_1.append(r.choices([35,36,38,40,"35","36","38","40","n"],[0.25,0.05,0.1,0.05,0.1,0.05,0.1,0.1,0.2])[0])
		elif linha_tambor_1[i] == "38":
			linha_tambor_1.append(r.choices([35,36,38,40,"35","36","38","40","n"],[0.1,0.05,0.1,0.05,0.1,0.05,0.1,0.25,0.2])[0])
		elif linha_tambor_1[i] == 40:
			linha_tambor_1.append(r.choices([35,36,38,40,"35","36","38","40","n"],[0.05,0.2,0.05,0.1,0.05,0.1,0.05,0.25,0.2])[0])
		elif linha_tambor_1[i] == "40":
			linha_tambor_1.append(r.choices([35,36,38,40,"35","36","38","40","n"],[0.05,0.1,0.1,0.25,0.05,0.05,0.1,0.1,0.2])[0])
		elif linha_tambor_1[i] == "n":
			linha_tambor_1.append(r.choices([35,36,38,40,"35","36","38","40","n"],[0.2,0.1,0.1,0.1,0.05,0.05,0.1,0.25,0.05])[0])
	altera_tambor_2 = r.choices(["sim","nao"],[0.2,0.8])[0]
	altera_tambor_3 = r.choices(["sim","nao"],[0.2,0.8])[0]
	altera_tambor_4 = r.choices(["sim","nao"],[0.2,0.8])[0]
	if altera_tambor_2 == "sim":
		linha_tambor_2 = []
		for i in range(0,len(linha_tambor_1)):
			linha_tambor_2.append(r.choices([linha_tambor_1[i],35,36,38,40,"35","36","38","40","n"],[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])[0])
	elif altera_tambor_2 == "nao":
		linha_tambor_2 = linha_tambor_1
	if altera_tambor_3 == "sim":
		linha_tambor_3 = []
		for i in range(0,len(linha_tambor_1)):
			linha_tambor_3.append(r.choices([linha_tambor_1[i],35,36,38,40,"35","36","38","40","n"],[0.1,0.1,0.1,0.1,0.05,0.05,0.2,0.05,0.05,0.2])[0])
	elif altera_tambor_3 == "nao":
		linha_tambor_3 = linha_tambor_1
	if altera_tambor_4 == "sim":
		linha_tambor_4 = []
		for i in range(0,len(linha_tambor_1)):
			linha_tambor_4.append(r.choices([linha_tambor_1[i],35,36,38,40,"35","36","38","40","n"],[0.05,0.2,0.05,0.1,0.1,0.2,0.05,0.1,0.05,0.1])[0])
	elif altera_tambor_4 == "nao":
		linha_tambor_4 = linha_tambor_1
	linha_tambor = [linha_tambor_1,linha_tambor_2,linha_tambor_3,linha_tambor_4]
	return(linha_tambor)

def melodia_blues_hexatonico(tonica,tonica_acorde,max,min,antecipa="nao",qual="1",tempo=4):
	melo = []
	duracoes = []
	campo = tonalidade(tonica,"blues hexatonico",fim=max,inicio=min)
	if tonica_acorde == "1":
		melo.append(r.choices([0,1,2,3,4,5,6],[0.4,0.125,0.03125,0.1,0.25,0.0625,0.03125])[0])
		duracoes.append(r.choices([2,1,0.5,0.25],[0.125,0.5,0.25,0.125])[0])
	elif tonica_acorde == "4":
		melo.append(r.choices([0,1,2,3,4,5,6],[0.25,0.0625,0.4,0.1,0.125,0.03125,0.03125])[0])
		duracoes.append(r.choices([2,1,0.5,0.25],[0.125,0.5,0.25,0.125])[0])
	elif tonica_acorde == "5":
		melo.append(r.choices([0,1,2,3,4,5,6],[0.25,0.03125,0.0625,0.0625,0.4,0.125,0.03125])[0])
		duracoes.append(r.choices([2,1,0.5,0.25],[0.125,0.5,0.25,0.125])[0])
	oitavado = r.choices(["sim","nao"],[0.2,0.8])[0]
	if oitavado == "sim":
		melo[0] = melo[0]+6
	if antecipa == "sim":
		if tonica_acorde == "1":
			kw = 0
			while sum(duracoes)<tempo:
				if tempo-sum(duracoes)>1:
					if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.2,0.05,0.2,0.2,0.1,0.125])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 1 or melo[kw] == 7:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.125,0.1,0.225,0.125,0.2,0.1])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 2 or melo[kw] == 8:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.2,0.4,0.05,0.1,0.15,0.05])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 3 or melo[kw] == 9:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.01,0.4,0.0125,0.01,0.01,0.3575,0.2])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.7,0.3])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 4 or melo[kw] == 10:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.075,0.2,0.2,0.125,0.25,0.05])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.3,0.7])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 5 or melo[kw] == 11:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.3,0.1,0.05,0.15,0.3,0.05])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
						melo.append(melo[kw]+adicionar)
					if melo[kw+1] > 12:
						melo[kw+1] = melo[kw+1]-6
					if melo[kw+1] < 0:
						melo[kw+1] =melo[kw+1]+6

					if tempo-sum(duracoes)>=2:
						duracoes.append(r.choices([2,1,0.5,0.25],[0.125,0.4,0.2,0.275])[0])
					elif tempo-sum(duracoes) == 1.75 or tempo-sum(duracoes) == 1.5 or tempo-sum(duracoes) == 1.25:
						duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) <= 1:
					if qual == "1":
						if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.2,0.05,0.2,0.2,0.1,0.125])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 1 or melo[kw] == 7:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.125,0.1,0.225,0.125,0.2,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 2 or melo[kw] == 8:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.2,0.4,0.05,0.1,0.15,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 3 or melo[kw] == 9:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.01,0.4,0.0125,0.01,0.01,0.3575,0.2])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.7,0.3])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 4 or melo[kw] == 10:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.075,0.2,0.2,0.125,0.25,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.3,0.7])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 5 or melo[kw] == 11:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.3,0.1,0.05,0.15,0.3,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						if melo[kw+1] > 12:
							melo[kw+1] = melo[kw+1]-6
						if melo[kw+1] < 0:
							melo[kw+1] =melo[kw+1]+6

					elif qual == "4":
						if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.2,0.125,0.2,0.125,0.125,0.025,0.2])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 1 or melo[kw] == 7:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.3,0.1,0.1,0.05,0.3,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 2 or melo[kw] == 8:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.2,0.1,0.05,0.1,0.25,0.05,0.25])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 3 or melo[kw] == 9:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.1,0.1,0.3,0.05,0.25,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 4 or melo[kw] == 10:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.15,0.25,0.1,0.3,0.1,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 5 or melo[kw] == 11:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.3,0.1,0.3,0.15,0.05,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						if melo[kw+1] > 12:
							melo[kw+1] = melo[kw+1]-6
						if melo[kw+1] < 0:
							melo[kw+1] =melo[kw+1]+6

					elif qual == "5":
						if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.125,0.1,0.125,0.25,0.2,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 1 or melo[kw] == 7:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.05,0.125,0.275,0.2,0.1,0.125])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 2 or melo[kw] == 8:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.175,0.25,0.25,0.1,0.125,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 3 or melo[kw] == 9:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.3,0.2,0.1,0.125,0.05,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 4 or melo[kw] == 10:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.25,0.1,0.15,0.3,0.1,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 5 or melo[kw] == 11:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.1,0.125,0.1,0.175,0.3,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						if melo[kw+1] > 12:
							melo[kw+1] = melo[kw+1]-6
						if melo[kw+1] < 0:
							melo[kw+1] =melo[kw+1]+6

					if tempo-sum(duracoes) == 1:
						duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
					elif tempo-sum(duracoes) == 0.75 or tempo-sum(duracoes) == 0.5:
						duracoes.append(r.choices([0.5,0.25],[0.5,0.5])[0])
					elif tempo-sum(duracoes) == 0.25:
						duracoes.append(0.25)

				
				kw=kw+1


		elif tonica_acorde == "4":
			kw = 0
			while sum(duracoes)<tempo:
				if tempo-sum(duracoes)>1:
					if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.2,0.125,0.2,0.125,0.125,0.025,0.2])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 1 or melo[kw] == 7:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.3,0.1,0.1,0.05,0.3,0.05])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 2 or melo[kw] == 8:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.2,0.1,0.05,0.1,0.25,0.05,0.25])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 3 or melo[kw] == 9:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.1,0.1,0.3,0.05,0.25,0.1])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 4 or melo[kw] == 10:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.15,0.25,0.1,0.3,0.1,0.05])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 5 or melo[kw] == 11:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.3,0.1,0.3,0.15,0.05,0.05])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
						melo.append(melo[kw]+adicionar)
					if melo[kw+1] > 12:
						melo[kw+1] = melo[kw+1]-6
					if melo[kw+1] < 0:
						melo[kw+1] =melo[kw+1]+6

					if tempo-sum(duracoes)>=2:
						duracoes.append(r.choices([2,1,0.5,0.25],[0.125,0.4,0.2,0.275])[0])
					elif tempo-sum(duracoes) == 1.75 or tempo-sum(duracoes) == 1.5 or tempo-sum(duracoes) == 1.25:
						duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				
				elif tempo-sum(duracoes)<=1:
					if qual == "1":
						if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.2,0.05,0.2,0.2,0.1,0.125])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 1 or melo[kw] == 7:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.125,0.1,0.225,0.125,0.2,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 2 or melo[kw] == 8:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.2,0.4,0.05,0.1,0.15,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 3 or melo[kw] == 9:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.01,0.4,0.0125,0.01,0.01,0.3575,0.2])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.7,0.3])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 4 or melo[kw] == 10:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.075,0.2,0.2,0.125,0.25,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.3,0.7])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 5 or melo[kw] == 11:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.3,0.1,0.05,0.15,0.3,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						if melo[kw+1] > 12:
							melo[kw+1] = melo[kw+1]-6
						if melo[kw+1] < 0:
							melo[kw+1] =melo[kw+1]+6

					elif qual == "4":
						if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.2,0.125,0.2,0.125,0.125,0.025,0.2])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 1 or melo[kw] == 7:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.3,0.1,0.1,0.05,0.3,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 2 or melo[kw] == 8:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.2,0.1,0.05,0.1,0.25,0.05,0.25])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 3 or melo[kw] == 9:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.1,0.1,0.3,0.05,0.25,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 4 or melo[kw] == 10:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.15,0.25,0.1,0.3,0.1,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 5 or melo[kw] == 11:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.3,0.1,0.3,0.15,0.05,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						if melo[kw+1] > 12:
							melo[kw+1] = melo[kw+1]-6
						if melo[kw+1] < 0:
							melo[kw+1] =melo[kw+1]+6

					elif qual == "5":
						if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.125,0.1,0.125,0.25,0.2,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 1 or melo[kw] == 7:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.05,0.125,0.275,0.2,0.1,0.125])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 2 or melo[kw] == 8:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.175,0.25,0.25,0.1,0.125,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 3 or melo[kw] == 9:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.3,0.2,0.1,0.125,0.05,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 4 or melo[kw] == 10:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.25,0.1,0.15,0.3,0.1,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 5 or melo[kw] == 11:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.1,0.125,0.1,0.175,0.3,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						if melo[kw+1] > 12:
							melo[kw+1] = melo[kw+1]-6
						if melo[kw+1] < 0:
							melo[kw+1] =melo[kw+1]+6

					if tempo-sum(duracoes) == 1:
						duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
					elif tempo-sum(duracoes) == 0.75 or tempo-sum(duracoes) == 0.5:
						duracoes.append(r.choices([0.5,0.25],[0.5,0.5])[0])
					elif tempo-sum(duracoes) == 0.25:
						duracoes.append(0.25)

				kw=kw+1
					


			
		elif tonica_acorde == "5":
			kw = 0
			while sum(duracoes)<tempo:
				if tempo-sum(duracoes)>1:
					if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.125,0.1,0.125,0.25,0.2,0.1])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 1 or melo[kw] == 7:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.05,0.125,0.275,0.2,0.1,0.125])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 2 or melo[kw] == 8:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.175,0.25,0.25,0.1,0.125,0.05])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 3 or melo[kw] == 9:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.3,0.2,0.1,0.125,0.05,0.1])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 4 or melo[kw] == 10:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.25,0.1,0.15,0.3,0.1,0.05])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
						melo.append(melo[kw]+adicionar)
					elif melo[kw] == 5 or melo[kw] == 11:
						adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.1,0.125,0.1,0.175,0.3,0.1])[0]
						adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
						melo.append(melo[kw]+adicionar)
					if melo[kw+1] > 12:
						melo[kw+1] = melo[kw+1]-6
					if melo[kw+1] < 0:
						melo[kw+1] =melo[kw+1]+6

					if tempo-sum(duracoes)>=2:
						duracoes.append(r.choices([2,1,0.5,0.25],[0.125,0.4,0.2,0.275])[0])
					elif tempo-sum(duracoes) == 1.75 or tempo-sum(duracoes) == 1.5 or tempo-sum(duracoes) == 1.25:
						duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])

				elif tempo-sum(duracoes)<=1:

					if qual == "1":
						if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.2,0.05,0.2,0.2,0.1,0.125])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 1 or melo[kw] == 7:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.125,0.1,0.225,0.125,0.2,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 2 or melo[kw] == 8:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.2,0.4,0.05,0.1,0.15,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 3 or melo[kw] == 9:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.01,0.4,0.0125,0.01,0.01,0.3575,0.2])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.7,0.3])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 4 or melo[kw] == 10:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.075,0.2,0.2,0.125,0.25,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.3,0.7])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 5 or melo[kw] == 11:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.3,0.1,0.05,0.15,0.3,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						if melo[kw+1] > 12:
							melo[kw+1] = melo[kw+1]-6
						if melo[kw+1] < 0:
							melo[kw+1] =melo[kw+1]+6
					
					elif qual == "4":
						if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.2,0.125,0.2,0.125,0.125,0.025,0.2])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 1 or melo[kw] == 7:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.3,0.1,0.1,0.05,0.3,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 2 or melo[kw] == 8:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.2,0.1,0.05,0.1,0.25,0.05,0.25])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 3 or melo[kw] == 9:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.1,0.1,0.3,0.05,0.25,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 4 or melo[kw] == 10:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.15,0.25,0.1,0.3,0.1,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 5 or melo[kw] == 11:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.3,0.1,0.3,0.15,0.05,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						if melo[kw+1] > 12:
							melo[kw+1] = melo[kw+1]-6
						if melo[kw+1] < 0:
							melo[kw+1] =melo[kw+1]+6

					elif qual == "5":
						if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.125,0.1,0.125,0.25,0.2,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 1 or melo[kw] == 7:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.05,0.125,0.275,0.2,0.1,0.125])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 2 or melo[kw] == 8:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.175,0.25,0.25,0.1,0.125,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 3 or melo[kw] == 9:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.3,0.2,0.1,0.125,0.05,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 4 or melo[kw] == 10:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.25,0.1,0.15,0.3,0.1,0.05])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						elif melo[kw] == 5 or melo[kw] == 11:
							adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.1,0.125,0.1,0.175,0.3,0.1])[0]
							adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
							melo.append(melo[kw]+adicionar)
						if melo[kw+1] > 12:
							melo[kw+1] = melo[kw+1]-6
						if melo[kw+1] < 0:
							melo[kw+1] =melo[kw+1]+6


					
					if tempo-sum(duracoes) == 1:
						duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
					elif tempo-sum(duracoes) == 0.75 or tempo-sum(duracoes) == 0.5:
						duracoes.append(r.choices([0.5,0.25],[0.5,0.5])[0])
					elif tempo-sum(duracoes) == 0.25:
						duracoes.append(0.25)

				kw=kw+1

					




	elif antecipa == "nao":
		if tonica_acorde == "1":
			kw = 0
			while sum(duracoes) <tempo:
				if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.2,0.05,0.2,0.2,0.1,0.125])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 1 or melo[kw] == 7:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.125,0.1,0.225,0.125,0.2,0.1])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 2 or melo[kw] == 8:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.2,0.4,0.05,0.1,0.15,0.05])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 3 or melo[kw] == 9:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.01,0.4,0.0125,0.01,0.01,0.3575,0.2])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.7,0.3])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 4 or melo[kw] == 10:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.075,0.2,0.2,0.125,0.25,0.05])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.3,0.7])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 5 or melo[kw] == 11:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.3,0.1,0.05,0.15,0.3,0.05])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
					melo.append(melo[kw]+adicionar)
				if melo[kw+1] > 12:
					melo[kw+1] = melo[kw+1]-6
				if melo[kw+1] < 0:
					melo[kw+1] =melo[kw+1]+6
				
				if sum(duracoes) <=2:
					duracoes.append(r.choices([2,1,0.5,0.25],[0.125,0.4,0.2,0.275])[0])
				elif tempo-sum(duracoes) == 1.75:
					duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) == 1.5:
					duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) == 1.25:
					duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) == 1:
					duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) == 0.75:
					duracoes.append(r.choices([0.5,0.25],[0.5,0.5])[0])
				elif tempo-sum(duracoes) == 0.5:
					duracoes.append(r.choices([0.5,0.25],[0.5,0.5])[0])
				elif tempo-sum(duracoes) == 0.25:
					duracoes.append(0.25)
				kw=kw+1
		elif tonica_acorde == "4":
			kw = 0
			while sum(duracoes)<tempo:
				if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.2,0.125,0.2,0.125,0.125,0.025,0.2])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 1 or melo[kw] == 7:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.3,0.1,0.1,0.05,0.3,0.05])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 2 or melo[kw] == 8:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.2,0.1,0.05,0.1,0.25,0.05,0.25])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 3 or melo[kw] == 9:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.1,0.1,0.3,0.05,0.25,0.1])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 4 or melo[kw] == 10:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.15,0.25,0.1,0.3,0.1,0.05])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 5 or melo[kw] == 11:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.3,0.1,0.3,0.15,0.05,0.05])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
					melo.append(melo[kw]+adicionar)
				if melo[kw+1] > 12:
					melo[kw+1] = melo[kw+1]-6
				if melo[kw+1] < 0:
					melo[kw+1] =melo[kw+1]+6
				
				if sum(duracoes) <=2:
					duracoes.append(r.choices([2,1,0.5,0.25],[0.125,0.4,0.2,0.275])[0])
				elif tempo-sum(duracoes) == 1.75:
					duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) == 1.5:
					duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) == 1.25:
					duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) == 1:
					duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) == 0.75:
					duracoes.append(r.choices([0.5,0.25],[0.5,0.5])[0])
				elif tempo-sum(duracoes) == 0.5:
					duracoes.append(r.choices([0.5,0.25],[0.5,0.5])[0])
				elif tempo-sum(duracoes) == 0.25:
					duracoes.append(0.25)
				kw=kw+1
		elif tonica_acorde == "5":
			kw = 0
			while sum(duracoes)<tempo:
				if melo[kw] == 0 or melo[kw] == 6 or melo[kw] == 12:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.125,0.1,0.125,0.25,0.2,0.1])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 1 or melo[kw] == 7:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.05,0.125,0.275,0.2,0.1,0.125])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 2 or melo[kw] == 8:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.175,0.25,0.25,0.1,0.125,0.05])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.6,0.4])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 3 or melo[kw] == 9:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.125,0.3,0.2,0.1,0.125,0.05,0.1])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.4,0.6])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 4 or melo[kw] == 10:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.05,0.25,0.1,0.15,0.3,0.1,0.05])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
					melo.append(melo[kw]+adicionar)
				elif melo[kw] == 5 or melo[kw] == 11:
					adicionar = r.choices([0,1,2,3,4,5,6],[0.1,0.1,0.125,0.1,0.175,0.3,0.1])[0]
					adicionar = r.choices([adicionar,adicionar-6],[0.5,0.5])[0]
					melo.append(melo[kw]+adicionar)
				if melo[kw+1] > 12:
					melo[kw+1] = melo[kw+1]-6
				if melo[kw+1] < 0:
					melo[kw+1] =melo[kw+1]+6

				if sum(duracoes) <=2:
					duracoes.append(r.choices([2,1,0.5,0.25],[0.125,0.4,0.2,0.275])[0])
				elif tempo-sum(duracoes) == 1.75:
					duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) == 1.5:
					duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) == 1.25:
					duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) == 1:
					duracoes.append(r.choices([1,0.5,0.25],[0.5,0.3,0.2])[0])
				elif tempo-sum(duracoes) == 0.75:
					duracoes.append(r.choices([0.5,0.25],[0.5,0.5])[0])
				elif tempo-sum(duracoes) == 0.5:
					duracoes.append(r.choices([0.5,0.25],[0.5,0.5])[0])
				elif tempo-sum(duracoes) == 0.25:
					duracoes.append(0.25)
				kw=kw+1

	return {"melodia":melo, "duracoes":duracoes}
	


def gerar_linha_de_bateria_2_aux(contratempos=8):
	linha1 = []   #primeira tempo forte, segunda tempo fraco, terceira contratempo46 e quarta contratempo42
	cadeia = cadeia_de_markov([[36,46],[36,42],[40,46],[40,42],[42],[46]],[[[0.6,0.4,0.3,0.3,1,1],[0.25,0.4,0.2,0.2,0,0],[0.1,0.1,0.4,0.1,0,0],[0.05,0.1,0.1,0.4,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],[[0,0,0,0,0,0],[1,0.7,1,0.4,0.3,1],[0,0,0,0,0,0],[0,0.2,0,0.4,0.3,0],[0,0.1,0,0.2,0.4,0],[0,0,0,0,0,0]],[[0,0,0,0,0,0],[0,0.5,0,0,0.1,0.1],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,0.4,1,1,0.7,0.3],[0,0.1,0,0,0.2,0.6]],[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0.5,0,0.1,0.1],[0,0,0,0,0,0],[0,0,0.1,0,0.6,0.2],[1,1,0.4,1,0.3,0.7]]],alternancia="sim")
	contra = r.choices(["sim","nao"],[0.1,0.9])[0]
	if contra == "sim":
		linha1.append(r.choices([[40,42],[36,42],[42]],[(4/7),(2/7),(1/7)])[0])
	elif contra == "nao":
		linha1.append(r.choices([[36,46],[36,42],[40,46],[40,42]],[(8/15),(4/15),(2/15),(1/15)])[0])

	if contra == "sim":
		for i in range(0,contratempos-1):
			if (i+2)%2==0:
				if i+2==2:
					linha1.append(r.choices([[36,46],[36,42],[40,46],[40,42]],[(8/15),(4/15),(2/15),(1/15)])[0])
				elif i+2 == 4:
					linha1.append(r.choices([[40,42],[36,42],[42]],[(4/7),(2/7),(1/7)])[0])
				elif i+2==6:
					linha1.append(markov(cadeia,linha1[0],alterna=1))
				elif i+2==8:
					linha1.append(markov(cadeia,linha1[1],alterna=2))
			elif (i+2)%2!=0:
				if i+2==3:
					for k in range(0,len(linha1[i])):
						if linha1[i][k] == 46:
							linha1.append(r.choices([[42],[46],[36,42]],[(4/7),(2/7),(1/7)])[0])
						elif linha1[i][k] == 42:
							linha1.append(r.choices([[46],[42],[40,46]],[(4/7),(2/7),(1/7)])[0])

				elif i+2>3:
					for k in range(0,len(linha1[i])):
						if linha1[i][k] == 46:
							linha1.append(markov(cadeia,linha1[i-2],alterna=3))
						elif linha1[i][k] == 42:
							linha1.append(markov(cadeia,linha1[i-2],alterna=4))

	elif contra == "nao":
		for i in range(0,contratempos-1):
			if (i+2)%2==0:
				for k in range(0,len(linha1[i])):
					if linha1[i][k] == 46:
						if i+2 == 2:
							linha1.append(r.choices([[42],[46],[36,42]],[(4/7),(2/7),(1/7)])[0])
						elif i+2 > 2:
							linha1.append(markov(cadeia,linha1[i-2],alterna=3))
					elif linha1[i][k] == 42:
						if i+2==2:
							linha1.append(r.choices([[46],[42],[40,46]],[(4/7),(2/7),(1/7)])[0])
						elif i+2 > 2:
							linha1.append(markov(cadeia,linha1[i-2],alterna=4))
			elif (i+2)%2!=0:
				if i+2==3:
					linha1.append(r.choices([[40,42],[36,42],[42]],[(4/7),(2/7),(1/7)])[0])
				elif i+2==7:
					linha1.append(markov(cadeia,linha1[1],alterna=2))
				elif i+2==5:
					linha1.append(markov(cadeia,linha1[0],alterna=1))



	return(linha1)

def gerar_linha_de_bateria_2(contra_tempos=8,grupo_compassos=4,modo_cowbell="nao"):
	um = gerar_linha_de_bateria_2_aux(contratempos=contra_tempos)
	um=grupo_compassos*um
	altera2 = r.choices(["sim","nao"],[0.3,0.7])[0]
	altera3 = r.choices(["sim","nao"],[0.5,0.5])[0]
	dois = []
	tres = []
	for i in range(0,len(um)):
		dois.append(um[i])
	if altera2 == "sim":
		for i in range(0,len(dois)):
			if type(dois[i])==int:
				if dois[i] == 46:
					dois[i] = 53
				elif dois[i] == 42:
					dois[i] == 51
			elif type(dois[i]) == list:
				for k in range(0,len(dois[i])):
					if dois[i][k] == 46:
						dois[i][k] == 53
					elif dois[i][k] == 42:
						dois[i][k] == 51
	if altera3 == "sim":
		tres = gerar_linha_de_bateria_2_aux(contratempos=contra_tempos)
		tres = grupo_compassos*tres
	elif altera3 == "nao":
		for i in range(0,len(um)):
			tres.append(um[i])
	tudo = um+dois+tres
	if modo_cowbell == "sim":
		for i in range(0,len(tudo)):
			if type(tudo[i])==list:
				for k in range(0,len(tudo[i])):
					if tudo[i][k]==46:
						tudo[i][k] = 52
					elif tudo[i][k]==42:
						tudo[i][k] = 56
			elif type(tudo[i])==int:
				if tudo[i] == 46:
					tudo[i] = 52
				elif tudo[i] == 42:
					tudo[i] = 56

	return(tudo)


def gerar_melodia_blues_hexatonico(tonica,tonica_acorde=0):
	base_notas = escala(tonica,"blues hexatonico")
	base_notas.pop(len(base_notas)-1)
	base_tempo = [0.5,1,1.5]
	melodia_tempo = []
	melodia_notas = []
	
	melodia_tempo.append(r.choices(base_tempo,[0.45,0.45,0.1])[0])
	if tonica_acorde=="1" or tonica_acorde==0:
		melodia_notas.append(r.choices([base_notas[0],base_notas[1],base_notas[4],base_notas[5]],[0.4,0.15,0.25,0.2])[0])
	elif tonica_acorde=="4":
		melodia_notas.append(r.choices([base_notas[0],base_notas[1],base_notas[2]],[0.2,0.2,0.6])[0])
	elif tonica_acorde=="5":
		melodia_notas.append(r.choices([base_notas[2],base_notas[3],base_notas[4],base_notas[5]],[0.1,0.1,0.65,0.15])[0])
	#cadeia = cadeia_de_markov(base_notas,[[0.05,0.15,0.15,0.1,0.25,0.35],[0.4,0.05,0.3,0.15,0.3,0.1],[0.1,0.25,0.05,0.2,0.1,0.05],[0.15,0.3,0.4,0.05,0.1,0.05],[0.25,0.2,0.05,0.4,0.05,0.4],[0.05,0.05,0.05,0.1,0.2,0.05]])
	cadeia_tempo = cadeia_de_markov(base_tempo,[[[0.3,0.2,1],[0.7,0.8,0],[0,0,0]],[[0.3,0.2,1],[0.5,0.6,0],[0.2,0.2,0]]],alternancia="sim")
	i = 0
	if tonica_acorde == 0:
		cadeia = cadeia_de_markov(base_notas,[[0.05,0.15,0.15,0.1,0.25,0.35],[0.4,0.05,0.3,0.15,0.3,0.1],[0.1,0.25,0.05,0.2,0.1,0.05],[0.15,0.3,0.4,0.05,0.1,0.05],[0.25,0.2,0.05,0.4,0.05,0.4],[0.05,0.05,0.05,0.1,0.2,0.05]])
	elif tonica_acorde!=0:
		if tonica_acorde=="1":
			cadeia = cadeia_de_markov(base_notas,[[0.05,0.15,0.15,0.1,0.25,0.35],[0.4,0.05,0.3,0.15,0.3,0.1],[0.1,0.25,0.05,0.2,0.1,0.05],[0.15,0.3,0.4,0.05,0.1,0.05],[0.25,0.2,0.05,0.4,0.05,0.4],[0.05,0.05,0.05,0.1,0.2,0.05]])
		elif tonica_acorde=="4":
			cadeia = cadeia_de_markov(base_notas,[[0.2,0.3,0.3,0.2,0.1,0.2],[0.05,0.1,0.1,0.1,0.15,0.1],[0.3,0.3,0.05,0.4,0.3,0.3],[0.25,0.1,0.35,0.05,0.2,0.15],[0.1,0.1,0.1,0.1,0.05,0.2],[0.1,0.1,0.1,0.15,0.2,0.05]])
		elif tonica_acorde=="5":
			cadeia = cadeia_de_markov(base_notas,[[0.05,0.15,0.05,0.05,0.15,0.15],[0.2,0.05,0.05,0.25,0.15,0.2],[0.05,0.05,0.1,0.2,0.1,0.1],[0.2,0.3,0.25,0.05,0.1,0.1],[0.3,0.25,0.3,0.4,0.2,0.4],[0.2,0.2,0.25,0.05,0.3,0.05]])
	while sum(melodia_tempo)<4:
		melodia_notas.append(markov(cadeia,melodia_notas[i]))
		if sum(melodia_tempo)%2==0:
			a = markov(cadeia_tempo,melodia_tempo[i],alterna=2)
		elif sum(melodia_tempo)%2!=0:
			a = markov(cadeia_tempo,melodia_tempo[i],alterna=1)
		if sum(melodia_tempo)+a<=4:
			melodia_tempo.append(a)
		else:
			while sum(melodia_tempo)+a>4:
				if sum(melodia_tempo)%2==0:
					a = markov(cadeia_tempo,melodia_tempo[i],alterna=2)
				elif sum(melodia_tempo)%2!=0:
					a = markov(cadeia_tempo,melodia_tempo[i],alterna=1)
			melodia_tempo.append(a)

		i = i+1
					

	#for i in range(0,10):
		#melodia_notas.append(markov(cadeia,melodia_notas[i]))
		#melodia_tempo.append(0.5)
	drone_note = r.choices(["sim","nao"],[0.3,0.7])[0]
	if drone_note == "sim":
		if tonica_acorde == "1" or tonica_acorde==0:
			drone_note = r.choices([base_notas[0]+12,base_notas[1]+12,base_notas[3]+12,base_notas[4]+12,base_notas[5]+12],[0.2,0.1,0.1,0.3,0.3])[0]
		elif tonica_acorde == "4":
			drone_note = r.choices([base_notas[0]+12,base_notas[1]+12,base_notas[2]+12,base_notas[3]+12,base_notas[4]+12,base_notas[5]+12],[0.6,0,0.3,0.1,0,0])[0]
		elif tonica_acorde == "5":
			drone_note = r.choices([base_notas[0]+12,base_notas[1]+12,base_notas[2]+12,base_notas[3]+12,base_notas[4]+12,base_notas[5]+12],[0,0,0,0.3,0.4,0.3])[0]

		for i in range(0,len(melodia_notas)):
			melodia_notas[i] = [melodia_notas[i],drone_note]

	dici = {"tempo":melodia_tempo, "notas":melodia_notas}
	return(dici)
