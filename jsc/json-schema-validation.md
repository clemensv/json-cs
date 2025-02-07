# JSON Schema Validation  
C. Vasters (Microsoft) February 2025

## Abstract

This document extends JSON Schema Core by defining additional validation
keywords that enable precise constraints on numeric values, strings, arrays,
objects, and conditional validations. This specification covers the semantics,
syntax, and evaluation of validation keywords including numeric validation
(`minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`, `multipleOf`),
string validation (`minLength`, `pattern`), array validation (`minItems`,
`maxItems`, `uniqueItems`, `contains`), object validation (`minProperties`,
`maxProperties`, `dependencies`, `patternProperties`, `propertyNames`), and
conditional validation (`if`, `then`, `else`, `not`). For each keyword, this
document specifies its applicability, the permitted value types or ranges, and
the related standards that must be observed. For schemas with extended numeric
types (such as long integers and decimals) whose base representation is a
string, numeric constraint values (e.g., for `minimum`, `maximum`) MUST be
provided as strings.

## Table of Contents

- [JSON Schema Validation](#json-schema-validation)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Validation Keywords](#2-validation-keywords)
    - [2.1. Numeric Validation Keywords](#21-numeric-validation-keywords)
      - [2.1.1. `minimum`](#211-minimum)
      - [2.1.2. `maximum`](#212-maximum)
      - [2.1.3. `exclusiveMinimum`](#213-exclusiveminimum)
      - [2.1.4. `exclusiveMaximum`](#214-exclusivemaximum)
      - [2.1.5. `multipleOf`](#215-multipleof)
    - [2.2. String Validation Keywords](#22-string-validation-keywords)
      - [2.2.1. `minLength`](#221-minlength)
      - [2.2.2. `pattern`](#222-pattern)
    - [2.3. Array Validation Keywords](#23-array-validation-keywords)
      - [2.3.1. `minItems`](#231-minitems)
      - [2.3.2. `maxItems`](#232-maxitems)
      - [2.3.3. `uniqueItems`](#233-uniqueitems)
      - [2.3.4. `contains`](#234-contains)
    - [2.4. Object Validation Keywords](#24-object-validation-keywords)
      - [2.4.1. `minProperties`](#241-minproperties)
      - [2.4.2. `maxProperties`](#242-maxproperties)
      - [2.4.3. `dependencies`](#243-dependencies)
      - [2.4.4. `patternProperties`](#244-patternproperties)
      - [2.4.5. `propertyNames`](#245-propertynames)
    - [2.5. Conditional and Negation Keywords](#25-conditional-and-negation-keywords)
      - [2.5.1. `if`, `then`, `else`](#251-if-then-else)
      - [2.5.2. `not`](#252-not)
  - [3. Interaction with JSON Schema Core](#3-interaction-with-json-schema-core)
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
validations. Each keyword description below details its purpose, applicability,
permitted values or ranges, and any related standards. For schemas with extended
numeric types (such as `int64`, `uint64`, `int128`, `uint128`, `decimal`),
constraint values are expressed as strings to preserve precision.

## 2. Validation Keywords

### 2.1. Numeric Validation Keywords

#### 2.1.1. `minimum`  
This keyword is applicable to schemas whose type is one of the numeric types.
For basic numeric types (e.g., `number`, `integer`, `float`, `double`), the
value of `minimum` MUST be a JSON number. For extended numeric types (e.g.,
`int64`, `uint64`, `int128`, `uint128`, `decimal`), the value of `minimum` MUST
be a JSON string representing the numeric value in its canonical form. An
instance is valid if its numeric value is greater than or equal to the value
specified in `minimum`. When used with the `number` type, the value SHOULD conform
to IEEE 754 double-precision representation.  
Example for basic type:
```json
{ "type": "number", "minimum": 10 }
```
Example for extended type:
```json
{ "type": "decimal", "minimum": "10.00" }
```

#### 2.1.2. `maximum`  
This keyword is applicable to schemas whose type is one of the numeric types.
For basic numeric types, the value of `maximum` MUST be a JSON number; for
extended numeric types, the value MUST be a JSON string representing the numeric
upper bound in canonical form. An instance is valid if its numeric value is less
than or equal to the value specified in `maximum`. When used with the `number`
type, the value SHOULD adhere to IEEE 754 double-precision constraints.  
Example for basic type:
```json
{ "type": "number", "maximum": 100 }
```
Example for extended type:
```json
{ "type": "decimal", "maximum": "100.00" }
```

#### 2.1.3. `exclusiveMinimum`  
This keyword is applicable to schemas with a numeric type. For basic numeric
types, the value of `exclusiveMinimum` MUST be a JSON number; for extended
numeric types, it MUST be a JSON string representing the strict lower bound. An
instance is valid if its numeric value is strictly greater than the value
specified in `exclusiveMinimum`. The value MUST conform to the representation
requirements of the underlying numeric type.  
Example for basic type:
```json
{ "type": "number", "exclusiveMinimum": 10 }
```
Example for extended type:
```json
{ "type": "int64", "exclusiveMinimum": "10" }
```

#### 2.1.4. `exclusiveMaximum`  
This keyword is applicable to schemas with a numeric type. For basic numeric
types, the value of `exclusiveMaximum` MUST be a JSON number; for extended
numeric types, it MUST be a JSON string representing the strict upper bound. An
instance is valid if its numeric value is strictly less than the value specified
in `exclusiveMaximum`. When applied to the `number` type, the value MUST observe
IEEE 754 double-precision constraints.  
Example for basic type:
```json
{ "type": "number", "exclusiveMaximum": 100 }
```
Example for extended type:
```json
{ "type": "decimal", "exclusiveMaximum": "100.00" }
```

#### 2.1.5. `multipleOf`  
This keyword is applicable to schemas with a numeric type. For basic numeric
types, the value of `multipleOf` MUST be a JSON number greater than zero; for
extended numeric types, the value MUST be a JSON string representing a positive
number. An instance is valid if dividing its numeric value by the value of
`multipleOf` results in an integer. For basic numeric types, the value SHOULD be
representable under IEEE 754 constraints.  
Example for basic type:
```json
{ "type": "number", "multipleOf": 5 }
```
Example for extended type:
```json
{ "type": "decimal", "multipleOf": "5" }
```

### 2.2. String Validation Keywords

#### 2.2.1. `minLength`  
This keyword is applicable exclusively to schemas with the type `string`. It
specifies the minimum number of characters required in a string instance. A
string is valid if its length is at least the integer value specified in
`minLength`. The value of `minLength` MUST be a non-negative integer.  
Example:
```json
{ "type": "string", "minLength": 3 }
```

#### 2.2.2. `pattern`  
This keyword is applicable exclusively to schemas with the type `string`. It
constrains a string instance to match a specified regular expression pattern. A
string is valid if the entire string conforms to the regular expression provided
in the `pattern` keyword. The value of `pattern` MUST be a string representing a
valid regular expression that conforms to the ECMA-262 standard.  
Example:
```json
{ "type": "string", "pattern": "^[A-Z][a-z]+$" }
```

### 2.3. Array Validation Keywords

#### 2.3.1. `minItems`  
This keyword is applicable exclusively to schemas with the type `array`. It
specifies the minimum number of elements required in an array instance. An array
is valid if its number of elements is at least the integer value specified in
`minItems`. The value of `minItems` MUST be a non-negative integer.  
Example:
```json
{ "type": "array", "minItems": 2 }
```

#### 2.3.2. `maxItems`  
This keyword is applicable exclusively to schemas with the type `array`. It
specifies the maximum number of elements permitted in an array instance. An
array is valid if its number of elements does not exceed the integer value
specified in `maxItems`. The value of `maxItems` MUST be a non-negative integer.  
Example:
```json
{ "type": "array", "maxItems": 10 }
```

#### 2.3.3. `uniqueItems`  
This keyword is applicable exclusively to schemas with the type `array`. It
enforces that all elements in the array are unique. An array is valid if, when
`uniqueItems` is set to true, no two elements are equal. The value of `uniqueItems`
MUST be a boolean (either true or false).  
Example:
```json
{ "type": "array", "uniqueItems": true }
```

#### 2.3.4. `contains`  
This keyword is applicable exclusively to schemas with the type `array`. It
requires that at least one element in the array instance satisfies the specified
schema provided as the value of `contains`. The value of `contains` MUST be a valid
JSON Schema object.  
Example:
```json
{ "type": "array", "contains": { "type": "string" } }
```

### 2.4. Object Validation Keywords

#### 2.4.1. `minProperties`  
This keyword is applicable exclusively to schemas with the type `object`. It
specifies the minimum number of properties that an object instance must contain.
An object is valid if it has at least the integer value specified in
`minProperties`. The value of `minProperties` MUST be a non-negative integer.  
Example:
```json
{ "type": "object", "minProperties": 1 }
```

#### 2.4.2. `maxProperties`  
This keyword is applicable exclusively to schemas with the type `object`. It
specifies the maximum number of properties that an object instance may contain.
An object is valid if it contains no more than the integer value specified in
`maxProperties`. The value of `maxProperties` MUST be a non-negative integer.  
Example:
```json
{ "type": "object", "maxProperties": 5 }
```

#### 2.4.3. `dependencies`  
This keyword is applicable exclusively to schemas with the type `object`. It
establishes dependencies between properties. For each property specified in
`dependencies`, if that property exists in the instance, then:  
- If the dependency is an array, each property name listed in that array MUST
  also exist in the instance. The array value MUST consist solely of strings
  that conform to the identifier rules defined in JSON Schema Core.  
- If the dependency is a schema, the instance MUST validate against that schema.  
Examples:  
Property Dependency:
```json
{
  "type": "object",
  "dependencies": {
    "credit_card": ["billing_address"]
  }
}
```  
Schema Dependency:
```json
{
  "type": "object",
  "dependencies": {
    "credit_card": { "type": "object", "properties": { "billing_address": { "type": "string" } } }
  }
}
```

#### 2.4.4. `patternProperties`  
This keyword is applicable exclusively to schemas with the type `object`. It
applies schemas to properties whose names match specified regular expressions.
For each property in the object instance, if its name matches a regular
expression defined in `patternProperties`, then its value MUST validate against
the corresponding schema. The property names used as keys in `patternProperties`
MUST be strings representing valid regular expressions conforming to the
ECMA-262 standard.  
Example:
```json
{
  "type": "object",
  "patternProperties": {
    "^[A-Z]": { "type": "string" }
  }
}
```

#### 2.4.5. `propertyNames`  
This keyword is applicable exclusively to schemas with the type `object`. It
validates the names of all properties in an object against a specified schema.
An object is valid if every property name in the instance validates against the
schema provided in `propertyNames`. The value of `propertyNames` MUST be a valid
JSON Schema object, and when using patterns, the regular expression must conform
to the ECMA-262 standard.  
Example:
```json
{
  "type": "object",
  "propertyNames": { "pattern": "^[a-z][a-zA-Z0-9]*$" }
}
```

### 2.5. Conditional and Negation Keywords

#### 2.5.1. `if`, `then`, `else`  
These keywords are applicable to any schema, regardless of its type. They enable
conditional validation logic. The `if` keyword specifies a schema used to test
the instance. In order to be valid per JSON Schema Core, each of the schema
expressions in `if`, `then`, and `else` MUST declare the applicable type. For
example, when applying conditional logic to object instances, the subschemas
MUST declare `"type": "object"`. An instance that validates against the schema
in `if` MUST also validate against the schema in `then` (if present).
Conversely, if the instance does not validate against the schema in `if`, it
MUST validate against the schema in `else` (if present).  
Example:
```json
{
  "if": { "type": "object", "properties": { "country": { "const": "USA" } } },
  "then": { "type": "object", "required": ["postal_code"] },
  "else": { "type": "object", "required": ["postal_code", "province"] }
}
```

#### 2.5.2. `not`  
This keyword is applicable to any schema, regardless of its type. It inverts the
validation outcome of the provided schema. An instance is valid if and only if
it does not validate against the schema defined in `not`. The value of `not`
MUST be a valid JSON Schema object.  
Example:
```json
{ "not": { "type": "null" } }
```

## 3. Interaction with JSON Schema Core

All validation keywords defined in this document shall be applied in addition to
the constraints specified in JSON Schema Core. When multiple validation keywords
are present, an instance must satisfy all applicable constraints to be
considered valid. Conditional keywords (`if`, `then`, `else`) are evaluated
after non-conditional validations. The evaluation of `not` is performed last,
ensuring that the instance does not match the negated schema.

## 4. Implementation Considerations

Validators shall process each validation keyword independently and combine
results using logical conjunction. Regular expression evaluation for `pattern`,
`patternProperties`, and `propertyNames` SHALL conform to the ECMAScript
Language Specification (ECMA-262). Numeric validations for basic types SHALL
account for floating-point precision in accordance with IEEE 754, and for
extended numeric types, constraint values SHALL be interpreted as precise string
representations.

## 5. Security Considerations

Complex regular expressions specified in `pattern`, `patternProperties`, and
`propertyNames` may lead to performance issues (e.g., ReDoS). Implementations
should mitigate such risks. Overly complex or deeply nested validation
constructs may impact performance and should be optimized. Conditional
validations should be designed to avoid ambiguous or conflicting validation
paths.

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