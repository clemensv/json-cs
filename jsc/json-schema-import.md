# JSON Schema Import  
C. Vasters (Microsoft) February 2025

## Abstract

This document specifies the `$import` and `$importdefs` keywords, as extensions
to [JSON Schema Core][JSON Schema Core]. These keywords allow a schema to import
definitions from external schema documents.

## Table of Contents
- [JSON Schema Import](#json-schema-import)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Conventions](#2-conventions)
  - [3. The `$import` and `$importdefs` Keywords](#3-the-import-and-importdefs-keywords)
    - [3.1 `$import` Keyword](#31-import-keyword)
    - [3.2 `$importdefs` Keyword](#32-importdefs-keyword)
  - [4. Examples](#4-examples)
  - [5. Security and Interoperability](#5-security-and-interoperability)
  - [6. IANA Considerations](#6-iana-considerations)
  - [7. References](#7-references)
  - [8. Author's Address](#8-authors-address)

## 1. Introduction

This document specifies the `$import` and `$importdefs` keywords, as extensions
to [JSON Schema Core][JSON Schema Core]. These keywords allow a schema to import
definitions from external schema documents.

All type reference expressions in [JSON Schema Core][JSON Schema Core], `$ref`
and `$extends` and `$mixins`, are limited to the current schema document. The
`$import` and `$importdefs` keywords enable schema authors to incorporate
external JSON Schema documents into a local schema. By mapping


## 2. Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
NOT", "SHOULD", and "OPTIONAL" in this document are to be interpreted
as described in [RFC2119](#9.1-normative-references) and
[RFC8174](#9.1-normative-references).

## 3. The `$import` and `$importdefs` Keywords

### 3.1 `$import` Keyword

The `$import` keyword is a reference expression whose value is an absolute URI
pointing to an external JSON Schema Core document. It is used to import the
external schema’s designated root type (as determined by its `$root` marker or
inherent structure) into a local namespace. In practice, `$import` shall appear
as the only property within an object under `$defs`, with the property name
determining the local namespace for the imported root type.

**Example:**
```json
{
  "$defs": {
    "ExternalRoot": {
      "$import": "https://example.com/external-schema.json"
    }
  }
}
```

It is permissible to use the `$import` keyword multiple times within a schema to
import multiple external root types into distinct local namespaces. It is also
permissible to import into the schema's root namespace by using `$import`
directly inside the `$defs` section.

### 3.2 `$importdefs` Keyword

The `$importdefs` keyword is a reference expression whose value is an absolute
URI pointing to an external JSON Schema Core document. It imports the entire
`$defs` section from the external schema into a local namespace. In practice,
`$importdefs` shall appear as the only property within an object under `$defs`,
with the property name determining the local namespace for the imported
definitions.

**Example:**
```json
{
  "$defs": {
    "ExternalDefinitions": {
      "$importdefs": "https://example.com/external-schema.json"
    }
  }
}
```

It is permissible to use the `$importdefs` keyword multiple times within a schema
to import multiple external `$defs` sections into distinct local namespaces. It
is also permissible to import into the schema's root `$defs` section by using
`$importdefs` directly inside the `$defs` section.

## 4. Examples

The following JSON Schema document demonstrates the use of both `$import` and
`$importdefs`:

```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
  "$defs": {
    "LocalTypes": {
      "MyLocalType": {
        "name": "MyLocalType",
        "type": "object",
        "properties": {
          "id": { "type": "string" }
        },
        "required": ["id"]
      }
    },
    "ExternalRoot": {
      "$import": "https://example.com/external-schema.json"
    },
    "ExternalDefinitions": {
      "$importdefs": "https://example.com/external-schema.json"
    }
  },
  "name": "RootType",
  "type": "object",
  "properties": {
    "local": { "$ref": "#/$defs/LocalTypes/MyLocalType" },
    "externalRoot": { "$ref": "#/$defs/ExternalRoot/RootType" },
    "externalDef": { "$ref": "#/$defs/ExternalDefinitions/SomeExternalType" }
  },
  "required": ["local", "externalRoot", "externalDef"]
}
```

In this example:
- The external schema's root type is imported into the `ExternalRoot` namespace
  using `$import`.
- All definitions from the external schema’s `$defs` section are imported into
  the `ExternalDefinitions` namespace using `$importdefs`.

## 5. Security and Interoperability

- Schema processing engines MUST resolve the absolute URIs specified in
  `$import` and `$importdefs`, fetch the external schemas, and validate them as
  JSON Schema Core documents.
- Imported definitions shall be merged into the local `$defs` under the
  designated namespace without altering the external definitions.
- Implementations SHOULD employ caching and robust error handling for remote
  schema retrieval.

- External schema URIs MUST originate from trusted sources.
- Remote fetching of schemas SHOULD be performed over secure protocols (e.g.,
  HTTPS) to mitigate tampering.
- Excessively deep or circular import chains MUST be detected and mitigated to
  avoid performance degradation and potential denial-of-service conditions.

## 6. IANA Considerations

This document does not require any IANA actions.

## 7. References

- [RFC2119] Bradner, S., “Key words for use in RFCs to Indicate Requirement
  Levels”, RFC 2119.
- [RFC8174] Leiba, B., “Ambiguity of Uppercase vs Lowercase in RFC 2119 Key
  Words”, RFC 8174.
- [JSON Schema Core] C. Vasters, “JSON Schema Core”, February 2025.

## 8. Author's Address

**Clemens Vasters**  
Microsoft  
Email: clemensv@microsoft.com

---

[JSON Schema Core]: ./json-schema-core.md
