import copy

from Data import CInstruction
from Data import CMnemonic

ContLoc=0   #Contador de localidades
DirCount=0  #Contador de direcciones
value=0
finalValue=0
"""Cargar los Mnemonicos disponibles"""
Mnemonicos=[]
def load_mnemonics(file_name):
    file=open(file_name)
    lines=file.readlines()
    file.close()
    mnemonic=CMnemonic()
    i=0
    for line in lines:
        linea=line.strip()
        code=linea.split('|')
        mnemonic.setInstruction(code[0])
        mnemonic.setModDirection(code[1])
        mnemonic.setLongInstruction(code[2])
        mnemonic.setCodOperation(code[3])
        Mnemonicos.append(copy.copy(mnemonic))


instructions = []
"""Lector de archivo .asm"""
def loader(file_name):
    instruction=CInstruction()
    with open(file_name) as file:
        lines=(line.rstrip() for line in file)
        lines=(line for line in lines if line)
        for line in lines:
            instruction=analize(line.strip())
            if(instruction.getMnemonico()=='ORG'):
                ContLoc=dir_to_Int(instruction.getDirection())
                print('0000'+ ' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write('0000'+ ' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection()+'\n')

            elif(instruction.getMnemonico()=='END'):
                print(ContLoc+ ' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())

            else:
                for i in range(len(Mnemonicos)):
                    if(instruction.getMnemonico()==Mnemonicos[i].getInstruction()):
                        #Aqui van a ir los if para mnemonicos chingones
                        Dir_Temp=instruction.getDirection()

                        if(Mnemonicos[i].getModDirection()=='INH' and Dir_Temp==' '):  #Comprobar si es inherente
                            print(
                                ContLoc+ ' ' +instruction.getMnemonico()+ ' '+Mnemonicos[i].getModDirection()+' '+
                                Mnemonicos[i].getLongInstruction()+' '+Mnemonicos[i].getCodOperation()
                                )
                            archivoFinal.write(
                                ContLoc+ ' ' +instruction.getMnemonico()+ ' '+Mnemonicos[i].getModDirection()+' '+
                                Mnemonicos[i].getLongInstruction()+' '+Mnemonicos[i].getCodOperation()+'\n'
                            )
                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break

                        elif(Dir_Temp!=' '):
                            Len_DirTemp=len(Dir_Temp)
                            if(Dir_Temp.find('#',0, Len_DirTemp)!=-1):  #SI encuentra que es de direccionamiento IMM 
                                value=convert_to_hex(Dir_Temp[1:Len_DirTemp])
                                if(instruction.getMnemonico()=='ADDD'):#condicion especial si es la instruccion ADDDD
                                    if(len(value)==1):
                                        finalValue='000'+value
                                    elif(len(value)==2):
                                        finalValue='00'+value
                                    elif(len(value)==3):
                                        finalValue+'0'
                                    else:
                                        finalValue=value

                                else:
                                    if(len(value)==1):
                                        finalValue='0'+value
                                    else:
                                        finalValue=value    
                                #print(finalValue)
                                print(
                                    ContLoc+ ' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection()+' '+
                                    Mnemonicos[i].getModDirection()+' '+Mnemonicos[i].getLongInstruction()+' '+
                                    Mnemonicos[i].getCodOperation()
                                )
                                archivoFinal.write(
                                    ContLoc+ ' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection()+' '+
                                    Mnemonicos[i].getModDirection()+' '+Mnemonicos[i].getLongInstruction()+' '+
                                    Mnemonicos[i].getCodOperation()+'\n'
                                )
                                ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                break

                            else:   #sino es de direccionamiento IMMM
                                value=convert_to_hex(Dir_Temp)
                                Len_DirTemp=len(value)
                                if(Len_DirTemp>2 and Mnemonicos[i].getLongInstruction()=='3'):
                                    if(Len_DirTemp==3):
                                        finalValue='0'+value
                                    else:
                                        finalValue=value

                                    print(
                                    ContLoc+ ' ' +instruction.getMnemonico()+ ' '+ instruction.getDirection()+' '+
                                    Mnemonicos[i].getModDirection()+' '+Mnemonicos[i].getLongInstruction()+' '+
                                    Mnemonicos[i].getCodOperation()
                                    )
                                    archivoFinal.write(
                                    ContLoc+ ' ' +instruction.getMnemonico()+ ' '+ instruction.getDirection()+' '+
                                    Mnemonicos[i].getModDirection()+' '+Mnemonicos[i].getLongInstruction()+' '+
                                    Mnemonicos[i].getCodOperation()+'\n'
                                    )
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break

                                elif(Len_DirTemp>=1 and Len_DirTemp<=2 and Mnemonicos[i].getModDirection()!='IMM'):
                                    if(Len_DirTemp==1):
                                        finalValue='0'+value
                                    else:
                                        finalValue=value
                                    print(
                                    ContLoc+ ' ' +instruction.getMnemonico()+ ' '+ instruction.getDirection()+' '+
                                    Mnemonicos[i].getModDirection()+' '+Mnemonicos[i].getLongInstruction()+' '+
                                    Mnemonicos[i].getCodOperation()
                                    )
                                    archivoFinal.write(
                                    ContLoc+ ' ' +instruction.getMnemonico()+ ' '+ instruction.getDirection()+' '+
                                    Mnemonicos[i].getModDirection()+' '+Mnemonicos[i].getLongInstruction()+' '+
                                    Mnemonicos[i].getCodOperation()+'\n'
                                    )
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break



"""Funcion que separa a la instruccion por campos"""
def analize(declaration):
    asm_line= declaration.split()
    asm_inst=CInstruction()
    len_inst=len(asm_line)

    if(len_inst==2):
        asm_inst.setMnemonico(asm_line[0])
        asm_inst.setDirection(asm_line[1])
    elif(len_inst==1):
        asm_inst.setMnemonico(asm_line[0])
    
    return asm_inst
    #print(asm_inst.getMnemonico(), asm_inst.getDirection())
      

"""Hexa a ENTERO DECIMAL"""  
def hex_to_dec(num_hex):
    return int(num_hex,16)
    

"""Funcion pa convertir una direccion a INT"""
def dir_to_Int(direct):
    return direct[1:len(direct)] 

"""Convierte de HEX Python a HEX ASM"""
def hex_to_dir(num_hex):
    return num_hex[2:len(num_hex)]

"""Funcion para actualizar el CONT LOC"""
def actualiza_ContLoc(contLoc,longInst):
    c=hex_to_dec(contLoc)+int(longInst)
    return hex_to_dir(hex(c))

"""Convertir direccion de cualquier base a HEXA"""
def convert_to_hex(direction):
    End_Str=len(direction)
    if(direction.find('$', 0, End_Str)!=-1):
        value=direction[1:End_Str]
    elif(direction.find('@', 0, End_Str)!=-1):
        value = hex_to_dir(hex(int(direction[1:End_Str],8)))
    elif(direction.find('%', 0, End_Str)!=-1):
        value = hex_to_dir(hex(int(direction[1:End_Str],2)))
    else:
        value = hex_to_dir(hex(int(direction)))

    return value

"""################## Programa principal ##################"""
archivoFinal = open("Practica_4.lst","w")
load_mnemonics("TABCOP.txt")
loader("P4.asm")
archivoFinal.close()
#for i in range(len(Mnemonicos)):
    #print(Mnemonicos[i].getInstruction(), Mnemonicos[i].getModDirection(), Mnemonicos[i].getCodOperation())

#print(len(value[1:len(value)]))