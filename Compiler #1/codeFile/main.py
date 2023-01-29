code = open('./../code5.txt')

#토큰코드 선언
ident = 1
const = 2
assign_op = 11
semi_colon = 12
add_op = 13
mult_op = 14
left_paren = 15
right_paren = 16

# 식별자, 연산자, 숫자의 개수 저장하는 변수
tokenDic={"ID":0,"CONST":0,"OP":0}
tokenDicList=[]
identDic={}
idConList=[]
tList=[]
lineList=[]

# 에러메시지를 리스트에 저장한 다음 한 번에 출력
error = []



def genWordList():
    wordList = []
    codeline=code.read().split('\n')
    for line in codeline:
        line=line.split(' ')
        list=[i for i in line if i]
        wordList.append(list)
    #공백 제거
    return wordList


# 단순어휘분석기
def lex(list):
    wordList=list
    for line in wordList:
        for word in line:
            #ident인지 확인
            idConList.append(word)
            idCon(word)
        tokenDicList.append(tokenDic.copy())
    return


def idCon(string):
    if string[0].isalpha()==True or string[0]=='_':
        for char in string:
            if char.isalnum()==True or char=='_':
                continue
            else:
                lookup(string)
                return
        tList.append(ident)
    elif string.isdigit()==True:
        tList.append(const)
    else:
        lookup(string)
        return


def lookup(string):
    if string == ':=' or string=='=' or string==':':
        tList.append(assign_op)
    elif string == ';':
        tList.append(semi_colon)
    elif string == '+' or string == '-':
        tList.append(add_op)
    elif string == '*' or string == '/':
        tList.append(mult_op)
    elif string == '(':
        tList.append(left_paren)
    elif string == ')':
        tList.append(right_paren)
    else:
        for i in string:
            if ord(i) <= 32:
                stringList = string.split(i)
                if idConList:
                    idConList.pop(-1)
                idConList.extend(stringList)
                print(stringList)
                for word in stringList:
                    print(word)
                    idCon(word)
                return
            elif i in ['(', ')', '+', '-', '*', '/', ';']:
                stringList = string.split(i)
                string=str(' '+i+' ').join(stringList).strip()
                stringList = string.split(' ')
                if idConList:
                    idConList.pop(-1)
                idConList.extend(stringList)
                for word in stringList:
                    idCon(word)
                return
            elif i in [':','=']:
                if ':=' in string:
                    stringList = string.split(':=')
                    string = str(' := ').join(stringList).strip()
                    stringList = string.split(' ')
                    if idConList:
                        idConList.pop(-1)
                    idConList.extend(stringList)
                    for word in stringList:
                        idCon(word)
                    return
                else:
                    stringList = string.split(i)
                    string = str(' '+i+' ').join(stringList).strip()
                    stringList = string.split(' ')
                    if idConList:
                        idConList.pop(-1)
                    idConList.extend(stringList)
                    for word in stringList:
                        idCon(word)
                    return
    return




# factor함수
def factor(list,value):
    if list[0]==left_paren:
        list.pop(0)
        lineList.append(idConList.pop(0))
        if list[0]==left_paren or list[0]==ident or list[0]==const:
            list,value=expression(list,value)
            if not list:
                lineList.append(')')
                error.append("(Warning) 닫는 괄호 추가")
            elif list[0]==right_paren:
                list.pop(0)
                lineList.append(idConList.pop(0))
            elif list[0]==left_paren:
                list.pop(0)
                idConList.pop(0)
                lineList.append(')')
                error.append("(Warning) 괄호 방향 변경")
            else:
                lineList.append(')')
                error.append('(Warning) 닫는 괄호 추가')
        elif list[0]==right_paren:
            if list[1]==ident or list[1]==const :
                error.append("(Warning) 괄호 제거: )")
                list.pop(0)
                idConList.pop(0)
                if list[0] == left_paren or list[0] == ident or list[0] == const:
                    list, value = expression(list, value)
                    if not list:
                        lineList.append(')')
                        error.append("(Warning) 닫는 괄호 추가")
                    elif list[0] == right_paren:
                        list.pop(0)
                        lineList.append(idConList.pop(0))
                    elif list[0] == left_paren:
                        list.pop(0)
                        idConList.pop(0)
                        lineList.append(')')
                        error.append("(Warning) 괄호 방향 변경")
                    else:
                        lineList.append(')')
                        error.append('(Warning) 닫는 괄호 추가')
            else:
                error.append("(Error) 해당 괄호에 맞는 right_paren을 찾을 수 없습니다.")
                list.pop(0)
                idConList.pop(0)
                list,value=factor(list,value)
        elif list[0]==assign_op or list[0]==semi_colon:
            error.append("(Warning) 한 문장에 하나만 사용 가능합니다: "+idConList.pop(0))
            list.pop(0)
            list,value=factor(list,value)
    elif list[0]==ident:
        tokenDic["ID"] += 1
        list.pop(0)
        if identDic[idConList[0]] :
            lineList.append(idConList[0])
            value=identDic[idConList.pop(0)]
        else:
            error.append("(Error) 정의되지 않은 변수(" +idConList[0]+")가 참조됨")
            identDic[idConList.pop(0)]='Unknown'
    elif list[0]==const:
        tokenDic["CONST"]+=1
        list.pop(0)
        lineList.append(idConList[0])
        value=int(idConList.pop(0))
    elif list[0]==add_op or list[0]==mult_op:
        error.append("(Warning) 중복 연산자 제거: "+idConList.pop(0))
        list.pop(0)
        list,value=factor(list,value)
    else:
        error.append("(Error) "+idConList.pop(0)+"을 인식할 수 없습니다")
        list.pop(0)
    return list,value

# factor_tail함수
def factorTail(list,value):
    if not list:
        return list,value
    elif list[0]==mult_op:
        list.pop(0)
        lineList.append(idConList[0])
        op=idConList.pop(0)
        list,temp=factor(list,value)
        tokenDic["OP"] += 1
        if value!="Unknown" and temp!="Unknown":
            if op=='*':
                value*=temp
            else:
                value/=temp
            list, value = factorTail(list, value)
        else:
            value="Unknown"
    return list,value


def term(list,value):
    list,value=factor(list,value)
    list,value=factorTail(list,value)
    return list,value


def termTail(list,value):
    if not list:
        return list,value
    elif list[0] == add_op:
        list.pop(0)
        lineList.append(idConList[0])
        op=idConList.pop(0)
        list,temp=term(list,value)
        tokenDic["OP"] += 1
        if value!="Unknown" and temp!="Unknown":
            if op=='+':
                value+=temp
            else:
                value-=temp
            list,value=termTail(list,value)
        else:
            value="Unknown"
    elif list[0]==left_paren:
        if list[1]==add_op:
            list.pop(0)
            error.append("(Warning) 괄호 오류 제거: "+idConList.pop(0))
            list, value=termTail(list,value)
    return list,value


def expression(list,value):
    list,value=term(list,value)
    list,value=termTail(list,value)
    return list,value


def statement(list):
    if list[0] == ident:
        list.pop(0)
        tokenDic["ID"]+=1
        lineList.append(idConList[0])
        id=idConList.pop(0)
        if list[0] == assign_op:
            list.pop(0)
            if idConList[0] == ':' or idConList[0] == '=':
                lineList.append(':=')
                error.append("(Warning) " + idConList[0] + "을 :=으로 변경")
            else:
                lineList.append(idConList[0])
            idConList.pop(0)
            value='Unknown'
            list,value=expression(list,value)
            identDic[id]=value
        elif list[1]==assign_op:
            error.append("(Warning) 인식할 수 없는 토큰 삭제: "+idConList.pop(0))
            list.pop(0)
            list.pop(0)
            if idConList[0] == ':' or idConList[0] == '=':
                lineList.append(':=')
                error.append("(Warning) " + idConList[0] + "을 :=으로 변경")
            else:
                lineList.append(idConList[0])
            idConList.pop(0)
            value = 'Unknown'
            list, value = expression(list, value)
            identDic[id] = value
        elif list[0]==ident:
            error.append("(Warning) assign_op가 필요합니다.")
            lineList.append(':=')
            value = 'Unknown'
            list, value = expression(list, value)
            identDic[id] = value
        else:
            error.append("(Error) assign_op가 없습니다.")
    else:
        error.append("(Error) ident가 없습니다.")
    return list


def statements(tokenList):
    tokenList=statement(tokenList)
    if not tokenList:
        print(' '.join(lineList))
        print(tokenDic)
        if error:
            for line in error:
                print(line)
        else:
            print("(OK)")
        print("Result==>",identDic)
    elif tokenList[0] == semi_colon:
        if tokenList[1] == semi_colon:
            error.append("(Warning) 중복 semicolon 제거")
            idConList.pop(0)
            tokenList.pop(0)
        tokenList.pop(0)
        lineList.append(idConList[0])
        idConList.pop(0)
        print(' '.join(lineList))
        lineList.clear()
        print(tokenDic)
        tokenDic["ID"] = 0
        tokenDic["CONST"] = 0
        tokenDic["OP"] = 0
        if error:
            for line in error:
                print(line)
            error.clear()
        else:
            print("(OK)")
        tokenList=statements(tokenList)
    elif tokenList[0]==ident:
        error.append("(Warning) statement와 statement 사이에는 semi_colon이 필요합니다.")
        lineList.append(';')
        print(' '.join(lineList))
        lineList.clear()
        print(tokenDic)
        tokenDic["ID"] = 0
        tokenDic["CONST"] = 0
        tokenDic["OP"] = 0
        if error:
            for line in error:
                print(line)
            error.clear()
        else:
            print("(OK)")
        tokenList = statements(tokenList)
    else:
        while tokenList[0]!=semi_colon:
            if not tokenList:
                error.append("(Error) 올바르지 않은 문장입니다.")
                return tokenList
            lineList.append(idConList.pop(0))
            tokenList.pop(0)
        error.clear()
        error.append("(Error) 올바르지 않은 문장입니다.")
        tokenList.pop(0)
        lineList.append(idConList[0])
        idConList.pop(0)
        print(' '.join(lineList))
        lineList.clear()
        print(tokenDic)
        tokenDic["ID"] = 0
        tokenDic["CONST"] = 0
        tokenDic["OP"] = 0
        if error:
            for line in error:
                print(line)
            error.clear()
        else:
            print("(OK)")
        tokenList = statements(tokenList)
    return tokenList

wordlist=genWordList()
lex(wordlist)
statements(tList)
