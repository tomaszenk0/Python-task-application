def create_file():
    name=input("Name of your file:")
    lines=[]
    print("ADD your data and when you will be want save the file - write END: \n")
    while True:
        line=input()
        if line.upper()=='END':
            break
        lines.append(line)
    with open(name, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

create_file()

