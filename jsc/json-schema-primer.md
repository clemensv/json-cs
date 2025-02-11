# JSON Schema Core Primer

This primer introduces JSON Schema Core, a modern, strictly typed schema
language that builds on familiar JSON Schema concepts from prior drafts, but has
been entirely refactored.

The new JSON Schema focuses on defining data types with clear, deterministic
constraints while supporting extensions for precise representations of numbers,
dates, and more. 

Conditional validation of JSON data against schemas with composition constructs
like `anyOf` or `allOf` has been split out into optional extensions, allowing
simple data definitions to remain lightweight and easy to understand.

Common programming language concepts like reuse and composition are supported
directly in the schema language without dragging in the entire complexity of
object-oriented programming.

## Table of Contents

- [JSON Schema Core Primer](#json-schema-core-primer)
  - [Table of Contents](#table-of-contents)
  - [Key Concepts](#key-concepts)
  - [Using Schema Core](#using-schema-core)
    - [Example: Defining a simple object type](#example-defining-a-simple-object-type)
    - [Example: Defining Primitive and Extended Types](#example-defining-primitive-and-extended-types)
    - [Example: Defining reusable types in `$defs`](#example-defining-reusable-types-in-defs)
    - [Example: Structuring types with namespaces](#example-structuring-types-with-namespaces)
    - [Example: Using an Array Type](#example-using-an-array-type)
    - [Example: Declaring Maps](#example-declaring-maps)
    - [Example: Declaring Sets](#example-declaring-sets)
  - [Using Companion Specifications](#using-companion-specifications)
    - [Example: Using the `altnames` Keyword](#example-using-the-altnames-keyword)
    - [Example: Using the `altenums` Keyword](#example-using-the-altenums-keyword)
    - [Example: Using the `unit` Keyword](#example-using-the-unit-keyword)
    - [Example: Using the `currency` Keyword](#example-using-the-currency-keyword)
  - [Using Validation](#using-validation)
    - [Example: Using Conditional Composition](#example-using-conditional-composition)
    - [Example: Using Validation Rules](#example-using-validation-rules)

## Key Concepts

The new JSON Schema Core is designed to look and feel very much like the JSON
Schema you already know, but somes rules have been tightened up to make it easier
to understand and use. Therefore, existing JSON Schema documents may need to be
updated to conform to the new rules.

- **Strict Typing:** Every schema must clearly specify the data type. For
  compound types (objects, arrays, sets), additional required metadata like a
  name and required property definitions help enforce structured data.
- **Extended Types:** In addition to JSON primitives such as string, number,
  boolean, and null, JSON Schema Core supports many extended primitive types
  (e.g., `int32`, `int64`, `decimal`, `date`, `uuid`) for high precision or
  format-specific data.
- **Compound Types:** The compound types have been extended to include `set` and `map`.
    - **Object:** Define structured data with a required `name` and a set of
      `properties`.
    - **Array:** List of items where the `items` attribute references a declared
      type without inline compound definitions.
    - **Set:** An unordered collection of unique elements.
    - **Map:** A collection of key-value pairs where keys are strings and values
      are of a declared type.
- **Namespaces:** Namespaces are a formal part of the schema language, allowing
  for more modular and deterministic schema definitions. Namespaces are used to
  scope type definitions.
- **Cross-Referencing:** The `$ref` keyword has been limited to referencing
  named types that exist within the same document. It can no longer reference
  and insert arbitrary JSON nodes and it can no longer reference external
  documents. To use types from other documents, you now need to use the
  `$import` keyword to import the types you need and then reference them.


## Using Schema Core 


### Example: Defining a simple object type

Here is an example of a simple object type definition:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
    "type": "object",
    "name": "Person",
    "properties": {
        "firstName": { "type": "string" },
        "lastName": { "type": "string" },
        "dateOfBirth": { "type": "date" }
    },
    "required": ["firstName", "lastName"]
}
```

If you are familiar with JSON Schema, you will instantly recognize the structure
of this schema. The `type` attribute specifies that this is an object type. The
`properties` attribute lists the properties of the object, and the `required`
attribute lists the properties that are required.

There are a few differences from prior version of JSON Schema. The `name`
attribute is new and is required for the root type. The `type` attribute is also
required and no longer implied to be `object` if not present. You may also
notice that the "dateOfBirth" property uses the new `date` type, which is an
extended native type.

### Example: Defining Primitive and Extended Types

Below is an example schema that defines a simple profile with a few more extended
types:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
    "type": "object",
    "name": "UserProfile",
    "properties": {
        "username": { "type": "string" },
        "dateOfBirth": { "type": "date" },
        "lastSeen": { "type": "datetime" },
        "score": { "type": "int64" },
        "balance": { "type": "decimal", "precision": 20, "scale": 2 },
        "isActive": { "type": "boolean" }
    },
    "required": ["username", "birthdate"]
}
```

The `int64` type is an extended type that represents a 64-bit signed integer.
The `decimal` type is another extended type that represents a decimal number
with a specified precision and scale. The `datetime` type is an extended type
that represents a date and time value.

### Example: Defining reusable types in `$defs`

To define reusable types, you can use the `$defs` keyword to define types that
can be referenced by other types in the same document. Here is an example:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
    "type": "object",
    "name": "UserProfile",
    "properties": {
        "username": { "type": "string" },
        "dateOfBirth": { "type": "date" },
        "lastSeen": { "type": "datetime" },
        "score": { "type": "int64" },
        "balance": { "type": "decimal", "precision": 20, "scale": 2 },
        "isActive": { "type": "boolean" },
        "address": { "type" : { "$ref": "#/$defs/Address" } }
    },
    "required": ["username", "birthdate"],
    "$defs": {
        "Address": {
            "type": "object",
            "properties": {
                "street": { "type": "string" },
                "city": { "type": "string" },
                "state": { "type": "string" },
                "zip": { "type": "string" }
            },
            "required": ["street", "city", "state", "zip"]
        }
    }
}
```

In this example, the `Address` type is defined in the `$defs` section and can be
referenced by other types in the same document using the `$ref` keyword. Mind
that the `$ref` keyword can now only reference types defined in the `$defs`
section of the same document. The keyword can only be used where a type is
expected.

### Example: Structuring types with namespaces

Namespaces are used to scope type definitions. Here is an example of how to use
namespaces to structure your types, with two differing `Address` types:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
    "type": "object",
    "name": "UserProfile",
    "properties": {
        "username": { "type": "string" },
        "dateOfBirth": { "type": "date" },
        "networkAddress": { "type" : { "$ref": "#/$defs/Network/Address" } },
        "physicalAddress": { "type": { "$ref": "#/$defs/Physical/Address" } }
    },
    "required": ["username", "birthdate"],
    "$defs": {
        "Network": {
            "Address": {
                "type": "object",
                "properties": {
                    "ipv4": { "type": "string" },
                    "ipv6": { "type": "string" }
                }
            }
        },
        "Physical": {
            "Address": {
                "type": "object",
                "properties": {
                    "street": { "type": "string" },
                    "city": { "type": "string" },
                    "state": { "type": "string" },
                    "zip": { "type": "string" }
                },
                "required": ["street", "city", "state", "zip"]
            }
        }
    }
}
```

### Example: Using an Array Type

This example shows how to define an array of strings, which is not much different
from defining an object:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
    "type": "array",
    "items": { "type": "string" }
}
```

What's new is that you can no longer define a compound type inline inside the `items`
attribute. Instead, you must define the type separately and reference it by name:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
    "type": "array",
    "items": { "type" : { "$ref": "#/$defs/Person" } },
    "$defs": {
        "Person" {
            "type": "object",
            "name": "Person",
            "properties": {
                "firstName": { "type": "string" },
                "lastName": { "type": "string" },
                "dateOfBirth": { "type": "date" }
            },
            "required": ["firstName", "lastName"]
        }
    }
}
```

### Example: Declaring Maps

This example shows how to define a map of strings to `Color` objects:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
    "type": "map",
    "values": { "type": { "$ref": "#/$defs/Color" } },
    "$defs": {
        "Color" {
            "type": "object",
            "name": "Color",
            "properties": {
                "red": { "type": "int32" },
                "green": { "type": "int32" },
                "blue": { "type": "int32" }
            },
            "required": ["red", "green", "blue"]
        }
    }
}
``` 

Instance data for this schema might look like this:

```json
{
    "rose": { "red": 255, "green": 0, "blue": 0 },
    "sky": { "red": 0, "green": 191, "blue": 255 },
    "grass": { "red": 0, "green": 128, "blue": 0 },
    "sun": { "red": 255, "green": 215, "blue": 0 },
    "cloud": { "red": 255, "green": 255, "blue": 255 },
    "moon": { "red": 192, "green": 192, "blue": 192 }
}
```

### Example: Declaring Sets

This example shows how to define a set of strings:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
    "type": "set",
    "items": { "type": "string" }
}
```

Sets differ from arrays in that they are unordered and contain only unique
elements. The schema above would match the following instance data:

```json
["apple", "banana", "cherry"]
```

## Using Companion Specifications

The JSON Schema Core specification is designed to be extensible through companion
specifications that provide additional features and capabilities. 

The full schema that includes all companion specifications is identified by the
`https://schemas.vasters.com/experimental/json-schema/v0` URI. Each companion
specification is identified by a unique identifier that can be used in the `$uses`
attribute to activate the companion specification for the schema document.

The feature identifiers for the companion specifications are:
- `Altnames`: Alternate names and descriptions for properties and types.
- `Units`: Symbols, scientific units, and currencies for numeric properties.
- `Conditionals`: Conditional composition and validation rules.
- `Imports`: Importing types from other schema documents.
- `Validation`: Validation rules for JSON data.

### Example: Using the `altnames` Keyword

The [JSON Schema Alternate Names and Descriptions](./json-schema-altnames.md) companion
specification introduces the `altnames` keyword to provide alternate names for
properties and types. Alternate names provide additional mappings that schema
processors may use for encoding, decoding, or user interface display.

Here is an example of how to use the `altnames` keyword:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-schema/v0",
    "$uses": ["Altnames"],
    "Person": {
        "type": "object",
        "altnames": {
            "json": "person_data",
            "lang:en": "Person",
            "lang:de": "Person"
        },
        "properties": {
            "firstName": {
                "type": "string",
                "altnames": {
                    "json": "first_name",
                    "lang:en": "First Name",
                    "lang:de": "Vorname"
                }
            },
            "lastName": {
                "type": "string",
                "altnames": {
                    "json": "last_name",
                    "lang:en": "Last Name",
                    "lang:de": "Nachname"
                }
            }
        },
        "required": ["firstName", "lastName"]
    }
}
```

Each named type or property in the schema has been given an `altnames` attribute
that provides alternate names for the type or property. 

The `json` key is used to specify alternate names for JSON encoding, meaning that if
the schema is used to encode or decode JSON data, the alternate key MUST be used
instead of the name in the schema.

Keys beginning with `lang:` are reserved for providing localized alternate names that
can be used for user interface display. Additional keys can be used for custom
purposes, subject to no conflicts with reserved keys or prefixes.

### Example: Using the `altenums` Keyword

The [JSON Schema Alternate Enumerations](./json-schema-altenums.md) companion
specification introduces the `altenums` keyword to provide alternative
representations for enumeration values defined by a type using the `enum`
keyword. Alternate symbols allow schema authors to map internal enum values to
external codes or localized display symbols.

Here is an example of how to use the `altenums` keyword:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-schema/v0",
    "$uses": ["Altnames"],
    "type": "object",
    "name": "Color",
    "properties": {
        "name": { "type": "string" },
        "value": { 
            "type": "string", 
            "enum": ["red", "green", "blue"],
            "altenums": {
                "lang:en": {
                    "red": "Red",
                    "green": "Green",
                    "blue": "Blue"
                },
                "lang:de": {
                    "red": "Rot",
                    "green": "Grün",
                    "blue": "Blau"
                }
            }
        }
    }
}
```

In this example, the `value` property has an `enum` attribute that defines the
possible values for the property. The `altenums` attribute provides alternative
names for each enumeration value. The `lang:en` key provides English names for
the enumeration values, and the `lang:de` key provides German names.

### Example: Using the `unit` Keyword

The [JSON Schema Symbols, Scientific Units, and Currencies](./json-schema-unit.md)
companion specification introduces the `unit` keyword to provide a standard way
to specify the unit of measurement for numeric properties. The `unit` keyword
allows schema authors to specify the unit of measurement for numeric properties
and provides a standard way to encode and decode numeric values with units.

Here is an example of how to use the `unit` keyword:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-schema/v0",
    "$uses": ["Units"],
    "type": "object",
    "name": "Pressure",
    "properties": {
        "value": { "type": "number", "unit": "Pa" }
    }
}
```

In this example, the `value` property has a `unit` attribute that specifies the
unit of measurement for the property. The unit of measurement is specified as a
string value. In this case, the unit of measurement is "Pa" for Pascals.

### Example: Using the `currency` Keyword

The [JSON Schema Symbols, Scientific Units, and Currencies](./json-schema-unit.md)
companion specification also introduces the `currency` keyword to provide a
standard way to specify the currency for monetary properties. The `currency`
keyword allows schema authors to specify the currency for monetary properties and
provides a standard way to encode and decode monetary values with currencies.

Here is an example of how to use the `currency` keyword:

```json
{
    "$schema": "https://schemas.vasters.com/experimental/json-schema/v0",
    "$uses": ["Units"],
    "type": "object",
    "name": "Price",
    "properties": {
        "value": { "type": "decimal", "precision": 20, "scale": 2, "currency": "USD" }
    }
}
```

In this example, the `value` property has a `currency` attribute that specifies
the currency for the property. The currency is specified as a string value. In
this case, the currency is "USD" for US Dollars.

## Using Validation

The companion specifications for conditional composition and validation provide
additional constructs for defining conditional validation rules and composing
that resemble those found in prior versions of JSON Schema. However, those have 
been split out into optional extensions to keep the core schema language simple.

### Example: Using Conditional Composition

The [JSON Schema Conditionals](./json-schema-conditional-composition.md) companion
specification introduces conditional composition constructs for combining multiple
schema definitions. In particular, this specification defines the semantics,
syntax, and constraints for the keywords `allOf`, `anyOf`, `oneOf`, and `not`,
as well as the `if`/`then`/`else` conditional construct.

The specification has several examples that show how to use the conditional
composition keywords.

### Example: Using Validation Rules

The [JSON Schema Validation](./json-schema-validation.md) companion specification
introduces additional validation rules for JSON data. 