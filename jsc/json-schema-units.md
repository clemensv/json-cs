# JSON Schema Symbols, Scientific Units, and Currencies 
C. Vasters (Microsoft) February 2025

## Abstract

This document specifies "JSON Schema Symbols, Scientific Units, and Currencies",
an extension to JSON Schema Core. This specification defines a set of annotation
keywords for associating scientific unit and currency metadata and constraints,
primarily for use with numeric values. 

JSON Schema Scientific Units provides a mechanism for schema authors to
explicitly declare the unit associated with numeric data, thereby enabling
precise mapping between schema representations and external data systems.

## Status of This Document

This document is an independent, experimental specification and is not
affiliated with any standards organization. It is a work in progress and may be
updated, replaced, or obsoleted by other documents at any time.

## Table of Contents

- [JSON Schema Symbols, Scientific Units, and Currencies](#json-schema-symbols-scientific-units-and-currencies)
  - [Abstract](#abstract)
  - [Status of This Document](#status-of-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Conventions](#2-conventions)
  - [3. Symbol Annotations](#3-symbol-annotations)
    - [3.1. The `symbol` Keyword](#31-the-symbol-keyword)
      - [3.2. The `symbols` Keyword](#32-the-symbols-keyword)
  - [4. Scientific Unit Annotations](#4-scientific-unit-annotations)
    - [4.1. The `unit` Keyword](#41-the-unit-keyword)
    - [4.2. Unit Annotations](#42-unit-annotations)
    - [4.3. Unit Prefixes](#43-unit-prefixes)
  - [5. Currency Annotations](#5-currency-annotations)
    - [5.1. The `currency` Keyword](#51-the-currency-keyword)
  - [6. Security and Interoperability Considerations](#6-security-and-interoperability-considerations)
  - [7. IANA Considerations](#7-iana-considerations)
  - [8. References](#8-references)
    - [8.1. Normative References](#81-normative-references)
    - [8.2. Informative References](#82-informative-references)
  - [9. Author's Address](#9-authors-address)

## 1. Introduction

This document is a companion specification to JSON Schema Core. It defines
annotation keywords that allow numeric types to be enriched with measurement
unit or currency information. 

The primary purpose of this extension is to help numeric values to bne
interpreted consistently by specifying their associated scientific units or
currencies.

This specification defines the syntax and semantics of the keywords that
annotate numeric types with scientific unit or currency information.
Implementations of JSON Schema Core that support this extension MUST process
these keywords according to the rules defined herein.

## 2. Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
NOT", "SHOULD", and "OPTIONAL" in this document are to be interpreted
as described in [RFC2119](#7.1-normative-references) and
[RFC8174](#7.1-normative-references).

## 3. Symbol Annotations

This section defines the keywords used to annotate schema elements with
symbols that accompany values when presented to users.

### 3.1. The `symbol` Keyword

The `symbol` keyword provides a mechanism for annotating a schema element with a
symbol that annotates the value of the element when presented to users.

The keyword MAY appear alongside the `type` keyword in object properties or
array items or map values.

-  The value of `symbol` MUST be a JSON string.
-  The string value of `symbol` SHOULD contain a Unicode character or a
   multi-character symbol that represents the value of the annotated element.
-  The `symbol` keyword MAY be used as an annotation on any schema element.
-  `symbol` MAY be used in conjunction with `unit` or `currency` annotations or
   independently.

Example:

```json
{
  "type": "number",
  "currency": "EUR",
  "symbol": "€"
}
```

or

```json
{
  "type": "number",
  "unit": "m/s^2",
  "symbol": "m/s²"
}
```

or 

```json
{
  "type": "number",
  "description": "Number of bunnies",
  "symbol": "bunnies"
}
```

#### 3.2. The `symbols` Keyword

The `symbols` keyword provides a mechanism for annotating a schema element with a
set of symbols that annotate the value of the element when presented to users.

The keyword MAY appear alongside the `type` keyword in object properties or
array items or map values.

-  The value of `symbols` MUST be a `map`
-  The keys of the `symbols` map MUST be strings that represent a purpose
   indicator. The `lang:` prefix is reserved for language-specific symbols.
   The suffix after the colon specifies the language code. The language code
    MUST conform to the [RFC4646][RFC4646] standard.
-  The values of the `symbols` map MUST be strings that represent the symbol
-  The `symbols` keyword MAY be used as an annotation on any schema element.

Example:

```json
{
  "type": "number",
  "description": "Number of bunnies",
  "symbols": {
    "lang:en": "Bunnies",
    "lang:de": "Kaninchen",
    "lang:fr": "Lapins"
  }
}
```

## 4. Scientific Unit Annotations

This section defines the keywords used to annotate numeric types with scientific
unit information.

### 4.1. The `unit` Keyword

The `unit` keyword provides a mechanism for annotating a numeric schema (or a
schema based on a numeric extended type such as `number`, `int32`, `uint32`,
`int64`, `uint64`, `int128`, `uint128`, `float`, `double`, or `decimal`) with
its measurement unit.

The keyword MAY appear alongside the `type` keyword in object properties or
array items or map values.

-  The value of `unit` MUST be a JSON string.
-  The string value of `unit` SHOULD contain:
   - An SI unit symbol or derived unit symbol conforming to the Bureau International des
     Poids et Mesures (BIPM) International System of Units (SI) \[[BIPM SI](#BIPM)\]
   - A unit symbol defined in ISO/IEC 80000 series \[[ISO 80000](#ISO80000)\]
   - A non-SI unit symbol defined in NIST Handbook 44 Appendix C \[[NIST HB44](#NIST44)\]

For "derived" SI units that reflect a multiplication, the unit symbols MUST be
separated by the asterisk character (`*`). For derived units that reflect a
division, the unit symbols MUST be separated by the forward slash (`/`). The
notation for exponentiation MUST be indicated using the caret (`^`). For
example, acceleration SHALL be denoted as `"m/s^2"`.  

Units that use Greek-language symbols (including supplementary or derived
units) such as Ohm (`"Ω"`) MUST be denoted with those Greek symbols (using
the corresponding Unicode code points).

The `unit` keyword MAY be used as an annotation on any schema element
whose underlying type is numeric. Schema processors that support JSON Schema
Scientific Units MUST use the value of the `unit` keyword to interpret,
convert, or display numeric values appropriately.

Example:

```json
{
  "type": "number",
  "unit": "m/s^2"
}
```

### 4.2. Unit Annotations

This is a list of common scientific units that MAY be used with the `unit`. Units are defined according to ISO/IEC 80000, BIPM SI, and NIST HB44:

| Measure               | `unit`  | Description                             | Reference    |
| --------------------- | ------- | --------------------------------------- | ------------ |
| Length                | `m`     | Meters, SI unit of length               | ISO 80000-3  |
| Velocity              | `m/s`   | Meters per second                       | ISO 80000-3  |
| Acceleration          | `m/s^2` | Meters per second squared               | ISO 80000-3  |
| Weight                | `kg`    | Kilograms, SI unit of mass              | ISO 80000-4  |
| Time                  | `s`     | Seconds, SI unit of time                | BIPM SI      |
| Temperature           | `K`     | Kelvin, SI unit of temperature          | BIPM SI      |
| Volume                | `L`     | Liters, non-SI unit accepted in SI      | BIPM SI      |
| Pressure              | `psi`   | Pounds per square inch, non-SI unit     | NIST HB44    |
| Energy                | `J`     | Joules, SI unit of energy               | BIPM SI      |
| Power                 | `W`     | Watts, SI unit of power                 | BIPM SI      |
| Electrical Resistance | `Ω`     | Ohms, SI unit of electrical resistance  | BIPM SI      |
| Electrical Current    | `A`     | Amperes, SI unit of electric current    | BIPM SI      |
| Light Intensity       | `cd`    | Candelas, SI unit of luminous intensity | BIPM SI      |
| Area                  | `m^2`   | Square meters, SI unit of area          | BIPM SI      |
| Volume                | `m^3`   | Cubic meters, SI unit of volume         | BIPM SI      |
| Length                | `ft`    | Feet, non-SI unit                       | NIST HB44    |
| Volume                | `gal`   | Gallon, non-SI unit                     | NIST HB44    |
| Pressure              | `bar`   | Bar, non-SI unit                        | NIST HB44    |
| Digital Storage       | `B`     | Bytes, non-SI unit                      | ISO 80000-13 |
| Data Rate             | `bit/s` | Bits per second                         | ISO 80000-13 |

### 4.3. Unit Prefixes

The following SI prefixes MAY be used with base units:

| Prefix | Symbol | Factor |
| ------ | ------ | ------ |
| yotta  | Y      | 10²⁴   |
| zetta  | Z      | 10²¹   |
| exa    | E      | 10¹⁸   |
| peta   | P      | 10¹⁵   |
| tera   | T      | 10¹²   |
| giga   | G      | 10⁹    |
| mega   | M      | 10⁶    |
| kilo   | k      | 10³    |
| milli  | m      | 10⁻³   |
| micro  | μ      | 10⁻⁶   |
| nano   | n      | 10⁻⁹   |
| pico   | p      | 10⁻¹²  |
| hecto  | h      | 10²    |

Examples:

-  `"km"`: Kilometers
-  `"mm"`: Millimeters
-  `"μm"`: Micrometers
-  `"nm"`: Nanometers
-  `"ps"`: Picoseconds
-  `"mΩ"`: Milliohms
-  `"kΩ"`: Kilohms
-  `"MW"`: Megawatts

## 5. Currency Annotations

This section defines the keywords used to annotate numeric types with currency
information.

### 5.1. The `currency` Keyword

The `currency` keyword provides a mechanism for annotating a numeric schema (or a
schema based on a numeric extended type such as `number`, `int32`, `uint32`,
`int64`, `uint64`, `int128`, `uint128`, `float`, `double`, or `decimal`) with
a currency annotation.

The keyword MAY appear alongside the `type` keyword in object properties or
array items or map values.

-  The value of `currency` MUST be a JSON string.
-  The string value of `currency` SHOULD contain a three-letter currency code
   conforming to the ISO 4217 standard.
-  The `currency` keyword MAY be used as an annotation on any schema element

Example:

```json
{
  "type": "number",
  "currency": "EUR"
}
```

## 6. Security and Interoperability Considerations

Alternate unit annotations do not affect the fundamental validation of instance
data. They are purely metadata and MUST be ignored by validators that do not
support this extension. Applications that rely on unit annotations for
conversion or display MUST implement appropriate validation against
recognized standards (BIPM SI and NIST HB44) to ensure consistency.

## 7. IANA Considerations

This document has no IANA actions.

## 8. References

### 8.1. Normative References

- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement
  Levels", BCP 14, RFC 2119.
- [RFC8174] Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key
  Words", RFC 8174.

### 8.2. Informative References

- [BIPM SI] Bureau International des Poids et Mesures, "The International System
  of Units (SI)".
- [NIST HB44] National Institute of Standards and Technology, "NIST Handbook
  44".
- [ISO 80000] ISO/IEC 80000 series, "Quantities and units", particularly:
  - ISO 80000-1:2022 General principles
  - ISO 80000-3:2019 Space and time
  - ISO 80000-4:2019 Mechanics  
  - ISO 80000-13:2008 Information science and technology

## 9. Author's Address

Clemens Vasters  
Microsoft  
Email: clemensv@microsoft.com

---

[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC8174]: https://tools.ietf.org/html/rfc8174
[RFC4646]: https://tools.ietf.org/html/rfc4646
[BIPM SI]: https://www.bipm.org/en/about-us/
[NIST HB44]: https://www.nist.gov/publications/handbook-44-specifications-weights-and-measures
[ISO 80000]: https://www.iso.org/standard/76921.html
