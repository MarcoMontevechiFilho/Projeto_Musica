import fuga as fu, funcoes as f
# a = fu.subject(mode="lidio",tonic="F",chords=[60])
# print(a.chords)
# a.get_melody()
# a.get_melody_score()
# notes=[]
# for i in a.melody["Notes"]:
#     notes.append(f.qualnota(i)[0])
# print(notes)
# print(a.melody["Durations"])
# print(a.melody_score)
a = fu.biome(num_species=5,species_num_fugues=100,fractions_of_parents=0.1,global_harmonic_references=-10,local_harmonic_references=0,range_references=3,variability_references=22.5,variability_chords_per_bar_references=-10,num_bar=10,ending_references=100,beginning_references=100)
a.converge_species(plot="no")
b=a.get_representative_individuals()
#print(b[0][0].get_definitive_music()[0][0])
b[0][0].write_file()
