# Hijri — Shia Islamic Hijri Calendar Data

A specialized Hijri calendar data repository for Shia Islamic applications, providing regularly updated Hijri dates based on authoritative religious sources.

## Purpose

This project provides Hijri calendar data for Islamic applications that require a Shia-oriented religious calendar rather than relying exclusively on astronomical or civil Hijri calculations.

The project aims to provide updated Hijri dates according to recognized Shia religious sources, including:

* Office of His Eminence Sayyid Ali al-Sistani
* Al-Kafeel / Al-Abbas Holy Shrine calendar
* Al-Mu'min application and its published Hijri calendar data

## Data Sources

The calendar data is intended to be cross-checked and updated according to the following sources:

### 1. Office of Sayyid Ali al-Sistani

The Hijri date published by the official office of His Eminence Sayyid Ali al-Sistani is considered a primary religious reference for determining the beginning of Hijri months according to Shia jurisprudence.

Source:
https://www.sistani.org/

### 2. Al-Kafeel / Al-Abbas Holy Shrine

The Al-Kafeel platform and the Al-Abbas Holy Shrine provide Islamic calendar information, religious occasions, and Hijri dates used by many Shia users.

Source:
https://alkafeel.net/

### 3. Al-Mu'min

The Al-Mu'min application is used as an additional reference for Islamic dates, religious occasions, and Shia calendar information.

## Important Note

Hijri dates related to the beginning of lunar months may differ between different calendar systems because the beginning of a month can depend on the religious determination of the crescent moon.

Therefore, this repository does not treat mathematical Hijri conversion alone as an authoritative determination of religious month beginnings.

The data is intended primarily for religious applications that require Shia Hijri calendar information.

## Data Format

The repository currently provides the Hijri calendar in JSON format:

`hijri.json`

The data can be consumed directly by mobile applications, websites, APIs, and other software projects.

Example:

```json
{
  "gregorian": "2026-09-06",
  "hijri": "1448-03-14",
  "month": "Rabi al-Awwal",
  "source": "Sistani",
  "verified": true
}
```

## Update Policy

Hijri dates should be reviewed and updated regularly, especially around:

* Beginning of Ramadan
* Eid al-Fitr
* Beginning of Dhu al-Hijjah
* Eid al-Adha
* Muharram
* Safar
* Arbaeen
* Other important religious occasions

When sources provide different dates, the repository should preserve the source information instead of silently replacing one date with another.

## Intended Use

This project can be used by:

* Islamic mobile applications
* Prayer and worship applications
* Hijri calendar applications
* Shia religious applications
* Religious notification systems
* Islamic event calendars
* Developers who need structured Hijri calendar data

## Disclaimer

This is an independent open-source software project and is not affiliated with or officially endorsed by the Office of Sayyid Ali al-Sistani, Al-Kafeel, Al-Abbas Holy Shrine, or the Al-Mu'min application.

Official religious rulings and announcements should always be verified through the respective official sources.

## License

This repository is intended to provide structured calendar data for software development and educational purposes.
