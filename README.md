# Lastenleikkitreffit

## Sovelluksen toiminnot
- Sovelluksessa voi kutsua lapselle leikkikavereita esim. puistoon, sisäleikkipuistoon tai kotiin. Sovelluksessa voi etsiä leikkiseuraa lähialueelta.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään sovellukseen kutsuja lasten leikkitreffeille. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään kutsuja.
- Käyttäjä näkee sovellukseen lisätyt kutsut. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät kutsut.
- Käyttäjä pystyy etsimään kutsuja hakusanalla tai muulla perusteella (esim. sijainti, lapsen ikä). Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä kutsuja.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät kutsut.
- Käyttäjä pystyy valitsemaan kutsuille yhden tai useamman luokittelun (esim. leikkipaikka, lapsen kiinnostuksen kohteet). Mahdolliset luokat ovat tietokannassa.
- Sovelluksessa on pääasiallisen tietokohteen (kutsut) lisäksi toissijainen tietokohde (myöntävä vastaus kutsuun), joka täydentää pääasiallista tietokohdetta. Käyttäjä pystyy lisäämään vastauksia muiden käyttäjien kutsuihin liittyen.

## Sovelluksen asennus (linux-ympäristö):  
Luo sovellukselle oma hakemisto:
```
	mkdir hakemiston_nimi
```
ja siirry hakemistoon:
```
	cd hakemiston_nimi
```
Tallenna hakemistoon sovelluksen githubista löytyvät .py tiedostot, schema.sql-tiedosto sekä templates-kansio sisältöineen (.html-tiedostot).
Luo tietokannan taulut schema.sql-tiedoston perusteella: 
```
	sqlite3 database.db < schema.sql
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
