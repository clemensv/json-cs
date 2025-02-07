# JSON Schema Alternate Names and Symbols  
C. Vasters (Microsoft) February 2025

## Abstract

This document specifies **JSON Schema Alternate Names and Symbols**, a companion
specification to JSON Schema Core. This extension provides a mechanism for
associating alternate names and symbols with named types, properties, and
enumerated values. Alternate names and symbols offer flexibility in mapping
schema definitions to different external representations and for localization
purposes.  

## Table of Contents

- [JSON Schema Alternate Names and Symbols](#json-schema-alternate-names-and-symbols)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Conventions](#2-conventions)
  - [3. Alternate Names and Symbols Keywords](#3-alternate-names-and-symbols-keywords)
    - [3.1. The "altnames" Keyword](#31-the-altnames-keyword)
      - [3.1.1. Reserved Keys and Prefixes](#311-reserved-keys-and-prefixes)
      - [3.1.2. Usage](#312-usage)
    - [3.2. The "altsymbols" Keyword](#32-the-altsymbols-keyword)
      - [3.2.1. Reserved Keys and Prefixes](#321-reserved-keys-and-prefixes)
      - [3.2.2. Usage](#322-usage)
      - [3.2.3. Example](#323-example)
  - [4. Integration with JSON Schema Core](#4-integration-with-json-schema-core)
  - [5. Security and Interoperability Considerations](#5-security-and-interoperability-considerations)
  - [6. IANA Considerations](#6-iana-considerations)
  - [7. References](#7-references)
    - [7.1. Normative References](#71-normative-references)
    - [7.2. Informative References](#72-informative-references)
  - [8. Author's Address](#8-authors-address)

## 1. Introduction

JSON Schema Alternate Names and Symbols is an extension to JSON Schema Core. It
defines two annotation keywords—**altnames** and **altsymbols**—which allow
schema authors to provide alternative identifiers and display representations
for types, properties, and enumeration values. These annotations facilitate
mapping between internal schema identifiers and external data representations
(e.g., JSON keys that do not conform to identifier rules) and support
internationalization by enabling localized labels.  

This specification complements JSON Schema Core by strictly defining the syntax
and semantics of alternate names and symbols. Implementations of JSON Schema
Core that support this extension MUST process these keywords as described
herein.

## 2. Conventions

The key words **"MUST"**, **"MUST NOT"**, **"REQUIRED"**, **"SHALL"**, **"SHALL
NOT"**, **"SHOULD"**, and **"OPTIONAL"** in this document are to be interpreted
as described in [RFC2119](#9.1-normative-references) and
[RFC8174](#9.1-normative-references).

## 3. Alternate Names and Symbols Keywords

This section defines the alternate names and symbols annotations.

### 3.1. The "altnames" Keyword

The `altnames` keyword provides alternative names for a named type or property.
Alternate names are not subject to the identifier syntax restrictions imposed on
primary names and MAY be used to map internal schema names to external
representations.

The value of `altnames` MUST be a JSON object (map) where each key is a purpose
indicator and each value is a string representing an alternate name.

#### 3.1.1. Reserved Keys and Prefixes

- The key `"json"` is RESERVED. When used, it specifies an alternate name for a
  property key when encoded in JSON.
- Keys starting with the prefix `"display:"` (e.g., `"display:en"`,
  `"display:fr"`) are RESERVED for localized display names.  
- Other keys are allowed for custom usage, provided they do not conflict with
  the reserved keys or prefixes.

#### 3.1.2. Usage

The `altnames` keyword MAY be included in any schema element that has an
explicit name (i.e., named types or properties). When present, the alternate
names provide additional mappings that schema processors MAY use for encoding,
decoding, or user interface display.


**Example:**

```json
{
  "Person": {
    "type": "object",
    "altnames": {
      "json": "person_data",
      "display:en": "Person",
      "display:de": "Person"
    },
    "properties": {
      "firstName": {
        "type": "string",
        "altnames": {
          "json": "first_name",
          "display:en": "First Name",
          "display:de": "Vorname"
        }
      },
      "lastName": {
        "type": "string",
        "altnames": {
          "json": "last_name",
          "display:en": "Last Name",
          "display:de": "Nachname"
        }
      }
    },
    "required": ["firstName", "lastName"]
  }
}
```

### 3.2. The "altsymbols" Keyword

The `altsymbols` keyword provides alternative representations (symbols) for
enumeration values defined by a type using the `enum` keyword. Alternate symbols
allow schema authors to map internal enum values to external codes or localized
display symbols.

The value of `altsymbols` MUST be a JSON object (map) where each key is a
purpose indicator and each corresponding value is an object mapping each
enumeration value (as defined in the `enum` array) to its alternate symbol.

#### 3.2.1. Reserved Keys and Prefixes

- The key `"json"` is RESERVED and MUST be used to specify alternate symbols for
  JSON encoding.  
- Keys beginning with `"display:"` (e.g., `"display:en"`, `"display:es"`) are
  RESERVED for providing localized alternate symbols.  
- Additional keys are permitted for custom usage, subject to no conflicts with
  reserved keys or prefixes.

#### 3.2.2. Usage

The `altsymbols` keyword MUST be used only with schemas that include an `enum`
keyword. When present, it provides alternative representations for each
enumeration value that schema processors MAY use for encoding or display
purposes.

#### 3.2.3. Example

```json
{
  "Color": {
    "type": "string",
    "enum": ["RED", "GREEN", "BLUE"],
    "altsymbols": {
      "json": {
        "RED": "#FF0000",
        "GREEN": "#00FF00",
        "BLUE": "#0000FF"
      },
      "display:en": {
        "RED": "Red",
        "GREEN": "Green",
        "BLUE": "Blue"
      },
      "display:de": {
        "RED": "Rot",
        "GREEN": "Grün",
        "BLUE": "Blau"
      }
    }
  }
}
```

## 4. Integration with JSON Schema Core

JSON Schema Alternate Names and Symbols is an extension to JSON Schema Core.
Schema documents that incorporate alternate names and symbols MUST conform to
JSON Schema Core. The keywords `altnames` and `altsymbols` are OPTIONAL
annotations. When provided, they supplement the core schema with additional
metadata for encoding and localization.

Implementations of JSON Schema Core that support this extension MUST process the
`altnames` and `altsymbols` keywords according to the rules set forth in this
specification.

## 5. Security and Interoperability Considerations

Alternate names and symbols annotations do not affect the validation of instance
data. They are purely metadata and MUST be ignored by validators that do not
support this extension. However, applications that rely on alternate names for
mapping or localization MUST implement appropriate safeguards to ensure that the
alternate identifiers are used consistently.

## 6. IANA Considerations

This document has no IANA actions.

## 7. References

### 7.1. Normative References

- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement
  Levels", BCP 14, RFC 2119.
- [RFC8174] Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key
  Words", RFC 8174.

### 7.2. Informative References

- [JSON Schema Core Specification] (refer to the companion core spec document)

## 8. Author's Address

**Clemens Vasters**  
Microsoft  
Email: clemensv@microsoft.com
