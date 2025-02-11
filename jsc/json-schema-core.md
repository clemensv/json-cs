# JSON Schema Core  
C. Vasters (Microsoft) February 2025

## Abstract

This document specifies _JSON Schema Core_, a data structure definition language
that enforces strict typing, modularity, and determinism. _JSON Schema Core_
describes [JSON][JSON]-encoded data such that mapping to and from programming languages
and databases and other data formats is straightforward.

## Table of Contents

- [JSON Schema Core](#json-schema-core)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Conventions Used in This Document](#2-conventions-used-in-this-document)
  - [3. JSON Schema Core Specification](#3-json-schema-core-specification)
    - [3.1. Schema Definition](#31-schema-definition)
      - [3.1.1. Schema](#311-schema)
      - [3.1.2. Non-Schema](#312-non-schema)
      - [3.1.3. Meta-Schemas](#313-meta-schemas)
    - [3.2. Data Types](#32-data-types)
      - [3.2.1. JSON Primitive Types](#321-json-primitive-types)
        - [3.2.1.1. `string`](#3211-string)
        - [3.2.1.2. `number`](#3212-number)
        - [3.2.1.3. `boolean`](#3213-boolean)
        - [3.2.1.4. `null`](#3214-null)
      - [3.2.2. Extended Primitive Types](#322-extended-primitive-types)
        - [3.2.2.1. `binary`](#3221-binary)
        - [3.2.2.2. `int32`](#3222-int32)
        - [3.2.2.3. `uint32`](#3223-uint32)
        - [3.2.2.4. `int64`](#3224-int64)
        - [3.2.2.5. `uint64`](#3225-uint64)
        - [3.2.2.6. `int128`](#3226-int128)
        - [3.2.2.7. `uint128`](#3227-uint128)
        - [3.2.2.8. `float`](#3228-float)
        - [3.2.2.9. `double`](#3229-double)
        - [3.2.2.10. `decimal`](#32210-decimal)
        - [3.2.2.11. `date`](#32211-date)
        - [3.2.2.12. `datetime`](#32212-datetime)
        - [3.2.2.13. `time`](#32213-time)
        - [3.2.2.14. `duration`](#32214-duration)
        - [3.2.2.15. `uuid`](#32215-uuid)
        - [3.2.2.16. `uri`](#32216-uri)
        - [3.2.2.17. `jsonpointer`](#32217-jsonpointer)
      - [3.2.3. Compound Types](#323-compound-types)
        - [3.2.3.1. `object`](#3231-object)
        - [3.2.3.2. `array`](#3232-array)
        - [3.2.3.3. `set`](#3233-set)
        - [3.2.3.4. `map`](#3234-map)
    - [3.3. Document Structure](#33-document-structure)
      - [3.3.1. `$schema` Keyword](#331-schema-keyword)
      - [3.3.2. `$id` Keyword](#332-id-keyword)
      - [3.3.3. `$root` Keyword](#333-root-keyword)
      - [3.3.4. `$defs` Keyword](#334-defs-keyword)
      - [3.3.5 `$ref` Keyword](#335-ref-keyword)
      - [3.3.6. Cross-references](#336-cross-references)
    - [3.4. Type System Rules](#34-type-system-rules)
      - [3.4.1. Type Declarations](#341-type-declarations)
      - [3.4.2. Reusable Types](#342-reusable-types)
      - [3.4.3. Type References](#343-type-references)
      - [3.4.4. Dynamic Structures](#344-dynamic-structures)
    - [3.5. Composition Rules](#35-composition-rules)
      - [3.5.1. Unions](#351-unions)
      - [3.5.1.1. Prohibition of Top-Level Unions](#3511-prohibition-of-top-level-unions)
    - [3.6. Identifier Rules](#36-identifier-rules)
    - [3.7. Structural Keywords](#37-structural-keywords)
      - [3.7.1. The `type` Keyword](#371-the-type-keyword)
      - [3.7.2. The `properties` Keyword](#372-the-properties-keyword)
      - [3.7.3. The `required` Keyword](#373-the-required-keyword)
      - [3.7.4. The `items` Keyword](#374-the-items-keyword)
      - [3.7.5. The `values` Keyword](#375-the-values-keyword)
      - [3.7.6. The `const` Keyword](#376-the-const-keyword)
      - [3.7.7. The `enum` Keyword](#377-the-enum-keyword)
      - [3.7.8. The `additionalProperties` Keyword](#378-the-additionalproperties-keyword)
    - [3.8. Type Annotation Keywords](#38-type-annotation-keywords)
      - [3.8.1. The `maxLength` Keyword](#381-the-maxlength-keyword)
      - [3.8.2. The `precision` Keyword](#382-the-precision-keyword)
      - [3.8.3. The `scale` Keyword](#383-the-scale-keyword)
    - [3.9. Documentation Keywords](#39-documentation-keywords)
      - [3.9.1. The `description` Keyword](#391-the-description-keyword)
      - [3.9.2. The `examples` Keyword](#392-the-examples-keyword)
    - [3.10. Extensions and Mixins](#310-extensions-and-mixins)
      - [3.10.1. The `abstract` Keyword](#3101-the-abstract-keyword)
      - [3.10.2. The `$extends` Keyword](#3102-the-extends-keyword)
      - [3.10.3. The `$mixins` Keyword](#3103-the-mixins-keyword)
  - [4. Reserved Keywords](#4-reserved-keywords)
  - [5. Security Considerations](#5-security-considerations)
  - [6. IANA Considerations](#6-iana-considerations)
  - [7. References](#7-references)
    - [7.1. Normative References](#71-normative-references)
    - [7.2. Informative References](#72-informative-references)
  - [8. Author's Address](#8-authors-address)
  - [9. Appendix: Metaschemas](#9-appendix-metaschemas)
    - [9.1. Base JSON Core Metaschema](#91-base-json-core-metaschema)
    - [9.2. Full JSON Core Metaschema](#92-full-json-core-metaschema)
    - [9.3. Validation JSON Core Metaschema](#93-validation-json-core-metaschema)

---

## 1. Introduction

This document specifies _JSON Schema Core_, a data structure definition language
that enforces strict typing, modularity, and determinism. _JSON Schema Core_
describes JSON-encoded data such that mapping to and from programming languages
and databases and other data formats is straightforward.

_JSON Schema Core_ simplifies many aspects of prior JSON Schema drafts by
factoring complex compositional features out from the core specification and
restricting the remaining composition features like `$ref` to being used to
refer to type definitions and not to arbitrary JSON fragments.

_JSON Schema Core_ is intentionally extensible, allowing additional features to
be layered on top. This version of the specification explicitly turns the core
specification into a data-definition language, while prior versions defined
matching patterns to be applied to document instances for the pruprose of
validation. 

Complementing _JSON Schema Core_ are a set of companion specifications that
extend the core schema language with additional, OPTIONAL features:

- [JSON Schema Alternate Names and Symbols](./json-schema-altnames.md): Provides
  a mechanism for defining alternate names and symbols for types and properties,
  including for the purposes of internationalization.
- [JSON Schema Scientific Units](./json-schema-units.md): Defines a keyword for
  specifying scientific units and constraints on numeric values.
- [JSON Schema Conditional Composition](json-schema-conditional-composition.md):
  Defines a set of conditional composition rules for evaluating schemas.
- [JSON Schema Validation](json-schema-validation.md): Specifies extensions to
  the core schema language for defining validation rules.
- [JSON Schema Import](json-schema-import.md): Defines a mechanism for importing
  external schemas and definitions into a schema document.

These companion specifications are enabled by the
[extensibility](#310-extensions-and-mixins) features of _JSON Schema Core_ and
are designed to be used in conjunction with the core schema language as a choice
of features that a JSON document or node can opt into.

A schema processor that opts into processing a companion spec MUST process the
schema according to the rules and in the order defined in the companion spec.

## 2. Conventions Used in This Document

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119](#91-normative-references) and
[RFC8174](#91-normative-references).

## 3. JSON Schema Core Specification

### 3.1. Schema Definition

#### 3.1.1. Schema

A "schema" is a JSON object that describes, constrains, and interprets a JSON
node. An example for a minimal schema is:

```json
{
  "name": "myname",
  "type": "string"
}
```

This schema constrains a JSON node to be of type `string`. 

All schemas have an associated name that serves as an identifier. In the example
above where the schema is a root object, the name is the value of the `name`
property. When the schema is embedded into a hierarchy of schemas, the name is
the key under which the schema is stored. The schemas of each of the properties
in an object schema are stored under the property name and the types inside a
namespace are stored under the type name in the namespace's type map. Whether as
value of a `name` property or as a key in a map, the name is subject to the
constraints defined in [section 3.6](#36-identifier-rules).

A "schema document" is a schema that represents the root of a schema hierarchy
and is the container format in which schemas are stored on disk or exchanged. A
schema document MAY contain multiple type definitions and namespaces. The
structure of schema documents is defined in [section
3.3](#33-document-structure).

JSON Schema Core is extensible. All keywords that are not explicitly defined in
this document MAY be used for custom annotations and extensions. This also
applies to keywords that begin with the `$` character. A complete list of
reserved keywords is provided in [section 3.11](#311-reserved-keywords).

The semantics of keywords defined in this document MAY be expanded by extension
specifications, but the core semantics of the keywords defined in this document
MUST NOT be altered. 

Be mindful that the use of custom keywords and annotations might conflict with
future versions of this specification or other extensions and that the authors
of this specification will not go out of their way to avoid such conflicts.

[Section 3.10](#310-extensions-and-mixins) details the extensibility features.

#### 3.1.2. Non-Schema

Non-schemas are objects that do not define a schema and therefore do not refer
to a `type`. The root of a [schema document](#33-document-structure) is a
non-schema unless it contains a `type` keyword.

Formally, a schema is a constrained non-schema that requires a `type` keyword.

The distinction between schemas and non-schemas is important for the [JSON
Schema Composition][JSON Schema Composition] companion specification, which
defines how schemas are combined and matched.

#### 3.1.3. Meta-Schemas

A meta-schema is a schema that defines the structure and constraints of a schema
document. Meta-schemas are used to validate schema documents and to ensure that
schemas are well-formed and conform to the JSON Schema Core specification.

The meta-schemas for JSON Schema Core and the companion specifications are
enumerated in the [Appendix: Metaschemas](#9-appendix-metaschemas).

Meta-schemas can extend existing meta-schemas by adding new keywords or
constraints. The `$schema` keyword is used to reference the meta-schema that a
schema document conforms to, the `$id` keyword is used to define the identifier
of the new meta-schema, and the `$import` keyword defined in the [JSON Schema
Import][JSON Schema Import] companion specification is used to import all
definitions from the foundational meta-schema.

### 3.2. Data Types

Data types are categorized into JSON Types, Extended Types, and Compound Types.

While JSON Schema builds on the JSON data type model, it introduces a rich set
of types to represent structured data more accurately and to allow more precise
integration with common data types used in programming languages and data
formats. All these extended types have a well-defined representation in JSON
primitive types.

#### 3.2.1. JSON Primitive Types

These types map directly to the underlying JSON representation:

##### 3.2.1.1. `string`

A sequence of Unicode characters enclosed in double quotes.

- Base type: [`string`](https://datatracker.ietf.org/doc/html/rfc8259#section-7)
- Annotations: The `maxLength` keyword can be used on a schema with the `string`
  type to specify the maximum length of the string. By default, the maximum
  length is unlimited. The purpose of the keyword is to inform consumers of the
  maximum space required to store the string.

##### 3.2.1.2. `number`

A numeric literal without quotes.

- Base type: [`number`](https://datatracker.ietf.org/doc/html/rfc8259#section-6)

Note that the `number` representation in JSON is a textual representation of a
decimal number (base-10) and therefore cannot accurately represent all possible
values of IEE754 floating-point numbers (base-2), in spite of [JSON
Numbers][JSON Numbers] leaning on the IEEE754 standard as a reference for the
value space.

##### 3.2.1.3. `boolean`

A literal `true` or `false` (without quotes).

- Base type: [`boolean`](https://datatracker.ietf.org/doc/html/rfc8259#section-3)

##### 3.2.1.4. `null`

A literal `null` (without quotes).

- Base type: [`null`](https://datatracker.ietf.org/doc/html/rfc8259#section-3)

#### 3.2.2. Extended Primitive Types

Extended types impose additional semantic constraints on the underlying JSON
types. These types are used to represent binary data, high-precision numeric
values, date and time information, and structured data.

Large integer and decimal types are used to represent high-precision numeric
values that exceed the range of IEEE 754 double-precision format, which is the
foundation for the `number` type in JSON. Per [RFC8259 Section 6][JSON Numbers],
interoperable JSON numbers have a range of -2⁵³ to 2⁵³–1, which is less than the
range of 64-bit and 128-bit values. Therefore, the `int64`, `uint64`, `int128`,
`uint128`, and `decimal` types are represented as strings to preserve precision.

The syntax for strings representing large integer and decimal types is based on
the [RFC8259 Section 6][JSON Numbers] syntax for integers and decimals:

- integer = `[minus] int`
- decimal = `[minus] int frac`

##### 3.2.2.1. `binary`

A binary value encoded in base64.

- Base type: `string`
- Constraints:
  - The string value MUST be a valid [Base64][Base64]-encoded binary value.

##### 3.2.2.2. `int32`

A 32-bit signed integer.

- Base type: `number`
- Constraints:
  - The numeric literal MUST be in the range -2³¹ to 2³¹–1.
  - No decimal points or quotes are allowed.

##### 3.2.2.3. `uint32`

A 32-bit unsigned integer.

- Base type: `number`
- Constraints:
  - The numeric literal MUST be in the range 0 to 2³²–1.
  - No decimal points or quotes are allowed.

##### 3.2.2.4. `int64`

A 64-bit signed integer. 

- Base type: `string`
- Constraints:
  - The string MUST conform to the [RFC8259 Section 6][JSON Numbers] definition
    for the `[minus] int` syntax. 
  - The string value MUST represent a 64-bit integer in the range -2⁶³ to 2⁶³–1.

##### 3.2.2.5. `uint64`

A 64-bit unsigned integer.

- Base type: `string`
- Constraints:
  - The string MUST conform to the [RFC8259 Section 6][JSON Numbers] definition
    for the `int` syntax.
  - The string value MUST represent a 64-bit integer in the range 0 to 2⁶⁴–1.

##### 3.2.2.6. `int128`

A 128-bit signed integer.

- Base type: `string`
- Constraints:
  - The string MUST conform to the [RFC8259 Section 6][JSON Numbers] definition
    for the `[minus] int` syntax.
  - The string value MUST represent a 128-bit integer in the range -2¹²⁷ to
    2¹²⁷–1.

##### 3.2.2.7. `uint128`

A 128-bit unsigned integer.

- Base type: `string`
- Constraints:
  - The string MUST conform to the [RFC8259 Section 6][JSON Numbers] definition
    for the `int` syntax.
  - The string value MUST represent a 128-bit integer in the range 0 to 2¹²⁸–1.

##### 3.2.2.8. `float`

A single-precision floating-point number.

- Base type: `number`
- Constraints:
  - Conforms to IEEE 754 single-precision value range limits (32 bits), which
    are 24 bits of significand and 8 bits of exponent, with a range of
    approximately ±3.4×10³⁸.

IEEE754 binary32 are base-2 encoded and therefore cannot represent all decimal
numbers accurately, and vice versa. In cases where you need to encode IEEE754
values precisely, store the IEE754 binary32 value as an `int32` or `uint32`
number.

##### 3.2.2.9. `double`

A double-precision floating-point number.

- Base type: `number`
- Constraints:
  - Conforms to IEEE 754 double-precision value range limits (64 bits),
    which are 53 bits of significand and 11 bits of exponent, with a range of
    approximately ±1.7×10³⁰⁸.

IEEE754 binary64 are base-2 encoded and therefore cannot represent all decimal
numbers accurately, and vice versa. In cases where you need to encode IEEE754
values precisely, store the IEE754 binary64 value as an `int64` or `uint64`
number.

##### 3.2.2.10. `decimal`

A decimal number supporting high-precision values.

- Base type: `string`
- Constraints:
  - The string value MUST conform to the [RFC8259 Section 6][JSON Numbers]
    definition for the `[minus] int frac` syntax.
  - Defaults: 34 significant digits and 7 fractional digits, which is the
    maximum precision supported by the IEEE 754 decimal128 format.
- Annotations:
  - The `precision` keyword MAY be used to specify the total number of
    significant digits.
  - The `scale` keyword MAY be used to specify the number of fractional digits.

##### 3.2.2.11. `date`

A date in YYYY-MM-DD form.

- Base type: `string`
- Constraints:
  - The string value MUST conform to the [RFC3339][RFC3339] `full-date` format.

##### 3.2.2.12. `datetime`

A date and time value with time zone offset.

- Base type: `string`
- Constraints:
  - The string value MUST conform to the [RFC3339][RFC3339] `date-time` format.

##### 3.2.2.13. `time`

A time-of-day value.

- Base type: `string`
- Constraints:
  - The string value MUST conform to the [RFC3339][RFC3339] `time` format.

##### 3.2.2.14. `duration`

A time duration.

- Base type: `string`
- Constraints:
  - The string value MUST conform to the [RFC3339][RFC3339] `duration` format.

##### 3.2.2.15. `uuid`

A universally unique identifier.

- Base type: `string`
- Constraints:
  - The string value MUST conform to the [RFC4122][RFC4122] `UUID` format.

##### 3.2.2.16. `uri`

A URI reference, relative or absolute.

- Base type: `string`
- Constraints:
  - The string value MUST conform to the [RFC3986][RFC3986] `uri-reference`
    format.

##### 3.2.2.17. `jsonpointer`

A JSON Pointer reference.

- Base type: `string`
- Constraints:
  - The string value MUST conform to the [RFC6901][RFC6901] JSON Pointer format.

#### 3.2.3. Compound Types

Compound types are used to structure related data elements. JSON Schema supports
the following compound types:

##### 3.2.3.1. `object`

The `object` type is used to define structured data with named properties. It's
represented as a JSON object, which is an unordered collection of key–value
pairs.

The `object` type MUST include a `name` attribute that defines the name of the
type.

The `object` type MUST include a `properties` attribute that defines the
properties of the object. The `properties` attribute MUST be a JSON object where
each key is a property name and each value is a schema definition for the
property. The object MUST contain at least one property definition.

The `object` type MAY include a `required` attribute that defines the required
properties of the object.

The `object` type MAY include an `additionalProperties` attribute that defines
whether additional properties are allowed and/or what their schema is.

Example:

```json
{
  "name": "Person",
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "int32" }
  },
  "required": ["name"],
  "additionalProperties": false
}
```
 
##### 3.2.3.2. `array`

An `array` type is used to define an ordered collection of elements. It's
represented as a JSON array, which is an ordered list of values.

The `items` attribute of an array MUST reference a declared type or a primitive
type. They MUST NOT declare inline definitions for compound types.

**Examples:**

```json
{
  "type": "array",
  "items": { "type": { "$ref": "#/Namespace/TypeName" } }
}
```

```json
{
  "type": "array",
  "items": { "type": "string" }
}
```
 
##### 3.2.3.3. `set`

The `set` type is used to define an unordered collection of unique elements.
It's represented as a JSON array where all elements are unique.

The `items` attribute of a `set` MUST reference a declared type or a primitive
type. They MUST NOT declare inline definitions for compound types.

Example:

```json
{
  "type": "set",
  "items": { "$ref": "#/Namespace/TypeName" }
}
```

```json
{
  "type": "set",
  "items": { "type": "string" }
}
```

##### 3.2.3.4. `map`

The `map` type is used to define dynamic key–value pairs. It's represented as a
JSON object where the keys are strings and the values are of a specific type.

All keys in a `map` MUST conform to the identifier rules.

The `values` attribute of a `map` MUST reference a declared type or a primitive
type. It MUST NOT declare inline definitions for compound types.

Example:

```json
{
  "type": "map",
  "values": { "$ref": "#/StringType" }
}
```


### 3.3. Document Structure

A JSON Schema document is a JSON object that contains schemas. 

The root of a JSON Schema document MUST be a JSON object. 

The root object MUST contain the following REQUIRED keywords:

- `$id`: A URI that is the unique identifier for this schema document.
- `$schema`: A string that identifies the version of the JSON Schema
  specification used.

The presence of both keywords identifies the document as a JSON Schema document.

The root object MAY contain the following OPTIONAL keywords:

- `$root`: A JSON Pointer that designates a type as the root type for instances.
- `$defs`: The root of the type definition namespace hierarchy.
- `type`: A type declaration for the root type of the document. Mutually
  exclusive with `$root`. 
- if `type` is present, all annotations and constraints applicable to this
  declared root type are also permitted at the root level.
- `name`: A string that defines the name of the root type. Required if `type` is
  present.

A "namespace" is a JSON object that provides a scope for type definitions or
other namespaces. Namespaces MAY be nested within other namespaces.

The `$defs` keyword forms the root of the namespace hierarchy for reusable type
definitions. All type definitions immediately under the `$defs` keyword are in
the root namespace. A `type` definition at the root is placed into the root
namespace as if it were a type definition under `$defs`. 

Any object in the `$defs` map that is not a type definition is a namespace.

Example with inline `type`:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
    "$id": "https://schemas.vasters.com/TypeName",
    "name": "TypeName",
    "type": "object",
    "properties": {
        "name": { "type": "string" }
    }
}
```

Example with `$root`:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
    "$id": "https://schemas.vasters.com/TypeName",
    "$root": "#/$defs/TypeName",
    "$defs": {
        "TypeName": {
            "type": "object",
            "properties": {
                "name": { "type": "string" }
            }
        }        
    }
}
```

Example with the root type in a namespace:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
    "$id": "https://schemas.vasters.com/TypeName",
    "$root": "#/$defs/Namespace/TypeName",
    "$defs": {
        "Namespace": {
            "TypeName": {
                "name": "TypeName",
                "type": "object",
                "properties": {
                    "name": { "type": "string" }
                }
            }
        }
    }
}
```


#### 3.3.1. `$schema` Keyword

The value of the REQUIRED `$schema` keyword MUST be an absolute URI. The keyword
has different functions in JSON Schema documents and JSON documents. 

- In JSON Schema documents, the `$schema` keyword references a meta-schema that
this document conforms to. 
- In JSON documents, the `$schema` keyword references a JSON schema document
that defines the structure of the JSON document.

The value of `$schema` corresponds to the `$id` of the meta-schema or schema
document.

The `$schema` keyword MUST be used at the root level of the document. 

Example:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
    "name": "TypeName",
    "type": "object",
    "properties": {
        "name": { "type": "string" }
    }
}
```

Use of the keyword `$schema` does NOT import the referenced schema document such
that its types become available for use in the current document. 

#### 3.3.2. `$id` Keyword

The REQUIRED `$id` keyword is used to assign a unique identifier to a JSON
Schema document. The value of `$id` MUST be an absolute URI. It SHOULD be a
resolvable URI (a URL).

The `$id` keyword is used to identify a schema document in references like
`$schema`.

The `$id` keyword MUST only be used once in a document, at the root level.

Example:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
    "$id": "https://schemas.vasters.com/TypeName",
    "name": "TypeName",
    "type": "object",
    "properties": {
        "name": { "type": "string" }
    }
}
```

#### 3.3.3. `$root` Keyword

The OPTIONAL `$root` keyword is used to designate any type defined in the
document as the root type for JSON nodes describe by this schema document. The
value of `$root` MUST be a valid JSON Pointer that resolves to an existing type
definition inside the `$defs` object.

The `$root` keyword MUST only be used once in a document, at the root level. Its
use is mutually exclusive with the `type` keyword.

Example:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
    "$id": "https://schemas.vasters.com/TypeName",
    "$root": "#/$defs/Namespace/TypeName",
    "$defs": {
        "Namespace": {
            "TypeName": {
            "name": "TypeName",
            "type": "object",
            "properties": {
                "name": { "type": "string" }
            }
        }
    }
}
```

#### 3.3.4. `$defs` Keyword

The `$defs` keyword defines a namespace hierarchy for reusable type definitions.
The keyword MUST be used at the root level of the document.

The value of the `$defs` keyword MUST be a map of types and namespaces. The
namespace at the root level of the `$defs` keyword is the root namespace.

A namespace is a JSON object that provides a scope for type definitions or other
namespaces. Any JSON object under the `$defs` keyword that is not a type
definition (containing the `type` attribute) is considered a namespace.


Example:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
    "$id": "https://schemas.vasters.com/TypeName",
    "$defs": {
        "Namespace": {
            "TypeName": {
                "name": "TypeName",
                "type": "object",
                "properties": {
                    "name": { "type": "string" }
                }
            }
        }
    }
}
```

#### 3.3.5 `$ref` Keyword

To reference a type definition within the same document, you MUST use a schema
containing a single property with the name `$ref` as the value of `type`. The
value of `$ref` MUST be a valid JSON Pointer that resolves to an existing type
definition.

Example:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
    "$id": "https://schemas.vasters.com/TypeName",
    "properties": {
        "name1": { "type": { "$ref": "#/$defs/Namespace/TypeName" }},
        "name2": { "type": { "$ref": "#/$defs/Namespace2/TypeName2" }}
    },
    "$defs": {
        "Namespace": {
            "TypeName": {
                "name": "TypeName",
                "type": "object",
                "properties": {
                    "name": { "type": "string" }
                }
            }
        },
        "Namespace2": {
            "TypeName2": {
                "name": "TypeName2",
                "type": "object",
                "properties": {
                    "name": { "type": { "$ref": "#/$defs/Namespace/TypeName" }}
                }
            }
        }
    }
}
```

> **Note:** The `$ref` keyword is only permitted inside the `type` attribute
> value of a schema definition, including in type unions. It is not permitted in
> other attributes or in the root object. This is a substantial, simplifying
> change from prior versions of JSON Schema, where `$ref` could be used to
> reference any JSON fragment from anywhere in the document.

#### 3.3.6. Cross-references 

In JSON Schema documents, the `$schema` keyword references the meta-schema of
this specification. In JSON documents, the `$schema` keyword references the
schema document that defines the structure of the JSON document. The value of
`$schema` is a URI. Ideally, the URI SHOULD be [a resolvable
URL](https://www.rfc-editor.org/rfc/rfc3986) to a schema document, but it's
primarily an identifier. As an identifier, it can be used as a lookup key in a
cache or schema-registry.

The `$extends` keyword is used to reference a type definition in the same
document. The value of `$extends` MUST be a JSON Pointer that resolves to a type
definition in the referenced schema document.

The `$mixins` keyword is used to reference type definitions. The value of
`$mixins` MUST be an array of JSON Pointers
([`jsonpointer`](#32217-jsonpointer)), whereby each JSON Pointer references a
type definition in the current schema document. 

Cross-references to external schema documents are generally not permitted in
JSON Schema Core. 

The OPTIONAL [JSON Schema Import][JSON Schema Import] companion specification is
the exception and provides a mechanism for importing definitions from external
schemas. 

### 3.4. Type System Rules

#### 3.4.1. Type Declarations

- Every schema element MUST declare its `type` referring to a primitive or
  compound type.
- Compound types MUST be declared in the `$defs` section, except for `map` and
  `array` types whose values are primitive, and for the root type of a document.
- Primitive and compound type definitions are not extensible outside of this
  specification.
- The defined types are:
    - JSON Primitive Types: `string`, `number`, `boolean`, `null`.
    - Extended Primitive Types: `int32`, `uint32`, `int64`, `uint64`, `int128`,
      `uint128`, `float`, `double`, `decimal`, `date`, `datetime`, `time`,
      `duration`, `uuid`, `uri`, `binary`, `jsonpointer`.
    - JSON Compound Types: `object`, `array`.
    - Extended Compound Types: `map`, `set`.

#### 3.4.2. Reusable Types

- Reusable, compound types MUST be declared in the `$defs` section. It's not
  permitted to declare compound types inline in arrays, maps, unions, or
  property definitions.
- Each type definition in the `$defs` section MUST have a unique name within its
  namespace. Names are case-sensitive. The same name MAY be used in different
  namespaces.

#### 3.4.3. Type References

- Use `$ref` to reference types declared within the same document.
- `$ref` MUST be a valid JSON Pointer resolving to an existing type definition.
- `$ref` MAY be accompanied by a `description` attribute to provide additional
  information about the referenced type in the context of the current schema.

#### 3.4.4. Dynamic Structures

- Use the `map` type for dynamic key–value pairs. The `object` type requires at
  least one property definition and it's therefore (intentionally) not possible
  to define an object with fully dynamic properties using
  `additionalProperties`.
- The `values` attribute of a `map` MUST reference a reusable type or a
  primitive type. Compound types cannot be defined inline in a `map`.
- The `items` attribute of an `array` or `set` MUST reference a reusable type or
  a primitive type. Compound types cannot be defined inline in an `array` or
  `set`.

### 3.5. Composition Rules

This section defines the rules for composing schemas. Further, OPTIONAL composition
rules are defined in the [JSON Schema Conditional Composition][JSON Schema Conditional Composition] companion
specification.

#### 3.5.1. Unions

- Type unions are formed as sets of primitive types and type references.
- A type union is a composite type reference and not a standalone compound type
  and is therefore not named.
- The JSON node described by a schema with a type union MUST conform to at least
  one of the types in the union.
- If the JSON node described by a schema with a type union conforms to more than
  one type in the union, the JSON node MUST be considered to be of the first
  matching type in the union.
- Inline definitions of compound types in a union are NOT permitted, except for
  `map` and `array` types whose values are primitive.

**Examples:**

Union of a string and a compound type:

```json
{
  "type": ["string", { "$ref": "#/Namespace/TypeName" } ]
}
```

Union of a string and an `int32`:

```json
{
  "type": ["string", "int32"]
}
```

A valid union of a string and a `map` of strings:

```json
{
  "type": ["string", { "type": "map", "values": { "type": "string" } } ]
}
```

An inline definition of a compound type in a union is NOT permitted:

```json
{
  "type": ["string", { "type": "object", "properties": { "name": { "type": "string" } } } ]
}
```

#### 3.5.1.1. Prohibition of Top-Level Unions

- The root of a JSON Schema document MUST NOT be an array.
- If a type union is desired as the type of the root of a document instance, the
  `$root` keyword MUST be used to designate a type union as the root type.

### 3.6. Identifier Rules

All property names and type names and map keys MUST conform to the regular
expression `[A-Za-z_][A-Za-z0-9_]*`. They MUST begin with a letter or underscore
and MAY contain letters, digits, and underscores. Keys and type names are
case-sensitive.

If names need to contain characters outside of this range, consider using the
[JSON Schema Alternate Names and Symbols][JSON Schema Alternate Names and
Symbols] companion specification to define those. 

### 3.7. Structural Keywords

#### 3.7.1. The `type` Keyword

Declares the type of a schema element as a primitive or compound type. The
`type` keyword MUST be present in every schema element. For unions, the value of
`type` MUST be an array of type references or primitive type names.

**Example**:

```json
{
  "type": "string"
}
```

#### 3.7.2. The `properties` Keyword

`properties` defines the properties of an `object` type. 

The `properties` keyword MUST contain a `map` of property names mapped to schema
definitions.

**Example**:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "int32" }
  }
}
```

#### 3.7.3. The `required` Keyword

`required` defines the required properties of an `object` type. The `required`
keyword MUST only be used in schemas of type `object`.

The value of the `required` keyword is a simple array of property names or an
array of arrays of property names. 

An array of arrays is used to define alternative sets of required properties.
When an alternative sets are used, exactly one of the sets MUST match the
properties of the object, meaning they are mutually exclusive.

Property names in the `required` array MUST be present in `properties`.

Example:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "int32" }
  },
  "required": ["name"]
}
```

Example with alternative sets:

Because the `name` property is required in both sets, the `name` property is
required in all objects. The `fins` property is required in the first set, and
the `legs` property is required in the second set. That means that an object MUST
have either `fins` or `legs` but not both.

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "fins": { "type": "int32" },
    "legs": { "type": "int32" },
    "wings": { "type": "int32" }
  },
  "required": [["name", "fins"], ["name", "legs"]]
}
```

#### 3.7.4. The `items` Keyword

Defines the schema for elements in an `array` or `set` type. 

The `items` keyword MUST only be used in schemas of type `array` and `set` and
MUST not include inline definitions of compound types.

Examples:

```json
{
  "type": "array",
  "items": { "type": { "$ref": "#/Namespace/TypeName" }}
}
```

```json
{
  "type": "array",
  "items": { "type": "string" }
}
```

#### 3.7.5. The `values` Keyword

Defines the schema for values in a `map` type. 

The `values` keyword MUST only be used in schemas of type `map` and MUST not
include inline definitions of compound types.

Example:

```json
{
  "type": "map",
  "values": { "type": "string" }
```

#### 3.7.6. The `const` Keyword

Constrains the values of the JSON node described by the schema to a single,
specific value. The `const` keyword MUST appear only in schemas with a primitive
`type`, and the instance value MUST match the provided constant exactly.

**Example**:

```json
{
  "type": "string",
  "const": "example"
}
```

#### 3.7.7. The `enum` Keyword

Constrains a schema to match one of a specific set of values. The `enum` keyword
MUST appear only in schemas with a primitive `type`, and all values in the enum
array MUST match that type. Values MUST be unique.

**Example**:

```json
{
  "type": "string",
  "enum": ["value1", "value2", "value3"]
}
```

It is NOT permitted to use `enum` in conjunction with a type union in `type`.

#### 3.7.8. The `additionalProperties` Keyword

`additionalProperties` defines whether additional properties are allowed in an
`object` type and, optionally, what their schema is. The value MUST be a boolean
or a schema. If set to `false`, no additional properties are allowed. If
provided with a schema, each additional property MUST conform to it.

**Example**:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" }
  },
  "additionalProperties": false
}
```


### 3.8. Type Annotation Keywords

Type annotation keywords provide additional metadata about the underlying type.
These keywords are used for documentation and validation of additional
constraints on types.

#### 3.8.1. The `maxLength` Keyword

Specifies the maximum allowed length for a string. The `maxLength` keyword MUST
be used only with `string` types, and the string’s length MUST not exceed this
value.

The purpose of `maxLength` is to provide a known storage constraint on the
maximum length of a string. The value MAY be used for validation.

**Example**:

```json
{
  "type": "string",
  "maxLength": 255
}
```

#### 3.8.2. The `precision` Keyword

Specifies the total number of significant digits for numeric values. The
`precision` keyword is used as an annotation for `number` or `decimal` types.

**Example**:

```json
{
  "type": "decimal",
  "precision": 10
}
```

#### 3.8.3. The `scale` Keyword

Specifies the number of digits to the right of the decimal point for numeric
values. The `scale` keyword is used as an annotation for `number` or `decimal`
types to constrain the fractional part.

**Example**:

```json
{
  "type": "decimal",
  "scale": 2
}
```

### 3.9. Documentation Keywords

Documentation keywords provide descriptive information for schema elements. They
are OPTIONAL but RECOMMENDED for clarity.

#### 3.9.1. The `description` Keyword

Provides a human-readable description of a schema element. The `description`
keyword SHOULD be used to document any schema element.

**Example**:

```json
{
  "type": "string",
  "description": "A person's name"
}
```

For multi-lingual descriptions, the [JSON Schema Alternate Names and
Symbols][JSON Schema Alternate Names and Symbols] companion provides an
extension to define several concurrent descriptions in multiple languages.

#### 3.9.2. The `examples` Keyword

Provides example instance values that conform to the schema. The `examples`
keyword SHOULD be used to document potential instance values.

**Example**:

```json
{
  "type": "string",
  "examples": ["example1", "example2"]
}
```

### 3.10. Extensions and Mixins

The `abstract` and `$extends` keywords enable controlled type extension,
supporting basic object-oriented-programming-style inheritance while not
permitting subtype polymorphism where a sub-type value can be assigned a
base-typed property. This approach avoids validation complexities and mapping
issues between JSON schemas, programming types, and databases.

The `$mixins` keyword allows merging properties from one or more mixin types
into a base schema for a specific JSON document or node. This mechanism works as
follows:

- A base schema defines core types. 
- Mix-in schemas provide additional properties to optionally extend these types
  on need.
- A JSON document combines the base schema with one or more mix-in schemas via
  `$mixins`, resulting in a composite schema with properties and constraints
  from all sources. 

Mixin types MAY override inherited properties, provided the
property type is preserved and all semantic constraints of the base schema are
maintained.

An _extensible type_ is declared as abstract and serves solely as a base for
extensions. For example, a base type _Address_ MAY be extended by
_StreetAddress_ and _PostOfficeBoxAddress_ via `$extends`, but _Address_ cannot
be used directly.

A _mixin type_ is declared as abstract and can be applied to any targeted object
type at the document instance level via `$mixins`. For example, a mixin type
_DeliveryInstructions_ might be applied to any _Address_ types in a document.

In the following example for _extensible types_, the Endpoint type is defined
with a `webEndpoint` property of type `HTTPEndpoint` and a `mqttEndpoint`
property of type `MQTTEndpoint`. Both `HTTPEndpoint` and `MQTTEndpoint` extend
the abstract `Endpoint` type via the `$extends` keyword. The `Endpoint` type
defines common properties, is declared as `abstract`, and cannot be used
directly.

```jsonc
{
    "$id": "https://schemas.vasters.com/NetworkEndpoints",
    "name": "NetworkEndpoints",
    "type": "object",
    "properties": {
        "webEndpoint": { "$ref": "#/$defs/HTTPEndpoint" },
        "mqttEndpoint": { "$ref": "#/$defs/MQTTEndpoint" }
    },
    "required": ["serverEndpoint"],
    "additionalProperties": true,  
    "$defs": {
        "Endpoint": {
            "name": "Endpoint",
            "type": "object",
            "abstract": true,
            "properties": {
                "uri": { "type": "string" },
                "timeout": { "type": "number" }
            },
            "required": ["uri", "timeout"]
        },
        "HTTPEndpoint": {
            "name": "HTTPEndpoint",
            "$extends": "#/$defs/Endpoint",
            "type": "object",
            "properties": {
                "method": { "type": "string" },
                "headers": { "type": "object" }
            },
            "required": ["method"],
            "additionalProperties": false
        },
        "MQTTEndpoint": {
            "name": "MQTTEndpoint",
            "$extends": "#/$defs/Endpoint",
            "type": "object",
            "properties": {
               "topic": { "type": "string" },
               "qos": { "type": "int32" }
            },
            "required": ["topic"],
            "additionalProperties": false
        }
    }
}
```

A _mixin type_ is explicitly designed to compose elements from base and
extension schema documents into a JSON document. In the following example, the
`OAuth2HTTPConfiguration` mixin type is defined in a separate schema that extends
the `HTTPEndpoint` type.

```jsonc
{
    "$id": "https://schemas.vasters.com/NetworkEndpoints",
    "name": "NetworkEndpoints",
    // ... existing properties from the NetworkEndpoints schema
    "$defs": {
        // ... existing types (Endpoint, HTTPEndpoint, MQTTEndpoint)
        "OAuth2HTTPConfiguration": {
            "name": "OAuth2HTTPConfiguration",
            "type": "object",
            "abstract": true,
            "$extends": "#/$defs/HTTPEndpoint",
            "properties": {
                "tokenEndpoint": { "type": "string" },
                "clientId": { "type": "string" },
                "clientSecret": { "type": "string" }
            },
            "required": ["tokenEndpoint", "clientId"],
            "additionalProperties": false
        }
    }
}
```

A document that uses the `NetworkEndpoints` schema and mixes in the
`OAuth2HTTPConfiguration` type is shown in the following example. The
`NetworkEndpoints` type is the root type of the document, and the
`OAuth2HTTPConfiguration` mixin is applied via the `$mixins` keyword. 

```jsonc
{
    "$schema": "https://schemas.vasters.com/NetworkEndpoints",
    "$mixins": ["https://schemas.vasters.com/NetworkEndpoints#/$defs/OAuth2HTTPConfiguration"],
    "serverEndpoint": {
        "uri": "https://api.example.com/data",
        "timeout": 30,
        "method": "GET",
        "headers": {
            "Accept": "application/json"
        },
        "tokenEndpoint": "https://auth.example.com/token",
        "clientId": "exampleClientId",
        "clientSecret": "exampleSecret"
    },
    "brokerEndpoint": {
        "uri": "mqtt://broker.example.com",
        "timeout": 10,
        "topic": "sensors/temp",
        "qos": 1
    }   
}
```

The upside of this approach is that users of the schema who don't need the
optional `OAuth2HTTPConfiguration` mixin can completely ignore it. It's an
abstract type that is only applied to the `HTTPEndpoint` type when explicitly
requested.

#### 3.10.1. The `abstract` Keyword

The `abstract` keyword declares a type as abstract. This prohibits its direct
use in any type declaration or as the type of a schema element. Abstract types
are used as base types for extension via `$extends` or as mixin types via
`$mixins`.

Abstract types implicitly permit additional properties (`additionalProperties`
is always `true`).

- **Value**: A boolean (`true` or `false`).
- **Rules**:
  - The `abstract` keyword MUST only be used in schemas of type `object`.
  - Abstract types MUST NOT be used as the type of a schema element or
    referenced via `$ref`.
  - The `additionalProperties` keyword MUST NOT be used on abstract types (its
    value is implicitly `true`).
  - Abstract types MAY extend other abstract types via `$extends`.


#### 3.10.2. The `$extends` Keyword

The `$extends` keyword merges all properties from an abstract base type into the
extending type. 

If the type using `$extends` is marked as `abstract` and referenced via
`$mixins`, the composite type _replaces_ the base type in the type model of the
document.

- **Value**: A JSON Pointer to an abstract type.
- **Rules**:
  - The `$extends` keyword MUST only be used in schemas of type `object`.
  - The value of `$extends` MUST be a valid JSON Pointer that points to an
    abstract type within the same document.
  - The extending type MUST merge the abstract type’s properties and constraints
    and MUST NOT redefine any inherited property.

#### 3.10.3. The `$mixins` Keyword

The `$mixins` keyword is used to merge properties from one or more mixin type
into the extending type. The mixin types MUST be abstract.

- **Value**: An array of JSON Pointers to abstract types.
- **Rules**:
  - The `$mixins` keyword MUST only be used in schemas of type `object`.
  - The values of `$mixins` MUST be a valid JSON Pointer that points to an
    abstract type within the same document.
  - The extending type MUST merge the mixin type’s properties and constraints
    and MAY redefine inherited properties.

## 4. Reserved Keywords

The following keywords are reserved in JSON Schema and MUST NOT be used as
custom annotations or extension keywords:

- `$defs`
- `$extends`
- `$id`
- `$ref`
- `$root`
- `$schema`
- `abstract`
- `additionalProperties`
- `const`
- `default`
- `description`
- `enum`
- `examples`
- `format`
- `items`
- `maxLength`
- `name`
- `precision`
- `properties`
- `required`
- `scale`
- `type`
- `values`

---

## 5. Security Considerations

JSON Schema documents are self-contained and MUST NOT allow external references
except for the `$schema` and `$mixins` keywords. Implementations MUST ensure
that all `$ref` pointers resolve within the same document to eliminate security
vulnerabilities related to external schema inclusion.

---

## 6. IANA Considerations

This document has no IANA actions.

---

## 7. References

### 7.1. Normative References

- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement
  Levels", BCP 14, RFC 2119.
- [RFC5646] Phillips, A., and M. Davis, "Tags for Identifying Languages", RFC
  5646.
- [RFC6901] Bryan, P., and K. Zyp, "JavaScript Object Notation (JSON) Pointer",
  RFC 6901.
- [RFC8174] Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key
  Words", RFC 8174.
- [Base64] Josefsson, S., "The Base16, Base32, and Base64 Data Encodings", RFC
  4648.
- [JSON] Crockford, D., "The application/json Media Type for JavaScript Object
  Notation (JSON)", RFC 4627.

### 7.2. Informative References

- [BIPM SI] Bureau International des Poids et Mesures, "The International System
  of Units (SI)".
- [NIST HB44] National Institute of Standards and Technology, "NIST Handbook
  44".
- [JSON Schema Draft-07] Wright, G., and H. Andrews, "JSON Schema: A Media Type
  for Describing JSON Documents".
- [JSON Schema Latest] JSON Schema Organization, "JSON Schema Specification".

---

## 8. Author's Address

**Clemens Vasters**  
Microsoft  
Email: clemensv@microsoft.com

---

## 9. Appendix: Metaschemas

Meta-schemas are JSON Schema documents that define the structure of JSON Schema
documents in terms of JSON Schema. This specification provides three metaschemas
for JSON Core schema documents:

### 9.1. Base JSON Core Metaschema

The base JSON Core Metaschema is a JSON Schema document that defines the structure of
JSON Core schema documents in strict compliance with this specification.

The JSON Core Metaschema is available at [./json-core-metaschema.json](./json-core-metaschema.json).

### 9.2. Full JSON Core Metaschema

The full JSON Core Metaschema Full is a JSON Schema document that extends the base JSON
Core Metaschema with the mixin-types defined in the companion specifications enumerated
in the [introductory section](#1-introduction).

The JSON Core Metaschema is available at [./json-core-metaschema-full.json](./json-core-metaschema-full.json).

### 9.3. Validation JSON Core Metaschema

The validation JSON Core Metaschema is a JSON Schema document that enables all
mixins and extensions defined in the full JSON Core Metaschema.

The JSON Core Metaschema is available at [./json-core-metaschema-validation.json](./json-core-metaschema-validation.json).

---

[RFC2119]: https://datatracker.ietf.org/doc/html/rfc2119
[RFC5646]: https://datatracker.ietf.org/doc/html/rfc5646
[RFC6901]: https://datatracker.ietf.org/doc/html/rfc6901
[RFC8174]: https://datatracker.ietf.org/doc/html/rfc8174
[RFC3339]: https://datatracker.ietf.org/doc/html/rfc3339
[RFC3339-5-6]: https://datatracker.ietf.org/doc/html/rfc3339#section-5.6
[RFC3339-AppA]: https://datatracker.ietf.org/doc/html/rfc3339#appendix-A
[RFC6901]: https://datatracker.ietf.org/doc/html/rfc6901
[Base64]: https://datatracker.ietf.org/doc/html/rfc4648
[JSON]: https://www.rfc-editor.org/rfc/rfc8259
[JSON Numbers]: https://www.rfc-editor.org/rfc/rfc8259#section-6

[BIPM SI]: https://www.bipm.org/en/publications/si-brochure
[NIST HB44]:
    https://www.nist.gov/pml/weights-and-measures/publications/nist-handbooks/handbook-44
[JSON Schema Draft-07]:
    https://json-schema.org/draft-07/json-schema-release-notes.html
[JSON Schema Latest]: https://json-schema.org/specification.html
[JSON Schema Conditional Composition]: ./json-schema-conditional-composition.md
[JSON Schema Alternate Names and Symbols]: ./json-altnames.md