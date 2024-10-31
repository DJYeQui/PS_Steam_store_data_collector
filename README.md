# Project Purpose

The purpose of the project is to create an automated system to retrieve data on games available in the PS Store. As a result, it has successfully scanned around 3,500 games and saved the data into a CSV file.

## Challenges and Required Adjustments

Since the PS Store lacks a consistent standard in many aspects, some data points were challenging to access or required manual adjustments due to varied representations. Here are some of the adjustments needed:

- **Rating Count**: The rating count sometimes appears as "1.6k." This data should be corrected manually after retrieval.
- **Genre Information**: Some games list their genres twice, e.g., "action, action."
- **Language Options**: Games offering separate language options for PS4 and PS5 may require adjustments due to extension of csv file.

After data retrieval, some cleaning and corrections are necessary. Additionally, it was observed that data for only around 20 out of 3,500 games could not be retrieved. Although this is a minor number, it’s still worth noting.

## Retrieved Data

The following data fields were retrieved:

- **Name** (Game name)
- **Current Price**
- **Discount Price**
- **PSN Discount Price** (Discounted price for PSN members)
- **PSN Price** (Price for PSN members)
- **Collected Date** (Date of data collection)
- **Published Date** (Release date)
- **Rate** (Game rating)
- **Rate Amount** (Number of ratings)
- **Languages Subtitle** (Subtitle languages)
- **Voice Language** (Voice-over languages)
- **Publisher**
- **Situation** (e.g., purchased, wishlisted)
- **Platforms** (Available platforms)
- **Link** (Game link)
