# Django ORM example

Tento repozitá prezentuje fungovanie ORM architektonického vzoru na príklade
Django ORM.

Príklad je postavený na dátovom modeli znázornenom na obrázku nižšie. Na naplnenie datasetu sme použíli
voľne prístupné dáta z [data.gov.sk](https://data.gov.sk/), ktoré mapujú zloženie parlamentu počas fungovania
samostatnej Slovenskej republiky (od roku 1993).

Príklady sa nachádzajú v priečinku `apps/core/examples`. Nevyplnená verzia sa nachádza v branci `empty`.

Projekt používa [poetry](https://python-poetry.org/) ako balíčkovací systém. Príklad konfiguračného súboru, sa
náchádza v súbore `.env.example`. Kompletná inštalácia ne Linuxe, môže vyzerať napríklad takto:

```shell
# Stiahnutie projekty
git clone https://github.com/Sibyx/fiit-orm-django-example.git orm_example
cd orm_example

# Vytvorenie virtuálneho prostredia a instalacia zavislosti
python -m venv venv
source venv/bin/activate
poetry install

# Vytvorenie konfiguracie
cp .env.example .env
vim .env

# Spustenie migracii
python manage.py migrate

# Stiahnutie aktuálnyc informácií o rozložení parlamentu
# šikovní skauti sa chcú pozrieť do apps/core/management/commands/seed.py
python manage.py seed

# Spustenie testov
python manage.py test
```

## Databáza

![](docs/eer.png)

---
S ❤️ FIIT STU
