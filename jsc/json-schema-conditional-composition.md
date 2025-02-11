# JSON Schema Conditional Composition
C. Vasters (Microsoft) February 2025

## Abstract

This document specifies JSON Schema Conditional Composition, an extension to
JSON Schema Core that introduces composition constructs for combining multiple
schema definitions. In particular, this specification defines the semantics,
syntax, and constraints for the keywords `allOf`, `anyOf`, `oneOf`, and `not`,
as well as the `if`/`then`/`else` conditional construct. 

## Status of This Document

This document is an independent, experimental specification and is not
affiliated with any standards organization. It is a work in progress and may be
updated, replaced, or obsoleted by other documents at any time.

## Table of Contents

- [JSON Schema Conditional Composition](#json-schema-conditional-composition)
  - [Abstract](#abstract)
  - [Status of This Document](#status-of-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Terminology and Conventions](#2-terminology-and-conventions)
  - [3. Composition and Evaluation Model](#3-composition-and-evaluation-model)
  - [4. Conditional composition Keywords](#4-conditional-composition-keywords)
    - [4.1. `allOf`](#41-allof)
    - [4.2. `anyOf`](#42-anyof)
    - [4.3. `oneOf`](#43-oneof)
    - [4.4. `not`](#44-not)
    - [4.5. `if`/`then`/`else`](#45-ifthenelse)
  - [5. Security Considerations](#5-security-considerations)
  - [6. IANA Considerations](#6-iana-considerations)
  - [7. References](#7-references)
  - [8. Author's Address](#8-authors-address)

## 1. Introduction

This document specifies JSON Schema Conditionals, an extension to JSON Schema
Core that introduces conditional composition constructs for combining multiple
schema definitions. In particular, this specification defines the semantics,
syntax, and constraints for the keywords `allOf`, `anyOf`, `oneOf`, and `not`,
as well as the `if`/`then`/`else` conditional construct. 

## 2. Terminology and Conventions

The key words MUST, MUST NOT, SHALL, SHALL NOT, REQUIRED,
SHOULD, and OPTIONAL are to be interpreted as described in
[RFC2119](https://datatracker.ietf.org/doc/html/rfc2119) and
[RFC8174](https://datatracker.ietf.org/doc/html/rfc8174).

Unless otherwise specified, all references to “schema” refer to a JSON Schema
Core schema object.

## 3. Composition and Evaluation Model

The keywords introduced in this document extend the set of keywords allowed for
schemas as defined in JSON Schema Core.

The focus of JSON Schema Core is on data definitions. The conditional
composition keywords introduced in this document allow authors to define
conditional matching rules that use these fundamental data definitions.

A schema document using these keywords is not a data definition but a rule set
for evaluating JSON node instances against schema definitions and lays the
groundwork for validation.

The keywords defined herein MAY extend all
[non-schema](./json-schema-core.md#312-non-schema) and
[schema](./json-schema-core.md#31-schema) definitions.

Fundamentally, evaluating a JSON node against a schema involves matching the
node against the schema's constraints. 

The outcome of evaluating a JSON node against a schema is ultimately a boolean
value that states whether the node met all constraints defined in the schema.
The evaluation also creates an understanding of which constraint was met for
each subschema during evaluation.

A schema evaluation engine traverses the given JSON node and the schema
definition, evaluating the node and the schema recursively. When a conditional
composition keyword is encountered, the engine evaluates each subschema
independently against the current node and then combines the results as
specified by the composition keyword.

## 4. Conditional composition Keywords

This section defines several composition keywords that combine schema
definitions with evaluation rules. Each keyword has a specific evaluation
semantics that determines the outcome of the validation process.

### 4.1. `allOf`

The value of the `allOf` keyword MUST be a type-union array containing at least
one schema object. An JSON node is valid against `allOf` if and only if it is
valid against every schema in the array. 

Consider the following schema:

```json
{
  "allOf": [
    {
      "type": "object",
      "properties": {
        "a": { "type": "string" }
      },
      "required": ["a"],
      "additionalProperties": true
    },
    {
      "type": "object",
      "properties": {
        "b": { "type": "number" }
      },
      "required": ["b"],
      "additionalProperties": true
    },
    {
      "type": "object",
      "properties": {
        "c": { "type": "boolean" }
      },
      "required": ["c"],
      "additionalProperties": true
    }
  ]
}
```

Here, a JSON node evaluates to `true` if it is an object with at least three
properties `a`, `b`, and `c`, where `a` is a string, `b` is a number, and `c` is
a boolean:

```json
{
  "a": "string",
  "b": 42,
  "c": true
}
```

The JSON node satisfies all constraints defined by all subschemas.

Conflicting constraints among subschemas result in an unsatisfiable schema, for
example, if two subschemas require the same property to have different types or
if one of the subschemas had `additionalProperties` set to `false`.

### 4.2. `anyOf`

The value of `anyOf` keyword must be a type-union array containing at least one
schema object. An JSON node is valid against `anyOf` if and only if it is valid
against at least one of the schemas in the array. 

Consider the following schema:

```json
{
  "anyOf": [
    {
      "type": "object",
      "properties": {
        "a": { "type": "string" }
      },
      "required": ["a"],
      "additionalProperties": true
    },
    {
      "type": "object",
      "properties": {
        "b": { "type": "number" }
      },
      "required": ["b"],
      "additionalProperties": true
    },
    {
      "type": "object",
      "properties": {
        "c": { "type": "boolean" }
      },
      "required": ["c"],
      "additionalProperties": true
    }
  ]
}
```

Here, a JSON node evaluates to `true` if it is an object with at least one of
the properties `a`, `b`, or `c`, where `a` is a string, `b` is a number, and `c`
is a boolean:

```json
{
  "a": "string"
}
```

or 

```json
{
  "b": 42,
  "c": true
}
```

Both JSON nodes satisfy the constraints defined by at least one subschema.

### 4.3. `oneOf`

The value of the `oneOf` keyword must be a type-union array containing at least
one schema object. An JSON node is valid against `oneOf` if and only if it is
valid against exactly one of the schemas in the array. 

Consider the following schema:

```json
{
  "oneOf": [
    {
      "type": "object",
      "properties": {
        "a": { "type": "string" }
      },
      "required": ["a"],
      "additionalProperties": true
    },
    {
      "type": "object",
      "properties": {
        "b": { "type": "number" }
      },
      "required": ["b"],
      "additionalProperties": true
    },
    {
      "type": "object",
      "properties": {
        "c": { "type": "boolean" }
      },
      "required": ["c"],
      "additionalProperties": true
    }
  ]
}
```

Here, a JSON node evaluates to `true` if it is an object with exactly one of the
properties `a`, `b`, or `c`, where `a` is a string, `b` is a number, and `c` is a boolean:

```json
{
  "a": "string"
}
```

The following JSON node evaluates to `false` because it matches two subschemas:

```json
{
  "a": "string",
  "b": 42
}
```


### 4.4. `not`

The value of the keyword `not` is a single schema object, which MAY be a type
union. An JSON node is valid against `not` if it is not valid against the
schema. For example, the schema is written as follows:

```json
{
    "not": { "type": "string" }
}
```

Here, a JSON node evaluates to `true` if it is not a string:

```json
42
```

### 4.5. `if`/`then`/`else`

The values of the keywords `if`, `then`, and `else` are a schema objects. If the
processed JSON node is valid against the `if` schema, the `then` schema further
constrains the JSON node and MUST match the input. If the processed JSON node is
not valid against the `if` schema, the `else` schema further constrains the JSON
node and MUST match the input.

Consider the following schema:

```json
{
  "if": {
    "properties": {
      "a": { "type": "string" }
    },
    "required": ["a"]
  },
  "then": {
    "properties": {
      "b": { "type": "number" }
    },
    "required": ["b"]
  },
  "else": {
    "properties": {
      "c": { "type": "boolean" }
    },
    "required": ["c"]
  }
}
```

Here, a JSON node evaluates to `true` if it is an object with a property `a` that
is a string, then it must also have a property `b` that is a number:

```json
{
  "a": "string",
  "b": 42
}
```

Otherwise, if the JSON node does not have a property `a` that is a string, it
must have a property `c` that is a boolean:

```json
{
  "c": true
}
```

or 

```json
{
  "a": 42,
  "c": false
}
```

## 5. Security Considerations

- The use of composition keywords does not alter the security model of JSON
  Schema Core; however, excessive nesting or overly complex compositions may
  impact performance and resource usage.
- Implementations MUST ensure that all subschema references resolve within the
  same document or trusted sources to prevent external schema injection.

## 6. IANA Considerations

This document does not require any IANA actions.

## 7. References

- [RFC2119] Bradner, S., “Key words for use in RFCs to Indicate Requirement
  Levels”, RFC 2119.
- [RFC8174] Leiba, B., “Ambiguity of Uppercase vs Lowercase in RFC 2119 Key
  Words”, RFC 8174.
- [JSON Schema Core] C. Vasters, “JSON Schema Core”, February 2025.

## 8. Author's Address

Clemens Vasters  
Microsoft  
Email: clemensv@microsoft.com