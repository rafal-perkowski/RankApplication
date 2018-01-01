#-*- coding:utf-8 -*-

# IMPORTS
from logindata import loginList
import pymysql
import hashlib
import getpass
from time import strftime, localtime

#TEXT INTRO
top500rankIntro = """
/$$$$$$$$ /$$$$$$  /$$$$$$$        /$$$$$$$   /$$$$$$   /$$$$$$        /$$$$$$$   /$$$$$$  /$$   /$$ /$$   /$$
|__  $$__//$$__  $$| $$__  $$      | $$____/  /$$$_  $$ /$$$_  $$      | $$__  $$ /$$__  $$| $$$ | $$| $$  /$$/
   | $$  | $$  \ $$| $$  \ $$      | $$      | $$$$\ $$| $$$$\ $$      | $$  \ $$| $$  \ $$| $$$$| $$| $$ /$$/ 
   | $$  | $$  | $$| $$$$$$$/      | $$$$$$$ | $$ $$ $$| $$ $$ $$      | $$$$$$$/| $$$$$$$$| $$ $$ $$| $$$$$/  
   | $$  | $$  | $$| $$____/       |_____  $$| $$\ $$$$| $$\ $$$$      | $$__  $$| $$__  $$| $$  $$$$| $$  $$  
   | $$  | $$  | $$| $$             /$$  \ $$| $$ \ $$$| $$ \ $$$      | $$  \ $$| $$  | $$| $$\  $$$| $$\  $$ 
   | $$  |  $$$$$$/| $$            |  $$$$$$/|  $$$$$$/|  $$$$$$/      | $$  | $$| $$  | $$| $$ \  $$| $$ \  $$
   |__/   \______/ |__/             \______/  \______/  \______/       |__/  |__/|__/  |__/|__/  \__/|__/  \__/
"""

#KLASA REPREZENTUJACA MODEL BAZY DANYCH
class DBModel:
    
    #LISTY KOLUMN BAZY DANYCH
    rankmonthsList=["id_rank","year_rank","month_rank"]
    countriesList=["id_cc","country","region","continent"]
    architecturesList=["id_arch","architecture"]
    segmentsList=["id_segm","segment"]
    interconnectsList=["id_interconn","interconnect","interconnect_family"]
    opsystemsList=["id_opsys","operating_system"]
    processorsList=["id_proc","processor","processor_technology","processor_speed"]
    systemfamsList=["id_sysfam","system_family"]
    manufacturersList=["id_manufact","manufacturer"]
    sitesList=["id_site","site","id_cc"]
    configurationsList=["id_config","id_proc","id_opsys","id_interconn","id_arch","id_manufact","id_sysfam","computer","processors_cores"]
    installationsList=["id_inst","id_site","id_config","id_segm","year"]
    ranksList=["id_rank","id_position","id_inst","rmax","rpeak","nmax"]
    rankusersList=["id_user","login","passwd","hashcode","email","username","userrole","accesslevel","accountstatus"]
    
    #LISTA LIST Z NAZWAMI KOLUMN
    columnNamesLists = [rankmonthsList,countriesList,architecturesList,segmentsList,interconnectsList,opsystemsList,processorsList,
                        systemfamsList,manufacturersList,sitesList,configurationsList,installationsList,ranksList,rankusersList]
    
    #LISTA NAZW TABEL
    tableNamesList = ["rankmonths","countries","architectures","segments","interconnects","opsystems","processors","systemfams","manufacturers","sites","configurations","installations","ranks","rankusers"]
    
    #LISTY DLUGOSCI POL W BAZIE DANYCH
    rankmonthsLen=[6,6,4]
    countriesLen=[3,30,40,15]
    architecturesLen=[6,20]
    segmentsLen=[6,20]
    interconnectsLen=[6,60,30]
    opsystemsLen=[6,70]
    processorsLen=[6,60,30,8]
    systemfamsLen=[6,50]
    manufacturersLen=[6,100]
    sitesLen=[6,150,3]
    configurationsLen=[6,6,6,6,6,6,6,150,11]
    installationsLen=[9,6,6,6,6]
    ranksLen=[6,6,9,12,12,10]
    rankusersLen=[6,20,20,64,30,30,20,6,6]
    
    #LISTA LIST Z DLUGOSCIAMI KOLUMN
    columnLenList = [rankmonthsLen,countriesLen,architecturesLen,segmentsLen,interconnectsLen,opsystemsLen,processorsLen,
                          systemfamsLen,manufacturersLen,sitesLen,configurationsLen,installationsLen,ranksLen,rankusersLen]
    
    #LISTY TYPOW KOLUMN BAZY DANYCH
    rankmonthsTypeList=["INTEGER","INTEGER","INTEGER"]
    countriesTypeList=["STRING","STRING","STRING","STRING"]
    architecturesTypeList=["INTEGER","STRING"]
    segmentsTypeList=["INTEGER","STRING"]
    interconnectsTypeList=["INTEGER","STRING","STRING"]
    opsystemsTypeList=["INTEGER","STRING"]
    processorsTypeList=["INTEGER","STRING","STRING","STRING"]
    systemfamsTypeList=["INTEGER","STRING"]
    manufacturersTypeList=["INTEGER","STRING"]
    sitesTypeList=["INTEGER","STRING","STRING"]
    configurationsTypeList=["INTEGER","INTEGER","INTEGER","INTEGER","INTEGER","INTEGER","INTEGER","STRING","STRING"]
    installationsTypeList=["INTEGER","INTEGER","INTEGER","INTEGER","INTEGER"]
    ranksTypeList=["INTEGER","INTEGER","INTEGER","DOUBLE","DOUBLE","INTEGER"]
    rankusersTypeList=["INTEGER","STRING","STRING","STRING","STRING","STRING","STRING","INTEGER","INTEGER"]
    
    #LISTA LIST Z TYPAMI KOLUMN
    columnTypesLists = [rankmonthsTypeList,countriesTypeList,architecturesTypeList,segmentsTypeList,interconnectsTypeList,opsystemsTypeList,processorsTypeList,
                             systemfamsTypeList,manufacturersTypeList,sitesTypeList,configurationsTypeList,installationsTypeList,ranksTypeList,rankusersTypeList]
    
    #LISTA NAZW WIDOKOW W BAZIE DANYCH
    viewsRankList = ["view_allranks_simple", "view_allranks_detailed", "view_newestrank", "view_polranks"]
    
    #LISTY PARAMETROW WIDOKOW - NAZWY I DLUGOSCI KOLUMN DO WYSWIETLENIA
    viewAllRankAList = ["RANK #", "YEAR", "MONTH", "POSITION", "SITE", "COUNTRY", "CODE", "MANUFACTURER", "PROCESSOR", "PROCESSOR SPEED [MHz]", "OPERATING SYSTEM", "ARCHITECTURE", "PROCESSORES/CORES", "RMAX [GFlop/s]", "RPEAK [GFlop/s]", "RMAX2RPEAK [%]"]
    viewAllRankAListLen = [6,6,4,6,80,30,3,50,50,8,50,20,11,12,12,10]
    viewAllRankBList = ["RANK #", "YEAR", "MONTH", "POSITION", "COMPUTER", "PROCESSORES/CORES", "COUNTRY", "CODE", "RMAX [GFlop/s]", "RPEAK [GFlop/s]", "RMAX2RPEAK [%]"]
    viewAllRankBListLen = [6,6,4,6,100,11,30,3,12,12,10]
    viewNewestRankList = ["RANK #", "YEAR", "MONTH", "POSITION", "COMPUTER", "PROCESSORES/CORES", "COUNTRY", "CODE", "RMAX [GFlop/s]", "RPEAK [GFlop/s]", "RMAX2RPEAK [%]"]
    viewNewestRankListLen = [6,6,4,6,100,11,30,3,12,12,10]
    viewPOLRank = ["RANK #", "YEAR", "MONTH", "POSITION", "SITE", "MANUFACTURER", "PROCESSOR", "PROCESSOR SPEED [MHz]", "OPERATING SYSTEM", "ARCHITECTURE", "PROCESSORES/CORES", "RMAX [GFlop/s]", "RPEAK [GFlop/s]", "RMAX2RPEAK [%]"]
    viewPOLRankLen = [6,6,4,6,80,50,50,8,50,20,11,12,12,10]
    
    #WERYFIKACJA AUTOINKREMENTACJI KLUCZA GLOWNEGO W BAZIE DANYCH
    autoIncList = [1,0,1,1,1,1,1,1,1,1,1,1,0,1]
    
    #LISTA PARAMETROW POLACZENIA Z BAZA DANYCH
    parameterslist = ["host", "user", "passwd", "db", "charset"]
    
    def __init__(self):
        #SLOWNIK [NAZWA TABELI : LISTA NAZW KOLUMN]
        self.tableNamesDictionary = self.genDictionary(self.tableNamesList, self.columnNamesLists)
        #SLOWNIK [NAZWA TABELI : LISTA DLUGOSCI KOLUMN]
        self.tableLensDictionary = self.genDictionary(self.tableNamesList, self.columnLenList)
        #SLOWNIK [NAZWA PARAMETRU : WARTOSC PARAMETRU]
        self.connectDictionary = self.genDictionary(self.parameterslist, loginList)
        #SLOWNIK [INDEKS TABELI : LISTA NAZW KOLUMN]
        self.indexNamesDictionary = self.genDictionary("", self.columnNamesLists)
        #SLOWNIK [INDEKS TABELI : LISTA DLUGOSCI KOLUMN]
        self.indexLensDictionary = self.genDictionary("", self.columnLenList)
        #SLOWNIK [INDEKS TABELI : LISTA MAX DLUGOSCI KOLUMN]
        self.maxLenDictionary = self.genMaxLenDict(self.indexNamesDictionary, self.indexLensDictionary, 100)
  
    #GENEROWANIE SLOWNIKA NA PODSTAWIE DWOCH LIST, KLUCZE: LISTA NAZW TABEL W BAZIE DANYCH, WARTOSCI: LISTA NAZW KOLUMN W TABELI BAZY DANYCH
    def genDictionary(self, keysList="", valuesList=""):
        retDict = {} 
        lenKeys = len(keysList)
        lenValues = len(valuesList)
        if (lenKeys!=0 and lenValues!=0):
            if(lenKeys == lenValues):
                for i in range(lenKeys):
                    retDict[keysList[i]] = valuesList[i]
        elif (lenKeys==0 and lenValues!=0):
            for i in range(lenValues):
                retDict[i] = valuesList[i]
        elif (lenKeys!=0 and lenValues==0):
            for i in range(lenKeys):
                retDict[keysList[i]] = i
        return retDict
    
    #OBLICZANIE MAKSYMALNEJ WARTOSCI PODANEJ LISTY WARTOSCI
    def maxValue(self, *argList):
        tmpValue = None
        if(len(argList)>0):
            tmpValue = argList[0]
            for listValue in argList:
                if(tmpValue<listValue):
                    tmpValue = listValue;
        return tmpValue;
    
    #GENEROWANIE SKROTU HASLA WEDLUG PODANEJ METODY Z BIBLIOTEKI "hashlib"
    def genPassword(self, passwordStr="", hashAlgorithm="sha256"):
        hashString = None
        if(hashAlgorithm == "md5"):
            hashString = hashlib.md5(passwordStr.encode('utf-8')).hexdigest()
        elif(hashAlgorithm == "sha1"):
            hashString = hashlib.sha1(passwordStr.encode('utf-8')).hexdigest()
        elif(hashAlgorithm == "sha224"):
            hashString = hashlib.sha224(passwordStr.encode('utf-8')).hexdigest()
        elif(hashAlgorithm == "sha256"):
            hashString = hashlib.sha256(passwordStr.encode('utf-8')).hexdigest()
        elif(hashAlgorithm == "sha384"):
            hashString = hashlib.sha384(passwordStr.encode('utf-8')).hexdigest()
        elif(hashAlgorithm == "sha512"):
            hashString = hashlib.sha512(passwordStr.encode('utf-8')).hexdigest()
        return hashString
    
    #WYDRUK SLOWNIKA NAZW KOLUMN, KLUCZE: INDEKSY TABEL, WARTOSCI: NAZWY KOLUMN
    def printNamesDict(self, dictDict):
        for i in range(len(dictDict)):
            #print(dictDict[i])
            print()
            for j in range(len(dictDict[i])):
                print(len(dictDict[i][j]), end=" ")
    
    #WYDRUK SLOWNIKA DLUGOSCI KOLUMN, KLUCZE: INDEKSY TABEL, WARTOSCI: MAKSYMALNE DLUGOSCI POL KOLUMN W BAZIE
    def printLengthsDict(self, dictDict):
        for i in range(len(dictDict)):
            #print(dictDict[i])
            print()
            for j in range(len(dictDict[i])):
                print(dictDict[i][j], end=" ")
    
    #GENEROWANIE SLOWNIKA MAKSYMALNYCH DLUGOSCI KOLUMN 
    def genMaxLenDict(self, indexNamesDict, indexLenDict, indexMaxLen):
        tmpDict = {}
        for i in range(len(indexNamesDict)):
            tmpDict[i] = []
            for j in range(len(indexNamesDict[i])):
                tmpInt = self.maxValue(len(indexNamesDict[i][j]), indexLenDict[i][j])
                if(tmpInt>indexMaxLen):
                    tmpInt = indexMaxLen
                tmpDict[i].append(tmpInt)
        return tmpDict
    
    #GENEROWANIE LISTY MAKSYMALNYCH DLUGOSCI KOLUMN
    def genMaxLenList(self, indexNamesList, indexLenList, indexMaxLen):
        tmpList = []
        for i in range(len(indexNamesList)):
            tmpInt = self.maxValue(len(indexNamesList[i]), indexLenList[i])
            if(tmpInt>indexMaxLen):
                tmpInt = indexMaxLen
            tmpList.append(tmpInt)
        return tmpList

#KLASA ZAPYTAN DO BAZY DANYCH GENEROWANYCH NA PODSTAWIE PODANYCH WZORCOW
class DBQuery:

    #PARAMETRYCZNE WZORCE ZAPYTAN DO BAZY DANYCH T-C-V (Table-Column-Value): %t - nazwa tabeli, %c - nazwa kolumny, %v - wartość kolumny
    selectFrom = ["SELECT * FROM %t;"]
    selectFromWhere = [
                    "SELECT * FROM %t WHERE %c=%v;",
                    "SELECT * FROM %t WHERE %c=%v AND %c=%v;"]
    insertIntoValues = [
                    "INSERT INTO %t (%c) VALUES (%v);",
                    "INSERT INTO %t (%c,%c) VALUES (%v,%v);",
                    "INSERT INTO %t (%c,%c,%c) VALUES (%v,%v,%v);",
                    "INSERT INTO %t (%c,%c,%c,%c) VALUES (%v,%v,%v,%v);",
                    "INSERT INTO %t (%c,%c,%c,%c,%c) VALUES (%v,%v,%v,%v,%v);",
                    "INSERT INTO %t (%c,%c,%c,%c,%c,%c) VALUES (%v,%v,%v,%v,%v,%v);",
                    "INSERT INTO %t (%c,%c,%c,%c,%c,%c,%c) VALUES (%v,%v,%v,%v,%v,%v,%v);",
                    "INSERT INTO %t (%c,%c,%c,%c,%c,%c,%c,%c) VALUES (%v,%v,%v,%v,%v,%v,%v,%v);",
                    "INSERT INTO %t (%c,%c,%c,%c,%c,%c,%c,%c,%c) VALUES (%v,%v,%v,%v,%v,%v,%v,%v,%v);",
                    "INSERT INTO %t (%c,%c,%c,%c,%c,%c,%c,%c,%c,%c) VALUES (%v,%v,%v,%v,%v,%v,%v,%v,%v,%v);"]
    #NUMER ZAPYTANIA ODPOWIADAJACY INDEKSOWI TABELI W BAZIE DANYCH
    insertIntoIndex = [1,3,0,0,1,0,2,0,0,2,7,2,4,7]
    updateSet = ["UPDATE %t SET %c=%v;"]
    updateSetWhere = [
                    "UPDATE %t SET %c=%v WHERE %c=%v;",
                    "UPDATE %t SET %c=%v WHERE %c=%v AND %c=%v;"]
    deleteFrom = ["DELETE FROM %t;"]
    deleteFromWhere = [
                    "DELETE FROM %t WHERE %c=%v;",
                    "DELETE FROM %t WHERE %c=%v AND %c=%v;"]
    
    #ZASTAPIENIE PODANEJ LICZBY ZNAKOW INNYM CIAGIEM ZNAKOW ZACZYNAJAC OD PODANEGO INDEKSU
    def replaceAt(self, listaStr, indexInt, lengthInt, insertStr):
        return listaStr[:indexInt] + str(insertStr) + listaStr[indexInt+lengthInt:]
    
    #GENEROWANIE ZAPYTANIA DO BAZY DANYCH NA PODSTAWIE WZORCA ZAPYTANIA I ZAWARTOSCI KROTKI KONFIGURACYJNEJ
    def genStatement(self, sqlStr, tupleStr):
        flagBool = True
        tupleInt = 0;
        indexInt = -1;
        tmpStr=sqlStr
        while(flagBool):
            indexInt = tmpStr.find("%")
            if(indexInt != -1):
                if(tupleStr[tupleInt] == None):
                    tmpStr = self.replaceAt(tmpStr, indexInt, 2, "null")
                elif(isinstance(tupleStr[tupleInt],str) and tmpStr[indexInt+1] == "v"):
                    tmpStr = self.replaceAt(tmpStr, indexInt, 2, "'" + tupleStr[tupleInt] + "'")
                else:
                    tmpStr = self.replaceAt(tmpStr, indexInt, 2, tupleStr[tupleInt])
            else:
                flagBool = False
            tupleInt += 1
        return tmpStr

#KLASA WYKORZYSTYWANA DO ZESTAWIENIA I ZAKONCZENIA POLACZENIA Z BAZA DANYCH
class DBConnection:
    
    def __init__(self, hostStr="", userStr="", passwdStr="", databaseStr="", charsetStr="", portInt=None, dbConnection=None, dbCursor=None):
        self.hostStr = hostStr
        self.userStr = userStr
        self.passwdStr = passwdStr
        self.databaseStr = databaseStr
        self.charsetStr = charsetStr
        self.portInt = portInt
        self.dbConnection = dbConnection
        self.dbCursor = dbCursor

    #ZWRACA REFERENCJE BIEZACEGO POLACZENIA DO BAZY DANYCH
    def getConnection(self):
        return self.dbConnection
    
    #ZWRACA REFERENCJE BIEZACEGO KURSORA DO BAZY DANYCH
    def getCursor(self):
        return self.dbCursor
    
    #ZESTAWIENIE POLACZENIA Z BAZA DANYCH
    def openConnection(self, hostStr="", userStr="", passwdStr="", databaseStr="", charsetStr="utf8mb4", portInt=3306):      
        try:
            if(not (bool(hostStr) and bool(userStr) and bool(passwdStr) and bool(databaseStr) and bool(portInt)) and bool(loginList)):
                self.dbConnection = pymysql.connect(loginList[0], loginList[1], loginList[2], loginList[3], charset=loginList[4], port=loginList[5])
                self.dbCursor = self.dbConnection.cursor()
                print("DBConnection: Połączenie z bazą danych zostało ustanowione!")
            else:
                self.hostStr = hostStr
                self.userStr = userStr
                self.passwdStr = passwdStr
                self.databaseStr = databaseStr
                self.charsetStr = charsetStr
                self.portInt = portInt
                self.dbConnection = pymysql.connect(self.hostStr, self.userStr, self.passwdStr, self.databaseStr, charset=self.charsetStr, port=self.portInt)
                self.dbCursor = self.dbConnection.cursor()
                print("DBConnection: Połączenie z bazą danych zostało ustanowione!")
        except:
            print("DBConnection: Błąd połączenia z bazą danych!")
        return self.dbConnection

    #ZAMKNIECIE POLACZENIA Z BAZA DANYCH
    def closeConnection(self):
        if(bool(self.dbConnection)):
            self.dbConnection.close()
            print("DBConnection: Połączenie z bazą danych zostało zakończone!")
    
    #ZWRACA CIAG ZNAKOW BEDACY SUMA WARTOSCI POL SKLADOWYCH OBIEKTU
    def __str__(self):
        return "[Host]: " + str(self.hostStr) + ", [User]: " + str(self.userStr) + ", [Password]: " + str(self.passwdStr) + ", [Database]: " + str(self.databaseStr) + ", [Charset]: "  + str(self.charsetStr)

#KLASA GRUPUJACA FUNKCJE DRUKOWANIA SFORMATOWANYCH TABEL BAZY DANYCH
class DBViewController:

    #DRUKOWANIE NAGLOWKA TABELI
    def printHeader(self, colList, lenList, sepStr, offsetStr):
        tmpString = sepStr
        for listValue in range(len(colList)):
            tmpString = tmpString + offsetStr + colList[listValue].upper().center(lenList[listValue]+len(offsetStr)) + sepStr
        return tmpString

    #GENEROWANIE FORMATU WYDRUKU TABELI
    def genStringFormat(self, lenList, sepStr, offsetStr):
        formatStr = sepStr
        for listValue in range(len(lenList)):
            formatStr = formatStr + offsetStr + "%-" + str(lenList[listValue]+len(offsetStr)) + "." + str(lenList[listValue]) +"s" + sepStr
        return formatStr

    #DRUKOWANIE WIERSZY TABELI
    def printTabRows(self, formatStr, tupleStr):
        print(formatStr % tupleStr)
    
    #DRUKOWANIE TABELI 
    def printTable(self, fetchResult, columnNamesList, maxLenList, sepStr, offsetStr):
        print(self.printHeader(columnNamesList, maxLenList, sepStr, offsetStr))
        formatStr = self.genStringFormat(maxLenList, sepStr, offsetStr)
        for i in range(len(fetchResult)):
            self.printTabRows(formatStr, fetchResult[i])

    #FUNKCJA ZWRACAJACA PRAWDE/FAŁSZ ZALEZNIE OD WYBRANEJ OPCJI PRZEZ UZYTKOWNIKA
    def choiceInput(self, introStr, errorStr, trueStr, falseStr):
        flagWhileBool = True
        flagReturnBool = False
        while(flagWhileBool):
            inputStr = input(introStr)
            if(inputStr.upper() == trueStr.upper()):
                flagReturnBool = True
                flagWhileBool = False
            elif(inputStr.upper() == falseStr.upper()):
                flagReturnBool = False
                flagWhileBool = False
            else:
                print(errorStr)
        return flagReturnBool

    #FUNCKJA WYSWIETLAJACA SFORMATOWANA STRONE WYBRANEJ TABELI
    def displayFetchRows(self, dbCursor, columnNamesList, maxLenList, displayInt=50):
        flagWhileBool = True
        countRowsInt = 0
        fetchRows = dbCursor.fetchall()
        fetchRowsLen = len(fetchRows)
        if(fetchRowsLen == 0):
            print("Brak rekordów wynikowych!")
        else:
            print("W tabeli znaleziono: [" + str(fetchRowsLen) + "] rekordów!")
            print()
            while(flagWhileBool):
                displayRows = fetchRows[countRowsInt : countRowsInt + displayInt]
                countRowsInt += displayInt
                self.printTable(displayRows, columnNamesList, maxLenList, "|", " ")
                if(len(displayRows) < displayInt):
                    flagWhileBool = False
                else:
                    flagWhileBool = self.choiceInput("[E]-EXIT, [ENTER]-DALEJ?", "Błędny wybór", "", "e")

#KLASA OBSLUGUJACA LOGOWANIE DO BAZY DANYCH
class DBLoginController:
    
    def __init__(self, dbConnection=None, dbCursor=None):
        self.dbQuery = DBQuery()
        self.dbConnection = dbConnection
        self.dbCursor = dbCursor
        self.flagAdmin = False
        self.flagUser = False
    
    #FUNKCJA POPRAWNEGO LOGOWANIA DO BAZY DANYCH
    def loginDB(self):
        flagReturnBool = False
        loginCounterInt = 0
        flagWhileBool = True
        while(flagWhileBool):
            print()
            loginCounterInt += 1
            print("[" + strftime("%Y.%m.%d %H:%M:%S", localtime()) + "]")
            self.loginStr = input("LOGIN: ")
            self.passwordStr = getpass.getpass("PASSWORD: ")
            try:
                statementStr = self.dbQuery.genStatement(self.dbQuery.selectFromWhere[1],("rankusers","login",self.loginStr,"passwd",self.passwordStr))
                self.dbCursor.execute(statementStr)
                fetchRows = self.dbCursor.fetchall()
                if(bool(fetchRows)):
                    flagWhileBool = False
                    flagReturnBool = True
                    userroleStr = fetchRows[0][6]
                    if(userroleStr == "admin"):
                        self.flagAdmin = True
                    elif(userroleStr == "user"):
                        self.flagUser = True
                    else:
                        print("Niezdefiniowana rola w bazie danych!")
                        flagReturnBool = False
                elif(loginCounterInt>2):
                    flagWhileBool = False
                    flagReturnBool = False
                    print("Przekroczono limit błędnych prób logowania!")
                else:
                    print("Błędne dane logowania!")
            except:
                print("Błąd wykonania zapytania w bazie danych!")
        return flagReturnBool


#KLASA KONTROLUJACA INTERFEJS ADMINISTRATORA BAZY DANYCH
class DBAdminController:
    
    def __init__(self, dbConnection=None, dbCursor=None):
        self.dbModel = DBModel()
        self.dbQuery = DBQuery()
        self.dbConnection = dbConnection
        self.dbCursor = dbCursor
        self.dbViewController = DBViewController()

    #OBSLUGA INTERAKCJI Z UZYTKOWNIKIEM NA POTRZEBY ZAPYTANIA INSERT
    def insertInput(self, indexTab):
        inputList = []
        inputList.append(self.dbModel.tableNamesList[indexTab])
        print("Wprowadz dane dla poszczegolnych kolumn (ENTER => NULL): ")
        for i in range(len(self.dbModel.columnNamesLists[indexTab])):
            if(i==0 and self.dbModel.autoIncList[indexTab]==1):
                continue;
            else:
                inputList.append(self.dbModel.columnNamesLists[indexTab][i])        
        for i in range(len(self.dbModel.columnNamesLists[indexTab])):
            if(i==0 and self.dbModel.autoIncList[indexTab]==1):
                continue;
            else:
                inputStr = input("[" + self.dbModel.columnTypesLists[indexTab][i] + "(" + str(self.dbModel.columnLenList[indexTab][i]) + ") " + self.dbModel.columnNamesLists[indexTab][i] +"]: ")
                if(inputStr == ""):
                    inputStr = None
                inputList.append(inputStr)
        return tuple(inputList)
    
    #OBSLUGA INTERAKCJI Z UZYTKOWNIKIEM NA POTRZEBY ZAPYTANIA DELETE
    def deleteInput(self, indexTab, indexCol):
        inputList = []
        inputList.append(self.dbModel.tableNamesList[indexTab])
        print("Podaj wartość wybranej kolumny:")
        inputStr = input("[" + self.dbModel.columnTypesLists[indexTab][indexCol] + "(" + str(self.dbModel.columnLenList[indexTab][indexCol]) + ") " + self.dbModel.columnNamesLists[indexTab][indexCol] +"]: ")
        if(inputStr == ""):
            inputStr = None
        inputList.append(self.dbModel.columnNamesLists[indexTab][indexCol])
        inputList.append(inputStr)
        if(indexTab == 12 and (indexCol==0 or indexCol==1)):
            flagBool = self.dbViewController.choiceInput("Czy chcesz podać wartość drugiej kolumny klucza (t/n)?","","t","n")
            if(flagBool):
                print("Podaj wartość ID modyfikowanego wiersza tabeli:")
                if(indexCol==0):
                    tmpIndex = 1
                else:
                    tmpIndex=0
                inputStr = input("[" + self.dbModel.columnTypesLists[indexTab][tmpIndex] + "(" + str(self.dbModel.columnLenList[indexTab][tmpIndex]) + ") " + self.dbModel.columnNamesLists[indexTab][tmpIndex] +"]: ")
                if(inputStr == ""):
                    inputStr = None
                inputList.append(self.dbModel.columnNamesLists[indexTab][tmpIndex])
                inputList.append(inputStr)
        return tuple(inputList)
    
    #OBSLUGA INTERAKCJI Z UZYTKOWNIKIEM NA POTRZEBY ZAPYTANIA UPDATE
    def updateInput(self, indexTab, indexCol):
        inputList = []
        inputList.append(self.dbModel.tableNamesList[indexTab])
        print("Podaj wartość wybranej kolumny:")
        inputStr = input("[" + self.dbModel.columnTypesLists[indexTab][indexCol] + "(" + str(self.dbModel.columnLenList[indexTab][indexCol]) + ") " + self.dbModel.columnNamesLists[indexTab][indexCol] +"]: ")
        if(inputStr == ""):
            inputStr = None
        inputList.append(self.dbModel.columnNamesLists[indexTab][indexCol])
        inputList.append(inputStr)
        print("Podaj wartość ID modyfikowanego wiersza tabeli:")
        inputStr = input("[" + self.dbModel.columnTypesLists[indexTab][0] + "(" + str(self.dbModel.columnLenList[indexTab][0]) + ") " + self.dbModel.columnNamesLists[indexTab][0] +"]: ")
        if(inputStr == ""):
            inputStr = None
        inputList.append(self.dbModel.columnNamesLists[indexTab][0])
        inputList.append(inputStr)
        if(indexTab == 12):
            print("Podaj wartość ID modyfikowanego wiersza tabeli:")
            inputStr = input("[" + self.dbModel.columnTypesLists[indexTab][1] + "(" + str(self.dbModel.columnLenList[indexTab][1]) + ") " + self.dbModel.columnNamesLists[indexTab][1] +"]: ")
            if(inputStr == ""):
                inputStr = None
            inputList.append(self.dbModel.columnNamesLists[indexTab][1])
            inputList.append(inputStr)
        print(tuple(inputList))
        return tuple(inputList)

    #WYKONANIE ZAPYTANIA SELECT W BAZIE DANYCH
    def selectDB(self, indexTab):
        selectBool = None
        try:
            statementStr = self.dbQuery.genStatement(self.dbQuery.selectFrom[0],(self.dbModel.tableNamesList[indexTab],))
            self.dbCursor.execute(statementStr)
            self.dbViewController.displayFetchRows(self.dbCursor, self.dbModel.columnNamesLists[indexTab], self.dbModel.maxLenDictionary[indexTab])
            print()
            selectBool = True
        except:
            print("Błąd wykonania zapytania SELECT w bazie danych!")
            selectBool = False
        return selectBool

    #WYKONANIE ZAPYTANIA INSERT W BAZIE DANYCH
    def insertDB(self, indexTab):
        insertBool = None    
        try:
            sqlTuple = self.insertInput(indexTab)
            statementStr = self.dbQuery.genStatement(self.dbQuery.insertIntoValues[self.dbQuery.insertIntoIndex[indexTab]],sqlTuple)
            self.dbCursor.execute(statementStr)
            self.dbConnection.commit()
            insertBool = True
        except:
            print("Błąd wykonania zapytania INSERT w bazie danych!")
            insertBool = False
        return insertBool

    #WYKONANIE ZAPYTANIA UPDATE W BAZIE DANYCH
    def updateDB(self, indexTab, indexCol):
        updateBool = None
        try:
            tupleStr = self.updateInput(indexTab, indexCol)
            if(indexTab!=12):
                statementStr = self.dbQuery.genStatement(self.dbQuery.updateSetWhere[0],tupleStr)
            else:
                statementStr = self.dbQuery.genStatement(self.dbQuery.updateSetWhere[1],tupleStr)
            self.dbCursor.execute(statementStr)
            self.dbConnection.commit()
            updateBool = True
        except:
            print("Błąd wykonania zapytania UPDATE w bazie danych!")
            updateBool = False
        return updateBool
    
    #WYKONANIE ZAPYTANIA DELETE W BAZIE DANYCH
    def deleteDB(self, indexTab, indexCol):
        deleteBool = None
        try:
            tupleStr = self.deleteInput(indexTab, indexCol)
            if(indexTab==12 and len(tupleStr)==5):
                statementStr = self.dbQuery.genStatement(self.dbQuery.deleteFromWhere[1],tupleStr)
            else:
                statementStr = self.dbQuery.genStatement(self.dbQuery.deleteFromWhere[0],tupleStr)
            self.dbCursor.execute(statementStr)
            self.dbConnection.commit()
            deleteBool = True
        except:
            print("Błąd wykonania zapytania DELETE w bazie danych!")
            deleteBool = False
        return deleteBool

#KLASA KONTROLUJACA INTERFEJS UZYTKOWNIKA BAZY DANYCH
class DBUserController:
    
    def __init__(self, dbConnection=None, dbCursor=None):
        self.dbModel = DBModel()
        self.dbQuery = DBQuery()
        self.dbConnection = dbConnection
        self.dbCursor = dbCursor
        self.dbViewController = DBViewController()

    #ZAPYTANIE SELECT DLA WIDOKU "view_allranks_detailed"
    def selectDBViewA(self):
        selectBool = None
        try:
            statementStr = self.dbQuery.genStatement(self.dbQuery.selectFrom[0],("view_allranks_detailed",))
            self.dbCursor.execute(statementStr)
            self.dbViewController.displayFetchRows(self.dbCursor, self.dbModel.viewAllRankAList, self.dbModel.genMaxLenList(self.dbModel.viewAllRankAList, self.dbModel.viewAllRankAListLen, 80))
            print()       
            selectBool = True
        except:
            print("Błąd wykonania zapytania SELECT w bazie danych!")
            selectBool = False
        return selectBool
    
    #ZAPYTANIE SELECT DLA WIDOKU "view_allranks_simple"
    def selectDBViewB(self):
        selectBool = None
        try:
            statementStr = self.dbQuery.genStatement(self.dbQuery.selectFrom[0],("view_allranks_simple",))
            self.dbCursor.execute(statementStr)
            self.dbViewController.displayFetchRows(self.dbCursor, self.dbModel.viewAllRankBList, self.dbModel.genMaxLenList(self.dbModel.viewAllRankBList, self.dbModel.viewAllRankBListLen, 80))
            print()       
            selectBool = True
        except:
            print("Błąd wykonania zapytania SELECT w bazie danych!")
            selectBool = False
        return selectBool
    
    #ZAPYTANIE SELECT DLA WIDOKU "view_newestrank"
    def selectDBViewC(self):
        selectBool = None
        try:
            statementStr = self.dbQuery.genStatement(self.dbQuery.selectFrom[0],("view_newestrank",))
            self.dbCursor.execute(statementStr)
            self.dbViewController.displayFetchRows(self.dbCursor, self.dbModel.viewNewestRankList, self.dbModel.genMaxLenList(self.dbModel.viewNewestRankList, self.dbModel.viewNewestRankListLen, 80))
            print()       
            selectBool = True
        except:
            print("Błąd wykonania zapytania SELECT w bazie danych!")
            selectBool = False
        return selectBool

    #ZAPYTANIE SELECT DLA WIDOKU "view_polranks"
    def selectDBViewD(self):
        selectBool = None
        try:
            statementStr = self.dbQuery.genStatement(self.dbQuery.selectFrom[0],("view_polranks",))
            self.dbCursor.execute(statementStr)
            self.dbViewController.displayFetchRows(self.dbCursor, self.dbModel.viewPOLRank, self.dbModel.genMaxLenList(self.dbModel.viewPOLRank, self.dbModel.viewPOLRankLen, 80))
            print()       
            selectBool = True
        except:
            print("Błąd wykonania zapytania SELECT w bazie danych!")
            selectBool = False
        return selectBool

#KLASA WYSWIETLAJACA MENU LOGOWANIA, ADMINISTRATORA I UZYTKOWNIKA
class DBMenu:
    
    menuAList = ["SELECT", "INSERT", "UPDATE", "DELETE", "-QUIT-"]
    optionsAList = [["1","S"], ["2","I"], ["3","U"], ["4", "D"], ["5", "Q"]]
    menuBList = ["ONE", "ALL", "BACK"]
    optionsBList = [["1","O"], ["2","C"], ["3","B"]]
    menuTabList = ["--BACK--"]
    optionsTabList = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","B"]
    optionsColList = ["1","2","3","4","5","6","7","8","9","10"]
    menuUList = ["DETAILED RANK", "SIMPLIFIED RANK", "NEWEST RANK", "POLAND IN RANKS","---EXIT---"]
    optionsUList = [["1","A"], ["2","B"], ["3","C"], ["4", "D"], ["5", "Q"]]
    flagAdmin = False
    flagUser = False
    
    def __init__(self):
        self.dbModel = DBModel()
        self.menuTabList = self.dbModel.tableNamesList + self.menuTabList
        self.dbQuery = DBQuery()
        self.dbDBConnection = DBConnection()
        self.dbConnection = self.dbDBConnection.openConnection()
        self.dbCursor = self.dbDBConnection.getCursor()
        if(bool(self.dbConnection) and bool(self.dbCursor)):
            self.mainMenu()

    #MENU GLOWNE
    def mainMenu(self):
        if(self.loginMenu()):
            if(self.flagAdmin):    
                self.adminMenu()
            elif(self.flagUser):
                self.userMenu()
        else:
            print("Wyjście z programu!")
            print()
            self.closeDBConnection()

    #MENU LOGOWANIA
    def loginMenu(self):
        dbLoginController = DBLoginController(self.dbConnection, self.dbCursor)
        print(top500rankIntro)
        print()
        retBool = dbLoginController.loginDB()
        if(retBool):
            self.flagAdmin=dbLoginController.flagAdmin
            self.flagUser=dbLoginController.flagUser
        return retBool

    #MENU ADMINISTRATORA
    def adminMenu(self):
        dbAdminController = DBAdminController(self.dbConnection, self.dbCursor)
        flagABool = True
        while(flagABool):
            print()
            print(self.datetimeTag())
            self.printMenuOptionsA(self.menuAList, self.optionsAList, " - ", "\n")
            inputStr = input("Wybierz opcję: ")
            print()
            if(inputStr == "1" or inputStr.upper() == "S"):
                flagBBool = True
                while(flagBBool):
                    print(self.datetimeTag())
                    print("[*** SELECT MENU ***]")
                    self.printMenuOptionsB(self.menuTabList, self.optionsTabList, " - ", "\n", True)
                    inputStr = input("Wybierz nr tabeli do wyświetlenia danych: ")
                    print()
                    if(inputStr.isnumeric() and int(inputStr)>0 and int(inputStr)<15):
                        indexTab = int(inputStr)-1
                        dbAdminController.selectDB(indexTab)
                    elif(inputStr.upper() == "B"):
                        flagBBool = False
                    else:
                        print("Wybierz opcję z MENU!")
                        print()
            elif(inputStr == "2" or inputStr.upper() == "I"):
                flagBBool = True
                while(flagBBool):
                    print(self.datetimeTag())
                    print("[*** INSERT MENU ***]")
                    self.printMenuOptionsB(self.menuTabList, self.optionsTabList, " - ", "\n", True)
                    inputStr = input("Wybierz nr tabeli do wprowadzenia danych: ")
                    print()
                    if(inputStr.isnumeric() and int(inputStr)>0 and int(inputStr)<15):
                        indexTab = int(inputStr)-1
                        dbAdminController.selectDB(indexTab)
                        dbAdminController.insertDB(indexTab)
                        dbAdminController.selectDB(indexTab)
                    elif(inputStr.upper() == "B"):
                        flagBBool = False
                    else:
                        print("Wybierz opcję z MENU!")
                        print()
            elif(inputStr == "3" or inputStr.upper() == "U"):
                flagBBool = True     
                while(flagBBool):
                    print(self.datetimeTag())
                    print("[*** UPDATE MENU ***]")
                    self.printMenuOptionsB(self.menuTabList, self.optionsTabList, " - ", "\n", True)
                    inputStr = input("Wybierz nr tabeli do modyfikacji danych: ")
                    print()
                    if(inputStr.isnumeric() and int(inputStr)>0 and int(inputStr)<15):
                        indexTab = int(inputStr)-1
                        dbAdminController.selectDB(indexTab)
                        flagCBool = True
                        while(flagCBool):
                            self.printMenuOptionsC(self.dbModel.columnNamesLists[indexTab], " - ", "\n", True)
                            inputStr = input("Wybierz nr kolumny do modyfikacji danych: ")
                            print()
                            if(inputStr.isnumeric() and int(inputStr)>0 and int(inputStr)<=len(self.dbModel.columnNamesLists[indexTab])):
                                indexCol = int(inputStr)-1
                                dbAdminController.updateDB(indexTab, indexCol)
                                dbAdminController.selectDB(indexTab)
                            elif(inputStr.upper() == "B"):
                                flagCBool = False
                            else:
                                print("Wybierz opcję z MENU!")
                                print()
                    elif(inputStr.upper() == "B"):
                        flagBBool = False
                    else:
                        print("Wybierz opcję z MENU!")
                        print()
            elif(inputStr == "4" or inputStr.upper() == "D"):
                flagBBool = True     
                while(flagBBool):
                    print(self.datetimeTag())
                    print("[*** DELETE MENU ***]")
                    self.printMenuOptionsB(self.menuTabList, self.optionsTabList, " - ", "\n", True)
                    inputStr = input("Wybierz nr tabeli do usunięcia danych: ")
                    print()
                    if(inputStr.isnumeric() and int(inputStr)>0 and int(inputStr)<15):
                        indexTab = int(inputStr)-1
                        dbAdminController.selectDB(indexTab)
                        flagCBool = True
                        while(flagCBool):
                            self.printMenuOptionsC(self.dbModel.columnNamesLists[indexTab], " - ", "\n", True)
                            inputStr = input("Wybierz nr kolumny do usunięcia danych: ")
                            print()
                            if(inputStr.isnumeric() and int(inputStr)>0 and int(inputStr)<=len(self.dbModel.columnNamesLists[indexTab])):
                                indexCol = int(inputStr)-1
                                dbAdminController.deleteDB(indexTab, indexCol)
                                dbAdminController.selectDB(indexTab)
                            elif(inputStr.upper() == "B"):
                                flagCBool = False
                            else:
                                print("Wybierz opcję z MENU!")
                                print()
                        print()
                    elif(inputStr.upper() == "B"):
                        flagBBool = False
                    else:
                        print("Wybierz opcję z MENU!")
                        print()
            elif(inputStr == "5" or inputStr.upper() == "Q"):
                flagABool = False
                print("Wylogowanie i wyjście z programu!")
                print()
                self.closeDBConnection()
            else:
                print("Wybierz opcję z MENU!")

    #MENU UZYTKOWNIKA
    def userMenu(self):
        dbUserController = DBUserController(self.dbConnection, self.dbCursor)
        flagABool = True
        while(flagABool):
            print()
            print(self.datetimeTag())
            self.printMenuOptionsA(self.menuUList, self.optionsUList, " - ", "\n")
            inputStr = input("Wybierz opcję: ")
            print()
            if(inputStr == "1" or inputStr.upper() == "A"):
                dbUserController.selectDBViewA()
            elif(inputStr == "2" or inputStr.upper() == "B"):
                dbUserController.selectDBViewB()
            elif(inputStr == "3" or inputStr.upper() == "C"):
                dbUserController.selectDBViewC()
            elif(inputStr == "4" or inputStr.upper() == "D"):
                dbUserController.selectDBViewD()
            elif(inputStr == "5" or inputStr.upper() == "Q"):
                flagABool = False
                print("Wylogowanie i wyjście z programu!")
                print()
                self.closeDBConnection()
            else:
                print("Wybierz opcję z MENU!")

    #DRUKOWANIE UPROSZCZONEGO MENU BEZ PODANEJ ODDZIELNIE LISTY OPCJI
    def printMenu(self, menuList, offsetStr, sepStr, caseBool=None):
        for i in range(len(menuList)):
            if(caseBool == True):
                print(menuList[i].upper() + offsetStr + sepStr, end = "")
            elif(caseBool == False):
                print(menuList[i].lower() + offsetStr + sepStr, end = "")
            else:
                print(menuList[i] + offsetStr + sepStr, end = "")

    #DRUKOWANIE MENU [A] Z PODANA LISTA OPCJI
    def printMenuOptionsA(self, menuList, optionsList, offsetStr, sepStr, caseBool=None):
        for i in range(len(menuList)):
            if(caseBool == True):
                print("[" + str(optionsList[i][0]) + "|" + optionsList[i][1] + "]" + offsetStr + "[" + menuList[i].upper() + "]" + sepStr, end = "")
            elif(caseBool == False):
                print("[" + str(optionsList[i][0]) + "|" + optionsList[i][1] + "]" + offsetStr + "[" + menuList[i].lower() + "]" + sepStr, end = "")
            else:
                print("[" + str(optionsList[i][0]) + "|" + optionsList[i][1] + "]" + offsetStr + "[" + menuList[i] + "]" + sepStr, end = "")
    
    #DRUKOWANIE MENU [B] Z PODANA LISTA OPCJI
    def printMenuOptionsB(self, menuList, optionsList, offsetStr, sepStr, caseBool=None):
        leadStr = ""
        for i in range(len(menuList)):
            if(len(optionsList[i])<2):
                leadStr = " "
            else:
                leadStr = ""
            if(caseBool == True):
                print(leadStr + "[" + optionsList[i] + "]" + offsetStr + "[" + menuList[i].upper() + "]" + sepStr, end = "")
            elif(caseBool == False):
                print(leadStr + "[" + optionsList[i] + "]" + offsetStr + "[" + menuList[i].lower() + "]" + sepStr, end = "")
            else:
                print(leadStr + "[" + optionsList[i] + "]" + offsetStr + "[" + menuList[i] + "]" + sepStr, end = "")
    
    #DRUKOWANIE MENU [C] BEZ PODANEJ ODDZIELNIE LISTY OPCJI
    def printMenuOptionsC(self, menuList, offsetStr, sepStr, caseBool=None):
        leadStr = ""
        for i in range(len(menuList)):
            if(caseBool == True):
                print(leadStr + "[" + str(i+1) + "]" + offsetStr + "[" + menuList[i].upper() + "]" + sepStr, end = "")
            elif(caseBool == False):
                print(leadStr + "[" + str(i+1) + "]" + offsetStr + "[" + menuList[i].lower() + "]" + sepStr, end = "")
            else:
                print(leadStr + "[" + str(i+1) + "]" + offsetStr + "[" + menuList[i] + "]" + sepStr, end = "")
        print(leadStr + "[B]" + offsetStr + "[---BACK---]" + sepStr, end = "")

    #WYWOLANIE FUNKCJI ZAMKNIECIA POLACZENIA Z BAZA DANYCH
    def closeDBConnection(self):
        if(bool(self.dbConnection)):
            self.dbDBConnection.closeConnection()
    
    #ZWRACA LOKALNA DATE I CZAS W POSTACI CIAGU ZNAKOW
    def datetimeTag(self):
        return "[" + strftime("%Y.%m.%d %H:%M:%S", localtime()) + "]"

main=DBMenu()
