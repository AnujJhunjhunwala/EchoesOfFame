import re

with open('conv1', 'r', encoding='utf-8') as plik:
    text = plik.read()

def format_text(t, person1, person2):
    text_splited = t.split()
    for i in range(len(text_splited)):
        text_splited[i] = re.sub(r'\s*\n\s*', '', text_splited[i])
    speaking_person = text_splited[0]
    if speaking_person == person1+":":
        listening_person = person2+":"
    else:
        listening_person = person1+":"
    line = ""
    formated_text = ""
    for i in range(1, len(text_splited)):
        if text_splited[i] == listening_person:
            formated_text += (speaking_person+line+"\n")
            listening_person = speaking_person
            speaking_person = text_splited[i]
            line = ""
        elif text_splited[i] == speaking_person:
            pass
        else:
            line += " "+text_splited[i]
    return formated_text
print(format_text(text, "Max_Stirner","Karl_Marx"))