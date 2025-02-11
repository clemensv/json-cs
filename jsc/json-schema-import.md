# JSON Schema Import  
C. Vasters (Microsoft) February 2025

## Abstract

This document specifies the `$import` and `$importdefs` keywords, as extensions
to [JSON Schema Core][JSON Schema Core]. These keywords allow a schema to import
definitions from external schema documents.

## Status of This Document

This document is an independent, experimental specification and is not
affiliated with any standards organization. It is a work in progress and may be
updated, replaced, or obsoleted by other documents at any time.

## Table of Contents
- [JSON Schema Import](#json-schema-import)
  - [Abstract](#abstract)
  - [Status of This Document](#status-of-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Conventions](#2-conventions)
  - [3. The `$import` and `$importdefs` Keywords](#3-the-import-and-importdefs-keywords)
    - [3.1 `$import` Keyword](#31-import-keyword)
    - [3.2 `$importdefs` Keyword](#32-importdefs-keyword)
  - [4. Examples](#4-examples)
    - [4.1. Example: Using `$import` to import an external schema](#41-example-using-import-to-import-an-external-schema)
    - [4.2. Example: Using `$import` with shadowing](#42-example-using-import-with-shadowing)
    - [4.3. Example: Using `$importdefs` to import the `$defs` section of an external schema](#43-example-using-importdefs-to-import-the-defs-section-of-an-external-schema)
  - [5. Resolving URIs](#5-resolving-uris)
  - [6. Security and Interoperability](#6-security-and-interoperability)
  - [7. IANA Considerations](#7-iana-considerations)
  - [8. References](#8-references)
  - [9. Author's Address](#9-authors-address)

## 1. Introduction

This document specifies the `$import` and `$importdefs` keywords, as extensions
to [JSON Schema Core][JSON Schema Core]. These keywords allow a schema to import
definitions from external schema documents.

All type reference expressions in [JSON Schema Core][JSON Schema Core], `$ref`
and `$extends` and `$addins`, are limited to references within the current
schema document. 

The `$import` and `$importdefs` keywords enable schema authors to incorporate
external schema documents into a schema.

Imports do not establish a reference relationship between the importing schema
and the imported schema. Imports _copy_ definitions from the imported schema
into the importing schema and those definitions are then treated as if they were
defined locally.

## 2. Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
NOT", "SHOULD", and "OPTIONAL" in this document are to be interpreted
as described in [RFC2119](#9.1-normative-references) and
[RFC8174](#9.1-normative-references).

## 3. The `$import` and `$importdefs` Keywords

The `$import` and `$importdefs` keywords are used to import definitions from
external schema documents into a local namespace within the current schema
document.

A schema processor MUST process the `$import` and `$importdefs` keywords before
processing any other keywords in the schema document.

The result of importing definitions is that the imported definitions are merged
into the local `$defs` section under the designated namespace as if they were
defined locally. 

A schema that uses `$import` or `$importdefs` MAY _shadow_ any imported
definitions with local definitions of the same name and in the same namespace,
replacing the imported definition entirely. Local definitions take precedence
over the imported definitions. A shadowing type cannot reference the imported
type that it shadows.

When importing definitions into a local namespace, the processor MUST ensure
that all imported cross-references are resolved within the imported definitions
themselves and not to the local schema. That means that any `jsonpointer`
instance (`$ref` or `$extends` or `$addins`) within imported definitions
MUST be prefixed with the local namespace under which the definitions were
imported. This applies recursively to any imported schema that itself contains
imports.

### 3.1 `$import` Keyword

The `$import` keyword is a reference expression whose value is an absolute URI
pointing to an external schema document. It is used to import all type
definitions of the external schema into a local namespace within the current
schema document.

When the keyword is used at the root level of a schema, the imported definitions
are available in the schema's root namespace. When used within the `$defs`
section, the imported definitions are available in the respective local
namespace.

> **Reminder**: Any type declaration at the root level of a schema and any type
> declaration at the root level of the `$defs` section is placed in the schema's
> root namespace per [JSON Schema Core, Section
> 3.3](json-schema-core.md#33-document-structure).

Example for `$import` at the root level:

```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
  "$import": "https://example.com/people.json"
}
```

Importing into the root namespace within the `$defs` section is equivalent to
the prior example:

```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
  "$defs": {
    "$import": "https://example.com/people.json"
  }
}
```	

One can also import into any local namespace within the `$defs` section:

```json
{
  "$defs": {
    "People": {
      "$import": "https://example.com/people.json"
    }
  }
}
```

The result of the import is that _all_ definitions from the external schema are
available under the `People` namespace. The namespace structure and any
cross-references that exist within an imported schema, including any imports
that it may have, are unaffected by being imported.

The `$import` keyword MAY be used many times within a schema to import multiple
external schemas into distinct local namespaces.

### 3.2 `$importdefs` Keyword

The `$importdefs` keyword is a reference expression whose value is an absolute
URI pointing to an external schema document. 

`$importdefs` works the same as `$import`, with the exception that it only
imports the `$defs` section of the external schema and not the root type.

The purpose of `$importdefs` is to use the type definitions from an external
schema as a library of types that can be referenced from within the local schema 
without importing the root type of the external schema.

## 4. Examples

### 4.1. Example: Using `$import` to import an external schema

Let the external schema be defined as follows:

```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
  "$id": "https://example.com/people.json",
  "name": "Person",
  "type": "object",
  "properties": {
    "firstName": { "type": "string" },
    "lastName": { "type": "string" },
    "address": { "$ref": "#/$defs/Address" }
  },
  "$defs": {
    "Address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "city": { "type": "string" }
      }
    }
  }
}
```

The importing schema uses `$import` to import the external schema into
the "People" namespace. The imported `Person` type is then used in the
local schema as the type of the `person` property:

```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
  "type": "object",
  "properties": {
    "person": {
      "type": { "$ref": "#/$defs/People/Person" }
    },
    "shippingAddress": {
      "type": { "$ref": "#/$defs/People/Address" }
    }
  },
  "$defs": {
    "People": {
      "$import": "https://example.com/people.json"
    }
  }
}
```

The imported `Person` type from the root of the external schema is available
under the `People` namespace in the local schema, alongside the imported
`Address` type.

The external schema can also be imported into the root namespace of the local
schema by using `$import` at the root level of the schema document in which case
the imported definitions are available in the root namespace of the local schema:

```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
  "$import": "https://example.com/people.json",
  "type": "object",
  "properties": {
    "person": {
      "type": { "$ref": "#/$defs/Person" }
    },
    "shippingAddress": {
      "type": { "$ref": "#/$defs/Address" }
    }
  },
}
```

The following schema is equivalent to the prior example:

```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
  "type": "object",
  "properties": {
    "person": {
      "type": { "$ref": "#/$defs/Person" }
    },
    "shippingAddress": {
      "type": { "$ref": "#/$defs/Address" }
    }
  },
  "$defs": {
    "$import": "https://example.com/people.json"
  }
}
```

### 4.2. Example: Using `$import` with shadowing

The external schema remains the same as in Example 4.1.

The importing schema uses `$import` to import the external schema into the
"People" namespace. The imported `Person` type is then used in the local
schema as the type of the `person` property. The local schema then also defines
an `Address` type that shadows the imported `Address` type within the same
namespace:

```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
  "type": "object",
  "properties": {
    "person": {
      "type": { "$ref": "#/$defs/People/Person" }
    }
  },
  "$defs": {
    "People": {
      "$import": "https://example.com/people.json",
      "Address": {
        "type": "object",
        "properties": {
          "street": { "type": "string" },
          "city": { "type": "string" },
          "postalCode": { "type": "string" },
          "country": { "type": "string" }
        }
      }
    }    
  }
}
```

### 4.3. Example: Using `$importdefs` to import the `$defs` section of an external schema

The external schema remains the same as in Example 4.1.

The importing schema uses `$importdefs` to import the `$defs` section of the
external schema into the "People" namespace. The imported `Address` type is then
used in the local schema as the type of the `shippingAddress` property as before.
However, the `Person` type is not imported and available.

```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
  "type": "object",
  "properties": {
    "shippingAddress": {
      "type": { "$ref": "#/$defs/People/Address" }
    }
  },
  "$defs": {
    "People": {
      "$importdefs": "https://example.com/people.json"
    }
  }
}
```

## 5. Resolving URIs

When resolving URIs, schema processors MUST follow the rules defined in
[RFC3986](https://tools.ietf.org/html/rfc3986) and
[RFC3987](https://tools.ietf.org/html/rfc3987).

This specification does not define any additional rules for resolving URIs 
into schema documents.


## 6. Security and Interoperability

- Schema processing engines MUST resolve the absolute URIs specified in
  `$import` and `$importdefs`, fetch the external schemas, and validate them to
  be schema documents.
- Implementations SHOULD employ caching and robust error handling for remote
  schema retrieval.
- External schema URIs SHOULD originate from trusted sources.
- Remote fetching of schemas SHOULD be performed over secure protocols (e.g.,
  HTTPS) to mitigate tampering.
- Excessively deep or circular import chains MUST be detected and mitigated to
  avoid performance degradation and potential denial-of-service conditions.

## 7. IANA Considerations

This document does not require any IANA actions.

## 8. References

- [RFC2119] Bradner, S., “Key words for use in RFCs to Indicate Requirement
  Levels”, RFC 2119.
- [RFC8174] Leiba, B., “Ambiguity of Uppercase vs Lowercase in RFC 2119 Key
  Words”, RFC 8174.
- [JSON Schema Core] C. Vasters, “JSON Schema Core”, February 2025.

## 9. Author's Address

**Clemens Vasters**  
Microsoft  
Email: clemensv@microsoft.com

---

[JSON Schema Core]: ./json-schema-core.md
