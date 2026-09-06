# Hijri — Shia Hijri Calendar & Prayer Times Data

A structured Hijri calendar data repository designed for Shia Islamic applications, with a focus on providing Hijri dates and religious timing information based on recognized Shia sources.

The project can be used by mobile applications, websites, and software systems that require Hijri calendar information and Islamic prayer-time data in a structured JSON format.

---

## Primary Data Source — Haqybat Al-Mu'min API

The primary technical data source used by this project is the official **Haqybat Al-Mu'min API**, provided through the Al-Kafeel platform.

The API provides Islamic prayer times and the corresponding Hijri date according to the location and timezone supplied to the API.

### Official API

**Prayer Times JSON API:**

https://hq.alkafeel.net/Api/init/init.php?v=jsonPrayerTimes

### API Parameters

The API supports location-based calculations using:

* `timezone` — The timezone of the requested location.
* `long` — Longitude of the requested city.
* `lati` — Latitude of the requested city.
* `v=jsonPrayerTimes` — Requests the prayer-times response in JSON format.

### Example

```text
https://hq.alkafeel.net/Api/init/init.php?timezone=+3&long=44&lati=32&v=jsonPrayerTimes
```

### Example JSON Response

```json
{
  "fajir": "5:18",
  "sunrise": "6:47",
  "doher": "11:53",
  "sunset": "4:59",
  "maghrib": "5:15",
  "date": "27 صفر 1438 هـ",
  "powerdby": "haqybat almomen"
}
```

The `date` field provides the Hijri date returned by the Haqybat Al-Mu'min service.

---

## Hijri Date Updates

This repository is intended to maintain updated Hijri-date information for Shia Islamic applications.

The data may be cross-checked against recognized Shia religious references, particularly:

1. **Haqybat Al-Mu'min API** — primary technical API source.
2. **Office of His Eminence Sayyid Ali al-Sistani** — religious reference for lunar-month determinations and announcements.
3. **Al-Kafeel / Al-Abbas Holy Shrine** — Islamic calendar and religious-event reference.

Because the beginning of a Hijri lunar month can depend on crescent visibility and religious determination, calculated Hijri dates should not automatically be treated as equivalent to an officially announced religious date.

---

## Religious Reference

For religiously significant dates, especially the beginning of lunar months, users should verify the date through the official announcements and rulings of the relevant religious authority.

The official website of the Office of Sayyid Ali al-Sistani is:

https://www.sistani.org/

---

## Haqybat Al-Mu'min Services

Haqybat Al-Mu'min provides several services through its API platform.

### Virtual Haqybat Al-Mu'min Box

https://hq.alkafeel.net/Api/index.php?model=standerdBlock

### Prayer Times JSON

https://hq.alkafeel.net/Api/index.php?model=jsonPrayerTimes

### Prayer Times API Endpoint

```text
https://hq.alkafeel.net/Api/init/init.php?v=jsonPrayerTimes&timezone=TIMEZONE&long=LONGITUDE&lati=LATITUDE
```

### PHP Example

```php
<?php

// Get Prayer Times
$timesJson = file_get_contents(
    "https://hq.alkafeel.net/Api/init/init.php?timezone=+3&long=44&lati=32&v=jsonPrayerTimes"
);

// Parse JSON
$Times = json_decode($timesJson);

// Fajr
echo $Times->fajir;

// Hijri Date
echo $Times->date;

?>
```

---

## Data Fields

The prayer-times API may return the following fields:

| Field      | Description              |
| ---------- | ------------------------ |
| `fajir`    | Fajr prayer time         |
| `sunrise`  | Sunrise time             |
| `doher`    | Dhuhr prayer time        |
| `sunset`   | Sunset time              |
| `maghrib`  | Maghrib prayer time      |
| `date`     | Hijri date               |
| `powerdby` | Data provider identifier |

---

## Location-Based Calculation

Prayer times can be requested for different locations by changing the timezone, longitude, and latitude parameters.

```text
timezone = Country / location timezone
long     = Longitude
lati     = Latitude
```

Example:

```text
timezone=+3
long=44
lati=32
```

The returned prayer times therefore depend on the geographical coordinates and timezone supplied to the API.

---

## Data Verification Strategy

To improve reliability, applications using this repository should distinguish between:

### Calculated / API Date

The Hijri date returned automatically by the Haqybat Al-Mu'min API.

### Religiously Confirmed Date

A Hijri date confirmed through an official religious announcement or authoritative Shia religious source.

When these dates differ, the repository should preserve the source information rather than silently changing one date to another.

---

## Intended Use

This repository can be used for:

* Shia Islamic mobile applications
* Hijri calendar applications
* Prayer-time applications
* Islamic religious-event calendars
* Ramadan and fasting applications
* Muharram and Safar calendars
* Arbaeen and religious-occasion notifications
* Islamic widgets
* Websites and web applications
* JSON-based calendar services
* Mobile application backends

---

## Important Disclaimer

This repository is an independent open-source software project.

It is **not officially affiliated with, operated by, or endorsed by** the Office of Sayyid Ali al-Sistani, Al-Kafeel, the Al-Abbas Holy Shrine, or the Haqybat Al-Mu'min application.

The Haqybat Al-Mu'min API is referenced as an external data source. Religious dates should be verified against the official announcements of the relevant religious authority, especially when determining the beginning of lunar months.

---

## Official / Reference Links

### Office of Sayyid Ali al-Sistani

https://www.sistani.org/

### Al-Kafeel

https://alkafeel.net/

### Haqybat Al-Mu'min API

https://hq.alkafeel.net/Api/

### Technical Support

https://alkafeel.net/contact/

### Haqybat Al-Mu'min — Facebook

https://www.facebook.com/haqibatalmomen

### Haqybat Al-Mu'min — Google Play

https://play.google.com/store/apps/details?id=net.alkafeel.mcb

### Haqybat Al-Mu'min — App Store

https://itunes.apple.com/us/app/hqybt-almwmn/id935681991

---

## License & Attribution

Applications using this repository should retain attribution to the original data source where applicable.

The repository's purpose is to organize and provide structured data for software development while preserving information about the original source of the data.

**Primary API Source: Haqybat Al-Mu'min — Al-Kafeel Platform**
