# JSON Schema Alternate Names and Descriptions
C. Vasters (Microsoft) February 2025

## Abstract

This document is an extension to [JSON Schema Core][JSON Schema Core]. It
defines three annotation keywords, `altnames`, `altenums`, and `descriptions`,
which allow schema authors to provide alternative identifiers, display names,
and multi-variant descriptions for types, properties, and enumeration values. 

## Status of This Document

This document is an independent, experimental specification and is not
affiliated with any standards organization. It is a work in progress and may be
updated, replaced, or obsoleted by other documents at any time.

## Table of Contents

- [JSON Schema Alternate Names and Descriptions](#json-schema-alternate-names-and-descriptions)
  - [Abstract](#abstract)
  - [Status of This Document](#status-of-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Conventions](#2-conventions)
  - [3. Keywords](#3-keywords)
    - [3.1. The `altnames` Keyword](#31-the-altnames-keyword)
    - [3.2. The `altenums` Keyword](#32-the-altenums-keyword)
    - [3.3. The `descriptions` Keyword](#33-the-descriptions-keyword)
  - [4. Security and Interoperability Considerations](#4-security-and-interoperability-considerations)
  - [5. IANA Considerations](#5-iana-considerations)
  - [6. References](#6-references)
    - [6.1. Normative References](#61-normative-references)
    - [6.2. Informative References](#62-informative-references)
  - [7. Author's Address](#7-authors-address)

## 1. Introduction

This document is an extension to [JSON Schema Core][JSON Schema Core]. It
defines three annotation keywords, `altnames`, `altenums`, and `descriptions`,
which allow schema authors to provide alternative identifiers, display names,
and multi-variant descriptions for types, properties, and enumeration values. 

These annotations facilitate mapping between internal schema identifiers and
external data representations (e.g., JSON keys that do not conform to identifier
rules) and support internationalization by enabling localized labels.  

## 2. Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
NOT", "SHOULD", and "OPTIONAL" in this document are to be interpreted
as described in [RFC2119](#9.1-normative-references) and
[RFC8174](#9.1-normative-references).

## 3. Keywords

This section defines the alternate names and symbols annotations.

### 3.1. The `altnames` Keyword

The `altnames` keyword provides alternative names for a named type or property.
Alternate names are not subject to the identifier syntax restrictions imposed on
`name` and MAY be used to map internal schema names to external representations.

The value of `altnames` MUST be a `map` where each key is a purpose indicator
and each value is a string representing an alternate name.

- The key `"json"` is RESERVED. When used, it specifies the property key to use
  for a property when encoded in JSON. This allows for JSON keys that do not
  conform to identifier rules.
- Keys starting with the prefix `"lang:"` (e.g., `"lang:en"`,
  `"lang:fr"`) are RESERVED for localized display names. The suffix after the
  colon specifies the language code. The language code MUST conform to the
  [RFC4646][RFC4646] standard. 
- Other keys are allowed for custom usage, provided they do not conflict with
  the reserved keys or prefixes.

The `altnames` keyword MAY be included in any schema element that has an
explicit name (i.e., named types or properties). When present, the alternate
names provide additional mappings that schema processors MAY use for encoding,
decoding, or user interface display.


Example:

```json
{
  "Person": {
    "type": "object",
    `altnames`: {
      "json": "person_data",
      "lang:en": "Person",
      "lang:de": "Person"
    },
    "properties": {
      "firstName": {
        "type": "string",
        `altnames`: {
          "json": "first_name",
          "lang:en": "First Name",
          "lang:de": "Vorname"
        }
      },
      "lastName": {
        "type": "string",
        `altnames`: {
          "json": "last_name",
          "lang:en": "Last Name",
          "lang:de": "Nachname"
        }
      }
    },
    "required": ["firstName", "lastName"]
  }
}
```

### 3.2. The `altenums` Keyword

The `altenums` keyword provides alternative representations (symbols) for
enumeration values defined by a type using the `enum` keyword. Alternate symbols
allow schema authors to map internal enum values to external codes or localized
display symbols.

The value of `altenums` MUST be a JSON object (map) where each key is a
purpose indicator and each corresponding value is an object mapping each
enumeration value (as defined in the `enum` array) to its alternate symbol.

- The key `"json"` is RESERVED and MUST be used to specify alternate symbols for
  JSON encoding. 
- Keys beginning with `"lang:"` (e.g., `"lang:en"`, `"lang:es"`) are
  RESERVED for providing localized alternate symbols.  
- Additional keys are permitted for custom usage, subject to no conflicts with
  reserved keys or prefixes.

The `altenums` keyword MUST be used only with schemas that include an `enum`
keyword. When present, it provides alternative representations for each
enumeration value that schema processors MAY use for encoding or display
purposes.

```json
{
  "Color": {
    "type": "string",
    "enum": ["RED", "GREEN", "BLUE"],
    `altenums`: {
      "json": {
        "RED": "#FF0000",
        "GREEN": "#00FF00",
        "BLUE": "#0000FF"
      },
      "lang:en": {
        "RED": "Red",
        "GREEN": "Green",
        "BLUE": "Blue"
      },
      "lang:de": {
        "RED": "Rot",
        "GREEN": "Grün",
        "BLUE": "Blau"
      }
    }
  }
}
```

### 3.3. The `descriptions` Keyword

The `descriptions` keyword provides multi-variant descriptions as an alternative
to the `description` keyword. The `descriptions` keyword allows schema authors to
provide localized or context-specific descriptions for types, properties, or
enumeration values.

The value of `descriptions` MUST be a `map` where each key is a purpose indicator
and each value is a string representing a description.

- Keys beginning with `"lang:"` (e.g., `"lang:en"`, `"lang:fr"`) are
  RESERVED for localized descriptions. The suffix after the colon specifies the
  language code. The language code MUST conform to the [RFC4646][RFC4646]
  standard.
- Other keys are allowed for custom usage, provided they do not conflict with
  the reserved keys or prefixes.

The `descriptions` keyword MAY be included in any schema element that can have
a description. When present, the descriptions provide additional mappings that
schema processors MAY use for user interface display.

Example:

```json
{
  "Person": {
    "type": "object",
    "descriptions": {
      "lang:en": "A person object with first and last name",
      "lang:de": "Ein Person-Objekt mit Vor- und Nachnamen",
      "lang:fr": "Un objet personne avec prénom et nom de famille",
      "lang:cn": "一个带有名字和姓氏的人对象",
      "lang:jp": "名前と姓を持つ人物オブジェクト"
    },
    "properties": {
      "firstName": {
        "type": "string",
        "descriptions": {
          "lang:en": "The first name of the person",
          "lang:de": "Der Vorname der Person",
          "lang:fr": "Le prénom de la personne",
          "lang:cn": "人的名字",
          "lang:jp": "人の名前"
        }
      },
      "lastName": {
        "type": "string",
        "descriptions": {
          "lang:en": "The last name of the person",
          "lang:de": "Der Nachname der Person",
          "lang:fr": "Le nom de famille de la personne",
          "lang:cn": "人的姓氏",
          "lang:jp": "人の姓"
        }
      }
    },
    "required": ["firstName", "lastName"]
  }
}
```

## 4. Security and Interoperability Considerations

Alternate names and symbols annotations do not affect the validation of instance
data. They are purely metadata and MUST be ignored by validators that do not
support this extension. However, applications that rely on alternate names for
mapping or localization MUST implement appropriate safeguards to ensure that the
alternate identifiers are used consistently.

## 5. IANA Considerations

This document has no IANA actions.

## 6. References

### 6.1. Normative References

- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement
  Levels", BCP 14, RFC 2119.
- [RFC8174] Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key
  Words", RFC 8174.
- [RFC4646] Phillips, A. and M. Davis, "Tags for Identifying Languages", RFC
  4646, DOI 10.17487/RFC4646, September 2006

### 6.2. Informative References

- [JSON Schema Core Specification] (refer to the companion core spec document)

## 7. Author's Address

Clemens Vasters  
Microsoft  
Email: clemensv@microsoft.com

---

[RFC4646]: https://tools.ietf.org/html/rfc4646
[JSON Schema Core]: ./json-schema-core.md