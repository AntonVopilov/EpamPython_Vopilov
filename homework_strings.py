""""

Задание 1

0) Повторение понятий из биологии (ДНК, РНК, нуклеотид, протеин, кодон)

1) Построение статистики по входящим в последовательность ДНК нуклеотидам 
для каждого гена (например: [A - 46, C - 66, G - 23, T - 34])

2) Перевод последовательности ДНК в РНК (окей, Гугл)

3) Перевод последовательности РНК в протеин*


*В папке files вы найдете файл rna_codon_table.txt - 
в нем содержится таблица переводов кодонов РНК в аминокислоту, 
составляющую часть полипептидной цепи белка.


Вход: файл dna.fasta с n-количеством генов

Выход - 3 файла:
 - статистика по количеству нуклеотидов в ДНК
 - последовательность РНК для каждого гена
 - последовательность кодонов для каждого гена

 ** Если вы умеете в matplotlib/seaborn или еще что, 
 welcome за дополнительными баллами за
 гистограммы по нуклеотидной статистике.
 (Не забудьте подписать оси)

P.S. За незакрытый файловый дескриптор - караем штрафным дезе.

"""

import json

with open("./files/rna_codon_table.txt", "r") as rna_codon_table_file:
    name_genom = None
    key = False
    condon_dict = {}
    for line in rna_codon_table_file:
        for item in line.split():
            if key:
                value = item
                condon_dict[key] = value
                key = False
            else:
                key = item


def count_nucleotides(dna: dict):

    DNA_symbols = ('A', 'C', 'G', 'T')
    dna_stat = {}

    for key, value in dna.items():
        dna_stat[key] = [(DNA_symbol, value.count(DNA_symbol)) for DNA_symbol in DNA_symbols]
    return dna_stat


def my_replace(s: str, old, new):
    s.split(old)
    return new.join(s.split(old))


def translate_from_dna_to_rna(dna: dict):

    rna = {}
    # replace уже нельзя :(

    for key, value in dna.items():
        rna_value = my_replace(value, 'T', 'U')
        rna[key] = rna_value[:(len(rna_value)//3) * 3]

    return rna



def translate_rna_to_protein(rna):

    global condon_dict

    def rna_to_protein(rna_str: str):
        i = 0
        res = ''
        while i != len(rna_str):
            res += condon_dict[rna_str[i:i+3]]
            i += 3
        return res

    protein = {}
    for key, value in rna.items():
        protein[key] = rna_to_protein(value)
    return protein


if __name__ == '__main__':

    dna = {}


    with open("./files/dna.fasta", "r") as dna_file:
        name_genom = None
        for line in dna_file:
            if line[0] == '>':
                name_genom = line.replace('\n', '')
                dna[name_genom] = ''
            else:
                dna[name_genom] += line.replace('\n', '')

    dna_stat = count_nucleotides(dna)
    rna = translate_from_dna_to_rna(dna)
    protein = translate_rna_to_protein(rna)

    with open('dna_stat.json', 'w') as file:
        json.dump(dna_stat, file, indent=4)
    with open('rna.json', 'w') as file:
        json.dump(rna, file, indent=4)
    with open('protein.json', 'w') as file:
        json.dump(protein, file, indent=4)
