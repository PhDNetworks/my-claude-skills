# Service Areas - Leeds & West Yorkshire

## areaServed JSON Templates

### Leeds Only
```json
"areaServed": {
  "@type": "City",
  "name": "Leeds",
  "sameAs": "https://en.wikipedia.org/wiki/Leeds"
}
```

### Leeds + Immediate Suburbs
```json
"areaServed": [
  {"@type": "City", "name": "Leeds"},
  {"@type": "City", "name": "Pudsey"},
  {"@type": "City", "name": "Morley"},
  {"@type": "City", "name": "Rothwell"},
  {"@type": "City", "name": "Horsforth"},
  {"@type": "City", "name": "Garforth"}
]
```

### West Yorkshire (Full Coverage)
```json
"areaServed": [
  {"@type": "City", "name": "Leeds"},
  {"@type": "City", "name": "Bradford"},
  {"@type": "City", "name": "Wakefield"},
  {"@type": "City", "name": "Huddersfield"},
  {"@type": "City", "name": "Halifax"}
]
```

### Leeds + Surrounding Towns (Detailed)
```json
"areaServed": [
  {"@type": "City", "name": "Leeds"},
  {"@type": "City", "name": "Bradford"},
  {"@type": "City", "name": "Wakefield"},
  {"@type": "City", "name": "Pudsey"},
  {"@type": "City", "name": "Morley"},
  {"@type": "City", "name": "Rothwell"},
  {"@type": "City", "name": "Horsforth"},
  {"@type": "City", "name": "Garforth"},
  {"@type": "City", "name": "Wetherby"},
  {"@type": "City", "name": "Otley"},
  {"@type": "City", "name": "Ilkley"},
  {"@type": "City", "name": "Guiseley"},
  {"@type": "City", "name": "Yeadon"},
  {"@type": "City", "name": "Castleford"},
  {"@type": "City", "name": "Pontefract"},
  {"@type": "City", "name": "Ossett"},
  {"@type": "City", "name": "Batley"},
  {"@type": "City", "name": "Dewsbury"},
  {"@type": "City", "name": "Bingley"},
  {"@type": "City", "name": "Shipley"}
]
```

## Leeds Postcodes by Area

### Central Leeds
- LS1 - City Centre
- LS2 - City Centre / University

### North Leeds
- LS6 - Headingley, Hyde Park
- LS7 - Chapel Allerton, Chapeltown
- LS8 - Roundhay, Oakwood
- LS16 - Adel, Bramhope
- LS17 - Moortown, Alwoodley

### South Leeds
- LS10 - Hunslet, Belle Isle
- LS11 - Beeston, Holbeck
- LS26 - Rothwell
- LS27 - Morley

### East Leeds
- LS9 - Harehills, Richmond Hill
- LS14 - Seacroft
- LS15 - Cross Gates
- LS25 - Garforth

### West Leeds
- LS5 - Kirkstall
- LS12 - Armley, Farnley
- LS13 - Bramley, Rodley
- LS28 - Pudsey, Farsley

### North West Leeds
- LS18 - Horsforth
- LS19 - Yeadon, Rawdon
- LS20 - Guiseley
- LS21 - Otley

### Wider West Yorkshire Postcodes
- BD (Bradford)
- WF (Wakefield)
- HD (Huddersfield)
- HX (Halifax)

## Geo Coordinates Reference

| Location | Latitude | Longitude |
|----------|----------|-----------|
| Leeds City Centre | 53.8008 | -1.5491 |
| Bradford | 53.7960 | -1.7594 |
| Wakefield | 53.6830 | -1.4977 |
| Huddersfield | 53.6450 | -1.7850 |
| Halifax | 53.7250 | -1.8630 |
| Pudsey | 53.8060 | -1.6630 |
| Morley | 53.7490 | -1.6000 |
| Horsforth | 53.8440 | -1.6380 |
| Wetherby | 53.9280 | -1.3850 |
| Otley | 53.9050 | -1.6900 |
| Garforth | 53.7920 | -1.3830 |
| Rothwell | 53.7500 | -1.4780 |
| Ossett | 53.6790 | -1.5790 |
| Castleford | 53.7250 | -1.3560 |
| Pontefract | 53.6910 | -1.3120 |

## Service Radius Templates

### 10-mile radius from Leeds
Covers: Leeds, Pudsey, Morley, Horsforth, Rothwell, Garforth, Wetherby

### 20-mile radius from Leeds
Adds: Bradford, Wakefield, Huddersfield, Halifax, Harrogate, York outskirts

### Description Templates

**Local focus:**
"Serving Leeds and surrounding areas including Pudsey, Morley, Horsforth, and Rothwell."

**West Yorkshire focus:**
"Covering all of West Yorkshire including Leeds, Bradford, Wakefield, Huddersfield, and Halifax."

**Regional focus:**
"Based in Leeds, serving customers across West Yorkshire and North Yorkshire."
