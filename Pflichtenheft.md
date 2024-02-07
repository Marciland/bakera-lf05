# Pflichtenheft
### Produktübersicht

![Alt text](http://cdn-0.plantuml.com/plantuml/png/NOyn3eCm34Ltdy8ZN04MfD9EtK3j78W12-AWu0ZrzWrjnT35-lhloRAhJKtGw1PGreNmHYofYbqQobu0caE0elQxBDvOj1JmqZpG6YKkeJWo2rech5CbdP4PsQq-A5CWISgLPJJTXqU7KIm-AIYrhxM4RMVj9ynowCr6cBNaLWf933aW8XRb3zpZe0F5Vb8UPsBzm-VXPqzYlykXIZ6z-0O0)

### Projektziele
  - Python-Programm zur Auswertung von Rohdaten
### Projektvorgaben
- Hardwarebasis
  - Unseren (Team) Laptops
- Softwarevoraussetzungen
  - [DockerCLI](https://www.docker.com/products/docker-desktop/)
- Einzusetzende Arbeitsmittel
  - [Datengrundlage](https://archive.sensor.community/2022/)
  - [VS-Code](https://code.visualstudio.com/)
- Nebenbedingungen
    - Cool sein
### Projektanforderungen
- Aufgaben und Funktionen des Produkts
  - Bereitstellen einer Datenbank samt Datensatz aus der Datzengrundlage
  - Bereitstellen einer Oberfläche zur auswertung der Daten, insbesondere:
    - (tägl. Höchst-, Tiefst- und Durchschnittswerte)(Nach Datumseingabe für die Wertetypen Temperatur, Luftfeuchtigkeit, Feinstaub)(Optional: grafische Auswertung der Daten)-->!Feinstaubdaten für ZWEI Partikelgrößen(PM10 und PM2,5)
- Benutzerschnittstelle
  - gängige Browser
- Lieferumfang
  - Docker Images für die Anwendung und Datenbank inklusive Volume
- Kompatibilität und Portierbarkeit
  - Plattform unabhängig, falls docker läuft
- Erweiterbarkeit und Änderbarkeit
  - Neue Routen für die API lassen sich leicht hinzufügen
  - Routen sind unabhängig voneinander geschrieben und somit leicht zu ändern
### Weitere Leistungen
- geplante Testreihen
  - Manuell getestet
- Qualitätssicherung
  - Unit tests
  - Integration Test
- Supportvereinbarungen
  - Keine
### Kostenkalkulation
### Literatur

[Pflichtenheft Vorlage](https://openbook.rheinwerk-verlag.de/it_handbuch/11_001.html#dodtp3db5d809-6a56-4229-a02f-1e3c3a627dda)