# JSON Schema Validation
C. Vasters (Microsoft) February 2025

## Abstract

This document extends JSON Schema Core by defining validation keywords that
enable precise constraints on numeric values, strings, arrays, objects, and
conditional validations.

This specification covers the semantics, syntax, and evaluation of validation
keywords including numeric validation (`minimum`, `maximum`, `exclusiveMinimum`,
`exclusiveMaximum`, `multipleOf`), string validation (`minLength`, `pattern`),
array validation (`minItems`, `maxItems`, `uniqueItems`, `contains`), and object
validation (`minProperties`, `maxProperties`, `dependencies`,
`patternProperties`, `propertyNames`).

Conditional validations are provided through the extensions of the separate
[JSON Schema Conditional Composition][JSON Schema Conditional Composition]
companion specification.

## Table of Contents

- [JSON Schema Validation](#json-schema-validation)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Conventions](#2-conventions)
  - [3. Validation Keywords](#3-validation-keywords)
    - [3.1. Numeric Validation Keywords](#31-numeric-validation-keywords)
      - [3.1.1. `minimum`](#311-minimum)
      - [3.1.2. `maximum`](#312-maximum)
      - [3.1.3. `exclusiveMinimum`](#313-exclusiveminimum)
      - [3.1.4. `exclusiveMaximum`](#314-exclusivemaximum)
      - [3.1.5. `multipleOf`](#315-multipleof)
    - [3.2. String Validation Keywords](#32-string-validation-keywords)
      - [3.2.1. `minLength`](#321-minlength)
      - [3.2.2. `pattern`](#322-pattern)
    - [3.3. Array and Set Validation Keywords](#33-array-and-set-validation-keywords)
      - [3.3.1. `minItems`](#331-minitems)
      - [3.3.2. `maxItems`](#332-maxitems)
      - [3.3.3. `uniqueItems`](#333-uniqueitems)
      - [3.3.4. `contains`](#334-contains)
      - [3.3.5. `maxContains`](#335-maxcontains)
      - [3.3.6. `minContains`](#336-mincontains)
    - [3.4. Object and Map Validation Keywords](#34-object-and-map-validation-keywords)
      - [3.4.1. `minProperties` and `minEntries`](#341-minproperties-and-minentries)
      - [3.4.2. `maxProperties` and `maxEntries`](#342-maxproperties-and-maxentries)
      - [3.4.3. `dependentRequired`](#343-dependentrequired)
      - [3.4.4. `patternProperties` and `patternKeys`](#344-patternproperties-and-patternkeys)
      - [3.4.5. `propertyNames` and `keyNames`](#345-propertynames-and-keynames)
      - [3.4.6. `has`](#346-has)
  - [4. Implementation Considerations](#4-implementation-considerations)
  - [5. Security Considerations](#5-security-considerations)
  - [6. IANA Considerations](#6-iana-considerations)
  - [7. References](#7-references)
  - [8. Author's Address](#8-authors-address)


## 1. Introduction

The JSON Schema Validation extension provides schema authors with additional
means to constrain instance data. These keywords are applied in conjunction with
the constructs defined in JSON Schema Core. The keywords defined herein include
numeric, string, array, and object validation keywords as well as conditional
validations.

For each keyword, this document specifies its applicability, the permitted value
types or ranges, and the related standards that must be observed.

## 2. Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
NOT", "SHOULD", and "OPTIONAL" in this document are to be interpreted
as described in [RFC2119](#7.1-normative-references) and
[RFC8174](#7.1-normative-references).

## 3. Validation Keywords

### 3.1. Numeric Validation Keywords

This section defines the validation keywords applicable to schemas with numeric
types. The value of each keyword MUST be in the value space of the numeric type
the keyword is applied to.

For schemas with extended numeric types (such as long integers and
decimals) whose base representation is a string, numeric constraint values
(e.g., for `minimum`, `maximum`) MUST be provided as strings.

#### 3.1.1. `minimum`

An instance is valid if its numeric value is greater than or equal to the value
specified in `minimum`.

Example for basic type:

```json
{ "type": "number", "minimum": 10 }
```
Example for extended type:
```json
{ "type": "decimal", "minimum": "10.00" }
```

#### 3.1.2. `maximum`

An instance is valid if its numeric value is less than or equal to the value
specified in `maximum`.

Example for basic type:

```json
{ "type": "number", "maximum": 100 }
```

Example for extended type:

```json
{ "type": "decimal", "maximum": "100.00" }
```

#### 3.1.3. `exclusiveMinimum`

An instance is valid if its numeric value is strictly greater than the value
specified in `exclusiveMinimum`.

Example for basic type:

```json
{ "type": "number", "exclusiveMinimum": 10 }
```

Example for extended type:

```json
{ "type": "int64", "exclusiveMinimum": "10" }
```

#### 3.1.4. `exclusiveMaximum`

An instance is valid if its numeric value is strictly less than the value
specified in `exclusiveMaximum`.

Example for basic type:

```json
{ "type": "number", "exclusiveMaximum": 100 }
```

Example for extended type:

```json
{ "type": "decimal", "exclusiveMaximum": "100.00" }
```

#### 3.1.5. `multipleOf`

An instance is valid if dividing its numeric value by the value of `multipleOf`
results in an integer value. The value of `multipleOf` MUST be a positive number.

Example for basic type:

```json
{ "type": "number", "multipleOf": 5 }
```

Example for extended type:

```json
{ "type": "decimal", "multipleOf": "5" }
```

### 3.2. String Validation Keywords

This section defines the validation keywords applicable to schemas with the type
`string`. The `maxLength` keyword is not included as it is part of JSON Schema
Core and is not redefined here.

#### 3.2.1. `minLength`

A string is valid if its length is at least the integer value specified in
`minLength`. The value of `minLength` MUST be a non-negative integer.

Example:

```json
{ "type": "string", "minLength": 3 }
```

#### 3.2.2. `pattern`

A string is valid if its entire value conforms to the regular expression
provided in the `pattern` keyword. The value of `pattern` MUST be a string
representing a valid regular expression that conforms to the ECMA-262 standard.

Example:

```json
{ "type": "string", "pattern": "^[A-Z][a-z]+$" }
```

### 3.3. Array and Set Validation Keywords

This section defines the validation keywords applicable to schemas with the type
`array` and `set`.

#### 3.3.1. `minItems`

An array or set is valid if its number of elements is at least the integer value
specified in `minItems`. The value of `minItems` MUST be a non-negative integer.

Example:

```json
{ "type": "array", "minItems": 2 }
```

#### 3.3.2. `maxItems`

An array or set is valid if its number of elements does not exceed the integer value
specified in `maxItems`. The value of `maxItems` MUST be a non-negative integer.

Example:

```json
{ "type": "array", "maxItems": 10 }
```

#### 3.3.3. `uniqueItems`

This keyword is only applicable schemas with the type `array` as this constraint
is inherent to `set`. An array is valid if, when `uniqueItems` is set to true,
no two elements are equal. The value of `uniqueItems` MUST be a boolean (either
true or false). 

Example:

```json
{ "type": "array", "uniqueItems": true }
```

#### 3.3.4. `contains`

An array or set is valid if at least one element satisfies the schema specified in
`contains`. The value of `contains` MUST be a valid JSON Schema object.

Example:

```json
{ "type": "array", "contains": { "type": "string" } }
```

The condition schema MAY contain a `const` keyword to specify a fixed value that
the array must contain.

Example:

```json
{ "type": "array", "contains": { "type": "string", "const": "foo" } }
```

#### 3.3.5. `maxContains`

An array or set is valid if at most the number of elements specified in `maxContains`
satisfy the schema specified in `contains`. The value of `maxContains` MUST be a
non-negative integer.

Example:

```json
{ "type": "array", "contains": { "type": "string" }, "maxContains": 2 }
```

#### 3.3.6. `minContains`

An array or set is valid if at least the number of elements specified in `minContains`
satisfy the schema specified in `contains`. The value of `minContains` MUST be a
non-negative integer.

Example:

```json
{ "type": "array", "contains": { "type": "string" }, "minContains": 2 }
```

### 3.4. Object and Map Validation Keywords

This section defines the validation keywords applicable to schemas with the type
`object` and `map`.

#### 3.4.1. `minProperties` and `minEntries`

An object is valid if it has at least as many properties as defined by the
integer value specified in `minProperties`. The value of `minProperties` MUST be
a non-negative integer. The `minEntries` keyword applies to equivalently `map`
types.

Example:

```json
{ "type": "object", "minProperties": 1 }
```

This constraint is useful for `object` definitions that use dynamic properties
via `additionalProperties` and `patternProperties`.

#### 3.4.2. `maxProperties` and `maxEntries`

An object is valid if it contains no more than the integer value specified in
`maxProperties`. The value of `maxProperties` MUST be a non-negative integer.
The `maxEntries` keyword applies to equivalently `map` types.

Example:

```json
{ "type": "object", "maxProperties": 5 }
```

#### 3.4.3. `dependentRequired`

This keyword establishes dependencies between object properties. The value is a
`map` of arrays of strings. Each entry in the map corresponds to a property name
in the object instance. If the property exists, then the properties listed in
the corresponding array MUST also exist in the instance. This keyword does not
apply to the `map` type.

Example:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "credit_card": { "type": "number" },
    "billing_address": { "type": "string" }
  },
  "dependencies": {
    "credit_card": ["billing_address"]
  },
  "required": ["name"]
}
```

#### 3.4.4. `patternProperties` and `patternKeys`

This keyword applies schemas to properties whose names match specified regular
expressions. For each property in the object instance, if its name matches a
regular expression defined in `patternProperties`, then its value MUST validate
against the corresponding schema. The property names used as keys in
`patternProperties` MUST be strings representing valid regular expressions
conforming to the ECMA-262 standard. The `patternKeys` keyword applies to
equivalently `map` types.

Example:

```json
{
  "type": "object",
  "patternProperties": {
    "^[A-Z]": { "type": "string" }
  }
}
```

> Note: All identifiers are additionally subject to the constraints of the
> identifier syntax in [JSON Schema Core][JSON Schema Core].

#### 3.4.5. `propertyNames` and `keyNames`

The `propertyNames` keyword validates the names of all properties in an object
against a `string` typed schema. An object is valid if every property name in
the object is valid. The schema MUST be of type `string`. The `keyNames` keyword
applies to equivalently `map` types.

Example:

```json
{
  "type": "object",
  "propertyNames": { "type": "string", "pattern": "^[a-z][a-zA-Z0-9]*$" }
}
```

#### 3.4.6. `has`

The `has` keyword validates that an object or map has at least one (property)
value that matches the schema. The schema MUST be of type `object`.

Example:

```json
{
  "type": "object",
  "has": { "type": "string" }
}
```

## 4. Implementation Considerations

Validators shall process each validation keyword independently and combine
results using a logical AND conjunction. Regular expression evaluation for
`pattern`, `patternProperties`, and `propertyNames` MUST conform to the
ECMAScript Language Specification (ECMA-262). 

## 5. Security Considerations

Complex regular expressions specified in `pattern`, `patternProperties`, and
`propertyNames` may lead to performance issues (e.g., ReDoS). Implementations
should mitigate such risks. Overly complex or deeply nested validation
constructs may impact performance and should be optimized.

## 6. IANA Considerations

This document does not require any IANA actions.

## 7. References

- [RFC2119] Bradner, S., “Key words for use in RFCs to Indicate Requirement
  Levels”, RFC 2119.
- [RFC8174] Leiba, B., “Ambiguity of Uppercase vs Lowercase in RFC 2119 Key
  Words”, RFC 8174.
- [JSON Schema Core] C. Vasters, “JSON Schema Core”, February 2025.
- [ECMA-262] ECMAScript Language Specification, ECMA International.

## 8. Author's Address

**Clemens Vasters**
Microsoft
Email: clemensv@microsoft.com