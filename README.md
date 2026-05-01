# Lastenleikkitreffit

## Sovelluksen toiminnot
- Sovelluksessa voi kutsua lapselle leikkikavereita esim. puistoon, sisäleikkipuistoon tai kotiin. Sovelluksessa voi etsiä leikkiseuraa.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään sovellukseen kutsuja lasten leikkitreffeille. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään kutsuja.
- Käyttäjä näkee sovellukseen lisätyt kutsut. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät kutsut.
- Käyttäjä pystyy etsimään kutsuja hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä kutsuja.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät kutsut.
- Käyttäjä pystyy valitsemaan kutsuille yhden luokittelun (leikkitreffien tekeminen). Luokat ovat tietokannassa.
- Sovelluksessa on pääasiallisen tietokohteen (kutsut) lisäksi kaksi toissijaista tietokohdetta (myöntävä vastaus kutsuun ja viestit osallistujien kesken), jotka täydentävät pääasiallista tietokohdetta. Käyttäjä pystyy lisäämään vastauksia muiden käyttäjien kutsuihin liittyen ja viestittelemään leikkitreffeille osallistuvien kesken.

## Sovelluksen asennus (linux-ympäristö):  
Luo sovellukselle oma hakemisto:
```
	mkdir hakemiston_nimi
```
ja siirry hakemistoon:
```
	cd hakemiston_nimi
```
Tallenna hakemistoon sovelluksen githubista löytyvät .py-tiedostot, .sql-tiedostot sekä templates-kansio sisältöineen (.html-tiedostot).  
Luo tietokannan taulut schema.sql-tiedoston avulla: 
```
	sqlite3 database.db < schema.sql
```
Tuo kantaan sovelluksen luokat init.sql-tiedoston avulla:
```
        sqlite3 database.db < init.sql
```

Luo hakemistoon Pythonin virtuaaliympäristö:
```
	python3 -m venv venv
```
Käynnistä virtuaaliympäristö: 
```
	source venv/bin/activate
```
Asenna flask kirjasto:
```
	pip install flask
```
Käynnistä sovellus:
```
	 flask run
```
##Sovelluksen testaus:
Luo ensin tunnus muutamalle eri käyttäjälle. Sen jälkeen voit lisätä käyttäjille kutsuja. Esimerkkisyöte kutsulle:  
Otsikko: Leikkipuistotreffit  
Tekeminen: Leikit ulkona leikkipuistossa  
Leikkipaikan nimi: Leikkipuisto Toinen linja  
Leikkipaikan osoite: Toinen linja 10  
Päivämäärä: 28.3.2026  
Kellonaika: 15:00  
Leikkikaverin nimi: Ville  
Leikkikaverin ikä: 4  
Lisätietoa: Villellä on mukana oma potkulauta.  

Voit ilmoittautua mukaan muiden leikkitreffeihin (ilmoittautumislomake näkyy vain, jos olet toisen käyttäjän lisäämässä kutsussa). Kun olet ilmoittautunut leikkitreffeille, pystyt keskustelemaan muiden osallistujien kanssa.
