# JSON Schema Composition  
C. Vasters (Microsoft) February 2025

## Abstract

This document specifies **JSON Schema Composition**, an extension to JSON Schema
Core that introduces additional composition constructs for combining multiple
schema definitions. In particular, this specification defines the semantics,
syntax, and constraints for the keywords **allOf**, **anyOf**, and **oneOf**.
These composition operators allow schema authors to build complex type
constraints by aggregating and disambiguating simpler schemas.

## Table of Contents

- [JSON Schema Composition](#json-schema-composition)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Terminology and Conventions](#2-terminology-and-conventions)
  - [3. Composition Keywords](#3-composition-keywords)
    - [3.1. `allOf`](#31-allof)
    - [3.2. `anyOf`](#32-anyof)
    - [3.3. `oneOf`](#33-oneof)
    - [3.4. `not`](#34-not)
    - [3.5. `if/then/else`](#35-ifthenelse)
  - [4. Interaction with JSON Schema Core](#4-interaction-with-json-schema-core)
  - [5. Implementation Considerations](#5-implementation-considerations)
  - [6. Security Considerations](#6-security-considerations)
  - [7. IANA Considerations](#7-iana-considerations)
  - [8. References](#8-references)
  - [9. Author's Address](#9-authors-address)

## 1. Introduction

JSON Schema Composition extends JSON Schema Core by enabling the combination of
multiple schema fragments into a single schema. This specification introduces
three composition keywords—**allOf**, **anyOf**, and **oneOf**—each with
distinct semantics for aggregating schema constraints. These extensions
facilitate reuse of schema definitions, refinement of type constraints, and
disambiguation of alternative representations.

## 2. Terminology and Conventions

The key words **MUST**, **MUST NOT**, **SHALL**, **SHALL NOT**, **REQUIRED**,
**SHOULD**, and **OPTIONAL** are to be interpreted as described in
[RFC2119](https://datatracker.ietf.org/doc/html/rfc2119) and
[RFC8174](https://datatracker.ietf.org/doc/html/rfc8174).

Unless otherwise specified, all references to “schema” refer to a JSON Schema
Core schema object. All composition subschemas MUST themselves be valid JSON
Schema Core documents or fragments.

## 3. Composition Keywords

### 3.1. `allOf`

The value of the `allOf` keyword must be a type-union array containing at least
one schema object. An instance is valid against `allOf` if and only if it is
valid against every schema in the array. For example, the schema is written as
follows:

```json
{
    "allOf": [
        { /* schema object A */ },
        { /* schema object B */ },
        { /* schema object C */ }
    ]
}
```

Each element in the array must be a valid JSON Schema Core schema. An instance
is valid if it satisfies all constraints specified by every schema in the array.
Conflicting constraints among subschemas result in an unsatisfiable schema.

### 3.2. `anyOf`

The value of `anyOf` keyword must be a type-union array containing at least one
schema object. An instance is valid against `anyOf` if and only if it is valid
against at least one of the schemas in the array. For example, the schema is
written as follows:

```json
{
    "anyOf": [
        { /* schema object A */ },
        { /* schema object B */ }
    ]
}
```

 Each element in the array must be a valid JSON Schema Core
schema. Validation succeeds if one or more of the subschemas validate the
instance. There is no requirement for the subschemas to be mutually exclusive.

### 3.3. `oneOf`

The value of the `oneOf` keyword must be a type-union array containing at least
one schema object. An instance is valid against `oneOf` if and only if it is
valid against exactly one of the schemas in the array. For example, the schema
is written as follows:

```json
{
    "oneOf": [
        { /* schema object A */ },
        { /* schema object B */ },
        { /* schema object C */ }
    ]
}
```

Each element in the array must be a valid JSON Schema Core schema. An instance
is valid if it validates against exactly one subschema. If none or more than one
subschema validates, the instance is invalid. Implementations may provide
detailed error reporting to indicate ambiguity when multiple subschemas
validate.

### 3.4. `not`

The value of the keyword `not` is a schema object. An instance is valid against `not` if it
is not valid against the schema. For example, the schema is written as follows:

```json
{
    "not": { /* schema object */ }
}
```

The `not` keyword must be a valid JSON Schema Core schema. An instance is valid
if it does not satisfy the constraints of the subschema. The `not` keyword is
equivalent to an `anyOf` construct with a single subschema and is provided for
readability and convenience.

### 3.5. `if/then/else`

The values of the keywords `if`, `then`, and `else` are a schema objects.
If the processed JSON node is valid against the `if` schema, the `then` schema 
further constrains the instance. If the processed JSON node is not valid against
the `if` schema, the `else` schema further constrains the instance. 

```json
{
    "if": { /* schema object */ },
    "then": { /* schema object */ },
    "else": { /* schema object */ }
}
```

Example:

```json
{
    "if": { "type": "string" },
    "then": { "minLength": 3 },
    "else": { "minLength": 5 }
}
```


## 4. Interaction with JSON Schema Core

- Composition keywords MAY be used at any level where a schema object is
  allowed.
- When a schema object contains composition keywords along with standard
  validation keywords (e.g., `type`, `properties`), the instance MUST satisfy
  both the core constraints and the constraints imposed by the composition
  keyword.
- The evaluation of **allOf**, **anyOf**, and **oneOf** occurs after the
  evaluation of the non-composition keywords in a schema object.
- Subschemas referenced within a composition keyword MAY use external or
  internal references as defined in JSON Schema Core.

## 5. Implementation Considerations

- Schema evaluation engines MUST process composition keywords by evaluating each
  subschema independently and then combining the results as specified.
- When using **oneOf**, implementations SHOULD guard against ambiguous
  validations by providing mechanisms for disambiguation.
- Authors are advised to avoid deeply nested composition constructs to prevent
  performance degradation.

## 6. Security Considerations

- The use of composition keywords does not alter the security model of JSON
  Schema Core; however, excessive nesting or overly complex compositions may
  impact performance and resource usage.
- Implementations MUST ensure that all subschema references resolve within the
  same document or trusted sources to prevent external schema injection.

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