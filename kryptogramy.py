import operator

class Kryptogram:

    def __init__(self, szyfr): # tworzymy kryptogram dla zaszyfrowanej linii tekstu
        self.tablica_znaków = []  # przechowywane tu będą znaki użyte kryptogramie
        bez_znakow_bialych = str(szyfr).strip()
        znaki_do_badania = bez_znakow_bialych.split(' ') # obrabiamy tekst
        
        for znak in znaki_do_badania:
            z = chr(int(znak,2))
            self.tablica_znaków.append(z) # zmieniamy szyfr w systemie dwójkowym na liczbę, a liczbę w znak i dodajemy do tablicy
                
    def znak_pozycja(self, pozycja):
        d = len(self.tablica_znaków)
        if(pozycja < d):
            return self.tablica_znaków[pozycja] # jeśli dana pozycja istnieje w tablicy znaków to ją zwracamy
        else:
            return "BŁĄÐ"
            
class Deszyfrowanie:
    
    def __init__(self, dane):
        
        self.czestotliwosc_wystepowania = {'a': 89, 'b': 15, 'c': 40, 'd': 33, 'e': 77, 'f': 3, 'g': 14, 'h': 11, 'i': 82, 
        'j': 23, 'k': 35, 'l': 21, 'm': 28, 'n': 55, 'o': 78, 'p': 31, 'q': 2, 'r': 47, 's': 43, 't': 41, 'u': 25, 'v': 1,
         'w': 46, 'x': 1, 'y': 38, 'z': 56, ' ': 95, ',': 16, ':': 8, '?': 8, '.': 8, '!': 8, '-': 8, ';': 8, '(': 8, ')': 8, '"': 8} # dodajemy nietypowe znaki pojawiające się w zdaniach
          
        for i in range(65, 91):
            self.czestotliwosc_wystepowania[chr(i)] = 15 # dodajemy duże litery
 
        for i in range(48, 58):
            self.czestotliwosc_wystepowania[chr(i)] = 6 # dodajemy cyfry
        
            
        
        self.kryptogramy = []    
        linie_danych = dane.splitlines() # dzielimy badany tekst na linie
        
        for linia in linie_danych:
            self.kryptogramy.append(Kryptogram(linia)) # i dodajemy je do kryptogramów
            
    def znajdz_klucz(self):
        klucz = []
        zakres = 0  # zakresem będzie najdłuższy kryptogram

        for kryptogram in self.kryptogramy:
            if len(kryptogram.tablica_znaków) > zakres:
                zakres = len(kryptogram.tablica_znaków) 
            
        for i in range(0, zakres):
            mozliwosci_kluczy = {} # znaki mogące być w kluczu
            badane_kryptogramy = [] # te o dlugosci mniejszej niz i

            # Szukanie takich kryptogramów
            for kryptogram in self.kryptogramy:
                if i < len(kryptogram.tablica_znaków):
                    badane_kryptogramy.append(kryptogram)

            for kryptogram in badane_kryptogramy:
            
                for znak in self.czestotliwosc_wystepowania.keys():

                    xor = (ord(kryptogram.znak_pozycja(i)) ^ ord(znak), self.czestotliwosc_wystepowania[znak])  # XORujemy znaki kryptogramu z literami alfabetu

                    if xor[0] not in mozliwosci_kluczy.keys():
                        mozliwosci_kluczy[xor[0]] = xor[1]
                    else:
                        mozliwosci_kluczy[xor[0]] = mozliwosci_kluczy.get(xor[0]) + self.czestotliwosc_wystepowania.get(znak)   # Wsadzamy w słownik częstotliwości wyników XOR

            posortowane = sorted(mozliwosci_kluczy.items(), key=operator.itemgetter(1), reverse=True)
            mozliwosci_kluczy = dict(posortowane)

            najwiecej = 0

            for znak in mozliwosci_kluczy.keys():
                licznik = 0

                for kryptogram in badane_kryptogramy:
                    if (chr(ord(kryptogram.znak_pozycja(i)) ^ znak)) in self.czestotliwosc_wystepowania.keys(): # Czy wynik XOR jest w znakach które podaliśmy na starcie
                        licznik += 1

                if licznik > najwiecej:
                    najwiecej = licznik
                    najlepszy_klucz = znak # Najlepszym kluczem będzie ten co będzie najwięcej razy w znakach alfabetu

            klucz.append(najlepszy_klucz)

        return klucz
        
    def wynik(self):
        wypisz = ""
        klucz = self.znajdz_klucz()
   
        for kryptogram in self.kryptogramy:
            for i in range(0, len(kryptogram.tablica_znaków)):
                wypisz += chr(ord(kryptogram.znak_pozycja(i)) ^ klucz[i])
            wypisz += '\n'

        return wypisz     




with open('dane.txt', 'r') as file:
    tekst = Deszyfrowanie(file.read())
print(tekst.wynik())

            
