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
                ContLocAux=ContLoc
                ContLoc=dir_to_Int(ASM_Inst.getDirection())
                
            
            elif(ASM_Inst.getMnemonico()=='EQU'):
                ContLocAux=convert_to_hex(ASM_Inst.getDirection())
                print(ContLoc+ ' ' +ASM_Inst.getLabel()+' '+ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())

            elif(ASM_Inst.getMnemonico()=='START'):
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLocAux=ContLoc
                ContLoc='0000'

            elif(ASM_Inst.getMnemonico()=='BSZ'or ASM_Inst.getMnemonico()=='ZMB'):
                ammountOfBytes=ASM_Inst.getDirection()
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLocAux=ContLoc
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(ASM_Inst.getMnemonico()=='FILL'):
                FillValues=ASM_Inst.getDirection().split(',')
                ammountOfBytes=FillValues[1]
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLocAux=ContLoc
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(ASM_Inst.getMnemonico()=='FCB'):
                ArrayValues=ASM_Inst.getDirection().split(',')
                ammountOfBytes=len(ArrayValues)
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLocAux=ContLoc
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(ASM_Inst.getMnemonico()=='FCC'):
                FCC_Values=ASM_Inst.getDirection().split('/')
                #print(FCC_Values)
                Cadena=FCC_Values[1]
                ammountOfBytes=len(Cadena)
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLocAux=ContLoc
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(ASM_Inst.getMnemonico()=='DC.B'):
                if(ASM_Inst.getDirection()!=''):
                    DB_Values=ASM_Inst.getDirection().split(',')
                    ammountOfBytes=len(DB_Values)
                else:
                    ammountOfBytes=1
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLocAux=ContLoc
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(ASM_Inst.getMnemonico()=='DC.W'):
                if(ASM_Inst.getDirection()!=''):
                    DB_Values=ASM_Inst.getDirection().split(',')
                    ammountOfBytes=len(DB_Values)
                else:
                    ammountOfBytes=1
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLocAux=ContLoc
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes*2)

            elif(ASM_Inst.getMnemonico()=='END'):
                print(ContLoc+ ' ' +ASM_Inst.getMnemonico()+ ' ' + ASM_Inst.getDirection())
                ContLocAux=ContLoc

            else:
                for i in range(len(Mnemonicos)):
                    if(ASM_Inst.getMnemonico()==Mnemonicos[i].getInstruction()):
                        #Aqui van a ir los if para mnemonicos chingones
                        Dir_Temp=ASM_Inst.getDirection()

                        if(ASM_Inst.getMnemonico()=='BEQ'):
                            ContLocAux=ContLoc
                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break

                        elif(ASM_Inst.getMnemonico()=='LBEQ'):
                            ContLocAux=ContLoc
                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break
                        
                        elif(ASM_Inst.getMnemonico()=='DBEQ'):
                            ContLocAux=ContLoc
                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break

                        elif(ASM_Inst.getMnemonico()=='BNE'):
                            ContLocAux=ContLoc
                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break
                        
                        elif(ASM_Inst.getMnemonico()=='LBNE'):
                            ContLocAux=ContLoc
                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break

                        elif(ASM_Inst.getMnemonico()=='IBNE'):
                            PreImprimir(ContLoc, ASM_Inst, Mnemonicos[i])
                            ContLocAux=ContLoc
                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break

                        elif(ASM_Inst.getMnemonico()=='LDAA' and Dir_Temp.find(',', 0, len(Dir_Temp))!=-1):
                            if(Dir_Temp.find('[', 0, len(Dir_Temp))!=-1):
                                if(Mnemonicos[i].getModDirection()=='[IDX2]'):
                                    PreImprimir(ContLoc, ASM_Inst, Mnemonicos[i])
                                    ContLocAux=ContLoc
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break
                            else:
                                End_Of_n=Dir_Temp.find(',', 0, len(Dir_Temp))
                                value=Dir_Temp[0:End_Of_n]
                                if(int(value) >= -16 and int(value) <= 15):
                                    if(Mnemonicos[i].getModDirection()=='IDX'):
                                        PreImprimir(ContLoc, ASM_Inst, Mnemonicos[i])
                                        ContLocAux=ContLoc
                                        ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                        break
                            
                                if(int(value) >= 16 or int(value) <= -17):
                                    if(int(value) < 0):
                                        hex_value=tohex(int(value), 64)
                                        hex_value=hex_value[14:len(hex_value)]
                                    else:
                                        hex_value=hex(int(value))
                                        hex_value=hex_value[2:len(hex_value)]
                                        

                                    if(Mnemonicos[i].getModDirection()=='IDX1' and len(hex_value) <=2 ):
                                        PreImprimir(ContLoc, ASM_Inst, Mnemonicos[i])
                                        ContLocAux=ContLoc
                                        ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                        break
                                    
                                    elif(Mnemonicos[i].getModDirection()=='IDX2' and len(hex_value)>2):
                                        PreImprimir(ContLoc, ASM_Inst, Mnemonicos[i])
                                        ContLocAux=ContLoc
                                        ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                        break

                        elif(Mnemonicos[i].getModDirection()=='INH' and Dir_Temp==''):  #Comprobar si es inherente
                            PreImprimir(ContLoc, ASM_Inst, Mnemonicos[i])
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
                                PreImprimir(ContLoc, ASM_Inst, Mnemonicos[i])
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

                                    PreImprimir(ContLoc, ASM_Inst, Mnemonicos[i])
                                    
                                    ContLocAux=ContLoc
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break

                                elif(Len_DirTemp>=1 and Len_DirTemp<=2 and Mnemonicos[i].getModDirection()!='IMM'):
                                    if(Len_DirTemp==1):
                                        finalValue='0'+value
                                    else:
                                        finalValue=value
                                    PreImprimir(ContLoc, ASM_Inst, Mnemonicos[i])
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
                finalValue='00 '*int(ammountOfBytes)
                print(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection()+' '+'LI='+ammountOfBytes+' '+finalValue+'\n')
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(instruction.getMnemonico()=='FILL'):
                FillValues=instruction.getDirection().split(',')
                ammountOfBytes=FillValues[1]
                hex_value=hex_to_dir(hex(int(FillValues[0])))

                if(len(hex_value)==1):
                    hex_value='0'+hex_value
                
                hex_value=hex_value+' '
                finalValue=hex_value*int(ammountOfBytes)

                print(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + 
                                    instruction.getDirection()+' LI='+ammountOfBytes+' '+finalValue+'\n')
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
                    finalValue=''
                    DB_Values=instruction.getDirection().split(',')
                    ammountOfBytes=len(DB_Values)
                    for i in range(ammountOfBytes):
                        strAux=convert_to_hex(DB_Values[i])
                        if(len(strAux)==1):
                            strAux='0'+strAux+' '
                        finalValue=finalValue+strAux
                else:
                    ammountOfBytes='1'
                    finalValue='00'
                LI=str(ammountOfBytes)
                print(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection()+' '+'LI='+LI+' '+finalValue+'\n')
                ContLoc=actualiza_ContLoc(ContLoc, ammountOfBytes)

            elif(instruction.getMnemonico()=='DC.W'):
                if(instruction.getDirection()!=''):
                    finalValue=''
                    DB_Values=instruction.getDirection().split(',')
                    ammountOfBytes=len(DB_Values)

                    for i in range(ammountOfBytes):
                        strAux=convert_to_hex(DB_Values[i])
                        if(len(strAux)==3):
                            strAux='0'+strAux+' '
                        elif(len(strAux)==2):
                            strAux='00'+strAux+' '
                        elif(len(strAux)==1):
                            strAux='000'+strAux+' '
                            
                        finalValue=finalValue+strAux
                else:
                    ammountOfBytes='2'
                    finalValue='0000'
                finalBytes=ammountOfBytes*2
                LI=str(finalBytes)

                print(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection())
                archivoFinal.write(ContLoc+ ' '+instruction.getLabel()+' ' +instruction.getMnemonico()+ ' ' + instruction.getDirection()+' '+'LI='+LI+' '+finalValue+'\n')
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
                        if(instruction.getMnemonico() == 'BEQ'):
                            bandera = False
                            message = True

                            #BUSCA EL VALOR DE LA ETIQUETA
                            comprobarEtiqueta=False

                            with open("TABSIM.txt") as file:
                                lines=(line.rstrip() for line in file)
                                lines=(line for line in lines if line)

                                for line in lines:
                                    lineSim = line.split(' ')
                                    directionSim = lineSim[1]
                                    labelSim = lineSim[0]

                                    if Dir_Temp == labelSim:
                                        comprobarEtiqueta=True
                                        firstNumber = directionSim[1:len(directionSim)]
                                        break


                            if(comprobarEtiqueta == False): 
                                firstNumber = convert_to_hex(instruction.getDirection())
                                if(firstNumber=="ND"):
                                    show_Error(ContLoc, instruction, Mnemonicos[i])
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break

                            secondNumber = actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())


                            comprobarSigno = int(firstNumber,16) - int(secondNumber,16)
                            result = ' '

                            if comprobarSigno < -128 or comprobarSigno > 127:
                                show_Error(ContLoc, instruction, Mnemonicos[i])
                                ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                break

                            if comprobarSigno < 0:
                                result = tohex(comprobarSigno,64)
                                finalValue = result[16:len(result)]

                            else:
                                result = hex(int(firstNumber,16) - int(secondNumber,16))
                                finalValue = result[2:len(result)]

                            if(len(finalValue)==1):
                                finalValue='0'+finalValue

                            save_Mnemonic(ContLoc, instruction, Mnemonicos[i], finalValue)

                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break
                        
                        elif instruction.getMnemonico() == 'LBEQ':

                            bandera = False
                            message = True

                            
                            #BUSCA EL VALOR DE LA ETIQUETA
                            comprobarEtiqueta=False

                            with open("TABSIM.txt") as file:
                                lines=(line.rstrip() for line in file)
                                lines=(line for line in lines if line)

                                for line in lines:
                                    lineSim = line.split(' ')
                                    directionSim = lineSim[1]
                                    labelSim = lineSim[0]

                                    if Dir_Temp == labelSim:
                                        comprobarEtiqueta=True
                                        firstNumber = directionSim[1:len(directionSim)]
                                        break


                            if(comprobarEtiqueta == False): 
                                firstNumber = convert_to_hex(instruction.getDirection())
                                if(firstNumber=="ND"):
                                    print(ContLoc+' '+instruction.getLabel()+' ' + Mnemonicos[i].getInstruction() + ' '+ instruction.getDirection() + ' ' + Mnemonicos[i].getModDirection() + ' ' + Mnemonicos[i].getLongInstruction() + ' ' + 'ERROR')
                                    archivoFinal.write(ContLoc+' '+instruction.getLabel()+ ' ' + Mnemonicos[i].getInstruction() + ' '+ instruction.getDirection() + ' ' + Mnemonicos[i].getModDirection() + ' ' + Mnemonicos[i].getLongInstruction() + ' ' + 'ERROR' + '\n')

                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break

                            secondNumber = actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())

                            comprobarSigno = int(firstNumber,16) - int(secondNumber,16)
                            result = ' '

                            if comprobarSigno < -32768 or comprobarSigno > 32767:
                                show_Error(ContLoc, instruction, Mnemonicos[i])
                                ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                break   

                            if comprobarSigno < 0:
                                result = tohex(comprobarSigno,64)
                                finalValue = result[14:len(result)]

                            else:
                                result = hex(int(firstNumber,16) - int(secondNumber,16))
                                finalValue = result[2:len(result)]
                                
                            if(len(finalValue)==3):
                                finalValue='0'+finalValue
                            elif(len(finalValue)==2):
                                finalValue='00'+finalValue
                            elif(len(finalValue)==1):
                                finalValue='000'+finalValue

                            save_Mnemonic(ContLoc, instruction, Mnemonicos[i], finalValue)

                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break
                        
                        elif(instruction.getMnemonico()=='DBEQ'):
                            bandera = False
                            message = True

                            strAux=Dir_Temp.split(',')
                            Direction_Temp=strAux[1]
                            registro=strAux[0]
                            #BUSCA EL VALOR DE LA ETIQUETA
                            comprobarEtiqueta=False
                            
                            with open("TABSIM.txt") as file:
                                lines=(line.rstrip() for line in file)
                                lines=(line for line in lines if line)

                                for line in lines:
                                    lineSim = line.split(' ')
                                    directionSim = lineSim[1]
                                    labelSim = lineSim[0]

                                    if Direction_Temp == labelSim:
                                        comprobarEtiqueta=True
                                        firstNumber = directionSim[1:len(directionSim)]
                                        break


                            if(comprobarEtiqueta == False): 
                                firstNumber = convert_to_hex(Direction_Temp)
                                if(firstNumber=="ND"):
                                    show_Error(ContLoc, instruction, Mnemonicos[i])
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break

                            secondNumber = actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())

                            comprobarSigno = int(firstNumber,16) - int(secondNumber,16)
                            #COMPRUEBA SI ESTA FUERA DE RANGO O NO
                            #print(firstNumber+","+secondNumber)
                            if comprobarSigno < -128 or comprobarSigno > 127:
                                show_Error(ContLoc, instruction, Mnemonicos[i])
                                ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                break

                            if comprobarSigno < 0:
                                result = tohex(comprobarSigno,64)
                                finalValue = result[16:len(result)]
                                #SI EL NUMERO ES NEGATIVO, BANDERA = TRUE
                                bandera = True

                            else:
                                result = hex(int(firstNumber,16) - int(secondNumber,16))
                                finalValue = result[2:len(result)]

                            if(len(finalValue)==1):
                                finalValue='0'+finalValue
                            

                            if registro == 'A':
                                codOp = ""

                                if bandera == True:
                                    codOp = '10' + finalValue

                                else:
                                    codOp = '00' + finalValue

                            elif registro == 'B':
                                codOp = ""

                                if bandera == True:
                                    codOp = '11' + finalValue

                                else:
                                    codOp = '01' + finalValue

                            elif registro == 'D':
                                codOp = ""

                                if bandera == True:
                                    codOp = '14' + finalValue

                                else:
                                    codOp = '04' + finalValue

                            elif registro == 'X':
                                codOp = ""

                                if bandera == True:
                                    codOp = '15' + finalValue

                                else:
                                    codOp = '05' + finalValue

                            elif registro == 'Y':
                                codOp = ""

                                if bandera == True:
                                    codOp = '16' + finalValue

                                else:
                                    codOp = '06' + finalValue

                            elif registro == 'SP':
                                codOp = ""

                                if bandera == True:
                                    codOp = '17' + finalValue

                                else:
                                    codOp = '07' + finalValue

                            save_Mnemonic(ContLoc, instruction, Mnemonicos[i], codOp)

                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break

                        elif instruction.getMnemonico() == 'BNE':

                            bandera = False
                            message = True

                            #BUSCA EL VALOR DE LA ETIQUETA
                            comprobarEtiqueta=False

                            with open("TABSIM.txt") as file:
                                lines=(line.rstrip() for line in file)
                                lines=(line for line in lines if line)

                                for line in lines:
                                    lineSim = line.split(' ')
                                    directionSim = lineSim[1]
                                    labelSim = lineSim[0]

                                    if Dir_Temp == labelSim:
                                        comprobarEtiqueta=True
                                        firstNumber = directionSim[1:len(directionSim)]
                                        break


                            if(comprobarEtiqueta == False): 
                                firstNumber = convert_to_hex(instruction.getDirection())
                                if(firstNumber=="ND"):
                                    show_Error(ContLoc, instruction, Mnemonicos[i])
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break

                            secondNumber = actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            #print(firstNumber+','+secondNumber)

                            comprobarSigno = int(firstNumber,16) - int(secondNumber,16)
                            result = ' '

                            if comprobarSigno < -128 or comprobarSigno > 127:
                                show_Error(ContLoc, instruction, Mnemonicos[i])
                                ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                break

                            if comprobarSigno < 0:
                                result = tohex(comprobarSigno,64)
                                finalValue = result[16:len(result)]
                                
                            else:
                                result = hex(int(firstNumber,16) - int(secondNumber,16))
                                finalValue = result[2:len(result)]

                            if(len(finalValue)==1):
                                finalValue='0'+finalValue

                            save_Mnemonic(ContLoc, instruction, Mnemonicos[i], finalValue)

                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break

                        elif instruction.getMnemonico() == 'LBNE':

                            bandera = False
                            message = True

                            #Comprobar si tiene etiqueta
                            comprobarEtiqueta=False

                            with open("TABSIM.txt") as file:
                                lines=(line.rstrip() for line in file)
                                lines=(line for line in lines if line)

                                for line in lines:
                                    lineSim = line.split(' ')
                                    directionSim = lineSim[1]
                                    labelSim = lineSim[0]

                                    if Dir_Temp == labelSim:
                                        comprobarEtiqueta=True
                                        firstNumber = directionSim[1:len(directionSim)]
                                        break


                            if(comprobarEtiqueta == False): 
                                firstNumber = convert_to_hex(instruction.getDirection())
                                if(firstNumber=="ND"):
                                    show_Error(ContLoc, instruction, Mnemonicos[i])

                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break

                            secondNumber = actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())

                            comprobarSigno = int(firstNumber,16) - int(secondNumber,16)
                            result = ' '

                            if(comprobarSigno < -32768 or comprobarSigno > 32767):
                                show_Error(ContLoc, instruction, Mnemonicos[i])
                                ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                break

                            if(comprobarSigno < 0):
                                result = tohex(comprobarSigno,64)
                                finalValue = result[14:len(result)]

                            else:
                                result = hex(int(firstNumber,16) - int(secondNumber,16))
                                finalValue = result[2:len(result)]

                            if(len(finalValue)==3):
                                finalValue='0'+finalValue
                            elif(len(finalValue)==2):
                                finalValue='00'+finalValue
                            elif(len(finalValue)==1):
                                finalValue='000'+finalValue

                            save_Mnemonic(ContLoc, instruction, Mnemonicos[i], finalValue)

                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break

                        elif instruction.getMnemonico() == 'IBNE':
                            bandera = False
                            message = True

                            strAux=Dir_Temp.split(',')
                            Direction_Temp=strAux[1]
                            registro=strAux[0]
                            #BUSCA EL VALOR DE LA ETIQUETA
                            comprobarEtiqueta=False
                            
                            with open("TABSIM.txt") as file:
                                lines=(line.rstrip() for line in file)
                                lines=(line for line in lines if line)

                                for line in lines:
                                    lineSim = line.split(' ')
                                    directionSim = lineSim[1]
                                    labelSim = lineSim[0]

                                    if Direction_Temp == labelSim:
                                        comprobarEtiqueta=True
                                        firstNumber = directionSim[1:len(directionSim)]
                                        break


                            if(comprobarEtiqueta == False): 
                                firstNumber = convert_to_hex(Direction_Temp)
                                if(firstNumber=="ND"):
                                    show_Error(ContLoc, instruction, Mnemonicos[i])
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break

                            secondNumber = actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())

                            comprobarSigno = int(firstNumber,16) - int(secondNumber,16)
                            #COMPRUEBA SI ESTA FUERA DE RANGO O NO
                            #print(firstNumber+","+secondNumber)
                            if comprobarSigno < -128 or comprobarSigno > 127:
                                show_Error(ContLoc, instruction, Mnemonicos[i])
                                ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                break

                            if comprobarSigno < 0:
                                result = tohex(comprobarSigno,64)
                                finalValue = result[16:len(result)]
                                #SI EL NUMERO ES NEGATIVO, BANDERA = TRUE
                                bandera = True

                            else:
                                result = hex(int(firstNumber,16) - int(secondNumber,16))
                                finalValue = result[2:len(result)]

                            if(len(finalValue)==1):
                                finalValue='0'+finalValue
                            

                            if registro == 'A':
                                codOp = ""

                                if bandera == True: #Si es negativo
                                    codOp = 'B0' + finalValue

                                else:
                                    codOp = 'A0' + finalValue

                            elif registro == 'B':
                                codOp = ""

                                if bandera == True:
                                    codOp = 'B1' + finalValue

                                else:
                                    codOp = 'A1' + finalValue

                            elif registro == 'D':
                                codOp = ""

                                if bandera == True:
                                    codOp = 'B4' + finalValue

                                else:
                                    codOp = 'A4' + finalValue

                            elif registro == 'X':
                                codOp = ""

                                if bandera == True:
                                    codOp = 'B5' + finalValue

                                else:
                                    codOp = 'A5' + finalValue

                            elif registro == 'Y':
                                codOp = ""

                                if bandera == True:
                                    codOp = 'B6' + finalValue

                                else:
                                    codOp = 'A6' + finalValue

                            elif registro == 'SP':
                                codOp = ""

                                if bandera == True:
                                    codOp = 'B7' + finalValue

                                else:
                                    codOp = 'A7' + finalValue

                            save_Mnemonic(ContLoc, instruction, Mnemonicos[i], codOp)

                            ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                            break

                        elif(instruction.getMnemonico()=='LDAA' and Dir_Temp.find(',', 0, len(Dir_Temp))!=-1):
                            if(Dir_Temp.find('[', 0, len(Dir_Temp))!=-1):
                                if(Mnemonicos[i].getModDirection()=='[IDX2]'):
                                    Aux_Dir=Dir_Temp[1:len(Dir_Temp)-1]
                                    Splited_Dir=Aux_Dir.split(',')
                                    value=Splited_Dir[0]
                                    if(int(value)<0):
                                        show_Error(ContLoc, instruction, Mnemonicos[i])
                                        ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                        break

                                    else:
                                        registro=Splited_Dir[1]
                                        if(registro=='X'):
                                            XB='11100011'
                                        elif(registro=='Y'):
                                            XB='11101011'
                                        elif(registro=='SP'):
                                            XB='11110011'
                                        elif(registro=='PC'):
                                            XB='11111011'

                                            
                                        finalValue=hex(int(XB,2))
                                        finalValue=finalValue[2:len(finalValue)]
                                        hex_value=hex(int(value))
                                        hex_value=hex_value[2:len(hex_value)]

                                        if(len(hex_value)==3):
                                            hex_value='0'+hex_value
                                        elif(len(hex_value)==2):
                                            hex_value='00'+hex_value
                                        elif(len(hex_value)==1):
                                            hex_value='000'+hex_value

                                        finalValue=finalValue+' '+hex_value

                                        save_Mnemonic(ContLoc, instruction, Mnemonicos[i], finalValue)
                                        ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                        break
                            else:
                                Splited_Dir=Dir_Temp.split(',')
                                value=Splited_Dir[0]
                                registro=Splited_Dir[1]

                                if(registro=='X'):
                                    rr='00'
                                elif(registro=='Y'):
                                    rr='01'
                                elif(registro=='SP'):
                                    rr='10'
                                elif(registro=='PC'):
                                    rr='11'
                                
                                if(int(value) >= -16 and int(value) <= 15):
                                    if(Mnemonicos[i].getModDirection()=='IDX'):
                                        formula=rr+'0'

                                        if(int(value)<0):
                                            bin_Value=bindigits(int(value),5)
                                        else:
                                            bin_Value=bin(int(value))
                                            bin_Value=bin_Value[2:len(bin_Value)]
                                            if len(bin_Value) == 1:
                                                bin_Value = '0000' + bin_Value
                                            elif len(bin_Value) == 2:
                                                bin_Value = '000' + bin_Value
                                            elif len(bin_Value) == 3:
                                                bin_Value = '00' + bin_Value
                                            elif len(bin_Value) == 4:
                                                bin_Value = '0' + bin_Value

                                        formula=formula+bin_Value

                                        hex_value=hex(int(formula,2))
                                        finalValue=hex_to_dir(hex_value)

                                        save_Mnemonic(ContLoc, instruction, Mnemonicos[i], finalValue)
                                        ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                        break
                            
                                if(int(value) >= 16 or int(value) <= -17):
                                    if(int(value) < 0):
                                        s='1'

                                        hex_value=tohex(int(value), 64)
                                        if(int(value)<-127):    #Si el valor se representa con mas de un byte
                                            hex_value=hex_value[14:len(hex_value)]
                                        else:   #Si el valor se representa con un byte
                                            hex_value=hex_value[16:len(hex_value)]
                                        
                                    else:
                                        s='0'
                                        hex_value=hex(int(value))
                                        hex_value=hex_value[2:len(hex_value)]
                                        

                                    if(Mnemonicos[i].getModDirection()=='IDX1' and len(hex_value) <=2 ):
                                        z='0'
                                        formula='111'+rr+'0'+z+s

                                        hex_formula=hex(int(formula,2))
                                        hex_formula=hex_to_dir(hex_formula)

                                        finalValue=hex_formula+' '+hex_value

                                        save_Mnemonic(ContLoc, instruction, Mnemonicos[i], finalValue)
                                        ContLocAux=ContLoc
                                        ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                        break
                                    
                                    elif(Mnemonicos[i].getModDirection()=='IDX2' and len(hex_value)>2):
                                        z='1'
                                        formula='111'+rr+'0'+z+s

                                        hex_formula=hex(int(formula,2))
                                        hex_formula=hex_to_dir(hex_formula)

                                        if(len(hex_value)==3):
                                            hex_value='0'+hex_value

                                        finalValue=hex_formula+' '+hex_value

                                        save_Mnemonic(ContLoc, instruction, Mnemonicos[i], finalValue)
                                        ContLocAux=ContLoc
                                        ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                        break

                        elif(Mnemonicos[i].getModDirection()=='INH' and Dir_Temp==''):  #Comprobar si es inherente
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
                                    if(len(value)>2):
                                        show_Error(ContLoc, instruction, Mnemonicos[i])
                                        break
                                    elif(len(value)==1):
                                        finalValue='0'+value
                                    else:
                                        finalValue=value    
                                #print(finalValue)
                                
                                save_Mnemonic(ContLoc, instruction, Mnemonicos[i], finalValue)
                                ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                break

                            else:   #sino es de direccionamiento IMMM
                                comprobarEtiqueta=False

                                with open("TABSIM.txt") as file:
                                    lines=(line.rstrip() for line in file)
                                    lines=(line for line in lines if line)

                                    for line in lines:
                                        lineSim = line.split(' ')
                                        directionSim = lineSim[1]
                                        labelSim = lineSim[0]

                                        if Dir_Temp == labelSim:
                                            comprobarEtiqueta=True
                                            value = directionSim[1:len(directionSim)]
                                            break


                                if(comprobarEtiqueta == False): 
                                    value = convert_to_hex(instruction.getDirection())
                                    if(value=="ND"):
                                        show_Error(ContLoc, instruction, Mnemonicos[i])
                                        ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                        break

                                #value=convert_to_hex(Dir_Temp)
                                Len_DirTemp=len(value)
                                if(Len_DirTemp>2 and (Mnemonicos[i].getLongInstruction()=='3' or Mnemonicos[i].getLongInstruction()=='4')):
                                    if(Len_DirTemp>4):
                                        show_Error(ContLoc, instruction, Mnemonicos[i])
                                        ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                        break
                                    
                                    elif(Len_DirTemp==4):
                                        finalValue=value
                                    elif(Len_DirTemp==3):
                                        finalValue='0'+value

                                    save_Mnemonic(ContLoc, instruction, Mnemonicos[i], finalValue)
                                    ContLoc=actualiza_ContLoc(ContLoc, Mnemonicos[i].getLongInstruction())
                                    break

                                elif(Len_DirTemp>=1 and Len_DirTemp<=2 and Mnemonicos[i].getModDirection()!='IMM'):
                                    if(Len_DirTemp==1):
                                        finalValue='0'+value
                                    else:
                                        finalValue=value
                                    save_Mnemonic(ContLoc, instruction, Mnemonicos[i], finalValue)
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
    elif(direction.isdigit()):
        value = hex_to_dir(hex(int(direction)))
    else:
        value="ND"
    return value

"""Funcion para imprimir todo con el formato que pidio la maestra solo para MNEMONICOS no para directivas"""
def save_Mnemonic(ContLoc, instruction, Mnemonico, finalValue):
    print(
        ContLoc+ ' '+instruction.getLabel()+ ' ' +instruction.getMnemonico()+ ' '+ 
        instruction.getDirection()+' '+Mnemonico.getModDirection()+' '+
        Mnemonico.getLongInstruction()+' '+Mnemonico.getCodOperation()+finalValue
    )
    archivoFinal.write(
        ContLoc+ ' '+instruction.getLabel()+ ' ' +instruction.getMnemonico()+ ' '+ 
        instruction.getDirection()+' '+Mnemonico.getModDirection()+' '+
        Mnemonico.getLongInstruction()+' '+Mnemonico.getCodOperation()+' '+finalValue+'\n'
    )

"""Funcion para mostrar error con MNEMONICOS"""
def show_Error(ContLoc, instruction, Mnemonico):
    print(ContLoc+' '+instruction.getLabel()+' ' + Mnemonico.getInstruction() + ' '+ instruction.getDirection() + ' ' + Mnemonico.getModDirection() + ' ' + Mnemonico.getLongInstruction() + ' ' + 'ERROR'
    )
    archivoFinal.write(ContLoc+' '+instruction.getLabel()+' ' + Mnemonico.getInstruction() + ' '+ instruction.getDirection() + ' ' + Mnemonico.getModDirection() + ' ' + Mnemonico.getLongInstruction() + ' ' + 'ERROR' + '\n'
    )

def PreImprimir(ContLoc, ASM_Inst, Mnemonico):
    print(
        ContLoc+ ' ' +ASM_Inst.getLabel()+' ' +ASM_Inst.getMnemonico()+ ' '+ ASM_Inst.getDirection()+' '+
        Mnemonico.getModDirection()+' '+'LI='+Mnemonico.getLongInstruction()+' '+
        Mnemonico.getCodOperation()
    )

"""Convertir de decimal a hexa negativo"""
def tohex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))

def bindigits(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

"""################## Programa principal ##################"""
archivoFinal = open("Practica_12.lst","w")
load_mnemonics("TABCOP.txt")
#loader("P4.asm")
print("PRECOMPILACION\n")
PreCompile("P12.asm")
print("\nCOMPILACION\n")
loader("P12.asm")
archivoFinal.close()
#for i in range(len(Mnemonicos)):
    #print(Mnemonicos[i].getInstruction(), Mnemonicos[i].getModDirection(), Mnemonicos[i].getCodOperation())

#print(len(value[1:len(value)]))