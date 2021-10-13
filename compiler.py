import copy

from Data import CInstruction
from Data import CMnemonic

ContLoc='0000'   #Contador de localidades
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

def PreCompile(file_name):
    TabSim = open("TABSIM.txt","w")
    ASM_Inst=CInstruction()
    ContLoc='0000'
    ContLocAux=0
    with open(file_name) as file:
        #lines=(line.rstrip() for line in file)
        lines=file.readlines()
        for line in lines:
            ASM_Inst=analizar(line)
            #print(ASM_Inst.getMnemonico())
            if(ASM_Inst.getMnemonico()=='ORG'):
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLoc=dir_to_Int(ASM_Inst.getDirection())
                ContLocAux=ContLoc
            
            elif(ASM_Inst.getMnemonico()=='EQU'):
                ContLocAux=convert_to_hex(ASM_Inst.getDirection())
                print(ContLoc+ ' ' +ASM_Inst.getLabel()+' '+ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())

            elif(ASM_Inst.getMnemonico()=='START'):
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLoc='0000'

            elif(ASM_Inst.getMnemonico()=='BSZ'or ASM_Inst.getMnemonico()=='ZMB'):
                ammountOfBytes=ASM_Inst.getDirection()
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(ASM_Inst.getMnemonico()=='FILL'):
                FillValues=ASM_Inst.getDirection().split(',')
                ammountOfBytes=FillValues[1]
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(ASM_Inst.getMnemonico()=='FCB'):
                ArrayValues=ASM_Inst.getDirection().split(',')
                ammountOfBytes=len(ArrayValues)
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(ASM_Inst.getMnemonico()=='FCC'):
                FCC_Values=ASM_Inst.getDirection().split('/')
                #print(FCC_Values)
                Cadena=FCC_Values[1]
                ammountOfBytes=len(Cadena)
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(ASM_Inst.getMnemonico()=='DC.B'):
                if(ASM_Inst.getDirection()!=''):
                    DB_Values=ASM_Inst.getDirection().split(',')
                    ammountOfBytes=len(DB_Values)
                else:
                    ammountOfBytes=1
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(ASM_Inst.getMnemonico()=='DC.W'):
                if(ASM_Inst.getDirection()!=''):
                    DB_Values=ASM_Inst.getDirection().split(',')
                    ammountOfBytes=len(DB_Values)
                else:
                    ammountOfBytes=1
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes*2)

            elif(ASM_Inst.getMnemonico()=='END'):
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLocAux=ContLoc

            else:
                for i in range(len(Mnemonicos)):
                    if(ASM_Inst.getMnemonico()==Mnemonicos[i].getInstruction()):
                        #Aqui van a ir los if para mnemonicos chingones
                        Dir_Temp=ASM_Inst.getDirection()

                        if(Mnemonicos[i].getModDirection()=='INH' and Dir_Temp==''):  #Comprobar si es inherente
                            print(
                                ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' '+Mnemonicos[i].getModDirection()+' '+
                                Mnemonicos[i].getLongInstruction()+' '+Mnemonicos[i].getCodOperation()
                                )
                            ContLocAux=ContLoc
                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break

                        elif(Dir_Temp!=' '):
                            Len_DirTemp=len(Dir_Temp)
                            if(Dir_Temp.find('#',0, Len_DirTemp)!=-1):  #SI encuentra que es de direccionamiento IMM 
                                value=convert_to_hex(Dir_Temp[1:Len_DirTemp])
                                if(ASM_Inst.getMnemonico()=='ADDD'):#condicion especial si es la instruccion ADDDD
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
                                    ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection()+' '+
                                    Mnemonicos[i].getModDirection()+' '+Mnemonicos[i].getLongInstruction()+' '+
                                    Mnemonicos[i].getCodOperation()
                                )
                                ContLocAux=ContLoc
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
                                    ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' '+ ASM_Inst.getDirection()+' '+
                                    Mnemonicos[i].getModDirection()+' '+Mnemonicos[i].getLongInstruction()+' '+
                                    Mnemonicos[i].getCodOperation()
                                    )
                                    ContLocAux=ContLoc
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break

                                elif(Len_DirTemp>=1 and Len_DirTemp<=2 and Mnemonicos[i].getModDirection()!='IMM'):
                                    if(Len_DirTemp==1):
                                        finalValue='0'+value
                                    else:
                                        finalValue=value
                                    print(
                                    ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' '+ ASM_Inst.getDirection()+' '+
                                    Mnemonicos[i].getModDirection()+' '+Mnemonicos[i].getLongInstruction()+' '+
                                    Mnemonicos[i].getCodOperation()
                                    )
                                    ContLocAux=ContLoc
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break

            if (ASM_Inst.getLabel())!='':        
                #print(ASM_Inst.getLabel(),ContLocAux)            
                TabSim.write(ASM_Inst.getLabel()+' '+'$'+ContLocAux+'\n')
    TabSim.close()


instructions = []
"""Lector de archivo .asm"""
def loader(file_name):
    instruction=CInstruction()
    ContLoc='0000'
    ContLocAux=0
    with open(file_name) as file:
        lines=file.readlines()
        for line in lines:
            instruction=analizar(line)
            if(instruction.getMnemonico()=='ORG'):
                print(ContLoc+' '+instruction.getLabel() +' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())

                archivoFinal.write(ContLoc+ ' '+instruction.getLabel() +' '+instruction.getMnemonico()+ ' ' +
                                    instruction.getDirection()+'\n'
                                )
                ContLoc=dir_to_Int(instruction.getDirection())

            elif(instruction.getMnemonico()=='EQU'):
                print(ContLoc+ ' ' +instruction.getLabel()+' '+instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' ' +instruction.getLabel()+' '+instruction.getMnemonico()+ ' ' + instruction.getDirection()+'\n')

            elif(instruction.getMnemonico()=='START'):
                print(ContLoc+ ' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' ' +instruction.getLabel()+' '+instruction.getMnemonico()+'\n')
                ContLoc='0000'
            
            elif(instruction.getMnemonico()=='BSZ'or instruction.getMnemonico()=='ZMB'):
                ammountOfBytes=instruction.getDirection()
                print(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection()+'\n')
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(instruction.getMnemonico()=='FILL'):
                FillValues=instruction.getDirection().split(',')
                ammountOfBytes=FillValues[1]
                print(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection()+'\n')
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(instruction.getMnemonico()=='FCB'):
                ArrayValues=instruction.getDirection().split(',')
                ammountOfBytes=len(ArrayValues)
                print(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection()+'\n')
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(instruction.getMnemonico()=='FCC'):
                FCC_Values=instruction.getDirection().split('/')
                #print(FCC_Values)
                Cadena=FCC_Values[1]
                ammountOfBytes=len(Cadena)
                print(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection()+'\n')
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(instruction.getMnemonico()=='DC.B'):
                if(instruction.getDirection()!=''):
                    DB_Values=instruction.getDirection().split(',')
                    ammountOfBytes=len(DB_Values)
                else:
                    ammountOfBytes=1
                print(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection()+'\n')
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(instruction.getMnemonico()=='DC.W'):
                if(instruction.getDirection()!=''):
                    DB_Values=instruction.getDirection().split(',')
                    ammountOfBytes=len(DB_Values)
                else:
                    ammountOfBytes=1
                print(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection()+'\n')
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes*2)

            elif(instruction.getMnemonico()=='END'):
                print(ContLoc+ ' '+instruction.getLabel()+' '+instruction.getMnemonico()+ ' ' + instruction.getDirection())

                archivoFinal.write(ContLoc+ ' '+instruction.getLabel()+ ' ' +instruction.getMnemonico()+ ' ' +
                                    instruction.getDirection()
                                )

            else:
                for i in range(len(Mnemonicos)):
                    if(instruction.getMnemonico()==Mnemonicos[i].getInstruction()):
                        #Aqui van a ir los if para mnemonicos chingones
                        Dir_Temp=instruction.getDirection()

                        if(Mnemonicos[i].getModDirection()=='INH' and Dir_Temp==''):  #Comprobar si es inherente
                            print(
                                ContLoc+ ' '+instruction.getLabel()+ ' ' +instruction.getMnemonico()+ ' '+Mnemonicos[i].getModDirection()+' '+
                                Mnemonicos[i].getLongInstruction()+' '+Mnemonicos[i].getCodOperation()
                                )
                            archivoFinal.write(
                                ContLoc+ ' '+instruction.getLabel()+ ' ' +instruction.getMnemonico()+ ' '+Mnemonicos[i].getModDirection()+' '+
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
                                    ContLoc+ ' '+instruction.getLabel()+ ' ' +instruction.getMnemonico()+ ' ' + 
                                    instruction.getDirection()+' '+ Mnemonicos[i].getModDirection()+' '+
                                    Mnemonicos[i].getLongInstruction()+' '+Mnemonicos[i].getCodOperation()
                                )
                                archivoFinal.write(
                                    ContLoc+ ' '+instruction.getLabel()+ ' ' +instruction.getMnemonico()+ ' ' + 
                                    instruction.getDirection()+' '+ Mnemonicos[i].getModDirection()+' '+
                                    Mnemonicos[i].getLongInstruction()+' '+Mnemonicos[i].getCodOperation()+'\n'
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
                                    ContLoc+ ' '+instruction.getLabel()+ ' ' +instruction.getMnemonico()+ ' '+ 
                                    instruction.getDirection()+' '+Mnemonicos[i].getModDirection()+' '+
                                    Mnemonicos[i].getLongInstruction()+' '+Mnemonicos[i].getCodOperation()
                                    )
                                    archivoFinal.write(
                                    ContLoc+ ' '+instruction.getLabel()+ ' ' +instruction.getMnemonico()+ ' '+ 
                                    instruction.getDirection()+' '+Mnemonicos[i].getModDirection()+' '+
                                    Mnemonicos[i].getLongInstruction()+' '+Mnemonicos[i].getCodOperation()+'\n'
                                    )
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break

                                elif(Len_DirTemp>=1 and Len_DirTemp<=2 and Mnemonicos[i].getModDirection()!='IMM'):
                                    if(Len_DirTemp==1):
                                        finalValue='0'+value
                                    else:
                                        finalValue=value
                                    print(
                                    ContLoc+ ' '+instruction.getLabel()+ ' ' +instruction.getMnemonico()+ ' '+ 
                                    instruction.getDirection()+' '+Mnemonicos[i].getModDirection()+' '+
                                    Mnemonicos[i].getLongInstruction()+' '+Mnemonicos[i].getCodOperation()
                                    )
                                    archivoFinal.write(
                                    ContLoc+ ' '+instruction.getLabel()+ ' ' +instruction.getMnemonico()+ ' '+ 
                                    instruction.getDirection()+' '+Mnemonicos[i].getModDirection()+' '+
                                    Mnemonicos[i].getLongInstruction()+' '+Mnemonicos[i].getCodOperation()+'\n'
                                    )
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break



"""Funcion que separa a la instruccion por campos"""
def analize(declaration):
    asm_line= declaration.split()
    asm_inst=CInstruction()
    len_inst=len(asm_line)

    if(len_inst==3):
        asm_inst.setLabel(asm_line[0])
        asm_inst.setMnemonico(asm_line[1])
        asm_inst.setDirection(asm_line[2])
    elif(len_inst==2):
        asm_inst.setMnemonico(asm_line[0])
        asm_inst.setDirection(asm_line[1])
    elif(len_inst==1):
        asm_inst.setMnemonico(asm_line[0])
    
    return asm_inst

def analizar(declaration):
    asm_line= declaration.split(' ')
    asm_inst=CInstruction()
    asm_inst.setLabel(asm_line[0])
    asm_inst.setMnemonico(asm_line[1])
    asm_inst.setDirection(asm_line[2])
    #print(asm_inst.getLabel())
    return asm_inst

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
    New_ContLoc=hex_to_dir(hex(c))

    if(len(New_ContLoc)==3):
        New_ContLoc='0'+New_ContLoc
    elif(len(New_ContLoc)==2):
        New_ContLoc='00'+New_ContLoc
    elif(len(New_ContLoc)==1):
        New_ContLoc='000'+New_ContLoc
    
    return New_ContLoc

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
#loader("P4.asm")
print("PRECOMPILACION\n")
PreCompile("P4.asm")
print("\nCOMPILACION\n")
loader("P4.asm")
archivoFinal.close()
#for i in range(len(Mnemonicos)):
    #print(Mnemonicos[i].getInstruction(), Mnemonicos[i].getModDirection(), Mnemonicos[i].getCodOperation())

#print(len(value[1:len(value)]))