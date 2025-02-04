# JSON Schema Scientific Units  
C. Vasters (Microsoft) February 2024

## Abstract

This document specifies **JSON Schema Scientific Units**, an extension to JSON
Schema Core. This specification defines a set of annotation keywords for
associating scientific unit metadata and constraints with numeric values. JSON
Schema Scientific Units provides a mechanism for schema authors to explicitly
declare the measurement unit associated with numeric data, thereby enabling
precise mapping between schema representations and external data systems.

## 1. Introduction

JSON Schema Scientific Units is a companion specification to JSON Schema Core.
It defines annotation keywords that allow numeric types to be enriched with
measurement unit information. The primary purpose of this extension is to ensure
that numeric values are interpreted consistently by specifying their associated
scientific units. This extension is particularly useful in applications where
unit conversion, display localization, or high-precision calculations are
required.

This specification defines the syntax and semantics of the keywords that
annotate numeric types with scientific unit information. Implementations of JSON
Schema Core that support this extension **MUST** process these keywords
according to the rules defined herein.

## 2. Conventions

The key words **"MUST"**, **"MUST NOT"**, **"REQUIRED"**, **"SHALL"**, **"SHALL
NOT"**, **"SHOULD"**, and **"OPTIONAL"** in this document are to be interpreted
as described in [RFC2119](#7.1-normative-references) and
[RFC8174](#7.1-normative-references).

## 3. Scientific Units Keywords

This section defines the keywords used to annotate numeric types with scientific
unit information.

### 3.1. The "unit" Keyword

The `unit` keyword provides a mechanism for annotating a numeric schema (or a
schema based on a numeric extended type such as `number`, `int32`, `uint32`,
`int64`, `uint64`, `int128`, `uint128`, `float`, `double`, or `decimal`) with
its measurement unit.

The value of `unit` **MUST** be a JSON string.

#### 3.1.1 Constraints

The string value of `unit` **SHOULD** contain an SI unit symbol or a derived
unit symbol in conformance with the definitions of the Bureau International
des Poids et Mesures (BIPM) International System of Units (SI) \[[BIPM
SI](#BIPM)\].  

Deviating from this, the field **MAY** contain a non-SI unit symbol as defined
in NIST Handbook 44 Appendix C \[[NIST HB44](#NIST44)\].  

For derived units that reflect a multiplication, the unit symbols **MUST** be
separated by the asterisk character (`*`). For derived units that reflect a
division, the unit symbols **MUST** be separated by the forward slash (`/`).
The notation for exponentiation **MUST** be indicated using the caret (`^`).
For example, acceleration **SHALL** be denoted as `"m/s^2"`.  

Units that use Greek-language symbols (including supplementary or derived
units) such as Ohm (`"Ω"`) **MUST** be denoted with those Greek symbols (using
the corresponding Unicode code points).

#### 3.1.2. Usage:

The `unit` keyword **MAY** be used as an annotation on any schema element
whose underlying type is numeric. Schema processors that support JSON Schema
Scientific Units **MUST** use the value of the `unit` keyword to interpret,
convert, or display numeric values appropriately.

#### 3.1.3. Examples

| Measure               | `unit`  | Description                             | Reference |
| --------------------- | ------- | --------------------------------------- | --------- |
| Length                | `m`     | Meters, SI unit of length               | BIPM SI   |
| Velocity              | `m/s`   | Meters per second                       | BIPM SI   |
| Acceleration          | `m/s^2` | Meters per second squared               | BIPM SI   |
| Weight                | `kg`    | Kilograms, SI unit of mass              | BIPM SI   |
| Time                  | `s`     | Seconds, SI unit of time                | BIPM SI   |
| Temperature           | `K`     | Kelvin, SI unit of temperature          | BIPM SI   |
| Volume                | `L`     | Liters, non-SI unit accepted in SI      | BIPM SI   |
| Pressure              | `psi`   | Pounds per square inch, non-SI unit     | NIST HB44 |
| Energy                | `J`     | Joules, SI unit of energy               | BIPM SI   |
| Power                 | `W`     | Watts, SI unit of power                 | BIPM SI   |
| Electrical Resistance | `Ω`     | Ohms, SI unit of electrical resistance  | BIPM SI   |
| Electrical Current    | `A`     | Amperes, SI unit of electric current    | BIPM SI   |
| Light Intensity       | `cd`    | Candelas, SI unit of luminous intensity | BIPM SI   |
| Length                | `ft`    | Feet, non-SI unit                       | NIST HB44 |
| Volume                | `gal`   | Gallon, non-SI unit                     | NIST HB44 |

## 4. Integration with JSON Schema Core

JSON Schema Scientific Units is an extension to JSON Schema Core. Schema
documents that incorporate the `unit` keyword **MUST** also conform to the rules
and constraints defined in JSON Schema Core. The `unit` keyword is considered
metadata and does not affect schema validation of numeric values; it is intended
solely to provide additional information for encoding, conversion, and display
purposes.

## 5. Security and Interoperability Considerations

Alternate unit annotations do not affect the fundamental validation of instance
data. They are purely metadata and **MUST** be ignored by validators that do not
support this extension. Applications that rely on unit annotations for
conversion or display **MUST** implement appropriate validation against
recognized standards (BIPM SI and NIST HB44) to ensure consistency.

## 6. IANA Considerations

This document has no IANA actions.

## 7. References

### 7.1. Normative References

- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement
  Levels", BCP 14, RFC 2119.
- [RFC8174] Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key
  Words", RFC 8174.

### 7.2. Informative References

- [BIPM SI] Bureau International des Poids et Mesures, "The International System
  of Units (SI)".
- [NIST HB44] National Institute of Standards and Technology, "NIST Handbook
  44".

## 8. Author's Address

**Clemens Vasters**  
Microsoft  
Email: clemensv@microsoft.com
