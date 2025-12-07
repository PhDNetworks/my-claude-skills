# Industry Mappings & Templates

## Schema @type by Industry

| Industry | @type | Alternative |
|----------|-------|-------------|
| Electrician | `Electrician` | `HomeAndConstructionBusiness` |
| Plumber | `Plumber` | `HomeAndConstructionBusiness` |
| Roofer | `RoofingContractor` | `HomeAndConstructionBusiness` |
| Gas Engineer | `HomeAndConstructionBusiness` | `LocalBusiness` |
| Plasterer/Renderer | `HomeAndConstructionBusiness` | `LocalBusiness` |
| Flooring/Carpets | `HomeAndConstructionBusiness` | `LocalBusiness` |
| Windows/Doors | `HomeAndConstructionBusiness` | `LocalBusiness` |
| Solar/Renewables | `HomeAndConstructionBusiness` | `LocalBusiness` |
| Dental Practice | `Dentist` | `MedicalBusiness` |
| Solicitor/Legal | `LegalService` | `Attorney` |
| Recruitment | `EmploymentAgency` | `LocalBusiness` |
| General Contractor | `GeneralContractor` | `HomeAndConstructionBusiness` |
| HVAC/Heating | `HVACBusiness` | `HomeAndConstructionBusiness` |
| Locksmith | `Locksmith` | `HomeAndConstructionBusiness` |
| Moving Company | `MovingCompany` | `LocalBusiness` |

## UK Trade Certifications

### Electrical
- NICEIC Approved Contractor
- NICEIC Domestic Installer
- NAPIT Registered
- ELECSA Approved
- Part P Registered

### Gas
- Gas Safe Registered (REQUIRED - include registration number)
- OFTEC Registered (oil)

### Roofing
- NFRC Member (National Federation of Roofing Contractors)
- Competent Roofer Scheme
- TrustMark Registered

### Windows/Doors
- FENSA Registered
- CERTASS Registered
- GGF Member (Glass and Glazing Federation)

### Renewables/Solar
- MCS Certified (Microgeneration Certification Scheme)
- RECC Member (Renewable Energy Consumer Code)
- NAPIT Registered

### General (applicable to most trades)
- Which? Trusted Traders
- Checkatrade Member
- TrustMark Registered
- Trading Standards Approved
- Federation of Master Builders
- Public Liability Insurance

## FAQ Templates by Industry

### Electrician
1. "How much does a full house rewire cost?" - Varies by property size, typically £3,000-£5,000 for a 3-bed. We provide free quotes.
2. "Do I need an EICR for my rental property?" - Yes, landlords must have a valid EICR every 5 years.
3. "Are you NICEIC approved?" - Yes, fully NICEIC approved with all work certified.
4. "Do you offer 24/7 emergency callouts?" - Yes, available 24/7 for electrical emergencies.
5. "How long does EV charger installation take?" - Typically 2-4 hours for standard installation.

### Roofer
1. "How much does a new roof cost?" - Depends on size and materials. Free surveys and quotes available.
2. "Do you repair flat roofs?" - Yes, we repair and install all flat roof types including EPDM and fibreglass.
3. "How long does roof replacement take?" - Most residential roofs completed in 3-5 days.
4. "Do you offer a guarantee?" - Yes, all work guaranteed with manufacturer warranties on materials.
5. "Can you fix a leaking roof quickly?" - Emergency repairs available, often same or next day.

### Plasterer/Renderer
1. "How much does rendering cost per m²?" - Typically £40-£80/m² depending on system and finish.
2. "What's the difference between render types?" - We offer silicone, monocouche, and traditional renders.
3. "How long does external rendering take?" - Average 3-bed house takes 5-7 days.
4. "Will rendering improve my home's insulation?" - Yes, especially with EWI systems.
5. "Do you offer coloured render?" - Yes, wide range of colours in through-coloured systems.

### Flooring/Carpets
1. "Do you offer free measuring?" - Yes, completely free no-obligation measuring service.
2. "Can you fit flooring I've bought elsewhere?" - Yes, we fit all types of flooring.
3. "How long does carpet fitting take?" - Most rooms completed same day.
4. "Do you remove old flooring?" - Yes, full uplift and disposal service available.
5. "What flooring is best for underfloor heating?" - LVT and engineered wood work best.

### Gas Engineer
1. "Are you Gas Safe registered?" - Yes, registration number XXX. (Always include actual number)
2. "How often should I service my boiler?" - Annually to maintain warranty and safety.
3. "How long does a boiler installation take?" - Standard swap typically 1 day.
4. "Do you offer boiler finance?" - Yes, 0% finance options available.
5. "What areas do you cover?" - We cover Leeds and surrounding areas within 20 miles.

### Windows/Doors
1. "Are you FENSA registered?" - Yes, all installations self-certified with FENSA.
2. "How long do new windows take to fit?" - Most homes completed in 1-2 days.
3. "What's your guarantee period?" - 10-year insurance-backed guarantee on all installations.
4. "Do you supply and fit composite doors?" - Yes, wide range of styles and colours.
5. "Will new windows reduce my energy bills?" - A-rated windows significantly improve insulation.

### Solar/Renewables
1. "Are you MCS certified?" - Yes, MCS certified for all installations.
2. "Can I get a government grant?" - We can advise on current grant schemes and eligibility.
3. "How long does solar panel installation take?" - Typically 1-2 days for residential systems.
4. "Will solar panels work on my roof?" - We offer free surveys to assess suitability.
5. "What's the payback period?" - Typically 6-10 years depending on usage and system size.

### Dental Practice
1. "Are you accepting new NHS patients?" - [Current status - update as needed]
2. "Do you offer emergency appointments?" - Yes, same-day emergency slots available.
3. "What finance options do you have?" - 0% finance available on treatments over £500.
4. "Do you offer teeth whitening?" - Yes, professional whitening treatments available.
5. "Is the practice wheelchair accessible?" - Yes, full disabled access available.

### Recruitment Agency
1. "Do candidates pay any fees?" - No, our service is completely free for candidates.
2. "What industries do you specialise in?" - [List specialisms]
3. "How quickly can you find me a job?" - Many candidates placed within 2 weeks.
4. "Do you offer temporary and permanent roles?" - Yes, both temp and perm placements.
5. "How do I register with you?" - Submit CV online or call to arrange consultation.

## Opening Hours JSON Templates

### Standard Trade (Mon-Fri 8-5, Sat morning)
```json
"openingHoursSpecification": [
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "08:00",
    "closes": "17:00"
  },
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": "Saturday",
    "opens": "09:00",
    "closes": "13:00"
  }
]
```

### 24/7 Emergency Service
```json
"openingHoursSpecification": [
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "00:00",
    "closes": "23:59"
  }
]
```

### Retail/Showroom
```json
"openingHoursSpecification": [
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "09:00",
    "closes": "17:30"
  },
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": "Saturday",
    "opens": "09:30",
    "closes": "16:30"
  }
]
```

### Dental/Medical (typical)
```json
"openingHoursSpecification": [
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday"],
    "opens": "09:00",
    "closes": "17:30"
  },
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": "Friday",
    "opens": "09:00",
    "closes": "17:00"
  }
]
```
