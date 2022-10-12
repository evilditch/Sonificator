# Sonificator
Make sonifications from numeral data (csv format)

Scatterplotin sonifikoinnin mallina [soni-py](https://github.com/lockepatton/sonipy), by Locke Patton and Emily Levesque.


## To-do 

Python SonificationTool:
- annetun numeerisen datan sonifikointi
- mahdollisuus määrittää ääneen liittyviä muuttujia
- eri tyyppiset sonifikaatiot

Jossain vaiheessa:
- tiedoston datan lukeminen ja muuntaminen sopivaan muotoon matemaattista käsittelyä varten 
- muutama valmis csv-tiedosto serverille (iris, ympyrä, sini, ihan vaan joku viiva tai muu käyrä)
  - valmiille tiedostoille valitsimet käyttöliittymään
- clientin puolelle tiedoston esikäsittelyä:
  - sarakkeiden nimet
  - valinta sarakkeista, mikä vastaa sonifikaatiossa mitäkin
  - serverille lähetetään tiedoston lisäksi tämä sarakeinfo
- serverin post-pyyntöön lisäksi saraketiedon käsittely
