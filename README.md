# Kursinis Darbas

## 1. Įvadas

Žaidimas, pavadinimu „Country Guesser" patikrina žaidėjo žinias geografijos srityje.  Paleidęs žaidimą, žaidėjas pirmiausia turi įvesti savo vardą. Žaidimo esmė labai paprasta. Žaidėjas turi atspėti valstybių pavadinimus pagal duotas užuominas. Klausimai ir atsakymai pateikiami anglų kalba. Šiuo metu žaidime sukurti du lygiai. Pirmąjame lygyje žaidėjas gauna užuominą ir tris variantus, jis turi įvesti skaičių to varianto, kuris jo nuomone yra teisingas. Antrajame lygyje žaidėjas pats turi sugalvoti atsakymą ir įvesti valstybės pavadinimą. Atsakius neteisingai ekrane išvedamas teisingas atsakymas. Po kiekvieno lygio, ekrane išvedami tame lygyje surinkti taškai, o pasibaigus žaidimui, taškai susumuojami ir išvedamas galutinis rezultatas, kuris kartu su žaidėjo vardu įrašomas į atskirą failą. 

## 2. Kodo analizė

##### Programos kodas pagrįstas tokiomis sampratomis, kaip polimorfizmas, enkapsuliacija, abstrakcija bei paveldėjimas.

#### Polimorfizmas: 

Polimorfizmas pritaikomas naudojant metodų perrašymą. Abstrakčioje tėvinėje klasėje „PlayGame" metodas *„_read_from_file"* paverčiamas abstrakčiu naudojant *„@abstractmethod"* dekoratorių iš *„abc"* modulio. Tuomet šis metodas yra skirtingai pritaikomas vaikinėse klasėse *„MultipleChoice"* ir *„TextInput"*. Abi vaikinės klasės perrašo *„_read_from_file"* metodą ir perskaito klausimus iš failų pagal skirtingus, pritaikytus tam konkretiems lygiams, klausimų formatus. 

###### Konkretus pavyyzdys iš kodo: 

``` 
class PlayGame(ABC):          
    @abstractmethod 
    def _read_from_file(self, filename):
    pass

class MultipleChoice(PlayGame):
    def _read_from_file(self, filename):
        # Daugiavariantių klausimų skaitymo įgyvendinimas

class TextInput(PlayGame):
    def _read_from_file(self, filename):
        # Teksto įvedimo klausimų skaitymo įgyvendinimas
```
Polimorfizmas leidžia vienodai tvarkyti vaikinių klasių objektus per bendrą sąsają *(PlayGame)*. Abi vaikinės klasės gali įgyvendinti abstraktų metodą skirtingai, kaip parodyta skirtingomis metodo „_read_from_file" implementacijomis vaikinėse klasėse „MultipleChoice" ir „TextInput".


#### Inkapsuliacija
Inkapsuliacija padeda paslėpti objekto vidinę būseną nuo išorinio pasaulio ir leidžia prie jos prieiti tik per gerai apibrėžtus sąsajas. Programos kode panaudojau *„Protected"*  (apsaugotus) atributus, žymimus su *„ _"* ženklu, padėtu prieš metodo pavadinimą. Ketinau naudoti „Private" (privačius) atributus, žymimus *„ __",* tačiau man nepavyko to įgyvendinti naudojant abstraktų metodą. 

######  Konkretus pavyzdys iš kodo: 
```
class PlayGame(ABC):
    def __init__(self, filename):
        self._filename = filename
        self._level_score = 0
        self._questions = self._read_from_file(filename)

    @abstractmethod
    def _read_from_file(self, filename):
        pass
```
Šioje dalyje *„_filename"*, *„_level_score"* ir *„_questions"* yra inkapsuliuotos *„PlayGame"* klasėje. Prie jų galima prieiti ir juos keisti tik klasės viduje arba jos vaikinėse klasėse dėl vieno pabraukimo prefikso.
*„_read_from_file"* metodas yra pateikiamas kaip abstraktus, nurodant, kad jį privalo įgyvendinti vaikinės klasės. Taip nuo išorės paslėpiamios visos klausimų skaitymo iš failo įgyvendinimo detalės. Be to, kode inkapsuliuojami metodai *„_play_multiple_choice"* ir *„_play_text_input"*, taip paslėpiamas žaidimo, su skirtingo tipo klausimais, detalės.

#### Abstrakcija.
 Panaudodami abstrakciją kode galime paslėpti sudėtingas implementacijas ir atskleisti tik esmines objekto savybes. Tai leidžia sutelkti dėmesį į tai, ką objektas daro, o ne tai, kaip jis tai daro. 

Čia „PlayGame" yra abstrakti tėvinė klasė su abstrakčiu metodu *„_read_from_file"*. Šioje vietoje metodas nieko neįgyvendina, todėl po juo užrašiau *„pass"*, metodą apibrėžia vaikinė klasė. Šis abstraktus metodas leidžia patogiai skaityti klausimus iš failo:

```
from abc import ABC, abstractmethod

class PlayGame(ABC):
    def __init__(self, filename):
        self._filename = filename
        self._level_score = 0
        self._questions = self._read_from_file(filename)

    @abstractmethod
    def _read_from_file(self, filename):
        pass
```

Tuomet vaikinės klasės šį metodą įgyvendina pagal savo poreikius:
```
class MultipleChoice(PlayGame):
    def _read_from_file(self, filename):
        # Implementation for reading multiple-choice questions

class TextInput(PlayGame):
    def _read_from_file(self, filename):
        # Implementation for reading text input questions
```
Abstrakcija šiame kode leidžia apibrėžti bendrą sąsają arba interface'ą (tėvinę *„PlayGame“* klasę), skirtą sąveikai su skirtingų tipų žaidimų lygiais (*„MultipleChoice“* ir *„TextInput“* vaikinėimis klasėmis), kartu paslepiant kiekvienam žaidimo tipui būdingą įgyvendinimo informaciją. 
.
```
class CountryGuessGame:
    def __init__(self):
        self._levels = []
        self._total_score = 0

    def add_level(self, filename, level_type):
        if level_type == "multiple_choice":
            level = MultipleChoice(filename)
        elif level_type == "text_input":
            level = TextInput(filename)
        else:
            raise ValueError("Invalid level type")
        self._levels.append(level)
```


#### Paveldėjimas (inheritance) 

Paveldėjimas leidžia klasėms paveldėti atributus ir metodus iš kitų klasių.

Kode *„PlayGame“* apibrėžiama kaip tėvinė klasė. Ji naudojama kaip šablonas kuriant įvairių tipų žaidimus. Ši klasė yra abstrakti, vaikinės klasės *„MultipleChoice“* ir „TextInput“ paveldi atributus ir metodus iš tėvinės klasės, tai atlieka pridėdami tėvinės klasės pavadinimą skliausteliuose po klasės pavadinimo: 
>*_„class MultipleChoice(PlayGame):"_*

Tėvinė klasė apibrėžia bendrą žaidimo sąsają, bet nepateikia konkrečių tam tikrų metodų, pvz., *„_read_from_file"*, įgyvendinimo, todėl mano kode kiekvienas poklasis panaudoja paveldėtus atributus skirtingai.

### Dizaino modeliai (design patterns)

Kode panaudoti dizaino modeliai:
  - Factory Method Pattern (Fabrikavimo Metodas)
  - Template Method Pattern (Šablono Modelis)
  
#### Factory Method Pattern (Fabrikavimo Metodas)

Šis šablonas kode naudojamas *„CountryGuessGame"* klasėje, *„add_level metode"*. Šablonas veikia kaip gamyklinis, sukurdamas žaidimo lygius pagal nurodytą lygio tipą (*„multiple_choice“* arba *„text_input“*). 
Metodas apima du parametrus: *„filename"* (failo pavadinimą) ir *„level_type"* (lygio tipą). Remiantis nurodytu lygio tipu, nusprendžiama, kurį konkretų žaidimo lygį sukurti. Jei *„level_type"* yra *„MultipleChoice"*, sukuriamas lygis su trimis atsakymo variantais. Jei *„level_type"* yra *"text_input"*, sukuriamas lygis be atsakymo variantų.

###### Konkretus pavyzdys iš kodo 
```
def add_level(self, filename, level_type):
    if level_type == "multiple_choice":
        level = MultipleChoice(filename)
    elif level_type == "text_input":
        level = TextInput(filename)
    else:
        raise ValueError("Invalid level type")
    self._levels.append(level)
```

Norint pridėti daugiau lygių, užtenka įrašti naują eilutę *„main"* funkcijoje, nurodant failo pavadinimą ir lygio tipą:
> game.add_level("failo_pavadinimas", "lygio_tipas")

tuomet fabrikavimo metodas sukurs tiek lygių, kiek čia įrašyta:
```
def main():
    game = CountryGuessGame()

    game.add_level("level_1.txt", "multiple_choice") 
    game.add_level("level_2.txt", "text_input")

    game.play_game()

if __name__ == "__main__":
    main()
```
#### Template Method Pattern (Šablono Modelis) 
Template metodas naudojamas norint sukurti tėvinės klasės algoritmo griaučius, kuriuos gali paveldėti vaikinės klasės, tačiau kartu perrašyti kai kuriuos algoritmo žingsnius nekeičiant jo struktūros.

Kode Template metodas įgyvendinamas *„PlayGame"* klasėje. Ši klasė apibrėžia abstraktų metodą *„_read_from_file"*, skirtą vaikinėms klasėms *(„multiple_choice“ arba „text_input“)*, kad galėtų skaityti klausimus ir atsakymus iš failo.  Apibrėždama jį kaip abstraktų, tėvinė klasė užtikrina, kad visi poklasiai juos įgyvendintų:
```
@abstractmethod
def _read_from_file(self, filename):
    pass
```
*„PlayGame klasėje"* taip pat pateikiami konkretūs metodai *„_play_multiple_choice"* ir *„_play_text_input"*, kurie atspindi bendrą žaidimo procesą. Šiuose metoduose pateikiami įprasti žaidimui reikalingi veiksmai, pvz.: klausimų rodymas, vartotojo įvesties apdorojimas ir rezultato atnaujinimas.
```
def _play_multiple_choice(self):
    # žaidimo su variantais įgyvendinimo detalės

def _play_text_input(self):
    # žaidimo su teksto įrašymu įgyvendinimo detalės
```

Naudodama Template metodą užtikrinu, kad bendra žaidimo proceso struktūra ir eiga skirtinguose žaidimo tipuose išliktų nuosekli, kartu leidžiant lanksčiai įgyvendinti atskirus veiksmus.

### Skaitymas iš failo
```
with open(filename, 'r') as file:
    lines = file.readlines()
```
Visi žaidimo klausimai yra laikomi tekstiniuose dokumentuose, kiekviename dokumente yra 10 klausimų bei visi atsakymai. Dokumento pavadinimas sutampa su lygio numeriu.  

Skaitymas iš failo teksto įvedimo ir variantų pasirinkimo lygiuose skiriasi, nes skirasi dokumente surašytų klausimų struktūra

„PlayGame" klasėje esantis abstraktus naudojamas kaip šablonas klausimams ir atsakymams iš failo skaityti:
```
@abstractmethod
def _read_from_file(self, filename):
    pass
```
Vaikinės klasės turi įgyvendina šį metodą skirtingai:


Klasėje, skirtoje lygiams su variantais, kiekvienas dokumento klausimas turi turėti penkias eilutes: patį klausimą, po to tris parinktis ir galiausiai teisingą atsakymą:
```
class MultipleChoice(PlayGame):
    def _read_from_file(self, filename):
        questions = []
        with open(filename, 'r') as file:
            lines = file.readlines()
            if len(lines) % 5 != 0:
                raise ValueError("Invalid file format: Each question should have 5 lines.")
            for i in range(0, len(lines), 5):
                question = lines[i].strip()
                options = [lines[i+j].strip() for j in range(1, 4)]
                answer = lines[i+4].strip()
                questions.append((question, options, answer))
        return questions
```

Klasėje, skirtoje lygiams su teksto įvedimu, vienoje eilutėje turi būti klausimas, o kitoje atsakymas:
```
class TextInput(PlayGame):
    def _read_from_file(self, filename):
        questions = []
        with open(filename, 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 2):
                question = lines[i].strip()  
                answer = lines[i+1].strip() 
                questions.append((question, answer))
        return questions
```
	
### Įrašymas į failą:

Žaidime į atskirą tekstinį dokumentą *„scores.txt"* įrašomas žaidėjo vardas ir jo per visa žaidimą surinkti taškai, tai leidžia saugoti žaidimų rezultatus. 
Įrašymas į failą atliekamas *„CountryGuessGame"* klasės *„play_game"* metode. 

###### Konkretus pavyzdys iš kodo:
```
	with open("scores.txt", "a") as f:
    	f.write(f"{player_name} scored {self._total_score} points!\n")
```
### Testavimas 

Atlikau visų neabstrakčių kodo klasių *(„MultipleChoice", „TextInput", „CountryGuessGame")* testavimą naudodama *„import unittest"*. Unittest modulis Python'e leidžia kurti ir vykdyti vienetinius testus. Šiais testais tikrinau savo kodą, įsitikindama, kad jis veikia teisingai, ir padeda išvengti klaidų bei nesklandumų.

## 3. Rezultatai ir apibendrinimas

a. Rezultatai:

* Gan lengvai sukūriau du skirtingus kodus, vienas skirtas klausimams su variantais, o kitas klausimams su valstybių pavadinimų įvedimu, tačiau buvo sunku iš jų padaryti vieną pilnai veikiantį kodą. 
* Sužinojau daug informacijos apie dizaino šablonus bei du iš jų pritaikiau. Bandžiau panaudoti kitokius šablonus, pvz.: „Singleton", „Decorator", tačiau teko juos pašalinti, nes jie trukdė bendram kodo veikimui, arba buvo nereikalingi.
* Daug išmokau apie pagrindines programavimo sampratas bei sėkmingai jas pritaikiau savo kode. 

b. Apibendrinimas: 

Suprogramavau žaidimą, kuriuo galiu testuoti draugų geografines žinias. Kurdama žaidimą ne tik sužinojau daugybę objektinio programaviimo savybių, bet ir pagerinau savo žinias apie įvairias valstybes, kol suradau visus, pakankamai sudėtingus, tačiau įdomius, klausimus.

c. Galimybės: 

* Žaidime galėčiau panaudoti dekoratoriaus dizaino šabloną (Decorator). Sukūrusi dekoratorius, kurie apgaubia žaidimo lygius ir prideda funkcijas, galiu pridėti laiko skaičiavimo funkciją ir užuomenų sistemą nekeisdama esminio kodo. 
* Žinoma, galiu lengvai pridėti daugybę naujų lygių, tam nereikia keisti kodo struktūros.


>Romantė Šiupšinskaitė EEf-23







