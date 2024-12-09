# JSON-CS (Compact Schema)

C. Vasters (Microsoft) November 2024

## Abstract

This document specifies **JSON-CS (Compact Schema)**, a schema language for JSON
data that enforces strict typing, modularity, and determinism. JSON-CS provides
a clear and self-contained approach to defining JSON data structures, requiring
explicit type declarations and reusable, hierarchical type definitions. It
ensures consistent structure, promoting clarity and scalability in schema
design.

JSON-CS leans on a substantially reduced set of structural elements of the
various Internet drafts published by the JSON Schema project. The motivation for
creating JSON-CS is that JSON Schema's compositional complexity is generally
seen as impractical for message and event definitions as well as for abstract
data structure definitions that are shared with the goal of aligning data
structures in programs and databases. On the other hand, JSON-CS expands the
information set with attributes like `unit` and `examples` to provide richer
formal descriptions of data structures as well as `altname` and `altsymbols` to
support internationalization and alternate naming conventions.

JSON-CS drops most compositional features of JSON Schema, such as `$ref` with
external references, `allOf`, `anyOf`, `oneOf`, `not`, `if`, `then`, `else`, and
`contains`. It also drops the majority of JSON Schemas validation features.
JSON-CS retains type unions in the form of an array of types in the `type`
keyword instead of using `oneOf`, but it does not support unions at the root
level of the schema document. The validation keywords `multipleOf`, `maximum`,
`minimum`, `exclusiveMaximum`, `exclusiveMinimum`, `maxItems`, `minItems`,
`uniqueItems`, `maxProperties`, `minProperties`, `minContains`, and
`maxContains` are dropped. `maxLength` is retained for strings, but `minLength`
is dropped. `pattern` is retained for strings.

JSON-CS also drops the `definitions`/`$defs` keyword and instead treats the
entire schema document as a single namespace.

## Status of This Memo

This is a thought experiment requesting feedback.

## Copyright Notice

Copyright (c) 2024 Microsoft Corporation. All rights reserved.

## Table of Contents

- [JSON-CS (Compact Schema)](#json-cs-compact-schema)
  - [Abstract](#abstract)
  - [Status of This Memo](#status-of-this-memo)
  - [Copyright Notice](#copyright-notice)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Conventions Used in This Document](#2-conventions-used-in-this-document)
  - [3. JSON-CS Specification](#3-json-cs-specification)
    - [3.1. Schema Definition](#31-schema-definition)
    - [3.2. Data Types](#32-data-types)
      - [3.2.1. Primitive Types](#321-primitive-types)
      - [3.2.2. Compound Types](#322-compound-types)
    - [3.3. Document Structure](#33-document-structure)
      - [3.3.1. Namespaces](#331-namespaces)
      - [3.3.2. Type Definitions](#332-type-definitions)
      - [3.3.3. Document root](#333-document-root)
      - [3.3.4. Alternate Names](#334-alternate-names)
        - [3.3.4.1. Alternate Names for JSON Encoding](#3341-alternate-names-for-json-encoding)
        - [3.3.4.2. Alternate Names for Display (Internationalization)](#3342-alternate-names-for-display-internationalization)
        - [3.3.4.3. Alternate Symbols for Enums](#3343-alternate-symbols-for-enums)
    - [3.4. Typing Rules](#34-typing-rules)
    - [3.5. Composition Rules](#35-composition-rules)
      - [3.5.1 Unions](#351-unions)
      - [3.5.1.1 Prohibition of Top-Level Unions](#3511-prohibition-of-top-level-unions)
      - [3.5.2 Maps](#352-maps)
      - [3.5.3. Arrays](#353-arrays)
    - [3.6. Identifier Rules](#36-identifier-rules)
    - [3.7. Structural Keywords](#37-structural-keywords)
      - [3.7.1. The "type" Keyword](#371-the-type-keyword)
      - [3.7.2. The "properties" Keyword](#372-the-properties-keyword)
      - [3.7.3. The "required" Keyword](#373-the-required-keyword)
      - [3.7.4. The "items" Keyword](#374-the-items-keyword)
      - [3.7.5. The "values" Keyword](#375-the-values-keyword)
      - [3.7.6. Reuse of Type Definitions with Restricted Polymorphism](#376-reuse-of-type-definitions-with-restricted-polymorphism)
        - [3.7.6.1. The "abstract" Keyword](#3761-the-abstract-keyword)
        - [3.7.6.2. The "$extends" Keyword](#3762-the-extends-keyword)
      - [3.7.7. Additional Structural Keywords](#377-additional-structural-keywords)
        - [3.7.7.1. The "const" Keyword](#3771-the-const-keyword)
        - [3.7.7.2. The "unit" Keyword](#3772-the-unit-keyword)
        - [3.7.7.3. The "format" Keyword](#3773-the-format-keyword)
        - [3.7.7.4. The "enum" Keyword](#3774-the-enum-keyword)
        - [3.7.7.5. The "description" Keyword](#3775-the-description-keyword)
        - [3.7.7.6. The "default" Keyword](#3776-the-default-keyword)
        - [3.7.7.7. The "additionalProperties" Keyword](#3777-the-additionalproperties-keyword)
        - [3.7.7.8. The "examples" Keyword](#3778-the-examples-keyword)
        - [3.7.7.9. The "altnames" Keyword](#3779-the-altnames-keyword)
        - [3.7.7.10. The "altsymbols" Keyword](#37710-the-altsymbols-keyword)
        - [3.7.7.10 The "maxLength" Keyword](#37710-the-maxlength-keyword)
    - [3.8. Validation Rules](#38-validation-rules)
    - [3.9. Reserved Keywords](#39-reserved-keywords)
  - [4. Examples](#4-examples)
    - [4.1. Using "const", "unit", and "format"](#41-using-const-unit-and-format)
    - [4.2. Using "description", "default", and "examples"](#42-using-description-default-and-examples)
    - [4.3. Using "additionalProperties"](#43-using-additionalproperties)
    - [4.4. Using "altnames" and "altsymbols"](#44-using-altnames-and-altsymbols)
  - [5. Compatibility with JSON Schema Drafts](#5-compatibility-with-json-schema-drafts)
    - [5.1. JSON Schema Draft-07 Compatibility](#51-json-schema-draft-07-compatibility)
      - [Example](#example)
    - [5.2. JSON Schema Draft-2019-09 and Later Compatibility](#52-json-schema-draft-2019-09-and-later-compatibility)
      - [Example](#example-1)
    - [5.3. Type References](#53-type-references)
    - [5.4. Schema Compatibility](#54-schema-compatibility)
      - [Constraints for Compatibility](#constraints-for-compatibility)
    - [5.5. Mapping Namespaces](#55-mapping-namespaces)
      - [Example with Namespaces](#example-with-namespaces)
    - [5.6. Limitations](#56-limitations)
  - [6. Security Considerations](#6-security-considerations)
  - [7. IANA Considerations](#7-iana-considerations)
  - [8. References](#8-references)
    - [8.1. Normative References](#81-normative-references)
    - [8.2. Informative References](#82-informative-references)
  - [9. Author's Address](#9-authors-address)
  - [10. Appendix: Metaschema](#10-appendix-metaschema)
    - [10.1 JSON-CS Metaschema](#101-json-cs-metaschema)
    - [10.2. JSON Schema Draft 07 Metaschema](#102-json-schema-draft-07-metaschema)

## 1. Introduction

JSON-CS (Compact Schema) is a schema language designed for defining JSON data
structures with strict typing, modularity, and determinism. It provides a clear
and self-contained approach to schema validation, requiring explicit type
declarations and reusable, hierarchical type definitions. JSON-CS enforces a
consistent structure that promotes clarity and scalability in schema design.

## 2. Conventions Used in This Document

The key words **"MUST"**, **"MUST NOT"**, **"REQUIRED"**, **"SHALL"**, **"SHALL
NOT"**, **"SHOULD"**, **"SHOULD NOT"**, **"RECOMMENDED"**, **"NOT
RECOMMENDED"**, **"MAY"**, and **"OPTIONAL"** in this document are to be
interpreted as described in [BCP 14](#RFC2119) \[[RFC2119](#RFC2119)\]
\[[RFC8174](#RFC8174)\] when, and only when, they appear in all capitals, as
shown here.

## 3. JSON-CS Specification

### 3.1. Schema Definition

A JSON-CS schema is a definition of a JSON node. The schema describes the
expected structure and constraints of JSON data at a particular node in the JSON
document. A minimal schema is:

```json
{ 
  "type": "string" 
}
```

This schema constrains a JSON node to be of type `string`. A JSON-CS document is
a composition of type definitions, each defining schemas for different parts of
the JSON data.

### 3.2. Data Types

#### 3.2.1. Primitive Types

The primitive types are:

- **string**: Represents textual data encoded in UTF-8.

- **integer**: Represents whole numbers without fractional components.

- **number**: Represents numeric values, including integers and floating-point
  numbers.

- **boolean**: Represents a logical value, either `true` or `false`.

- **null**: Represents an explicit absence of a value.

#### 3.2.2. Compound Types

The compound types are:

- **object**: An unordered collection of zero or more name-value pairs, where
  names (also called keys) are strings, and values are any valid JSON value.

- **array**: An ordered list of zero or more values.

- **map**: A special type similar to an object, where all keys conform to
  identifier rules, and all values conform to a specified schema.

### 3.3. Document Structure

A JSON-CS document is a JSON object that contains type definitions. The
structure of the document defines namespaces, types, and can include alternate
names for types and properties.

A JSON-CS document SHOULD be made distinguishable from other JSON documents by use
of the `$schema` keyword. The `$schema` keyword is a string that identifies the
version of the JSON-CS specification used in the document.

For this version of the specification, the identifier is set to
`"https://schemas.vasters.com/experimental/json-cs/v0"`.

```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-cs/v0",
  "type": "string"
}
```

As explained in section [5. Compatibility with JSON Schema
Drafts](#5-compatibility-with-json-schema-drafts), the `$schema` value can
also be used to indicate (limited) compatibility with JSON Schema drafts to a
JSON-CS document processor.

Types can be defined into the empty namespace at the root of the document or
within explicitly named namespaces.

For example, the following JSON-CS document defines a `Person` type at the root
level. The `name` keyword is used to name the type. The `name` keyword is
OPTIONAL but RECOMMENDED.

```json
{
  "name": "Person",
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name", "age"],
  "additionalProperties": false  
}
```

If and only if a `type` is defined at the [root of the
document](#333-document-root), any other type declaration MUST be placed into
the empty namespace explicitly as the "Address" type below. Both "Person" and
Address" types of the example below are thus effectively placed into the empty
namespace.

As will be discussed in section [5. Compatibility with JSON Schema
Drafts](#5-compatibility-with-json-schema-drafts), the empty namespace
declaration below is equivalent to JSON Schema's `definitions`/`$defs` keyword.

Also shown in the example below is the use of the `$ref` keyword to reference
the "Address" type from the "Person" type. In JSON-CS, the `$ref` keyword MUST
be used exclusively to reference schemas declared within the same document.

```json
{
  "name": "Person",
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "integer" },
    "address" : { "$ref" : "#/Address" }
  },
  "required": ["name", "age"],
  "additionalProperties": false,
  "" : {
    "Address": {
        "name": "Address",
        "type": "object",
        "properties": {
          "street": { "type": "string" },
          "city": { "type": "string" },
          "state": { "type": "string" },
          "zip": { "type": "string" }
        },
        "required": ["street", "city", "state", "zip"],
        "additionalProperties": false
    }
  }
}
```

If no `type` is defined at the root of the document, the document is considered to be
the root of the empty namespace. The following example defines the same types as
above, but without a root-level `type` present.

```json
{
    "Person": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "age": { "type": "integer" },
        "address" : { "$ref" : "#/Address" }
      },
      "required": ["name", "age"],
      "additionalProperties": false
    },
    "Address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" },
        "zip": { "type": "string" }
      },
      "required": ["street", "city", "state", "zip"],
      "additionalProperties": false
    }
}
```

A definition with an explicit empty namespace declaration is equivalent to the
definition above:

```json
{
    "" : {
        "Person": {
           ...
        },
        "Address": {
          ...
        }
    }
}
```

The following example places both types into a namespace named "MyTypes":

```json
{
  "MyTypes": {
    "Person": {
      ...
    },
    "Address": {
      ...
    }
  }
}
```

#### 3.3.1. Namespaces

A namespace is a logical grouping of type definitions. Namespaces are defined
using keys at the root of the document or nested within other namespaces.

Namespaces can be nested to create hierarchical structures.

The empty namespace is the root namespace of the document. Types defined at the
root of the document without a namespace key are placed into the empty
namespace.

An empty string (`""`) is used to represent the empty namespace. If the empty
namespace is explicitly declared, no other namespace can be defined at the root
level.

If a `type` is defined at the root of the document, any other type declaration
MUST be placed into the empty namespace explicitly by using the empty string
(`""`) as the key at the root level and placing the type definition within it.

#### 3.3.2. Type Definitions

A type definition associates a name with a schema. Type definitions are placed
within namespaces.

A type defined at the root of the document without a namespace key is place into
the empty namespace. A type defined at the root of the document without a `name`
key is an anonymous type.

If a `name` keyword is present, its value MUST be a string conforming to the
identifier rules and it MUST match the key of the type definition (unless the
type is the root type).

#### 3.3.3. Document root

Generally, a JSON-CS schema is a collection of type definitions that is meant to
exchange data structure definitions between systems.

For the purpose of using JSON-CS schemas as a validation mechanism for JSON
document instances, one or more of the type definitions in the schema can be
designated as the expected root type(s) of the document or object to be validated.
This is done using the `$root` keyword.

The OPTIONAL `$root` keyword is a JSON Pointer expression or an array of such
expressions that MUST be resolvable to (a) schema declaration(s) within the
document. If the value is an array, it forms a type union for the root type.

A root type is implicitly defined by a `type` definition at the root of the
document.

The following example designates the "Person" type as the root type:

```json
{
  "$root": "#/MyTypes/Person",
  "MyTypes": {
    "Person": {
      ...
    },
    "Address": {
      ...
    }
  }
}
```

This example designates a type union of "Person" and "Address" as the root type:

```json
{
  "$root": ["#/MyTypes/Person", "#/MyTypes/Address"],
  "MyTypes": {
    "Person": {
      ...
    },
    "Address": {
      ...
    }
  }
}
```

#### 3.3.4. Alternate Names

All named types and properties **MAY** have an optional `altnames` attribute,
which is a map of alternative names for the named type or property. Alternative
names are different from identifiers in that they are not restricted to the
identifier rules and can be any string.

The `altnames` attribute allows for the specification of alternative names for
various purposes, such as mapping to JSON keys that do not conform to the
identifier rules, or providing localized display names for internationalization.

The `key` of an alternate name in the `altnames` map indicates its purpose,
while the `value` is the alternative name itself. The key value `"json"` and the
key-prefix `"display:"` are reserved; any other keys are user-defined.

For enumerated types (types using the `enum` keyword), the `altsymbols`
attribute is used to provide alternate names for the enumeration values. The
`altsymbols` attribute contains a map where each key is the purpose of the
alternate name, and the value is another map. This inner map is keyed by the
enumeration value and contains the alternate name.

##### 3.3.4.1. Alternate Names for JSON Encoding

For JSON encoding purposes, the `altnames` attribute can be used to map property
names to JSON keys that are incompatible with the identifier rules. The reserved
key for this purpose is `"json"`.

**Example**:

```json
{
  "": {
    "Contact": {
      "type": "object",
      "properties": {
        "firstName": {
          "type": "string",
          "altnames": { "json": "first-name" }
        },
        "lastName": {
          "type": "string",
          "altnames": { "json": "last-name" }
        }
      },
      "required": ["firstName", "lastName"],
      "additionalProperties": false
    }
  }
}
```

- **Explanation**:

  - Defines a `Contact` type with properties `firstName` and `lastName`.

  - The `altnames` attribute is used to specify that in JSON encoding, the
    property `firstName` corresponds to the JSON key `"first-name"`, and
    `lastName` corresponds to `"last-name"`.

  - This allows the schema to map properties to JSON keys that include
    characters not allowed in identifiers, such as hyphens.

##### 3.3.4.2. Alternate Names for Display (Internationalization)

For the purpose of internationalization, the `altnames` attribute can provide
localized display names for types and properties. The reserved key-prefix for
this purpose is `"display:"`, followed by a language code as defined by [RFC
5646](#RFC5646).

**Example**:

```json
{
  "": {
    "Address": {
      "type": "object",
      "properties": {
        "street": {
          "type": "string",
          "altnames": {
            "display:de": "Straße",
            "display:ja": "番地",
            "display:fr": "Rue"
          }
        },
        "city": {
          "type": "string",
          "altnames": {
            "display:de": "Stadt",
            "display:ja": "市",
            "display:fr": "Ville"
          }
        },
        "state": {
          "type": "string",
          "altnames": {
            "display:de": "Bundesland",
            "display:ja": "都道府県",
            "display:fr": "État"
          }
        },
        "zip": {
          "type": "string",
          "altnames": {
            "display:de": "Postleitzahl",
            "display:ja": "郵便番号",
            "display:fr": "Code postal"
          }
        }
      },
      "required": ["street", "city", "state", "zip"],
      "additionalProperties": false
    }
  }
}
```

- **Explanation**:

  - Defines an `Address` type with properties `street`, `city`, `state`, and
    `zip`.

  - The `altnames` attribute provides localized display names for each property
    in German (`"display:de"`), Japanese (`"display:ja"`), and French
    (`"display:fr"`).

  - This allows applications to present property names in the user's preferred
    language.

##### 3.3.4.3. Alternate Symbols for Enums

For enumerated types (types that use the `enum` keyword), the `altsymbols`
attribute provides alternative names for enumeration values. The `altsymbols`
attribute is a map where each key is the purpose (e.g., `"json"`), and the value
is a map of enumeration values to their alternate names.

**Example**:

```json
{
  "": {
    "Color": {
      "type": "string",
      "enum": ["RED", "GREEN", "BLUE"],
      "altsymbols": {
        "json": {
          "RED": "#FF0000",
          "GREEN": "#00FF00",
          "BLUE": "#0000FF"
        }
      }
    }
  }
}
```

- **Explanation**:

  - Defines a `Color` type which is a string constrained to the values `"RED"`,
    `"GREEN"`, or `"BLUE"` using the `enum` keyword.

  - The `altsymbols` attribute specifies that in JSON encoding, the value
    `"RED"` corresponds to `"#FF0000"`, `"GREEN"` to `"#00FF00"`, and `"BLUE"`
    to `"#0000FF"`.

  - This allows the schema to map enum values to alternate representations, such
    as color codes.

### 3.4. Typing Rules

1. **Type Declarations**:

- Every schema element **MUST** explicitly declare its `type`.

- Supported types are:

  - Primitive types: `string`, `integer`, `number`, `boolean`, `null`.

  - Compound types: `object`, `array`, `map`.

1. **Reusable Types**:

- Types **MUST** be declared within namespaces and referenced using `$ref`.

3. **Type References**:

- `$ref` **MUST** be used exclusively to reference previously declared types
  within the same document.

- A `$ref` value **MUST** resolve to a valid JSON Pointer
  \[[RFC6901](#RFC6901)\] that points to an already declared type.

- `$ref` **MUST** only be used as the value of a `type` attribute and **MUST
  NOT** be combined with additional attributes.

1. **Prohibition of Inline Definitions**:

- Types **MUST NOT** be defined inline in arrays, maps, or unions or within
  property definitions. However, inside unions or property definitions, the definition
  of `map` and `array` types with primitive values is allowed.
- Only references to compound type declared in the document or primitive
  types are allowed in these contexts.

1. **Dynamic Structures**:

- Dynamic key-value pairs are defined using the `map` type.
- The `values` attribute of a `map` **MUST** reference a compound type
  declared in the document or be a primitive type.

### 3.5. Composition Rules

#### 3.5.1 Unions

- JSON-CS supports type unions using an array in the `type` attribute.

- Each type in the array **MUST** reference a compound type declared in the
  document or be a primitive type. Inline type definitions of compound typed
  are **NOT** allowed, with the exception of `map` and `array` types with
  primitive values.

- **Examples**:

  This example defines a union of a string and a compound type:

  ```json
  {
    "type": ["string", { "$ref": "#/Namespace/TypeName" }]
  }
  ```

  This example defines a union of a string and a primitive type:

  ```json
  {
    "type": ["string", "integer"]
  }
  ```

  This example shows a permitted union of a string and a map of strings:

  ```json
  {
    "type": ["string", { "type": "map", "values": { "type": "string" } }]
  }
  ```

  This negative example shows an inline definition of a compound type in a union,
  which is NOT allowed:

  ```json
  {
    "type": ["string", { "type": "object", "properties": { "name": { "type": "string" } } }]
  }
  ```

#### 3.5.1.1 Prohibition of Top-Level Unions

- The root of a JSON-CS document **MUST NOT** be an array.
- Use the $root keyword to designate a type union as the root type.

#### 3.5.2 Maps

- The `map` type allows dynamic key-value pairs where all keys **MUST**
  conform to identifier rules.

- The `values` attribute **MUST** reference a compound type declared in the
  document or be a primitive type. Inline type definitions, including `map`or
  `array` definitions, are **NOT** allowed.

- **Example**:

  ```json
  {
    "type": "map",
    "values": { "$ref": "#/StringType" }
  }
  ```

#### 3.5.3. Arrays

- The `items` attribute of an array **MUST** reference a compound type declared
  in the document or be a primitive type. Inline type definitions, including
  `map`or `array` definitions, are **NOT** allowed.

- **Examples**:

  ```json
  {
    "type": "array",
    "items": { "$ref": "#/Namespace/TypeName" }
  }
  ```

 ```json
  {
    "type": "array",
    "items": { "type": "string" }
  }
  ```

### 3.6. Identifier Rules

1. **Key and Name Format**:

JSON-CS restricts the format of keys and type names such that they cause minimal
conflicts with programming languages and tools. The `altnames` attribute can be
used to provide alternative names that use unrestricted characters for specific
purposes.

- All keys and type names **MUST** conform to the regular expression pattern
  `[A-Za-z_][A-Za-z0-9_]*`, meaning they must start with a letter or
   underscore and can contain letters, digits, and underscores.
- Keys and type names are case-sensitive.
- Reserved root-level keywords **MUST NOT** be used as keys or names.

1. **map Key Constraints**:

   - Keys in a `map` type **MUST** conform to the identifier rules.

### 3.7. Structural Keywords

JSON-CS utilizes a set of structural keywords to describe schemas in detail.
These keywords define the structure and constraints of data types.

#### 3.7.1. The "type" Keyword

- **Purpose**: Declares the type of a schema element.

- **Value**: A string representing a single type or an array of types
  representing a union.

- **Rules**:

  - **MUST** be present in every schema element.

  - For unions, the `type` value is an array of type references or primitive
    type names.

- **Example**:

  ```json
  { "type": "string" }
  ```

  ```json
  { "type": ["string", { "$ref": "#/Namespace/TypeName" }] }
  ```

#### 3.7.2. The "properties" Keyword

- **Purpose**: Defines the properties (i.e., named members) of an `object` type.

- **Value**: An object where each key is a property name, and each value is a
  schema defining the property's expected type and constraints.

- **Rules**:

  - The `properties` keyword **MUST** only be used within schemas of type
    `object`.

  - Each property name in `properties` **MUST** conform to the [identifier rules](#36-identifier-rules)
    (`[_A-Za-z][A-Za-z0-9_]*`).

  - Each property's schema **MUST** include an explicit `type` declaration.

  - Property schemas **MUST NOT** contain inline type definitions for compound
    types; they **MUST** reference previously declared types using `$ref`.

- **Example**:

  ```json
  {
    "type": "object",
    "properties": {
      "name": { "type": "string" },
      "address": { "type": { "$ref": "#/Namespace/Address" } }
    }
  }
  ```

#### 3.7.3. The "required" Keyword

- **Purpose**: Specifies which properties are mandatory in an `object` type.

- **Value**: An array of strings, each representing a property name that
  **MUST** be present.

- **Rules**:

  - The `required` keyword **MUST** only be used within schemas of type
    `object`.

  - Each property name listed in `required` **MUST** be defined in the
    `properties` keyword of the same schema.

  - The `required` array **MUST NOT** contain duplicate property names.

- **Example**:

  ```json
  {
    "type": "object",
    "properties": {
      "id": { "type": "string" },
      "name": { "type": "string" }
    },
    "required": ["id", "name"]
  }
  ```

#### 3.7.4. The "items" Keyword

- **Purpose**: Defines the schema for elements within an `array` type.

- **Value**: A schema that **MUST** be a reference to a previously declared
  type.

- **Rules**:

  - The `items` keyword **MUST** only be used within schemas of type `array`.

  - The schema specified in `items` **MUST NOT** contain inline type definitions
    for compound types; it **MUST** reference a compound type declared in the document using
    `$ref`.

- **Example**:

  ```json
  {
    "type": "array",
    "items": { "$ref": "#/Namespace/TypeName" }
  }
  ```

#### 3.7.5. The "values" Keyword

- **Purpose**: Defines the schema for values within a `map` type.

- **Value**: A schema that **MUST** be a reference to a previously declared
  type.

- **Rules**:

  - The `values` keyword **MUST** only be used within schemas of type `map`.

  - The schema specified in `values` **MUST NOT** contain inline type
    definitions for compound types; it **MUST** reference a previously declared
    type using `$ref`.

- **Example**:

  ```json
  {
    "type": "map",
    "values": { "$ref": "#/Namespace/ValueType" }
  }
  ```

#### 3.7.6. Reuse of Type Definitions with Restricted Polymorphism

The `abstract` and `$extends` keywords facilitate the reuse of definitions
across multiple types while explicitly disallowing subtype polymorphism. This
mechanism allows you to define a base class equivalent in object-oriented
programming, sharing its properties and constraints across multiple types
without referencing the base class to implicitly allow any extending type in its
place.

`$extends` serves as a simple composition mechanism, borrowing definitions from
an abstract type as if they were locally defined. This restriction aims to avoid
the complexity of subtype polymorphism when projecting such structures onto
programming languages, frameworks, or databases that do not support
polymorphism, while still enabling the reuse of common properties and
constraints across multiple, semantically similar types.

For example, the following schema defines an abstract type `Address` with common
properties and constraints that are shared by two types that extend it. The
types `StreetAddress` and `PostOfficeBoxAddress` extend the `Address` type with
further properties. The `Person` type **MUST NOT** reference the `Address`
type directly, but it **MAY** reference the extending types `StreetAddress` and
`PostOfficeBoxAddress` in a type union as shown for the `postalAddress` property.

```jsonc
{
  "Person": {
    "name": "Person",
    "type": "object",
    "properties": {
      "name": { "type": "string" },
      "residenceAddress": { 
        "$ref": "#/StreetAddress" //*** reference to an extending type
      },
      "postalAddress": [ //*** type union of extending types
        { "$ref": "#/StreetAddress" },  
        { "$ref": "#/PostOfficeBoxAddress" }
      ]
    },
    "required": ["name", "residenceAddress"],
    "additionalProperties": true,
  },
  "Address": {
    "name": "Address",
    "type": "object",
    "abstract": true,  //*** Declares the type as abstract
    "properties": {
      "city": { "type": "string" },
      "region": { "type": "string" },
      "countryCode": { "type": "string" },
      "postalCode": { "type": "string" }        
    },
    "required": ["city", "region", "countryCode", "postalCode"]
  },
  "StreetAddress": {
    "name": "StreetAddress",
    "$extends": "#/Address", //*** Extends the abstract type Address
    "type": "object",
    "properties": {
      "street": { "type": "string" },
      "unit": { "type": "string" },
      "floor": { "type": "string" },
      "building": { "type": "string" },
    },
    "required": ["street"], //*** effective required constraint is 
                           // ["city", "region", "countryCode", "postalCode", "street"]
    "additionalProperties": false
  },
  "PostOfficeBoxAddress": {
    "name": "PostOfficeBoxAddress",
    "$extends": "#/Address", //*** Extends the abstract type Address
    "type": "object",
    "properties": {
      "poBox": { "type": "string" }
    },
    "required": ["poBox"], //*** effective required constraint is 
                           // ["city", "region", "countryCode", "postalCode", "poBox"]
    "additionalProperties": false
  }
}
```

> **Note**: A programming language projection MAY choose to represent `Address`
> and its extending types as a class hierarchy and it MAY choose to allow
> subtype polymorphism using the shared extended type  when implementing the
> `postalAddress` property in the `Person` class. The point of the JSON-CS
> restrictions is to avoid imposing the complexity of subtype polymorphism on
> all projections.

##### 3.7.6.1. The "abstract" Keyword

- **Purpose**: Declares a type as abstract, meaning it cannot be used directly
  but can be extended by other types.

- **Value**: A boolean value (`true` or `false`).

- **Rules**:

  - **MUST** only be used within `object` type definitions.

  - Abstract types **MUST NOT** be used as the type of a schema element and **MUST NOT**
    be referenced via `$ref`.

  - the [`additionalProperties`](#3777-the-additionalproperties-keyword) keyword
    **MUST NOT** be used on abstract types. Its implied value is `true`.

  - abstract types **MAY** extend other abstract types using the `$extends`
    keyword.

##### 3.7.6.2. The "$extends" Keyword

- **Purpose**: Extends a type by copying and merging properties and constraints
  from an abstract type.

- **Value**: A string representing a JSON Pointer to the abstract type to extend.

- **Rules**:

  - **MUST** only be used within `object` type definitions.
    The value of `$extends` **MUST** be a single, valid JSON Pointer that points
    to an abstract type defined in the same document.

  - abstract types **MAY** extend other abstract types using the `$extends`
    keyword, meaning that a processor **MUST** traverse the extension chain to
    determine all properties and constraints for an extending type.

  - The `$extends` keyword copies all properties and constraints from the
    abstract type into the extending type. All properties and constraints
    defined in the extending type are merged with those of the abstract type.
    The order of properties in the extending type is preserved.

  - The extending type **MUST NOT** repeat or redefine properties that are
    already defined in the abstract type. 
    
  - the [`required`](#373-the-required-keyword) constraint of the extended type
    is merged with the `required` constraint of the extending type. In the above
    example, the `required` constraint of `StreetAddress` is merged with the
    constraint of `Address` and the effective `required` constraint of
    `StreetAddress` is `["city", "region", "countryCode", "postalCode",
    "street"]`.


#### 3.7.7. Additional Structural Keywords

##### 3.7.7.1. The "const" Keyword

- **Purpose**: Constrains a schema to accept only a specific value.

- **Value**: A primitive value (string, number, integer, boolean, or null).

- **Rules**:

  - **MUST** only be used in schemas that have a primitive `type`.

  - The instance **MUST** be equal to the value specified in `const`.

- **Example**:

  ```json
  { "type": "string", "const": "fixedValue" }
  ```

##### 3.7.7.2. The "unit" Keyword

- **Purpose**: Specifies the SI unit symbol associated with a numeric property
  or type.

- **Value**: A string representing a unit symbol.

- **Rules**:

  - **MAY** be used with schemas of type `number` or `integer`.

  - Provides metadata about the unit of measurement for the value.

  - The `unit` field **SHOULD** contain an SI unit symbol or a derived unit
    symbol in conformance with the definitions of the Bureau International des
    Poids et Mesures (BIPM) International System of Units (SI) \[[BIPM
    SI](#BIPM)\].

  - Deviating from this, the field **MAY** contain a non-SI unit symbol as
    defined in NIST Handbook 44 Appendix C \[[NIST HB44](#NIST44)\].

  - For derived units that reflect a multiplication, the unit symbols are
    separated by `*`. For derived units that reflect a division, the unit
    symbols are separated by `/`. The notation for exponentiation is `^`. For
    example, acceleration is denoted as `"m/s^2"`.

  - Units that use Greek-language symbols (including supplementary or derived
    units) like Ohm (`"Ω"`) are denoted with those Greek symbols (Unicode code
    points).

- **Examples**:

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
  | Electrical Resistance | `Ω`     | Ohms, SI unit of electrical resistance  | BIPM SI   |
  | Electrical Current    | `A`     | Amperes, SI unit of electric current    | BIPM SI   |
  | Light Intensity       | `cd`    | Candelas, SI unit of luminous intensity | BIPM SI   |
  | Length                | `ft`    | Feet, non-SI unit                       | NIST HB44 |
  | Volume                | `gal`   | Gallon, non-SI unit                     | NIST HB44 |

- **Example Usage**:

  ```json
  {
    "type": "number",
    "unit": "m/s^2",
    "description": "Acceleration in meters per second squared"
  }
  ```

##### 3.7.7.3. The "format" Keyword

- **Purpose**: Provides semantic validation for primitive types beyond basic
  type checking.

- **Value**: A string specifying the format to be applied. The value **SHOULD**
  be taken from the list of supported formats defined below.

- **Rules**:

  - **MAY** be used with schemas of type `string`, `number`, or `integer`.

  - Validators **SHOULD** implement format validation for the defined formats.

- **Supported Format Values**:

  - **String Formats**:

    - `date-time`: A string representing a date and time in RFC 3339 format.
    - `date`: A string representing a full-date as per RFC 3339.
    - `time`: A string representing a full-time as per RFC 3339.
    - `duration`: A string representing a duration as per ISO 8601.
    - `email`: A string representing an email address.
    - `hostname`: A string representing a valid hostname.
    - `ipv4`: A string representing an IPv4 address.
    - `ipv6`: A string representing an IPv6 address.
    - `uri`: A string representing a URI.
    - `uuid`: A string representing a UUID.
    - `regex`: A string representing a regular expression.

  - **Numeric Formats**:

    - `int32`: A 32-bit signed integer.
    - `int64`: A 64-bit signed integer.
    - `int128`: A 128-bit signed integer.
    - `uint32`: A 32-bit unsigned integer.
    - `uint64`: A 64-bit unsigned integer.
    - `uint128`: A 128-bit unsigned integer.
    - `float`: A single-precision (32-bit) floating-point number.
    - `double`: A double-precision (64-bit) floating-point number.
    - `decimal`: An arbitrary-precision decimal number.

- **Handling of Large Numbers**:

  - JSON's number type is based on IEEE 754 double-precision floating-point
    format, which cannot accurately represent all 64-bit or 128-bit integers.

  - When using formats like `int64`, `uint64`, `int128`, `uint128`, numbers
    **MUST** be represented as strings in JSON to preserve precision and avoid
    loss of information.

  - Validators and processors **MUST** interpret these string-encoded numbers
    according to their specified formats.

- **Example Usage**:

  - **64-bit Integer**:

    ```json
    {
      "type": "string",
      "format": "int64",
      "description": "A 64-bit signed integer represented as a string"
    }
    ```

  - **128-bit Unsigned Integer**:

    ```json
    {
      "type": "string",
      "format": "uint128",
      "description": "A 128-bit unsigned integer represented as a string"
    }
    ```

  - **Date-Time String**:

    ```json
    {
      "type": "string",
      "format": "date-time",
      "description": "An RFC 3339 formatted date-time string"
    }
    ```

##### 3.7.7.4. The "enum" Keyword

- **Purpose**: Restricts a string or numeric type to a fixed set of values.

- **Value**: An array of unique values that are acceptable for the instance.

- **Rules**:

  - **MUST** be used with schemas of type `string`, `number`, or `integer`.

  - The instance value **MUST** be equal to one of the values in the `enum`
    array.

- **Example**:

  ```json
  {
    "type": "string",
    "enum": ["RED", "GREEN", "BLUE"]
  }
  ```

##### 3.7.7.5. The "description" Keyword

- **Purpose**: Provides a human-readable description of the schema.

- **Value**: A string containing the description.

- **Rules**:

  - **MAY** be used in any schema element.

  - Helps in documentation and understanding of the schema.

- **Example**:

  ```json
  { "type": "string", "description": "User's full name" }
  ```

##### 3.7.7.6. The "default" Keyword

- **Purpose**: Specifies a default value for the schema or property.

- **Value**: A value that is valid for the schema.

- **Rules**:

  - **MAY** be used in any schema element.

  - The default value is used when an explicit value is not provided.

- **Example**:

  ```json
  { "type": "integer", "default": 42 }
  ```

##### 3.7.7.7. The "additionalProperties" Keyword

- **Purpose**: Controls whether properties other than those defined in
  `properties` are allowed in an `object` type, and if so, how they are
  validated.

- **Value**: A boolean or a schema.

  - **Boolean**:

    - `false` indicates that no additional properties are allowed.

    - `true` indicates that additional properties are allowed, and their values
      are not validated.

  - **Schema**:

    - Specifies that additional properties are allowed, and each additional
      property's value **MUST** conform to the specified schema.

- **Rules**:

  - **MUST** only be used within schemas of type `object`.

  - If omitted, the default behavior allows additional properties, and their
    values are not validated.

  - When a schema is provided, it **MUST** be a reference to a previously
    declared type.

  - Invalid on [abstract types](#376-reuse-of-type-definitions-with-restricted-polymorphism).

- **Examples**:

  - **Using Boolean Value**:

    ```json
    {
      "type": "object",
      "properties": {
        "id": { "type": "string" }
      },
      "additionalProperties": false
    }
    ```

  - **Using Schema Value**:

    ```json
    {
      "type": "object",
      "properties": {
        "knownProperty": { "type": "string" }
      },
      "additionalProperties": { "$ref": "#/Namespace/AdditionalPropType" }
    }
    ```

##### 3.7.7.8. The "examples" Keyword

- **Purpose**: Provides example instances that are valid against the schema.

- **Value**: An array of example objects, each containing:

  - `"description"`: A string describing the example.

  - `"value"`: A value that is valid for the schema.

- **Rules**:

  - **MAY** be used in any schema element.

  - Helps in documentation and understanding of the schema usage.

- **Example**:

  ```json
  {
    "type": "string",
    "examples": [
      {
        "description": "An example username",
        "value": "john_doe"
      },
      {
        "description": "Another example username",
        "value": "jane_smith"
      }
    ]
  }
  ```

##### 3.7.7.9. The "altnames" Keyword

- **Purpose**: Provides alternative names for types and properties for various
  purposes, such as JSON encoding or display localization.

- **Value**: An object (map) where each key is the purpose of the alternate
  name, and the value is the alternative name as a string.

- **Rules**:

  - **MAY** be used in any named type or property definition.

  - The keys `"json"` and the prefix `"display:"` are reserved.

- **Reserved Keys**:

  - `"json"`: Used to specify alternate names for JSON encoding.

  - `"display:<language-code>"`: Used to specify localized display names, where
    `<language-code>` is a language code as per [RFC 5646](#RFC5646).

- **Example**:

  See sections [3.3.4.1](#3341-alternate-names-for-json-encoding) and
  [3.3.4.2](#3342-alternate-names-for-display-internationalization) for
  examples.

##### 3.7.7.10. The "altsymbols" Keyword

- **Purpose**: Provides alternative names for enumeration values (enum) for
  various purposes.

- **Value**: An object (map) where each key is the purpose of the alternate
  symbol, and the value is a map of enumeration values to their alternate names.

- **Rules**:

  - **MAY** be used in schemas that use the `enum` keyword.

  - The keys `"json"` and the prefix `"display:"` are reserved.

- **Reserved Keys**:

  - `"json"`: Used to specify alternate values for JSON encoding.

  - `"display:<language-code>"`: Used to specify localized display names for
    enum values.

- **Example**:

  See section [3.3.4.3](#3343-alternate-symbols-for-enums) for an example.

##### 3.7.7.10 The "maxLength" Keyword

- **Purpose**: Specifies the maximum length of a string.
- **Value**: A non-negative integer.
- **Rules**:
  - **MAY** be used in schemas of type `string`.
  - The length of the string **MUST NOT** exceed the value specified in
    `maxLength`.

- **Example**:

- ```json
  {
    "type": "string",
    "maxLength": 10
  }
  ```

##### 3.7.7.11 The "pattern" Keyword

- **Purpose**: Specifies a regular expression pattern that a string value must
  match.
- **Value**: A string containing a regular expression pattern.
- **Rules**:
  - **MAY** be used in schemas of type `string`.
  - The string value **MUST** match the regular expression pattern specified in
    `pattern`.

- **Example**:

- ```json
  {
    "type": "string",
    "pattern": "^[A-Za-z0-9_]+$"
  }
  ```

### 3.8. Validation Rules

1. **Type Resolution**:

   - A type reference (`$ref`) **MUST** resolve to a valid, previously declared
     type in the document.

   - Unresolved references **MUST** result in a validation error.

2. **Prohibited Patterns**:

   - External references, such as URIs with authorities (e.g.,
     `http://example.com/schema`), are **INVALID**.

   - Fragment-only pointers (e.g., `"$ref": "#"`) are **INVALID**.

3. **Inline Definitions**:

   - Inline type definitions are **NOT** allowed in arrays, maps, or unions.

   - All compound types **MUST** be declared separately and referenced.

4. **Unique Names**:

   - Type names **MUST** be unique within a namespace, and fully qualified names
     **MUST** be globally unique.

   - Duplicate type names within the same namespace **MUST** result in a
     validation error.

5. **Property Definitions**:

   - For `object` types, the `properties` keyword defines the named properties
     of the object.

   - Each property name **MUST** conform to identifier rules.

   - Each property's schema **MUST** have an explicit `type` declaration.

   - Property schemas **MUST NOT** contain inline definitions of compound types.

6. **Required Properties**:

   - The `required` keyword lists property names that **MUST** be present in the
     object.

   - Property names in `required` **MUST** be defined in `properties`.

   - Missing required properties in an instance **MUST** result in a validation
     error.

7. **map Key Constraints**:

   - Keys in a `map` instance **MUST** conform to the identifier rules.

   - Non-conforming keys **MUST** result in a validation error.

8. **Data Type Constraints**:

   - Instances **MUST** conform to the type definitions specified in the schema.

   - Violations of type constraints (e.g., a string where an integer is
     expected) **MUST** result in a validation error.

9. **Enum Constraints**:

   - The `enum` keyword **MUST** only be used in schemas that have a primitive
     `type`.

   - If `enum` is used, the instance **MUST** be equal to one of the values
     specified.

10. **Const Constraints**:

    - The `const` keyword **MUST** only be used in schemas that have a primitive
      `type`.

    - If `const` is used, the instance **MUST** be equal to the value specified.

11. **Additional Properties**:

    - If `additionalProperties` is set to `false`, any properties not defined in
      `properties` **MUST** result in a validation error.

    - If `additionalProperties` is set to `true`, additional properties are
      allowed, and their values are not validated against any schema.

    - If `additionalProperties` is a schema, additional properties are allowed,
      and each additional property's value **MUST** conform to the specified
      schema.

12. **Format Validation**:

    - When the `format` keyword is present, validators **SHOULD** validate the
      value against the specified format.

    - For numeric formats that exceed JSON's native number representation (e.g.,
      `int64`, `int128`), values **MUST** be represented as strings, and
      validators **MUST** interpret them accordingly.

13. **Maximum Length and Pattern constraints**:

    - If `maxLength` is used, the length of the string **MUST** be less or equal
      to the value specified.

    - If `pattern` is used, the string value **MUST** match the regular
      expression pattern specified.

### 3.9. Reserved Keywords

- `$schema`: Indicates the schema version.

- `$root`: References the root schema inside the document.

- `$id`: Provides a unique identifier for the schema document.

- `$ref`: Used exclusively for type references within the document.

- `type`: Declares the type of an object, array, or map.

- Other keywords introduced in this specification (e.g., `const`, `unit`,
  `format`, `enum`, `description`, `default`, `additionalProperties`,
  `examples`, `altnames`, `altsymbols`) are reserved and **MUST NOT** be used as
  type or property names.

## 4. Examples

### 4.1. Using "const", "unit", and "format"

```json
{
  "Measurement": {
    "type": "object",
    "properties": {
      "value": {
        "type": "string",
        "format": "int64",
        "unit": "m/s^2",
        "description": "Acceleration in meters per second squared, as a 64-bit integer"
      },
      "type": { "type": "string", "const": "acceleration" }
    },
    "required": ["value", "type"],
    "additionalProperties": false
  }
}
```

- **Explanation**:

  - Defines a `Measurement` type with properties `value` and `type`.

  - The `value` property is a string representing a 64-bit integer (`"format":
    "int64"`) with a unit of meters per second squared (`"m/s^2"`).

  - The `type` property is a string constrained to the constant value
    `"acceleration"` using `const`.

  - `additionalProperties` is set to `false`, disallowing any properties other
    than `value` and `type`.

### 4.2. Using "description", "default", and "examples"

```json
{
  "User": {
    "type": "object",
    "properties": {
      "username": {
        "type": "string",
        "description": "The user's login name",
        "examples": [
          { "description": "A typical username", "value": "alice123" }
        ]
      },
      "email": {
        "type": "string",
        "format": "email",
        "description": "The user's email address",
        "default": "user@example.com",
        "examples": [
          { "description": "An example email", "value": "alice@example.com" }
        ]
      }
    },
    "required": ["username", "email"],
    "additionalProperties": false
  }
}
```

- **Explanation**:

  - Defines a `User` type with `username` and `email` properties.

  - Uses `description` to provide human-readable explanations.

  - Provides `default` values for properties.

  - Includes `examples` to illustrate valid instances.

### 4.3. Using "additionalProperties"

- **Example with Boolean Value**:

  ```json
  {
    "Config": {
      "type": "object",
      "properties": {
        "setting1": { "type": "string" },
        "setting2": { "type": "integer", "default": 10 }
      },
      "additionalProperties": true
    }
  }
  ```

  - **Explanation**:

    - Defines a `Config` type with `setting1` and `setting2` properties.

    - `additionalProperties` is set to `true`, allowing extra properties beyond
      those defined.

    - Extra properties are not validated by the schema unless additional
      definitions are provided.

- **Example with Schema Value**:

  ```json
  {
    "Config": {
      "type": "object",
      "properties": {
        "setting1": { "type": "string" }
      },
      "additionalProperties": { "$ref": "#/SettingValue" }
    },
    "SettingValue": {
      "type": ["string", "number", "boolean"]
    }
  }
  ```

  - **Explanation**:

    - Defines a `Config` type with a known property `setting1`.

    - `additionalProperties` is set to a schema reference `#/SettingValue`.

    - Any additional properties beyond `setting1` are allowed, but their values
      must conform to the `SettingValue` type.

    - `SettingValue` is a union type that can be a string, number, or boolean.

### 4.4. Using "altnames" and "altsymbols"

**Example with Alternate Names for JSON Encoding**:

```json
{
  "": {
    "Person": {
      "type": "object",
      "properties": {
        "firstName": {
          "type": "string",
          "altnames": { "json": "first-name" }
        },
        "lastName": {
          "type": "string",
          "altnames": { "json": "last-name" }
        }
      },
      "required": ["firstName", "lastName"],
      "additionalProperties": false
    }
  }
}
```

- **Explanation**:

  - Maps property names `firstName` and `lastName` to JSON keys `first-name` and
    `last-name` respectively.

**Example with Alternate Names for Display (Internationalization)**:

```json
{
  "": {
    "Product": {
      "type": "object",
      "altnames": {
        "display:es": "Producto",
        "display:zh": "产品"
      },
      "properties": {
        "name": {
          "type": "string",
          "altnames": {
            "display:es": "Nombre",
            "display:zh": "名称"
          }
        },
        "price": {
          "type": "number",
          "altnames": {
            "display:es": "Precio",
            "display:zh": "价格"
          }
        }
      },
      "required": ["name", "price"],
      "additionalProperties": false
    }
  }
}
```

- **Explanation**:

  - Provides localized display names for the `Product` type and its properties
    in Spanish (`"display:es"`) and Chinese (`"display:zh"`).

**Example with Alternate Symbols for Enums**:

```json
{
  "": {
    "Status": {
      "type": "string",
      "enum": ["ACTIVE", "INACTIVE", "PENDING"],
      "altsymbols": {
        "json": {
          "ACTIVE": "A",
          "INACTIVE": "I",
          "PENDING": "P"
        },
        "display:fr": {
          "ACTIVE": "Actif",
          "INACTIVE": "Inactif",
          "PENDING": "En attente"
        }
      }
    }
  }
}
```

- **Explanation**:

  - Defines a `Status` type with enum values `"ACTIVE"`, `"INACTIVE"`, and
    `"PENDING"`.

  - The `altsymbols` attribute maps these enum values to alternate
    representations.

    - For JSON encoding (`"json"`), the values are mapped to `"A"`, `"I"`, and
      `"P"`.

    - For French display (`"display:fr"`), the values are mapped to `"Actif"`,
      `"Inactif"`, and `"En attente"`.

## 5. Compatibility with JSON Schema Drafts

JSON-CS shares similarities with JSON Schema and aims for compatibility where
possible. This section describes how JSON-CS schemas can interoperate with JSON
Schema drafts, specifically draft-07 and later versions, and how simple schemas
are fully compatible when they stay within the constraints of JSON-CS.

### 5.1. JSON Schema Draft-07 Compatibility

In JSON Schema draft-07, the root of the schema document typically contains a
`$schema` attribute that specifies the version of the JSON Schema standard being
used. For draft-07, this value is:

```json
"$schema": "http://json-schema.org/draft-07/schema#"
```

In JSON-CS, when the `$schema` attribute is set to
`"http://json-schema.org/draft-07/schema#"`, the `definitions` attribute in the
root object corresponds to the default (empty) namespace of JSON-CS. This means
that types defined within the `definitions` object are part of the empty
namespace and can be referenced accordingly.

#### Example

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "Person": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "age": { "type": "integer" }
      },
      "required": ["name"]
    }
  }
}
```

In this example, the `Person` type is defined within the `definitions` object,
which aligns with the empty namespace in JSON-CS.

### 5.2. JSON Schema Draft-2019-09 and Later Compatibility

In JSON Schema drafts from 2019-09 onward, the `definitions` attribute has been
replaced by the `$defs` attribute. In JSON-CS, when using these later drafts,
the `$defs` attribute similarly contains types within the default (empty)
namespace.

#### Example

```json
{
  "$schema": "https://json-schema.org/draft/2019-09/schema",
  "$defs": {
    "Person": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "age": { "type": "integer" }
      },
      "required": ["name"]
    }
  }
}
```

Here, the `Person` type is defined within the `$defs` object, corresponding to
the empty namespace in JSON-CS.

### 5.3. Type References

In both JSON Schema draft-07 and later versions, types defined in `definitions`
or `$defs` can be referenced using `$ref` with a JSON Pointer.

- For draft-07:

  ```json
  { "$ref": "#/definitions/Person" }
  ```

- For draft-2019-09 and later:

  ```json
  { "$ref": "#/$defs/Person" }
  ```

In JSON-CS, type references within the same document use `$ref` with JSON
Pointers as well, aligning with this approach.

### 5.4. Schema Compatibility

Simple schemas that stay within the constraints of JSON-CS are fully compatible
with JSON Schema drafts. If a schema uses only the features and constructs
allowed in JSON-CS, it can be interpreted by JSON Schema validators that support
the corresponding draft.

#### Constraints for Compatibility

- **Type Declarations**: Must use explicit `type` declarations.

- **Type References**: Must use `$ref` to reference types within the same
  document.

- **No External References**: Must not use external URIs in `$ref`.

- **No Inline Definitions**: Must not define types inline within arrays, maps,
  or unions.

- **Keywords**: Must use keywords consistent with JSON Schema drafts.

### 5.5. Mapping Namespaces

JSON-CS namespaces can be mapped to JSON Schema's `definitions` or `$defs`
objects. Each namespace in JSON-CS can correspond to a nested object within
`definitions` or `$defs`.

#### Example with Namespaces

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "MyNamespace": {
      "Type1": {
        "type": "object",
        "properties": {
          "prop1": { "type": "integer" }
        }
      },
      "Type2": {
        "type": "array",
        "items": { "$ref": "#/definitions/MyNamespace/Type1" }
      }
    }
  }
}
```

In this example, `MyNamespace` is represented as an object within `definitions`,
and types within that namespace are defined accordingly.

### 5.6. Limitations

While JSON-CS aims for compatibility, certain features specific to JSON-CS may
not be directly supported in JSON Schema drafts, such as:

- The `map` type: JSON Schema uses `patternProperties` and
  `additionalProperties` to achieve similar functionality.

- The strict prohibition of inline definitions in arrays, maps, or unions.

- The use of `unit` and other metadata keywords specific to JSON-CS.

Therefore, when designing schemas intended for compatibility with JSON Schema
validators, it's important to consider these limitations and adjust the schema
accordingly.

## 6. Security Considerations

JSON-CS schemas are self-contained and do not allow external references,
reducing the risk of including untrusted or malicious schemas. Implementations
**MUST** ensure that all `$ref` pointers resolve within the same document to
prevent security vulnerabilities related to external schema inclusion.

## 7. IANA Considerations

This document has no IANA actions.

## 8. References

### 8.1. Normative References

- <a name="RFC2119"></a>[RFC2119] Bradner, S., "Key words for use in RFCs to
  Indicate Requirement Levels", BCP 14, RFC 2119, DOI:
  [10.17487/RFC2119](https://doi.org/10.17487/RFC2119), March 1997,
  <https://www.rfc-editor.org/info/rfc2119>.

- <a name="RFC5646"></a>[RFC5646] Phillips, A., and M. Davis, "Tags for
  Identifying Languages", BCP 47, RFC 5646, DOI:
  [10.17487/RFC5646](https://doi.org/10.17487/RFC5646), September 2009,
  <https://www.rfc-editor.org/info/rfc5646>.

- <a name="RFC6901"></a>[RFC6901] Bryan, P., and K. Zyp, "JavaScript Object
  Notation (JSON) Pointer", RFC 6901, DOI:
  [10.17487/RFC6901](https://doi.org/10.17487/RFC6901), April 2013,
  <https://www.rfc-editor.org/info/rfc6901>.

- <a name="RFC8174"></a>[RFC8174] Leiba, B., "Ambiguity of Uppercase vs
  Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, DOI:
  [10.17487/RFC8174](https://doi.org/10.17487/RFC8174), May 2017,
  <https://www.rfc-editor.org/info/rfc8174>.

### 8.2. Informative References

- <a name="BIPM"></a>[BIPM SI] Bureau International des Poids et Mesures, "The
  International System of Units (SI)", 9th edition, 2019,
  <https://www.bipm.org/en/publications/si-brochure>.

- <a name="NIST44"></a>[NIST HB44] National Institute of Standards and
  Technology, "NIST Handbook 44: Specifications, Tolerances, and Other Technical
  Requirements for Weighing and Measuring Devices", 2023, Appendix C,
  <https://www.nist.gov/pml/weights-and-measures/publications/handbooks/handbook-44>.

- <a name="JSONSchema07"></a>[JSON Schema Draft-07] Wright, G., and H. Andrews,
  "JSON Schema: A Media Type for Describing JSON Documents", Internet-Draft,
  July 2018,
  <https://datatracker.ietf.org/doc/html/draft-handrews-json-schema-01>.

- <a name="JSONSchemaLatest"></a>[JSON Schema Latest] JSON Schema Organization,
  "JSON Schema Specification", <https://json-schema.org/>.

## 9. Author's Address

**Clemens Vasters**  
Microsoft  
Email: [clemensv@microsoft.com](mailto:clemensv@microsoft.com)

## 10. Appendix: Metaschema

### 10.1 JSON-CS Metaschema

The JSON-CS metaschema is a JSON-CS schema that formally defines the structure
and constraints for JSON-CS schemas.

```json
{
  "$schema": "https://schemas.microsoft.com/experimental/json-cs/v0",
  "$root": "#/schemaDocument",
  "schemaDocument": {
    "name": "schemaDocument",
    "description": "The root type representing a JSON-CS document.",
    "type": "object",
    "properties": {
      "schema": {
        "type": "string",
        "format": "uri",
        "description": "Specifies the version of the JSON-CS specification.",
        "altnames": { "json": "$schema" }
      },
      "root": {
        "type": ["string", { "type": "array", "items": { "type": "string" } }],
        "description": "References the root schema inside the document.",
        "altnames": { "json": "$root" }
      },
      "id": {
        "type": "string",
        "format": "uri",
        "description": "Provides a unique identifier for the schema document.",
        "altnames": { "json": "$id" }
      }
    },
    "additionalProperties": { "$ref": "#/typeDefinitionOrNamespace" },
    "required": ["type"]
  },
  "typeDefinitionOrNamespace": {
    "name": "typeDefinitionOrNamespace",
    "description": "A union type that can be either a typeDefinition or a namespace.",
    "type": [{"$ref": "#/typeDefinition"}, {"$ref": "#/namespace"} ]
  },
  "typeDefinition": {
    "name": "typeDefinition",
    "description": "Defines a type in JSON-CS.",
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "description": "The name of the type."
      },
      "abstract": {
        "type": "boolean",
        "description": "Indicates whether the type is abstract."
      },
      "extends": {
        "$ref": "#/refDefinition",
        "description": "References a base type that this type extends.",
        "altnames": { "json": "$extends" }
      },
      "type": {
        "$ref": "#/typeExpression",
        "description": "The type expression of the type."
      },
      "properties": {
        "$ref": "#/propertiesDefinition",
        "description": "Defines the properties of an object type."
      },
      "required": {
        "$ref": "#/stringArray",
        "description": "Specifies required properties."
      },
      "items": {
        "$ref": "#/typeExpression",
        "description": "Defines the schema for elements within an array type."
      },
      "values": {
        "$ref": "#/typeExpression",
        "description": "Defines the schema for values within a map type."
      },
      "additionalProperties": {
        "$ref": "#/additionalPropertiesDefinition",
        "description": "Controls validation of additional properties in an object."
      },
      "enum": {
        "$ref": "#/primitiveArray",
        "description": "Restricts a string or numeric type to a fixed set of values."
      },
      "const": {
        "$ref": "#/primitiveValue",
        "description": "Constrains a schema to accept only a specific value."
      },
      "format": {
        "type": "string",
        "description": "Provides semantic validation for primitive types."
      },
      "unit": {
        "type": "string",
        "description": "Specifies the SI unit symbol associated with a numeric property."
      },
      "description": {
        "type": "string",
        "description": "Provides a human-readable description of the schema."
      },
      "default": {
        "$ref": "#/primitiveValue",
        "description": "Specifies a default value for the schema or property."
      },
      "examples": {
        "$ref": "#/examplesDefinition",
        "description": "Provides example instances that are valid against the schema."
      },
      "altnames": {
        "$ref": "#/altNames",
        "description": "Provides alternative names for types and properties."
      },
      "altsymbols": {
        "$ref": "#/altSymbols",
        "description": "Provides alternative symbols for enumeration values."
      },
      "maxLength": {
        "type": "integer",
        "description": "Specifies the maximum length of a string."
      },
      "pattern": {
        "type": "string",
        "description": "Specifies a regular expression pattern that a string value must match."
      }
    },
    "additionalProperties": false
  },
  "typeExpression": {
    "name": "typeExpression",
    "description": "Represents the 'type' attribute in a typeDefinition, which can be a single typeReference or an array of typeReferences for unions.",
    "type": [
      { "$ref": "#/typeReference" },
      {
        "type": "array",
        "items": { "$ref": "#/typeReference" }
      }
    ]
  },
  "typeReference": {
    "name": "typeReference",
    "description": "References a type, either a primitive type name or a $ref to another type.",
    "type": [
      { "$ref": "#/primitiveTypeName" },
      { "$ref": "#/refDefinition" }
    ]
  },
  "primitiveTypeName": {
    "name": "primitiveTypeName",
    "description": "Enumerates the allowed primitive type names in JSON-CS.",
    "type": "string",
    "enum": [
      "string",
      "integer",
      "number",
      "boolean",
      "null",
      "object",
      "array",
      "map"
    ]
  },
  "mapDefinition": {
    "name": "mapDefinition",
    "description": "Defines a map type in JSON-CS.",
    "type": "object",
    "properties": {
      "type": {
        "type": "string",
        "enum": ["map"],
        "description": "The type of the map."
      },
      "values": {
        "$ref": "#/itemDefinitionOrRef",
        "description": "Defines the schema for values within the map."
      },
      "description": {
        "type": "string",
        "description": "Provides a human-readable description of the map."
      }
    },
    "additionalProperties": false
  },
  "arrayDefinition": {
    "name": "arrayDefinition",
    "description": "Defines an array type in JSON-CS.",
    "type": "object",
    "properties": {
      "type": {
        "type": "string",
        "enum": ["array"],
        "description": "The type of the array."
      },
      "items": {
        "$ref": "#/itemDefinitionOrRef",
        "description": "Defines the schema for elements within the array."
      },
      "description": {
        "type": "string",
        "description": "Provides a human-readable description of the array."
      }
    },
    "additionalProperties": false
  },
  "itemDefinitionOrRef": {
    "name": "itemDefinitionOrRef",
    "description": "A union type that can be either a typeDefinition or a refDefinition.",
    "type": [{ "$ref": "#/typeDefinition" }, { "$ref": "#/refDefinition" }]
  },
  "itemDefinition" : {
    "name": "itemDefinition",
    "description": "Defines an item within an array, including its type and optional keywords.",
    "type": "object",
    "properties": {
      "type" : {
        "$ref": "#/typeExpression",
        "description": "The type of the item."
      },
    }
  },
  "refDefinition": {
    "name": "refDefinition",
    "description": "Defines the structure of a $ref reference.",
    "type": "object",
    "properties": {
      "ref": {
        "type": "string",
        "format": "uri-reference",
        "description": "A JSON Pointer to a type definition within the same document.",
        "altnames": { "json": "$ref" }
      },
      "description": {
        "type": "string",
        "description": "Provides a human-readable description of the reference."
      }
    },
    "additionalProperties": false
  },
  "propertiesDefinition": {
    "name": "propertiesDefinition",
    "description": "A map of property names to propertyDefinitions within an object type.",
    "type": "map",
    "values": { "$ref": "#/propertyDefinitionOrRef" }
  },
  "propertyDefinitionOrRef": {
    "name": "propertyDefinitionOrRef",
    "description": "A union type that can be either a propertyDefinition or a refDefinition.",
    "type": [{ "$ref": "#/propertyDefinition" }, { "$ref": "#/refDefinition" }]
  },
  "propertyDefinition": {
    "name": "propertyDefinition",
    "description": "Defines a property within an object, including its type and optional keywords.",
    "type": "object",
    "properties": {
      "type": {
        "$ref": "#/typeExpression",
        "description": "The type of the property."
      },
      "format": {
        "type": "string",
        "description": "Provides semantic validation for primitive types."
      },
      "pattern": {
        "type": "string",
        "description": "Specifies a regular expression pattern that a string value must match."
      },
      "maxLength": {
        "type": "integer",
        "description": "Specifies the maximum length of a string."
      },
      "altnames": {
        "$ref": "#/altNames",
        "description": "Provides alternative names for the property."
      },
      "description": {
        "type": "string",
        "description": "Provides a human-readable description of the property."
      },
      "const": {
        "$ref": "#/primitiveValue",
        "description": "Constrains the property to accept only a specific value."
      },
      "enum": {
        "$ref": "#/primitiveArray",
        "description": "Restricts the property to a fixed set of values."
      },
      "default": {
        "$ref": "#/primitiveValue",
        "description": "Specifies a default value for the property."
      },
      "examples": {
        "$ref": "#/examplesDefinition",
        "description": "Provides example values for the property."
      },
      "unit": {
        "type": "string",
        "description": "Specifies the SI unit symbol associated with a numeric property."
      }
    },
    "additionalProperties": false
  },
  "stringArray": {
    "name": "stringArray",
    "description": "An array of strings.",
    "type": {"type": "array",
    	"items": { "type": "string" }
            }
  },
  "primitiveArray": {
    "name": "primitiveArray",
    "description": "An array of primitive values.",
    "type": "array",
    "items": { "$ref": "#/primitiveValue" }
  },
  "primitiveValue": {
    "name": "primitiveValue",
    "description": "A primitive value: string, number, integer, boolean, or null.",
    "type": ["string", "number", "integer", "boolean", "null"]
  },
  "additionalPropertiesDefinition": {
    "name": "additionalPropertiesDefinition",
    "description": "Represents the 'additionalProperties' keyword, which can be a boolean or a typeReference.",
    "type": ["boolean", { "$ref": "#/typeReference" }]
  },
  "examplesDefinition": {
    "name": "examplesDefinition",
    "description": "Defines how examples are structured in JSON-CS.",
    "type": "array",
    "items": { "$ref": "#/exampleDefinition" }
  },
  "exampleDefinition": {
    "name": "exampleDefinition",
    "description": "Provides an example instance that is valid against the schema.",
    "type": "object",
    "properties": {
      "description": {
        "type": "string",
        "description": "A description of the example."
      },
      "value": {
        "$ref": "#/primitiveValue",
        "description": "The example value."
      }
    },
    "additionalProperties": false
  },
  "altNames": {
    "name": "altNames",
    "description": "Provides alternative names for types and properties for various purposes.",
    "type": { "type": "map",
    "values": { "type": "string" }}
  },
  "altSymbols": {
    "name": "altSymbols",
    "description": "Provides alternative symbols for enumeration values.",
    "type": "map",
    "values": { "$ref": "#/altSymbolMapping" }
  },
  "altSymbolMapping": {
    "name": "altSymbolMapping",
    "description": "Maps enumeration values to their alternate symbols.",
    "type": {"type": "map",
    "values": { "type": "string" }}
  },
  "namespace": {
    "name": "namespace",
    "description": "Allows for nesting of type definitions within namespaces.",
    "type": "map",
    "values": { "$ref": "#/typeDefinitionOrNamespace" }
  }
}
```

### 10.2. JSON Schema Draft 07 Metaschema

The following is a JSON Schema draft-07 metaschema for JSON-CS.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://schemas.vasters.com/experimental/json-cs/v0",
  "title": "JSON-CS Metaschema",
  "description": "The metaschema for JSON-CS, expressed in JSON Schema draft-07.",
  "type": "object",
  "properties": {
    "$schema": {
      "type": "string",
      "format": "uri",
      "description": "Specifies the version of the JSON-CS specification."
    },
    "$root": {
      "anyOf": [
        { "type": "string" },
        {
          "type": "array",
          "items": { "type": "string" }
        }
      ],
      "description": "References the root schema inside the document."
    },
    "$id": {
      "type": "string",
      "format": "uri",
      "description": "Provides a unique identifier for the schema document."
    },
    "" : {
      "$ref": "#/definitions/namespace"
    }
  },
  "oneOf": [
      { "$ref": "#/definitions/typeDefinition" },
      {
        "patternProperties": {
          "^[A-Za-z_][A-Za-z0-9_]*$": {
            "$ref": "#/definitions/typeDefinitionOrNamespace"
          }
        }
      }
  ],
  "definitions": {
    "typeDefinitionOrNamespace": {
      "description": "A union type that can be either a typeDefinition or a namespace.",
      "anyOf": [
        { "$ref": "#/definitions/typeDefinition" },
        { "$ref": "#/definitions/namespace" }
      ]
    },
    "typeDefinition": {
      "description": "Defines a type in JSON-CS.",
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "The name of the type."
        },
        "abstract": {
          "type": "boolean",
          "description": "Indicates that the type is abstract and must only be used via $extends."
        },
        "$extends": {
          "$ref": "#/definitions/refDefinition",
          "description": "References a type that this type extends."
        },
        "type": {
          "$ref": "#/definitions/typeExpression",
          "description": "The type expression of the type."
        },
        "properties": {
          "$ref": "#/definitions/propertiesDefinition",
          "description": "Defines the properties of an object type."
        },
        "required": {
          "$ref": "#/definitions/stringArray",
          "description": "Specifies required properties."
        },
        "items": {
          "$ref": "#/definitions/typeReference",
          "description": "Defines the schema for elements within an array type."
        },
        "values": {
          "$ref": "#/definitions/typeReference",
          "description": "Defines the schema for values within a map type."
        },
        "additionalProperties": {
          "$ref": "#/definitions/additionalPropertiesDefinition",
          "description": "Controls validation of additional properties in an object."
        },
        "enum": {
          "$ref": "#/definitions/primitiveArray",
          "description": "Restricts a string or numeric type to a fixed set of values."
        },
        "const": {
          "$ref": "#/definitions/primitiveValue",
          "description": "Constrains a schema to accept only a specific value."
        },
        "format": {
          "type": "string",
          "description": "Provides semantic validation for primitive types."
        },
        "unit": {
          "type": "string",
          "description": "Specifies the SI unit symbol associated with a numeric property."
        },
        "description": {
          "type": "string",
          "description": "Provides a human-readable description of the schema."
        },
        "default": {
          "$ref": "#/definitions/primitiveValue",
          "description": "Specifies a default value for the schema or property."
        },
        "examples": {
          "$ref": "#/definitions/examplesDefinition",
          "description": "Provides example instances that are valid against the schema."
        },
        "altnames": {
          "$ref": "#/definitions/altNames",
          "description": "Provides alternative names for types and properties."
        },
        "altsymbols": {
          "$ref": "#/definitions/altSymbols",
          "description": "Provides alternative symbols for enumeration values."
        },
        "maxLength": {
          "type": "integer",
          "description": "Specifies the maximum length of a string."
        },
        "pattern": {
          "type": "string",
          "description": "Specifies a regular expression pattern that a string value must match."
        }
      },
      "required": ["type"],
      "additionalProperties": false
    },
    "typeExpression": {
      "description": "Represents the 'type' attribute in a typeDefinition, which can be a single typeReference or an array of typeReferences for unions.",
      "anyOf": [
        { "$ref": "#/definitions/typeReference" },
        {
          "type": "array",
          "items": { "$ref": "#/definitions/typeReference" }
        }
      ]
    },
    "typeReference": {
      "description": "References a type, either a primitive type name or a $ref to another type.",
      "anyOf": [
        { "$ref": "#/definitions/primitiveTypeName" },
        { "$ref": "#/definitions/refDefinition" },
        { "$ref": "#/definitions/arrayDefinition" },
        { "$ref": "#/definitions/mapDefinition" }
      ]
    },
    "primitiveTypeName": {
      "description": "Enumerates the allowed primitive type names in JSON-CS.",
      "type": "string",
      "enum": [
        "string",
        "integer",
        "number",
        "boolean",
        "null",
        "object",
        "array",
        "map"
      ]
    },
    "arrayDefinition": {
      "description": "Defines an array type in JSON-CS.",
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "The name of the map."
        },
        "type": {
          "type": "string",
          "enum": ["array"],
          "description": "The type of the array."
        },
        "items": {
          "$ref": "#/definitions/itemDefinitionOrRef",
          "description": "Defines the schema for elements within the array."
        },
        "description": {
          "type": "string",
          "description": "Provides a human-readable description of the array."
        }
      },
      "required": ["type"],
      "additionalProperties": false
    },
    "mapDefinition": {
      "description": "Defines a map type in JSON-CS.",
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "The name of the map."
        },
        "type": {
          "type": "string",
          "enum": ["map"],
          "description": "The type of the map."
        },
        "values": {
          "$ref": "#/definitions/itemDefinitionOrRef",
          "description": "Defines the schema for values within the map."
        },
        "description": {
          "type": "string",
          "description": "Provides a human-readable description of the map."
        }
      },
      "required": ["type"],
      "additionalProperties": false
    },
    "itemDefinitionOrRef": {
      "description": "A union type that can be either a typeDefinition or a refDefinition.",
      "anyOf": [
        { "$ref": "#/definitions/itemDefinition" },
        { "$ref": "#/definitions/refDefinition" }
      ]
    },
    "itemDefinition" : {
      "description": "Defines an item within an array, including its type and optional keywords.",
      "type": "object",
      "properties": {
        "type" : {
          "$ref": "#/definitions/typeExpression",
          "description": "The type of the item."
        }
      },
      "additionalProperties": false
    },
    "refDefinition": {
      "description": "Defines the structure of a $ref reference.",
      "type": "object",
      "properties": {
        "$ref": {
          "type": "string",
          "format": "uri-reference",
          "description": "A JSON Pointer to a type definition within the same document."
        },
        "description": {
          "type": "string",
          "description": "Provides a human-readable description of the reference."
        }
      },
      "required": ["$ref"],
      "additionalProperties": false
    },
    "propertiesDefinition": {
      "description": "Defines the properties of an object type.",
      "type": "object",
      "patternProperties": {
        "^[A-Za-z_][A-Za-z0-9_]*$": { "$ref": "#/definitions/propertyDefinitionOrRef" }
      },
      "additionalProperties": false
    },
    "propertyDefinitionOrRef": {
      "description": "A union type that can be either a propertyDefinition or a refDefinition.",
      "anyOf": [
        { "$ref": "#/definitions/propertyDefinition" },
        { "$ref": "#/definitions/refDefinition" }
      ]
    },
    "propertyDefinition": {
      "description": "Defines a property within an object, including its type and optional keywords.",
      "type": "object",
      "properties": {
        "type": {
          "$ref": "#/definitions/typeExpression",
          "description": "The type of the property."
        },
        "format": {
          "type": "string",
          "description": "Provides semantic validation for primitive types."
        },
        "pattern": {
          "type": "string",
          "description": "Specifies a regular expression pattern that a string value must match."
        },
        "maxLength": {
          "type": "integer",
          "description": "Specifies the maximum length of a string."
        },
        "altnames": {
          "$ref": "#/definitions/altNames",
          "description": "Provides alternative names for the property."
        },
        "description": {
          "type": "string",
          "description": "Provides a human-readable description of the property."
        },
        "const": {
          "$ref": "#/definitions/primitiveValue",
          "description": "Constrains the property to accept only a specific value."
        },
        "enum": {
          "$ref": "#/definitions/primitiveArray",
          "description": "Restricts the property to a fixed set of values."
        },
        "default": {
          "$ref": "#/definitions/primitiveValue",
          "description": "Specifies a default value for the property."
        },
        "examples": {
          "$ref": "#/definitions/examplesDefinition",
          "description": "Provides example values for the property."
        },
        "unit": {
          "type": "string",
          "description": "Specifies the SI unit symbol associated with a numeric property."
        }
      },
      "required": ["type"],
      "additionalProperties": false
    },
    "stringArray": {
      "description": "An array of strings.",
      "type": "array",
      "items": { "type": "string" }
    },
    "primitiveArray": {
      "description": "An array of primitive values.",
      "type": "array",
      "items": { "$ref": "#/definitions/primitiveValue" }
    },
    "primitiveValue": {
      "description": "A primitive value: string, number, integer, boolean, or null.",
      "type": ["string", "number", "integer", "boolean", "null"]
    },
    "additionalPropertiesDefinition": {
      "description": "Represents the 'additionalProperties' keyword, which can be a boolean or a typeReference.",
      "anyOf": [
        { "type": "boolean" },
        { "$ref": "#/definitions/typeReference" }
      ]
    },
    "examplesDefinition": {
      "description": "Defines how examples are structured in JSON-CS.",
      "type": "array",
      "items": { "$ref": "#/definitions/exampleDefinition" }
    },
    "exampleDefinition": {
      "description": "Provides an example instance that is valid against the schema.",
      "type": "object",
      "properties": {
        "description": {
          "type": "string",
          "description": "A description of the example."
        },
        "value": {
          "$ref": "#/definitions/primitiveValue",
          "description": "The example value."
        }
      },
      "required": ["value"],
      "additionalProperties": false
    },
    "altNames": {
      "description": "Provides alternative names for types and properties for various purposes.",
      "type": "object",
      "additionalProperties": { "type": "string" }
    },
    "altSymbols": {
      "description": "Provides alternative symbols for enumeration values.",
      "type": "object",
      "additionalProperties": { "$ref": "#/definitions/altSymbolMapping" }
    },
    "altSymbolMapping": {
      "description": "Maps enumeration values to their alternate symbols.",
      "type": "object",
      "additionalProperties": { "type": "string" }
    },
    "namespace": {
      "description": "Allows for nesting of type definitions within namespaces.",
      "type": "object",
      "patternProperties": {
        "^[A-Za-z_][A-Za-z0-9_]*$": { "$ref": "#/definitions/typeDefinitionOrNamespace" }
      },
      "additionalProperties": false
    }
  }
}
```
