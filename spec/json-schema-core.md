# JSON Schema Core  
C. Vasters (Microsoft) February 2024

## Abstract

This document specifies **JSON Schema Core**, a data structure definition
language for JSON data that enforces strict typing, modularity, and determinism.
JSON Schema Core provides a clear and self‐contained approach to defining JSON
data structures.

JSON Schema Core simplifies many aspects of prior JSON Schema drafts by removing
complex compositional features from the core specification. JSON Schema Core is
intentionally extensible, allowing additional features to be layered on top.

Complementing JSON Schema Core are a set of companion specifications that extend
the core schema language with additional features:

- **JSON Schema Alternate Names and Symbols**: Provides a mechanism for defining
  alternate names and symbols for types and properties.
- **JSON Schema Scientific Units**: Defines a set of keywords for specifying
  scientific units and constraints on numeric values.
- **JSON Schema Composition**: Defines a set of composition rules for combining
  multiple schemas into a single schema including external references.
- **JSON Schema Validation**: Specifies extensions to the core schema language
  for defining pattern matching and validation rules.

## Table of Contents

- [JSON Schema Core](#json-schema-core)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Conventions Used in This Document](#2-conventions-used-in-this-document)
  - [3. JSON Schema Core Specification](#3-json-schema-core-specification)
    - [3.1. Schema Definition](#31-schema-definition)
    - [3.2. Data Types](#32-data-types)
      - [3.2.1. JSON Primitive Types](#321-json-primitive-types)
        - [3.2.1.1. string](#3211-string)
        - [3.2.1.2. number](#3212-number)
        - [3.2.1.3. boolean](#3213-boolean)
        - [3.2.1.4. null](#3214-null)
      - [3.2.2. Extended Primitive Types](#322-extended-primitive-types)
        - [3.2.2.1. binary](#3221-binary)
        - [3.2.2.2. int32](#3222-int32)
        - [3.2.2.3. uint32](#3223-uint32)
        - [3.2.2.4. int64](#3224-int64)
        - [3.2.2.5. uint64](#3225-uint64)
        - [3.2.2.6. int128](#3226-int128)
        - [3.2.2.7. uint128](#3227-uint128)
        - [3.2.2.8. float](#3228-float)
        - [3.2.2.9. double](#3229-double)
        - [3.2.2.10. decimal](#32210-decimal)
        - [3.2.2.11. date](#32211-date)
        - [3.2.2.12. datetime](#32212-datetime)
        - [3.2.2.13. time](#32213-time)
        - [3.2.2.14. duration](#32214-duration)
        - [3.2.2.15. uuid](#32215-uuid)
        - [3.2.2.16. uri](#32216-uri)
      - [3.2.3. Compound Types](#323-compound-types)
        - [3.2.3.1. object](#3231-object)
      - [3.5.3.2. array](#3532-array)
      - [3.2.3.3. set](#3233-set)
      - [3.2.3.4. map](#3234-map)
    - [3.3. Document Structure](#33-document-structure)
      - [3.3.1. $schema Keyword](#331-schema-keyword)
      - [3.3.2. $id Keyword](#332-id-keyword)
      - [3.3.3. $root Keyword](#333-root-keyword)
      - [3.3.4. $defs Keyword](#334-defs-keyword)
      - [3.3.5 $ref Keyword](#335-ref-keyword)
    - [3.4. Type System Rules](#34-type-system-rules)
    - [3.5. Composition Rules](#35-composition-rules)
      - [3.5.1. Unions](#351-unions)
      - [3.5.1.1. Prohibition of Top-Level Unions](#3511-prohibition-of-top-level-unions)
    - [3.6. Identifier Rules](#36-identifier-rules)
    - [3.7. Structural Keywords](#37-structural-keywords)
      - [3.7.1. The "type" Keyword](#371-the-type-keyword)
      - [3.7.2. The "properties" Keyword](#372-the-properties-keyword)
      - [3.7.3. The "required" Keyword](#373-the-required-keyword)
      - [3.7.4. The "items" Keyword](#374-the-items-keyword)
      - [3.7.5. The "values" Keyword](#375-the-values-keyword)
      - [3.7.6. The "const" Keyword](#376-the-const-keyword)
      - [3.7.7. The "enum" Keyword](#377-the-enum-keyword)
      - [3.7.8. The "additionalProperties" Keyword](#378-the-additionalproperties-keyword)
    - [3.8. Type Annotation Keywords](#38-type-annotation-keywords)
      - [3.8.1. The "maxLength" Keyword](#381-the-maxlength-keyword)
      - [3.8.2. The "precision" Keyword](#382-the-precision-keyword)
      - [3.8.3. The "scale" Keyword](#383-the-scale-keyword)
    - [3.9. Documentation Keywords](#39-documentation-keywords)
      - [3.9.1. The "description" Keyword](#391-the-description-keyword)
      - [3.9.2. The "examples" Keyword](#392-the-examples-keyword)
    - [3.10. Reuse of Type Definitions with Restricted Polymorphism](#310-reuse-of-type-definitions-with-restricted-polymorphism)
      - [3.11.1. The "abstract" Keyword](#3111-the-abstract-keyword)
      - [3.11.2. The "$extends" Keyword](#3112-the-extends-keyword)
  - [4. Validation Rules](#4-validation-rules)
  - [5. Reserved Keywords](#5-reserved-keywords)
  - [6. Security Considerations](#6-security-considerations)
  - [7. IANA Considerations](#7-iana-considerations)
  - [8. References](#8-references)
    - [8.1. Normative References](#81-normative-references)
    - [8.2. Informative References](#82-informative-references)
  - [9. Author's Address](#9-authors-address)
  - [10. Appendix: Metaschema](#10-appendix-metaschema)
    - [10.1. JSON Schema Metaschema](#101-json-schema-metaschema)
    - [10.2. JSON Schema Metaschema](#102-json-schema-metaschema)

---

## 1. Introduction

This document specifies JSON Schema Core (hereafter referred to as JSON Schema),
a schema language for JSON data that enforces strict typing, modularity, and
determinism. 

JSON Schema Core simplifies many aspects of prior JSON Schema drafts by removing
complex compositional features from the core specification. JSON Schema Core is
intentionally extensible, allowing additional features to be layered on top.

Complementing JSON Schema Core are a set of companion specifications that extend
the core schema language with additional, optional features:

- [JSON Schema Alternate Names and Symbols](./json-schema-altnames.md): Provides
  a mechanism for defining alternate names and symbols for types and properties.
- [JSON Schema Scientific Units](./json-schema-units.md): Defines a set of
  keywords for specifying scientific units and constraints on numeric values.
- [JSON Schema Composition](json-schema-composition.md): Defines a set of
  composition rules for combining multiple schemas into a single schema.
- [JSON Schema Validation](json-schema-validation.md): Specifies extensions to
  the core schema language for defining pattern matching and validation rules.
- [JSON Schema Import](json-schema-import.md): Defines a mechanism for importing
  external schemas and definitions into a schema document.  

## 2. Conventions Used in This Document

The key words **"MUST"**, **"MUST NOT"**, **"REQUIRED"**, **"SHALL"**, **"SHALL
NOT"**, **"SHOULD"**, **"SHOULD NOT"**, **"RECOMMENDED"**, and **"OPTIONAL"** in
this document are to be interpreted as described in
[RFC2119](#91-normative-references) and [RFC8174](#91-normative-references).

## 3. JSON Schema Core Specification

### 3.1. Schema Definition

A JSON Schema schema is a JSON object that describes, constrains, and
interprets a JSON node. An example for a minimal schema is:

```json
{
  "name": "myname",
  "type": "string"
}
```

This schema constrains a JSON node to be of type `string`. A JSON Schema
object is a composition of type definitions, each defining the schema for a
part of the JSON data.

A JSON schema _document_ is a JSON Schema schema that represents the root
of a schema hierarchy and is the container format in which schemas are stored on
disk or exchanged. A schema document MAY contain multiple type definitions and
namespaces. The structure of schema _documents_ is defined in [section
3.3](#33-document-structure).

All keywords that are not explicitly defined in this document MAY be used for
custom annotations and extensions. This also applies to keywords that begin with
the `$` character. A complete list of reserved keywords is provided in [section
3.11](#311-reserved-keywords).

The semantics of all keywords defined in this document MAY be expanded by extension
specifications that build on JSON Schema Core, but the core semantics of the
keywords defined in this document MUST NOT be altered.

Be mindful, however, that the use of custom keywords and annotations might
conflict with future versions of this specification or other extensions and that
the authors of this specification will not go out of their way to avoid such
conflicts.

### 3.2. Data Types

Data types in JSON Schema are categorized into JSON Types, Extended Types, and
Compound Types.

While JSON Schema builds on the JSON data type model, it introduces a richer set
of types to represent structured data more accurately and to allow more precise
integration with common data types used in programming languages and data
formats. All these extended types have a well-defined representation in JSON
primitive types.

#### 3.2.1. JSON Primitive Types

These types map directly to the underlying JSON representation:

##### 3.2.1.1. string

- **Representation**: A sequence of Unicode characters enclosed in double
  quotes.  
- **Mapping**: Maps directly to a JSON string.
- **Annotations**: The `maxLength` keyword can be used on a schema with the
  `string` type to specify the maximum length of the string. By default, the
  maximum length is unlimited. The purpose of the keyword is to inform consumers
  of the maximum space required to store the string.

##### 3.2.1.2. number

- **Representation**: A numeric literal without quotes.  
- **Mapping**: Maps directly to a JSON number following IEEE 754
  double-precision format.  

##### 3.2.1.3. boolean

- **Representation**: The literal `true` or `false` (without quotes).  
- **Mapping**: Maps directly to a JSON boolean.  

##### 3.2.1.4. null

- **Representation**: The literal `null` (without quotes).  
- **Mapping**: Maps directly to the JSON `null` value.  

#### 3.2.2. Extended Primitive Types

Extended types impose additional semantic constraints on the underlying JSON
types. These types are used to represent binary data, high-precision numeric
values, date and time information, and structured data.

Large integer and decimal types are used to represent high-precision numeric
values that exceed the range of IEEE 754 double-precision format, which is the
foundation for the `number` type in [JSON, Section 6][JSON Number]. These types
are represented as strings to preserve precision.

##### 3.2.2.1. binary

- **Underlying JSON Type**: `string`
- **Representation**: A JSON string.
- **Constraints**: The string value MUST be a valid [Base64][Base64]-encoded
  binary value.

##### 3.2.2.2. int32

- **Underlying JSON Type**: `number`
- **Representation**: A numeric literal without decimal points or quotes.
- **Constraints**: The value MUST be in the range -2³¹ to 2³¹–1.

##### 3.2.2.3. uint32

- **Underlying JSON Type**: `number`
- **Representation**: A numeric literal without decimal points or quotes.
- **Constraints**: The value MUST be in the range 0 to 2³²–1.

##### 3.2.2.4. int64

- **Underlying JSON Type**: `string`
- **Representation**: A JSON string.
- **Constraints**: The string value MUST represent a 64-bit signed integer in
  the range -2⁶³ to 2⁶³–1 using the `int` syntax defined in [RFC8259, Section
  6][JSON Numbers].

##### 3.2.2.5. uint64

- **Underlying JSON Type**: `string`
- **Representation**: A JSON string.
- **Constraints**: The string value MUST represent a 64-bit unsigned integer in
  the range 0 to 2⁶⁴–1 using the `int` syntax defined in [RFC8259, Section
    6][JSON Numbers].

##### 3.2.2.6. int128

- **Underlying JSON Type**: `string`
- **Representation**: A JSON string.
- **Constraints**: The string value MUST represent a 128-bit signed integer in
  the range -2¹²⁷ to 2¹²⁷–1 using the `int` syntax defined in [RFC8259, Section
    6][JSON Numbers].

##### 3.2.2.7. uint128

- **Underlying JSON Type**: `string`
- **Representation**: A JSON string.
- **Constraints**: The string value MUST represent a 128-bit unsigned integer in
  the range 0 to 2¹²⁸–1 using the `int` syntax defined in [RFC8259, Section
    6][JSON Numbers].

##### 3.2.2.8. float

- **Underlying JSON Type**: `number`
- **Representation**: A numeric literal without quotes.
- **Constraints**: The value is a single-precision floating-point number
  conforming to limits defined in IEEE 754 for single-precision format: 32 bits,
  8 bits for exponent, 23 bits for mantissa.

##### 3.2.2.9. double

- **Underlying JSON Type**: `number`
- **Representation**: A numeric literal without quotes.
- **Constraints**: The value MUST conform to the limits of IEEE 754
  double-precision format: 64 bits, 11 bits for exponent, 52 bits for mantissa.

##### 3.2.2.10. decimal

- **Underlying JSON Type**: `string`
- **Representation**: A JSON string.
- **Constraints**: The string value MUST represent a decimal number. The value
  MUST conform to a `[minus] int [ frac ]` expression as defined in [RFC8259,
  Section 6][JSON Numbers]. In absence of annotations, the default `precision`
  is 34 significant digits, and the default `scale` is 7 fractional digits, a
  range from -999999999999999999999999999.9999999 to
  +999999999999999999999999999.9999999.
- **Annotations**: The `precision` and `scale` keywords MAY be used on a schema
  with the `decimal` type to specify the total number of significant digits and
  the number of digits to the right of the decimal point.

##### 3.2.2.11. date

- **Underlying JSON Type**: `string`
- **Representation**: A string conforming to the [RFC3339][RFC3339]
  [`full-date`][RFC3339-5-6] format (`YYYY-MM-DD`).

##### 3.2.2.12. datetime

- **Underlying JSON Type**: `string`
- **Representation**: A string conforming to the [RFC3339][RFC3339]
  [`date-time`][RFC3339-5-6] format, including time zone offset information.

##### 3.2.2.13. time

- **Underlying JSON Type**: `string`
- **Representation**: A string conforming to the [RFC3339][RFC3339]
  [`time`][RFC3339-5-6] format.

##### 3.2.2.14. duration

- **Underlying JSON Type**: `string`
- **Representation**: A string conforming to the [RFC3339][RFC3339]
  [`duration`][RFC3339-AppA] format.

##### 3.2.2.15. uuid

- **Underlying JSON Type**: `string`
- **Representation**: A string conforming to the [RFC4122][RFC4122] `UUID` format.

##### 3.2.2.16. uri

- **Underlying JSON Type**: `string`
- **Representation**: A string conforming to the [RFC3986][RFC3986]
  [`uri-reference`](https://datatracker.ietf.org/doc/html/rfc3986#section-4.1)
  format. This type permits both relative and absolute URIs.

#### 3.2.3. Compound Types

Compound types are used to structure related data elements. JSON Schema
supports the following compound types:

##### 3.2.3.1. object

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

**Example:**

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
 
#### 3.5.3.2. array

An `array` type is used to define an ordered collection of elements. It's
represented as a JSON array, which is an ordered list of values.

The `items` attribute of an array MUST reference a declared type or a primitive
type. They MUST NOT declare inline definitions for compound types.

**Examples:**

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
 
#### 3.2.3.3. set

The `set` type is used to define an unordered collection of unique elements. It's
represented as a JSON array where all elements are unique.

The `items` attribute of a `set` MUST reference a declared type or a primitive
type. They MUST NOT declare inline definitions for compound types.

**Example:**

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

#### 3.2.3.4. map

The `map` type is used to define dynamic key–value pairs. It's represented as a
JSON object where the keys are strings and the values are of a specific type.

All keys in a `map` MUST conform to the identifier rules.

The `values` attribute of a `map` MUST reference a declared type or a primitive
type. It MUST NOT declare inline definitions for compound types.

**Example:**

```json
{
  "type": "map",
  "values": { "$ref": "#/StringType" }
}
```


### 3.3. Document Structure

A JSON Schema document is a JSON object that contains type definitions. The
document structure defines namespaces and types.

A namespace is a JSON object that provides a scope for type definitions or other
namespaces. Namespaces MAY be therefore be nested within other namespaces.

The root of a JSON Schema document MUST be a JSON object. The root object
MAY contain the following keywords:

- `$schema`: A string that identifies the version of the JSON Schema
  specification used.
- `$id`: A URI that assigns a unique identifier to the schema document.
- `$root`: A JSON Pointer that designates a type as the root type for instances.
- `$defs`: The root of the type definition namespace hierarchy.
- `type`: A type declaration for the root type of the document. Mutually
  exclusive with `$root`.
- if `type` is present, all annotations and constraints applicable to the root
  type are also permitted at the root level.
- `name`: A string that defines the name of the root type. Required if `type` is
  present.

#### 3.3.1. $schema Keyword

A JSON Schema document SHOULD be distinguishable from other JSON documents by
the use of the `$schema` keyword. The `$schema` keyword is a string that
identifies the version of the JSON Schema specification used. For this
version, the identifier MUST be:

```
"https://schemas.vasters.com/experimental/json-core/v0"
```

The `$schema` keyword MUST be used at the root level of the document. 

For example:

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

#### 3.3.2. $id Keyword

The `$id` keyword is OPTIONAL and MAY be used to assign a unique identifier to a
JSON Schema document. The value of `$id` MUST be a valid URI. It MAY be but
might not be a resolvable URI.

The `$id` keyword is used to reference a schema document from other documents.

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

#### 3.3.3. $root Keyword

The `$root` keyword is used to designate any type defined in the document as the
root type for JSON nodes describe by this schema document. The value of `$root`
MUST be a valid JSON Pointer that resolves to an existing type definition inside
the `$defs` object.

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

#### 3.3.4. $defs Keyword

The `$defs` keyword is used to define a namespace hierarchy for reusable type
definitions. The `$defs` keyword MUST be used at the root level of the document.

The `$defs` keyword MAY contain type definitions or nested namespaces. The 
namespace at the root level of the `$defs` keyword is the empty namespace.

A namespace is a JSON object that provides a scope for type definitions or other
namespaces. Any JSON object under the `$defs` keyword that is not a type
definition (containing the `type` attribute) is considered a namespace.


Example:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
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

#### 3.3.5 $ref Keyword

To reference a type definition within the same document, use a JSON schema
containing a single property with the name `$ref`. The value of `$ref` MUST be a
valid JSON Pointer that resolves to an existing type definition.

The `$ref` keyword MUST NOT be combined with additional attributes. Such
references can be used with any occurrence of the `type` attribute.

Example:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
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
                    "name": { "$ref": "#/$defs/Namespace/TypeName" }
                }
            }
        }
    }
}
```


### 3.4. Type System Rules

1. **Type Declarations**:  
   Every schema element MUST explicitly declare its `type` using a primitive or
   compound type. The primitive and compound type choices are NOT extensible
   outside of this specification.
   - **JSON Primitive Types**: `string`, `number`, `boolean`, `null`.
   - **Extended Primitive Types**: `int32`, `uint32`, `int64`, `uint64`, `int128`,
     `uint128`, `float`, `double`, `decimal`, `date`, `datetime`, `time`,
     `duration`, `uuid`, `uri`, `binary`.
   - **JSON Compound Types**: `object`, `array`.
   - **Extended Compound Types**: `map`, `set`.

2. **Reusable Types**:  
   All reusable types that are to be used more than once within the document
   MUST be declared within the `$defs` section.

3. **Type References**:  
   `$ref` MUST be used exclusively to reference types declared within the same
   document. The value of `$ref` MUST be a valid JSON Pointer that resolves to
   an existing type definition. `$ref` MUST NOT be combined with additional
   attributes.

4. **Prohibition of Inline Definitions**:  
   Inline definitions of types in arrays, maps, unions, or property definitions
   are STRICTLY PROHIBITED. All compound types MUST be declared separately in
   the `$defs` section and referenced via `$ref`.

5. **Dynamic Structures**:  
   Dynamic key–value pairs MUST be defined using the `map` type. The `values`
   attribute of a `map` MUST reference a declared type or a primitive type. A schema of type `object` MUST have a `properties` attribute with at least one property definition.

### 3.5. Composition Rules

This section defines the rules for composing JSON schemas. This specification
only defines the core composition rules. Additional composition rules are
defined in companion specifications.

#### 3.5.1. Unions

- JSON Schema supports type unions via an array in the `type` attribute.
- Each element in the union array MUST be a reference to a declared type or a
  primitive type.
- Inline definitions of compound types in a union are STRICTLY PROHIBITED,
  except for `map` and `array` types whose values are primitive.

**Examples:**

Union of a string and a compound type:

```json
{
  "type": ["string", { "$ref": "#/Namespace/TypeName" }]
}
```

Union of a string and an int32:

```json
{
  "type": ["string", "int32"]
}
```

A valid union of a string and a map of strings:

```json
{
  "type": ["string", { "type": "map", "values": { "type": "string" } }]
}
```

An inline definition of a compound type in a union is STRICTLY PROHIBITED:

```json
{
  "type": ["string", { "type": "object", "properties": { "name": { "type": "string" } } }]
}
```

#### 3.5.1.1. Prohibition of Top-Level Unions

- The root of a JSON Schema document MUST NOT be an array.
- The `$root` keyword MUST be used to designate a type union as the root type.

### 3.6. Identifier Rules

1. **Key and Name Format**:  
   All property names and type names MUST conform to the regular expression
   `[A-Za-z_][A-Za-z0-9_]*`. They MUST begin with a letter or underscore and MAY
   contain letters, digits, and underscores. Keys and type names are
   case-sensitive.

2. **Map Key Constraints**:  
   Keys in a `map` instance MUST conform to the identifier rules.

### 3.7. Structural Keywords

#### 3.7.1. The "type" Keyword

- **Purpose**: Declares the type of a schema element.
- **Value**: A string representing a single type or an array representing a
  union of types.
- **Rules**:
  - The `type` keyword MUST be present in every schema element.
  - For unions, the value of `type` MUST be an array of type references or
    primitive type names.

**Example:**

```json
{ "type": "string" }
```

```json
{ "type": ["string", { "$ref": "#/Namespace/TypeName" }] }
```

#### 3.7.2. The "properties" Keyword

- **Purpose**: Defines the properties of an `object` type.
- **Value**: A JSON object where each key is a property name and each value is a
  schema definition for the property.
- **Rules**:
- The `properties` keyword MUST only be used in schemas of type `object`.
- The `properties` keyword MUST be present in every schema of type `object`.
- The `properties` keyword MUST contain at least one property definition.
- The property names MUST conform to the identifier rules.
- The property definitions MUST NOT include inline definitions for compound
  types; they MUST reference a declared type via `$ref`.

**Example:**

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "int32" }
  }
}
```

#### 3.7.3. The "required" Keyword

- **Purpose**: Defines the required properties of an `object` type.
- **Value**: An array of property names.
- **Rules**:
  - The `required` keyword MUST only be used in schemas of type `object`.
  - The `required` keyword MUST NOT be used in schemas of type `map`.
  - The `required` keyword MUST NOT be used in schemas of type `set`.
  - The property names in the `required` array MUST be present in the `properties`
    object.

**Example:**
    
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

#### 3.7.4. The "items" Keyword

- **Purpose**: Defines the schema for elements in an `array` type.
- **Value**: A schema that MUST reference a declared type.
- **Rules**:
  - The `items` keyword MUST only be used in schemas of type `array`.
  - The schema specified in `items` MUST NOT include inline definitions for
    compound types; it MUST reference a declared type via `$ref`.

**Example:**

```json
{
  "type": "array",
  "items": { "$ref": "#/Namespace/TypeName" }
}
```

#### 3.7.5. The "values" Keyword

- **Purpose**: Defines the schema for values in a `map` type.
- **Value**: A schema that MUST reference a declared type.
- **Rules**:
  - The `values` keyword MUST only be used in schemas of type `map`.
  - The schema specified in `values` MUST NOT include inline definitions for
    compound types; it MUST reference a declared type via `$ref`.

**Example:**

```json
{
  "type": "map",
  "values": { "$ref": "#/Namespace/ValueType" }
}
```

#### 3.7.6. The "const" Keyword

- **Purpose**: Constrains a schema to accept only one specific value.
- **Value**: A primitive value (string, number, integer, boolean, or null).
- **Rules**:
  - The `const` keyword MUST only be used in schemas with a primitive `type`.
  - The instance value MUST equal the value specified by `const`.

**Example:**

```json
{ "type": "string", "const": "fixedValue" }
```

#### 3.7.7. The "enum" Keyword

- **Purpose**: Constrains a schema to accept only a specific set of values.
- **Value**: An array of primitive values (strings, numbers, integers, booleans,
  or nulls).
- **Rules**:
- The `enum` keyword MUST only be used in schemas with a primitive `type`.
- The instance value MUST be one of the values specified in the `enum` array.
- The `enum` array MUST contain at least one value.
- The values in the `enum` array MUST be unique.
- The values in the `enum` array MUST be of the same type as the schema type.

**Example:**

```json
{ "type": "string", "enum": ["value1", "value2"] }
```

#### 3.7.8. The "additionalProperties" Keyword

- **Purpose**: Defines whether additional properties are allowed and/or what their
  schema is.
- **Value**: A schema that MUST reference a declared type or a primitive type.
- **Rules**:
  - The `additionalProperties` keyword MUST only be used in schemas of type
    `object`.
  - The schema specified in `additionalProperties` MUST NOT include inline
    definitions for compound types; it MUST reference a declared type via `$ref`.
  - The value of `additionalProperties` MUST be a boolean or a schema.
  - If `additionalProperties` is `true`, any additional properties are allowed.
  - If `additionalProperties` is `false`, no additional properties are allowed.
  - If `additionalProperties` is a schema, additional properties MUST conform to
    the schema.

**Example:**

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "int32" }
  },
  "additionalProperties": false
}
```

### 3.8. Type Annotation Keywords

Type annotation keywords provide additional metadata about the underlying type.
These keywords are used for documentation and validation of additional
constraints on types.

#### 3.8.1. The "maxLength" Keyword

- **Purpose**: Specifies the maximum allowed length for a string.
- **Value**: A non-negative integer.
- **Rules**:
  - The `maxLength` keyword MUST be used with elements of type `string`.
  - The length of the string value MUST NOT exceed the specified value.
  
**Example:**

```json
{
  "type": "string",
  "maxLength": 10
}
```

#### 3.8.2. The "precision" Keyword

- **Purpose**: Specifies the total number of significant digits for numeric
  values.
- **Value**: A non-negative integer.
- **Rules**:
  - The `precision` keyword MUST be used as an annotation with elements of type
    `number` or `decimal` when high precision is required.
  - It provides a constraint on the total number of significant digits.
  
**Example:**

```json
{
  "type": "decimal",
  "precision": 10
}
```

#### 3.8.3. The "scale" Keyword

- **Purpose**: Specifies the number of digits to the right of the decimal point.
- **Value**: A non-negative integer.
- **Rules**:
  - The `scale` keyword MUST be used as an annotation with elements of type
    `number` or `decimal` to constrain the fractional part.
  
**Example:**

```json
{
  "type": "decimal",
  "scale": 2
}
```

### 3.9. Documentation Keywords

Documentation keywords provide descriptive information for schema elements. They
are OPTIONAL but RECOMMENDED for clarity.

#### 3.9.1. The "description" Keyword

- **Purpose**: Provides a human-readable description of a schema element.
- **Value**: A string.
- **Rules**:
  - The `description` keyword SHOULD be used to document any schema element.
  
#### 3.9.2. The "examples" Keyword

- **Purpose**: Provides example instance values that conform to the schema.
- **Value**: An array of objects, each containing a `description` and a `value`.
- **Rules**:
  - The `examples` keyword SHOULD be used to document potential instance values.

### 3.10. Reuse of Type Definitions with Restricted Polymorphism

The keywords `abstract` and `$extends` ENABLE the reuse of definitions while
STRICTLY PROHIBITING unrestricted subtype polymorphism. This mechanism allows a
base (abstract) type to define common properties and constraints that MAY be
extended by other types, but the abstract type itself MUST NOT be used directly.

- **$extends**: MUST copy all properties and constraints from an abstract type
  into the extending type.
- Abstract types MUST NOT be referenced directly via `$ref`.
- Abstract types MAY extend other abstract types via `$extends`.
- The extending type MUST merge the abstract type’s properties and constraints
  and MUST NOT redefine any inherited property.

**Example:**

```jsonc
{
  "Person": {
    "name": "Person",
    "type": "object",
    "properties": {
      "name": { "type": "string" },
      "residenceAddress": { "$ref": "#/StreetAddress" },
      "postalAddress": [
        { "$ref": "#/StreetAddress" },
        { "$ref": "#/PostOfficeBoxAddress" }
      ]
    },
    "required": ["name", "residenceAddress"],
    "additionalProperties": true
  },
  "Address": {
    "name": "Address",
    "type": "object",
    "abstract": true,
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
    "$extends": "#/Address",
    "type": "object",
    "properties": {
      "street": { "type": "string" },
      "unit": { "type": "string" },
      "floor": { "type": "string" },
      "building": { "type": "string" }
    },
    "required": ["street"],
    "additionalProperties": false
  },
  "PostOfficeBoxAddress": {
    "name": "PostOfficeBoxAddress",
    "$extends": "#/Address",
    "type": "object",
    "properties": {
      "poBox": { "type": "string" }
    },
    "required": ["poBox"],
    "additionalProperties": false
  }
}
```

#### 3.11.1. The "abstract" Keyword

- **Purpose**: Declares a type as abstract, thereby prohibiting its direct use.
- **Value**: A boolean (`true` or `false`).
- **Rules**:
  - The `abstract` keyword MUST only be used in schemas of type `object`.
  - Abstract types MUST NOT be used as the type of a schema element or
    referenced via `$ref`.
  - The `additionalProperties` keyword MUST NOT be used on abstract types (its
    value is implicitly `true`).
  - Abstract types MAY extend other abstract types via `$extends`.

#### 3.11.2. The "$extends" Keyword

- **Purpose**: Extends a type by merging properties and constraints from an
  abstract type.
- **Value**: A JSON Pointer to the abstract type.
- **Rules**:
  - The `$extends` keyword MUST only be used in schemas of type `object`.
  - The value of `$extends` MUST be a valid JSON Pointer that points to an
    abstract type within the same document.
  - The extending type MUST merge the abstract type’s properties and constraints
    and MUST NOT redefine any inherited property.


## 4. Validation Rules

1. **Type Resolution**:  
   A type reference (`$ref`) MUST resolve to a declared type in the document.
   Unresolved references MUST result in a validation error.

2. **Prohibited Patterns**:  
   External references (e.g., URIs with authorities) MUST NOT be used.
   Fragment-only pointers (e.g., `"$ref": "#"`) are INVALID.

3. **Inline Definitions**:  
   Inline definitions of compound types in arrays, maps, or unions are STRICTLY
   PROHIBITED. All compound types MUST be declared separately and referenced via
   `$ref`.

4. **Unique Names**:  
   Type names MUST be unique within a namespace, and fully qualified names MUST
   be globally unique. Duplicate type names within the same namespace MUST
   result in a validation error.

5. **Property Definitions**:  
   For `object` types, the `properties` keyword defines named properties. Each
   property name MUST conform to identifier rules. Each property’s schema MUST
   include an explicit `type` declaration. Inline definitions of compound types
   in properties are STRICTLY PROHIBITED.

6. **Required Properties**:  
   The `required` keyword lists property names that MUST be present. Each name
   in `required` MUST be defined in `properties`. Omission of a required
   property in an instance MUST result in a validation error.

7. **Map Key Constraints**:  
   Keys in a `map` instance MUST conform to the identifier rules. Non-conforming
   keys MUST result in a validation error.

8. **Data Type Constraints**:  
   Instance values MUST conform to the declared type definitions. Type
   mismatches (e.g., a string provided where an integer is expected) MUST result
   in a validation error.

9. **Enum Constraints**:  
   The `enum` keyword MUST only be used with primitive types. An instance value
   MUST equal one of the values specified in the `enum` array.

10. **Const Constraints**:  
    The `const` keyword MUST only be used with primitive types. An instance
    value MUST equal the constant value specified.

11. **Additional Properties**:  
    If `additionalProperties` is `false`, any property not defined in
    `properties` MUST result in a validation error. If a schema is provided,
    every additional property value MUST conform to that schema.

12. **Type Annotation Constraints**:  
    Type annotation keywords (e.g., `maxLength`, `precision`, `scale`) provide
    additional constraints on the underlying type. Validators SHALL enforce
    these constraints according to their definitions.

## 5. Reserved Keywords

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

## 6. Security Considerations

JSON Schema documents are self-contained and MUST NOT allow external
references. Implementations MUST ensure that all `$ref` pointers resolve within
the same document to eliminate security vulnerabilities related to external
schema inclusion.

---

## 7. IANA Considerations

This document has no IANA actions.

---

## 8. References

### 8.1. Normative References

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

### 8.2. Informative References

- [BIPM SI] Bureau International des Poids et Mesures, "The International System
  of Units (SI)".
- [NIST HB44] National Institute of Standards and Technology, "NIST Handbook
  44".
- [JSON Schema Draft-07] Wright, G., and H. Andrews, "JSON Schema: A Media Type
  for Describing JSON Documents".
- [JSON Schema Latest] JSON Schema Organization, "JSON Schema Specification".



---

## 9. Author's Address

**Clemens Vasters**  
Microsoft  
Email: clemensv@microsoft.com

---

## 10. Appendix: Metaschema

### 10.1. JSON Schema Metaschema

The JSON Schema metaschema is a JSON Schema Core document that defines the
structure for JSON Schema Core schemas.

```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
  "$id": "https://schemas.vasters.com/experimental/json-core-metaschema/v0",
  "type": "object",
  "properties": {
    "$schema": {
      "type": "uri",
      "const": "https://schemas.vasters.com/experimental/json-core/v0"
    },
    "$id": {
      "type": "uri"
    },
    "$root": {
      "type": "string"
    },
    "$defs": {
      "type": "object",
      "additionalProperties": {
        "$ref": "#/definitions/TypeDefinition"
      }
    },
    "name": {
      "type": "string"
    },
    "type": {
      "type": [
        "string",
        "array"
      ]
    },
    "properties": {
      "type": "object",
      "additionalProperties": {
        "$ref": "#/definitions/TypeDefinition"
      }
    },
    "required": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "additionalProperties": {
      "type": [
        "boolean",
        "object"
      ]
    },
    "items": {
      "$ref": "#/definitions/TypeDefinition"
    },
    "values": {
      "$ref": "#/definitions/TypeDefinition"
    },
    "const": {},
    "enum": {
      "type": "array"
    },
    "maxLength": {
      "type": "integer"
    },
    "precision": {
      "type": "integer"
    },
    "scale": {
      "type": "integer"
    },
    "description": {
      "type": "string"
    },
    "examples": {
      "type": "array"
    },
    "abstract": {
      "type": "boolean"
    },
    "$extends": {
      "type": "string"
    },
    "$ref": {
      "type": "string"
    }
  },
  "additionalProperties": false,
  "definitions": {
    "TypeDefinition": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "type": {
          "type": [
            "string",
            "array"
          ]
        },
        "properties": {
          "type": "object",
          "additionalProperties": {
            "$ref": "#/definitions/TypeDefinition"
          }
        },
        "required": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "additionalProperties": {
          "type": [
            "boolean",
            "object"
          ]
        },
        "items": {
          "$ref": "#/definitions/TypeDefinition"
        },
        "values": {
          "$ref": "#/definitions/TypeDefinition"
        },
        "const": {},
        "enum": {
          "type": "array"
        },
        "maxLength": {
          "type": "integer"
        },
        "precision": {
          "type": "integer"
        },
        "scale": {
          "type": "integer"
        },
        "description": {
          "type": "string"
        },
        "examples": {
          "type": "array"
        },
        "abstract": {
          "type": "boolean"
        },
        "$extends": {
          "type": "string"
        },
        "$ref": {
          "type": "string"
        }
      },
      "required": [
        "type"
      ],
      "additionalProperties": false
    }
  }
}
```

### 10.2. JSON Schema Metaschema

This version of the metaschema uses the composition extension and validation
extensions defined in [JSON Schema Composition](./json-schema-composition.md)
and [JSON Schema Validation](./json-schema-validation.md).


```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
  "$id": "https://schemas.vasters.com/experimental/json-core-metaschema/v0",
  "type": "object",
  "properties": {
    "$schema": {
      "type": "uri",
      "const": "https://schemas.vasters.com/experimental/json-core/v0"
    },
    "$id": {
      "type": "uri"
    },
    "$root": {
      "type": "string"
    },
    "$defs": {
      "type": "object",
      "additionalProperties": {
        "$ref": "#/definitions/TypeDefinition"
      }
    }
  },
  "additionalProperties": {
    "$ref": "#/definitions/TypeDefinition"
  },
  "definitions": {
    "TypeDefinition": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "type": {
          "anyOf": [
            { "type": "string" },
            {
              "type": "array",
              "items": { "type": "string" }
            }
          ]
        },
        "properties": {
          "type": "object",
          "additionalProperties": {
            "$ref": "#/definitions/TypeDefinition"
          }
        },
        "required": {
          "type": "array",
          "items": { "type": "string" }
        },
        "additionalProperties": {
          "anyOf": [
            { "type": "boolean" },
            { "$ref": "#/definitions/TypeDefinition" }
          ]
        },
        "items": {
          "$ref": "#/definitions/TypeDefinition"
        },
        "values": {
          "$ref": "#/definitions/TypeDefinition"
        },
        "const": {},
        "enum": {
          "type": "array"
        },
        "minLength": {
          "type": "integer"
        },
        "maxLength": {
          "type": "integer"
        },
        "pattern": {
          "type": "string"
        },
        "precision": {
          "type": "integer"
        },
        "scale": {
          "type": "integer"
        },
        "minimum": {
          "anyOf": [
            { "type": "number" },
            { "type": "string" }
          ]
        },
        "maximum": {
          "anyOf": [
            { "type": "number" },
            { "type": "string" }
          ]
        },
        "exclusiveMinimum": {
          "anyOf": [
            { "type": "number" },
            { "type": "string" }
          ]
        },
        "exclusiveMaximum": {
          "anyOf": [
            { "type": "number" },
            { "type": "string" }
          ]
        },
        "multipleOf": {
          "anyOf": [
            { "type": "number" },
            { "type": "string" }
          ]
        },
        "minItems": {
          "type": "integer"
        },
        "maxItems": {
          "type": "integer"
        },
        "uniqueItems": {
          "type": "boolean"
        },
        "contains": {
          "$ref": "#/definitions/TypeDefinition"
        },
        "minProperties": {
          "type": "integer"
        },
        "maxProperties": {
          "type": "integer"
        },
        "dependencies": {
          "type": "object",
          "additionalProperties": {
            "anyOf": [
              {
                "type": "array",
                "items": { "type": "string" }
              },
              { "$ref": "#/definitions/TypeDefinition" }
            ]
          }
        },
        "patternProperties": {
          "type": "object",
          "additionalProperties": {
            "$ref": "#/definitions/TypeDefinition"
          }
        },
        "propertyNames": {
          "$ref": "#/definitions/TypeDefinition"
        },
        "if": {
          "$ref": "#/definitions/TypeDefinition"
        },
        "then": {
          "$ref": "#/definitions/TypeDefinition"
        },
        "else": {
          "$ref": "#/definitions/TypeDefinition"
        },
        "not": {
          "$ref": "#/definitions/TypeDefinition"
        },
        "allOf": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/definitions/TypeDefinition"
          }
        },
        "anyOf": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/definitions/TypeDefinition"
          }
        },
        "oneOf": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/definitions/TypeDefinition"
          }
        },
        "description": {
          "type": "string"
        },
        "examples": {
          "type": "array"
        },
        "abstract": {
          "type": "boolean"
        },
        "$extends": {
          "type": "string"
        },
        "$ref": {
          "type": "string"
        }
      },
      "required": [
        "type"
      ],
      "additionalProperties": false
    }
  }
}
```

[RFC2119]: https://datatracker.ietf.org/doc/html/rfc2119
[RFC5646]: https://datatracker.ietf.org/doc/html/rfc5646
[RFC6901]: https://datatracker.ietf.org/doc/html/rfc6901
[RFC8174]: https://datatracker.ietf.org/doc/html/rfc8174
[RFC3339]: https://datatracker.ietf.org/doc/html/rfc3339
[RFC3339-5-6]: https://datatracker.ietf.org/doc/html/rfc3339#section-5.6
[RFC3339-AppA]: https://datatracker.ietf.org/doc/html/rfc3339#appendix-A
[Base64]: https://datatracker.ietf.org/doc/html/rfc4648
[JSON]: https://www.rfc-editor.org/rfc/rfc8259
[JSON Numbers]: https://www.rfc-editor.org/rfc/rfc8259#section-6

[BIPM SI]: https://www.bipm.org/en/publications/si-brochure
[NIST HB44]:
    https://www.nist.gov/pml/weights-and-measures/publications/nist-handbooks/handbook-44
[JSON Schema Draft-07]:
    https://json-schema.org/draft-07/json-schema-release-notes.html
[JSON Schema Latest]: https://json-schema.org/specification.html