# JSON Schema Import  
C. Vasters (Microsoft) February 2024

## Abstract

This document specifies the JSON Schema Import extension that allows a schema to
import definitions from external namespaces and compose schemas from multiple
sources.

## Table of Contents
- [JSON Schema Import](#json-schema-import)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Import Rules](#2-import-rules)
    - [2.1 `$import` Keyword](#21-import-keyword)
    - [2.2 `$importdefs` Keyword](#22-importdefs-keyword)
  - [3. Examples](#3-examples)
  - [4. Security and Interoperability](#4-security-and-interoperability)
  - [5. Security Considerations](#5-security-considerations)
  - [6. IANA Considerations](#6-iana-considerations)
  - [7. References](#7-references)
  - [8. Author's Address](#8-authors-address)

## 1. Introduction

JSON Schema Import Extensions allow schema authors to incorporate external JSON
Schema documents into a local schema. By mapping external schemas into local
namespaces via `$import` and `$importdefs`, all type definitions and reusable
components become available for reference using local JSON Pointers.

## 2. Import Rules

### 2.1 `$import` Keyword

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

### 2.2 `$importdefs` Keyword

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

## 3. Examples

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

## 4. Security and Interoperability

- Schema processing engines MUST resolve the absolute URIs specified in
  `$import` and `$importdefs`, fetch the external schemas, and validate them as
  JSON Schema Core documents.
- Imported definitions shall be merged into the local `$defs` under the
  designated namespace without altering the external definitions.
- Implementations SHOULD employ caching and robust error handling for remote
  schema retrieval.

## 5. Security Considerations

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
- [JSON Schema Core] C. Vasters, “JSON Schema Core”, February 2024.

## 8. Author's Address

**Clemens Vasters**  
Microsoft  
Email: clemensv@microsoft.com