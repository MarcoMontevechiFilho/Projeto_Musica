"""
Transformar score de harmonia local em função que olha para os vizinhos simetricamente
Colocar números primos nos scores
Teremos um vetor de scores e um score global com thresholds para cada um deles
"""


import funcoes as f, random as r, warnings, matplotlib.pyplot as plt
from datetime import date
from midiutil import MIDIFile
from math import ceil

harmonic_reference = [[0,7,14],[2,5,9,12],[3,4,10,11],[1,6,8,13]]
#harmonic_reference = [[0,7,14],[3,4,10,11],[2,5,9,12],[1,6,8,13]]
modes_from_tonics = {"C":"maior","D":"dorico","E":"frigio","F":"lidio","G":"mixolidio","A":"menor"}
tonics_from_modes = {"maior":"C","menor":"A","jonio":"C","dorico":"D","frigio":"E","lidio":"F","mixolidio":"G","eolio":"A"}

class subject:
    def __init__(self, chords, mode, tonic):
        self.get_chords(chords)
        self.tonic=tonic
        self.mode=mode
        self.get_midi_tonic()
        self.get_midi_scale()
        self.get_melody()

    def get_midi_tonic(self):
        self.midi_tonic = f.nota(self.tonic)
        if type(self.midi_tonic)==list:
            self.midi_tonic=self.midi_tonic[0]
        while self.midi_tonic<55:
            self.midi_tonic=self.midi_tonic+12
        while self.midi_tonic>66:
            self.midi_tonic=self.midi_tonic-12
    
    def get_chords(self,chords):
        self.chords=[]
        for i in chords:
            if type(i)==int:
                note_candidate = f.qualnota(i)
                for k in note_candidate:
                    if len(k)==1:
                        note_candidate=k
                        break
                self.chords.append(note_candidate)
            elif type(i)==list:
                all=[]
                for k in i:
                    note_candidate = f.qualnota(k)
                    for w in note_candidate:
                        if len(w)==1:
                            note_candidate=w
                            break
                    all.append(note_candidate)
                self.chords.append(all)
    
    def get_midi_scale(self):
        scale = []
        scale.append(self.midi_tonic)
        for i in range(1,len(f.dic_modos[self.mode])):
            scale.append(scale[i-1]+f.dic_modos[self.mode][i-1])
        self.midi_scale = scale

    def get_melody(self):
        notes = []
        durations = []
        for i in self.chords:
            notes_number = r.choices([1,2,3,4,5,6,7,8],k=1)[0]
            for i in range(0,notes_number):
                notes.append(r.choices(["n"]+list(range(-7,15)))[0])
            if notes_number==1:
                population = [4]
            elif notes_number==2:
                population = [2,2]
            elif notes_number==3:
                population = [2,1,1]
            elif notes_number==4:
                population = r.choices([[1,1,1,1],[2,1,0.5,0.5]])[0]
            elif notes_number==5:
                population = [1,1,1,0.5,0.5]
            elif notes_number==6:
                population = [1,1,0.5,0.5,0.5,0.5]
            elif notes_number==7:
                population = [1,0.5,0.5,0.5,0.5,0.5,0.5]
            elif notes_number==8:
                population = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
            while len(population)>0:
                durations.append(population.pop(r.choices(list(range(0,len(population))))[0]))
            actual_notes = []
            for i in notes:
                if i == "n":
                    actual_notes.append(i)
                elif 0<=i<=6:
                    actual_notes.append(self.midi_scale[i])
                elif i>=7 and i !=14:
                    actual_notes.append(self.midi_scale[i-7]+12)
                elif i==14:
                    actual_notes.append(self.midi_scale[0]+24)
                elif i<0 and i!=7:
                    actual_notes.append(self.midi_scale[i+7]-12)
                elif i ==-7:
                    actual_notes.append(self.midi_scale[0]-24)

        self.melody = {"Notes":actual_notes,"Durations":durations}

    def get_melody_score(self):

        def get_interval_score(midi_note,midi_note_2):
            if midi_note == "n":
                return 0
            while midi_note > self.midi_scale[-1]:
                midi_note=midi_note-12
            while midi_note < self.midi_scale[0]:
                midi_note=midi_note+12
            while midi_note_2 > self.midi_scale[-1]:
                midi_note_2=midi_note_2+12
            while midi_note_2 < self.midi_scale[0]:
                midi_note_2=midi_note_2+12
            diff=self.midi_scale.index(midi_note)-self.midi_scale.index(midi_note_2)
            if midi_note<midi_note_2:
                diff=diff+7
            if diff==0:
                return 10
            elif diff==4:
                return 5
            elif diff == 2:
                return 3
            elif diff == 3 or 5:
                return 0
            elif diff == 1 or 6:
                return -5
        harmonic_to_chords=0
        range=0
        directional=0
        rythm=0
        beginning = 0
        ending = 0
        init_loop_var=0
        end_loop_var=0
        for i in self.chords:
            if type(i)==str:
                while sum(self.melody["Durations"][init_loop_var:end_loop_var+1])!=4:
                    end_loop_var=end_loop_var+1
                for k in self.melody["Notes"][init_loop_var:end_loop_var]:
                    harmonic_to_chords=harmonic_to_chords+get_interval_score(k,f.nota(i,5))
                init_loop_var=end_loop_var+1
                end_loop_var=init_loop_var
            elif type(i)==list:
                while sum(self.melody["Durations"][init_loop_var:end_loop_var+1])<2:
                    end_loop_var=end_loop_var+1
                for k in self.melody["Notes"][init_loop_var:end_loop_var]:
                    harmonic_to_chords=harmonic_to_chords+get_interval_score(k,f.nota(i[0],5))
                end_loop_var_2=end_loop_var
                while sum(self.melody["Durations"][init_loop_var:end_loop_var_2+1])!=4:
                    end_loop_var_2=end_loop_var_2+1
                for k in self.melody["Notes"][end_loop_var:end_loop_var_2]:
                    harmonic_to_chords=harmonic_to_chords+get_interval_score(k,f.nota(i[1],5))
                init_loop_var=end_loop_var_2+1
                end_loop_var=init_loop_var
        self.melody_score=harmonic_to_chords

class fuga:       ###############init function
    def __init__(self, chords=None, num_bar=None, num_voices=None, mode=None, tonic=None):  ##initializing fugue object

        self.chords=chords
        if self.chords==None:
            self.num_bar=num_bar
        else:
            self.num_bar=len(self.chords)
        self.num_voices=num_voices
        self.mode=mode
        self.tonic=tonic

        self.check_parameters()

        self.get_midi_tonic()

        self.get_midi_scale()

        self.score = self.getChordsharscore()

        self.subject_=None

############################################### seeding functions

    def seed_chords(self):                      ####getting random chords
        chords = []
        if r.choices([1,2])[0]==1:
            chords.append(r.choices([-14,-12,-10,-7,-5,-3,0,2,4,7,9,11,14])[0])
        else:
            chords.append([0,r.choices([-14,-12,-10,-7,-5,-3,0,2,4,7,9,11,14])[0]])
        for i in range(0,self.num_bar-1):  #####defining number of chords per bar. Maximum of two chords per bar
            num_chords = r.choices([1,2])[0]
            if num_chords == 1:
                chords.append(r.choices(list(range(-14,15)))[0])
            elif num_chords == 2:
                x = []
                for k in range(0,2):
                    x.append(r.choices(list(range(-14,15)))[0])
                chords.append(x)
        self.chords=chords
        
    def seed_num_bar(self):                     ####getting random number of bars 
        self.num_bar = r.choices([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])[0]   

    def seed_num_voices(self):                 #####getting random number of voices
        self.num_voices = r.choices(list(range(1,7)))[0]

    def seed_tonic_and_mode(self):                             ######getting random tonic
        self.tonic = r.choices(["C","D","E","F","G","A"])[0]
        self.mode = modes_from_tonics[self.tonic]

#####################################################checking parameters

    def check_parameters(self):

        if self.num_bar == None:           #########checking number of bars
            self.seed_num_bar()

        if self.num_voices == None:          #####checking voices parameter
            self.seed_num_voices()

        if self.chords == None:        ##########checking chords parameter
            self.seed_chords()

        if self.tonic == None and self.mode == None:           #####checking tonic and mode parameters
            self.seed_tonic_and_mode()
        elif self.tonic == None and self.mode != None:
            if self.mode in ["maior","menor","jonio","dorico","frigio","lidio","mixolidio","eolio"]:
                self.tonic = tonics_from_modes[self.mode]
            else:
                print("Invalid mode. Enter valid mode: ")
                self.mode = input("")
                self.check_parameters()
        elif self.tonic != None and self.mode == None:
            if self.tonic in ["C","D","E","F","G","A"]:
                self.tonic=self.tonic
            else:
                print("Invalid tonic. Enter valid tonic: ")
                while self.tonic not in ["C","D","E","F","G","A"]:
                    self.tonic = input("")
                    print("Invalid tonic. Enter valid tonic: ")
            self.mode = modes_from_tonics[self.tonic]
        elif self.mode != None and self.tonic != None:
            if self.tonic in ["C","D","E","F","G","A"]:
                if self.mode in ["maior","menor","jonio","dorico","frigio","lidio","mixolidio","eolio"]:
                    if self.tonic == tonics_from_modes[self.mode]:
                        pass
                    elif self.tonic != tonics_from_modes[self.mode]:
                        self.tonic = tonics_from_modes[self.mode]
                        print("Invalid tonic for this mode. Switching tonic to "+self.tonic)

######################################################## interpreting music numbers etc.

    def get_midi_tonic(self):
        if self.tonic not in ["A","G"]:
            self.midi_tonic=f.nota(self.tonic,5)
        elif self.tonic in ["A","G"]:
            self.midi_tonic=f.nota(self.tonic,4)

    def get_midi_scale(self):
        scale = []
        scale.append(self.midi_tonic)
        for i in range(1,len(f.dic_modos[self.mode])):
            scale.append(scale[i-1]+f.dic_modos[self.mode][i-1])
        self.midi_scale = scale

    def get_definitive_music(self):    ####returns a vector with midi numbers for each chord and a vector with the duration of
                                       ####each note
        defi =[[],[]]
        for i in self.chords:
            if type(i) == int:
                if i < len(self.midi_scale) and i >= 0:
                    defi[0].append(self.midi_scale[i])
                    defi[1].append(2)
                elif i >= len(self.midi_scale):
                    count = 0
                    while i >= len(self.midi_scale):
                        i = i-7
                        count = count+1
                    defi[0].append(self.midi_scale[i]+(count*12))
                    defi[1].append(2)
                elif i < 0:
                    count = 0
                    while i < 0:
                        i = i + 7
                        count = count+1
                    defi[0].append(self.midi_scale[i]-(count*12))
                    defi[1].append(2)
            elif type(i) == list:
                for k in i:
                    if k < len(self.midi_scale) and k >= 0:
                        defi[0].append(self.midi_scale[k])
                        defi[1].append(2)
                    elif k >= len(self.midi_scale):
                        count = 0
                        while k >= len(self.midi_scale):
                            k = k - 7
                            count = count + 1
                        defi[0].append(self.midi_scale[k]+(count*12))
                        defi[1].append(1)
                    elif k < 0:
                        count = 0
                        while k < 0:
                            k = k + 7
                            count = count+1
                        print("#########K: "+str(k))
                        print("midi scale: "+str(self.midi_scale))
                        print("mode: "+str(self.mode))
                        defi[0].append(self.midi_scale[k]-(count*12))
                        defi[1].append(1)
        
        return(defi)

 ########################################### writing file

    def write_file(self,filename=None):
        if filename==None:
            filename="Fugue_in_"+str(self.tonic)+"_"+str(self.mode)+str(date.today())
        track    = 0
        channel  = 0
        time     = 0    # In beats
        duration = 1    # In beats
        tempo    = 60   # In BPM
        volume   = 100  # 0-127, as per the MIDI standard

        MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
        MyMIDI.addTempo(track, time, tempo)

        MyMIDI.addTempo(track, time, tempo)

        definitive_music = self.get_definitive_music()
        time_count=0

#        for i, pitch in enumerate(degrees):
#            MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)
        
        for i in range(0,len(definitive_music[0])):
            MyMIDI.addNote(track, channel, definitive_music[0][i], time + time_count, definitive_music[1][i], volume)
            time_count = time_count + definitive_music[1][i]
            


        with open(filename+".mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)
        
        arq = open(filename+".txt","w+")
        arq.write("Acordes: " + str(self.chords) + "\n")
        arq.write("Modo: " + str(self.mode) + "\n")
        arq.write("Tonic: " + str(self.tonic) + "\n")
        arq.write("Defi[0]: " + str(definitive_music[0])+"\n")
        arq.write("Defi[1]: " + str(definitive_music[1])+"\n")
        arq.write("Global Harmonic Score: " + str(self.score["Global harmonic score"])+"\n")
        arq.close()


################################# getting musical scores

    def getNumChordsPerBarScore(self,chords):
        if len(chords)==1:
            return(0)
        else:
            one=0
            two=0
            for i in chords:
                if type(i)==int or type(i)==float:
                    one+=1
                elif type(i)==list:
                    two+=1
            return(abs(one-two))

    def getChordslocalharscore(self,chords):
        score = 0
        for i in range(0,len(chords)-1):
            diff = chords[i+1]-chords[i]
            while diff<0:
                diff = diff+7
            if diff in harmonic_reference[0]:
                score = score + 7
            elif diff in harmonic_reference[1]:
                score = score + 3
            elif diff in harmonic_reference[2]:
                score = score - 3
            elif diff in harmonic_reference[3]:
                score = score - 7

        return(score)

    def getChordsglobalharscore(self,chords):
        score = 0
        for i in chords:
            while i < 0:
                i = i+7
            if i in harmonic_reference[0]:
                score = score + 7
            elif i in harmonic_reference[1]:
                score = score + 3
            elif i in harmonic_reference[2]:
                score = score - 3
            elif i in harmonic_reference[3]:
                score = score - 7
        
        return(score)

    def getRangescore(self,chords):
        return(max(chords)-min(chords))

    def getVariabilityscore(self,chords):
        score=0
        for i in range(0,len(chords)-1):
            for k in range(i,len(chords)-1):
                score=score+abs(chords[i]-chords[k])*(1/(k-i+1))
        return(score)

    def getEndingHarScore(self):
        if self.chords[-1] in [0,7,14]:
            return 10
        elif self.chords[-1] in [3,4,10,11]:
            return 5
        else:
            return 0

    def getBeginningHarScore(self):
        if type(self.chords[0])==int:
            if self.chords[0] in [-14,-7,0,7,14]:
                return 10
            elif self.chords[0] in [-12,-10,-5,-3,2,4,9,11]:
                return 3
            else:
                return 0
        elif type(self.chords[0])==list:
            if self.chords[0][0] in [-14,-7,0,7,14]:
                return 10
            elif self.chords[0][0] in [-12,-10,-5,-3,2,4,9,11]:
                return 3
            else:
                return 0

    def getChordsharscore(self):
        linear_chords = []
        for i in (self.chords):
            if type(i)==int:
                linear_chords.append(i)
            elif type(i)==list:
                for k in i:
                    linear_chords.append(k)
        
        global_fugue_score = self.getChordsglobalharscore(linear_chords)
        local_fugue_score = self.getChordslocalharscore(linear_chords)
        range_score = self.getRangescore(linear_chords)
        var_score = self.getVariabilityscore(linear_chords)
        number_of_chords_per_bar=self.getNumChordsPerBarScore(self.chords)
        ending_score=self.getEndingHarScore()
        beginning_score=self.getBeginningHarScore()
        return({"Global harmonic score":global_fugue_score/len(self.chords),"Local harmonic score":local_fugue_score/len(self.chords), "Range score":range_score, "Variability score":var_score/len(self.chords),"Variability in number of chords per bar":number_of_chords_per_bar/len(self.chords), "Ending score":ending_score, "Beginning score":beginning_score})

class pool:   ##########class responsible for generating, breeding, analyzing and mutating fugues
    
    def __init__(self,number=100,fugues=None,fraction_of_parents=0.1,global_harmonic_reference=0,local_harmonic_reference=0,range_reference=14,variability_reference=22.5,variability_chords_per_bar_reference=0.5,num_bar=7,ending_reference=10,beginning_reference=10):
        self.number=number
        self.fraction_of_parents=fraction_of_parents
        self.global_harmonic_reference=global_harmonic_reference
        self.local_harmonic_reference=local_harmonic_reference
        self.range_reference=range_reference
        self.variability_reference=variability_reference
        self.variability_chords_per_bar_reference=variability_chords_per_bar_reference
        self.num_bar=num_bar
        self.ending_reference=ending_reference
        self.beginning_reference=beginning_reference
        self.parents=None
        self.offspring=None
        
        if fugues == None:
            fugues = []
            for i in range(0,number):
                fugues.append(fuga(num_bar=self.num_bar))
            self.fugues=fugues

        elif fugues != None and type(fugues) == list:
            if len(fugues) == number:
                self.fugues = fugues
            else:
                x = len(fugues)
                for i in range(x,number):
                    fugues.append(fuga(num_bar=self.num_bar))
                self.fugues = fugues

    def get_representative_individuals(self):
        models=[self.fugues[0]]
        models_chords=[self.fugues[0].chords]
        for i in self.fugues:
            if i.chords not in models_chords:
                models.append(i)
                models_chords.append(i.chords)
        
        return models

    def define_parents(self):
        parents=self.sort_by_score()
        self.parents=[]
        for i in range(0,int(len(parents)*self.fraction_of_parents)):
            self.parents.append(parents[i][0])
        return(self.parents)

    def get_distance_from_reference(self,fugue):
        vec = []
        reference = [self.global_harmonic_reference,self.local_harmonic_reference,self.range_reference,self.variability_reference,self.variability_chords_per_bar_reference,self.ending_reference,self.beginning_reference]
        point_in_score_space=list(fugue.score.values())
        distance=0
        for k in range(0,len(point_in_score_space)):
            distance=distance+(point_in_score_space[k]-reference[k])**2
        return distance**(1/2)
        
    def sort_by_score(self):
        vec = []
        for i in self.fugues:
            vec.append([i,self.get_distance_from_reference(i)])
        return(self.quick_sort_score(vec))
    
    def quick_sort_score(self,vector):
        less=[]
        equal=[]
        greater=[]

        if len(vector)>1:
            pivot = vector[0]
            for x in vector:
                if x[1] < pivot[1]:
                    less.append(x)
                elif x[1] == pivot[1]:
                    equal.append(x)
                elif x[1] > pivot[1]:
                    greater.append(x)
            return(self.quick_sort_score(less)+equal+self.quick_sort_score(greater))
        else:
            return(vector)
    
    def get_average_population_score(self,score_type):
        val = 0
        for i in self.fugues:
            val=val+i.score[score_type]
        return val/len(self.fugues)

    def get_distance_from_reference(self,fugue):
        reference=[self.global_harmonic_reference,self.local_harmonic_reference,self.range_reference,self.variability_reference,self.variability_chords_per_bar_reference,self.ending_reference,self.beginning_reference]
        distance=0
        point_in_score_space=list(fugue.score.values())
        for i in range(0,len(point_in_score_space)):
            distance=distance+(point_in_score_space[i]-reference[i])**2
        return distance**(1/2)
        
    def get_average_population_distance_from_reference(self):
        val=0
        for i in range(0,len(self.fugues)):
            val=val+self.get_distance_from_reference(self.fugues[i])
        return val/len(self.fugues)

    def get_average_parents_score(self,score_type):
        if self.parents==None:
            warnings.warn("Parents have not been defined!")
        else:
            val = 0
            for i in self.parents:
                val = val+i.score[score_type]
            return val/len(self.parents)

    def breed(self,random_comparison_percentage=0.1):
        def return_smaller_list(list1,list2):
            if len(list1)<=len(list2):
                return list1
            else:
                return list2

        def return_bigger_list(list1,list2):
            if len(list1)>len(list2):
                return list1
            else:
                return list2

        def repeated_index(li,element):
            aux_list=[]
            indexes=[]
            for i in li:
                aux_list.append(i)
            counter = 0
            while True:
                try:
                    indexes.append(aux_list.index(element)+counter)
                    aux_list.pop(aux_list.index(element))
                    counter=counter+1
                except:
                    if counter == 0:
                        return False
                    else:
                        return indexes
            return False

        def cyclic_list(li,index1,index2):
            if index2<=len(li):
                return li[index1:index2]
            else:
                return li[index1:]+li[:index2%len(li)]

        def is_subsequence(small_list,big_list):
            indexes = repeated_index(big_list,small_list[0])
            if indexes == False:
                return [False]
            for i in indexes:
                if small_list==cyclic_list(big_list,i,i+len(small_list)):
                    return [small_list,i,i+len(small_list)]
            return [False]

        def get_bigger_subsequence(x,y):
            small = return_smaller_list(x,y)
            big = return_bigger_list(x,y)
            memory=[]
            for i in range(0,len(small)-2):
                eval = is_subsequence(small[i:len(small)],big)
                if eval[0]!=False:
                    memory.append(eval+[i,len(small)])
                eval = is_subsequence(small[0:len(small)-i],big)
                if eval[0]!=False:
                    memory.append(eval+[0,len(small)-i])
            diffs=[]
            if len(memory)>0:
                for i in memory:
                    diffs.append(len(i[0]))
                return memory[diffs.index(max(diffs))]

            return None
        offspring = []
        for i in self.parents:
            if random_comparison_percentage<=1:
                breeding_candidates = r.sample(self.parents,k=ceil(random_comparison_percentage*len(self.parents)))
                for k in breeding_candidates:
                    if k.chords!=i.chords:
                        small = return_smaller_list(k.chords,i.chords)
                        big = return_bigger_list(k.chords,i.chords)
                        eval = get_bigger_subsequence(small,big)
                        if eval != None:
                            offspring.append(fuga(chords=small[:eval[-1]]+big[eval[-3]:]))
                            offspring.append(fuga(chords=big[:eval[-4]]+small[eval[-2]:]))
                        else:
                            divise = r.choices(list(range(0,len(small))))[0]
                            offspring.append(fuga(chords=big[0:divise]+small[divise:len(small)]))
                            offspring.append(fuga(chords=small[0:divise]+big[divise:len(big)]))
        self.offspring=offspring

    def mutate(self,fraction_of_parents_mutation=0.01,fraction_of_offspring_mutation=0.01):
        def change_random_chord(fugue):
            new_chords=fugue.chords
            index_to_be_changed=r.choices(list(range(0,len(new_chords))))[0]
            if type(index_to_be_changed)==list:
                number_of_chords=2
            else:
                number_of_chords=1
            to_be_changed=r.choices(list(range(-14,15)),k=number_of_chords)
            if len(to_be_changed)==1:
                to_be_changed=to_be_changed[0]
            new_chords[index_to_be_changed]=to_be_changed
            return fuga(chords=new_chords)
        def scramble_chords(fugue):
            new_chords=fugue.chords
            a = r.choices(list(range(0,len(new_chords))))[0]
            new_vector = []
            for i in range(0,len(new_chords)):
                new_vector.append((new_chords[a:]+new_chords[:a])[i])
            return fuga(chords=new_vector)
        if self.offspring!=None:
            indexes = r.choices(list(range(0,len(self.offspring))),k=ceil(fraction_of_offspring_mutation*len(self.offspring)))
            for i in indexes:
                new_offspring=r.choices([scramble_chords(self.offspring[i]),change_random_chord(self.offspring[i])])[0]
                self.offspring.pop(i)
                self.offspring.append(new_offspring)
        if self.parents!=None:
            indexes = r.choices(list(range(0,len(self.parents))),k=ceil(fraction_of_parents_mutation*len(self.parents)))
            for i in indexes:
                new_parent=r.choices([scramble_chords(self.parents[i]),change_random_chord(self.parents[i])])[0]
                self.parents.pop(i)
                self.parents.append(new_parent)

    def call_Darwin(self):
        reference=[self.global_harmonic_reference,self.local_harmonic_reference,self.range_reference,self.variability_reference,self.variability_chords_per_bar_reference,self.ending_reference,self.beginning_reference]
        vec = []
        death_pool=self.parents+self.offspring+self.fugues
        for i in death_pool:
            point_in_score_space=list(i.score.values())
            distance=0
            for k in range(0,len(point_in_score_space)):
                distance=distance+(point_in_score_space[k]-reference[k])**2
            distance=distance**(1/2)
            vec.append([i,distance])
        survivors=self.quick_sort_score(vec)
        for i in range(0,len(self.fugues)):
            self.fugues[i]=survivors[i][0]
        self.offspring=None
        self.parents=None
    
    def converge(self,plot="no",iterations=100):
        if plot=="yes":
            average_distance=[]
            iteration_number=[]
        counter=0
        average=0.1
        average_vec=[]
        recent_average=self.get_average_population_distance_from_reference()
        converge_var=0
        while converge_var==0 and counter<iterations:
            previous_average=recent_average
            print("Generation "+str(counter))
            self.define_parents()
            print("Defining parents...")
            self.breed(random_comparison_percentage=average**2)
            print("Breeding...")
            self.mutate(fraction_of_offspring_mutation=average,fraction_of_parents_mutation=average)
            print("Mutating...")
            self.call_Darwin()
            print("Calling Darwin...")
            recent_average=self.get_average_population_distance_from_reference()
            average = recent_average/previous_average
            counter=counter+1
            average_vec.append(average)
            if len(average_vec)>3:
                if average_vec[-1]>0.97 and average_vec[-2]>0.97 and average_vec[-3]>0.97:
                    converge_var=1
            if average>1:
                average=0
            if plot=="yes":
                average_distance.append(recent_average)
                iteration_number.append(counter)
        
        if plot=="yes":
            fig = plt.figure()
            plt.plot(iteration_number,average_distance,label="average distance")
            plt.plot(iteration_number,average_vec,label="mutation factor")
            fig.suptitle('Convergence')
            plt.xlabel('Generation')
            plt.ylabel('Distance from reference')
            plt.show()

class biome:

    def __init__(self,species=[],num_species=5,species_num_fugues=100,fractions_of_parents=0.1,global_harmonic_references=0,local_harmonic_references=0,range_references=14,variability_references=22.5,variability_chords_per_bar_references=0.5,num_bar=7,ending_references=10,beginning_references=10):
        self.num_species=num_species
        self.species=species

        self.species_num_fugues=species_num_fugues
        self.fractions_of_parents=fractions_of_parents
        self.global_harmonic_references=global_harmonic_references
        self.local_harmonic_references=local_harmonic_references
        self.range_references=range_references
        self.variability_references=variability_references
        self.variability_chords_per_bar_references=variability_chords_per_bar_references
        self.num_bar=num_bar
        self.ending_references=ending_references
        self.beginning_references=beginning_references 

        self.check_parameters()

    def converge_species(self,plot="no"):
        for i in self.species:
            i.converge(plot=plot)

    def check_vectors(self,vector_candidate):
        typ = type(vector_candidate)
        if typ!=list:
            new_vec=[]
            for i in range(0,self.num_species):
                new_vec.append(vector_candidate)
            return new_vec
        else:
            while len(vector_candidate)<self.num_species:
                vector_candidate.append(vector_candidate[-1])
            return vector_candidate

    def check_parameters(self):
        self.fractions_of_parents=self.check_vectors(self.fractions_of_parents)
        self.global_harmonic_references=self.check_vectors(self.global_harmonic_references)
        self.local_harmonic_references=self.check_vectors(self.local_harmonic_references)
        self.range_references=self.check_vectors(self.range_references)
        self.variability_references=self.check_vectors(self.variability_references)
        self.variability_chords_per_bar_references=self.check_vectors(self.variability_chords_per_bar_references)
        self.num_bar=self.check_vectors(self.num_bar)
        self.species_num_fugues=self.check_vectors(self.species_num_fugues)
        self.ending_references=self.check_vectors(self.ending_references)
        self.beginning_references=self.check_vectors(self.beginning_references) 
        if self.species!=None:
            while len(self.species)>self.num_species:
                self.species.pop(-1)
            while len(self.species)<self.num_species:
                position_in_vectors=len(self.species)
                self.species.append(pool(number=self.species_num_fugues[position_in_vectors],fraction_of_parents=self.fractions_of_parents[position_in_vectors],global_harmonic_reference=self.global_harmonic_references[position_in_vectors],local_harmonic_reference=self.local_harmonic_references[position_in_vectors],range_reference=self.range_references[position_in_vectors],variability_reference=self.variability_references[position_in_vectors],variability_chords_per_bar_reference=self.variability_chords_per_bar_references[position_in_vectors],num_bar=self.num_bar[position_in_vectors]))

    def get_representative_individuals(self):
        vec = []
        for i in self.species:
            vec.append(i.get_representative_individuals())
        return vec