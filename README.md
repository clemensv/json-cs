# JSON Compact Schema (JSON-CS)

Author: Clemens Vasters, Microsoft Corporation, clemensv@microsoft.com

**JSON Compact Schema** (JSON-CS) is a compact schema language for the JSON data
format. JSON-CS also aims to be a schema definition language that can be used to
define data structures abstractly and share them across programs, databases,
messaging systems, and REST APIs.

The specification document can be found [here](json-cs.md).

- [JSON Compact Schema (JSON-CS)](#json-compact-schema-json-cs)
  - [Status](#status)
  - [Motivation](#motivation)
  - [Goals](#goals)
  - [Examples](#examples)
    - [Example 1: Basic Type Definition](#example-1-basic-type-definition)
    - [Example 2: Reusing JSON Schema Definitions](#example-2-reusing-json-schema-definitions)
    - [Example 4: Using Alternate Names for Encodings](#example-4-using-alternate-names-for-encodings)
    - [Example 5: Using Units of Measure](#example-5-using-units-of-measure)
    - [Example 6: Better Documentation with Examples](#example-6-better-documentation-with-examples)
    - [Example 7: Using Namespaces](#example-7-using-namespaces)
    - [Example 8: Declaring the root type of a document](#example-8-declaring-the-root-type-of-a-document)
    - [Example 9: Sharing Definitions with Restricted Polymorphism](#example-9-sharing-definitions-with-restricted-polymorphism)
    - [Example 11: Disambiguating Type Unions with Discriminators](#example-11-disambiguating-type-unions-with-discriminators)
  - [Full Specification](#full-specification)

## Status

This is an experimental specification for discussion.

## Motivation

JSON-CS schema documents quite intentionally resemble [JSON
Schema](https://json-schema.org/), and there is a [compatibility mapping](spec/json-cs.md#5-compatibility-with-json-schema-drafts) between
JSON-CS and JSON Schema, but otherwise this is separate effort.

While JSON Schema is popular and widely used, its composition model is
enormously complex. It's possible to write simple looking JSON Schemas that
define data structures that are nearly impossible to implement consistently in
common programming languages or databases.

The example below shows a valid Draft-07 JSON Schema that looks innocuous at
first glance, but illustrates some of the issues:

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type" : "object",
    "properties" : {
      "1st Option": { "type" : "string" },
      "2nd Option": {
        "oneOf" : [
          {"$ref": "#/definitions/TypeA" },
	  	    {"$ref": "#/definitions/TypeB" },
          {
            "type" : "object",
            "patternProperties" : {
              "^prop-[a-z]+$" : { "type" : "string" }
            } 
          }
        ]
      },
      "3rd Option": { 
        "type" : "object",
        "properties" : {
              "prop-d" : { "type" : "string" }
            },
        "allOf" : [
          {"$ref": "#/definitions/TypeA" },
          {"$ref": "#/definitions/TypeC" }
        ]
      }
    },
    "definitions": {
        "TypeA": {
            "type": "object",
            "properties": {
                "prop-a": { "type": ["string", "integer"], "enum": ["foo", 42] },
                "prop-b": { "$ref": "#/definitions/TypeA" }
            },
            "anyOf": [ { "required": ["prop-a"] }, { "required": ["prop-b"] } ]            
        },
        "TypeB": {
            "type": "object",
            "properties": {
                "prop-a": { "type": "boolean"},
                "prop-b": { "$ref": "#/definitions/TypeA" }
            },
            "allOf": [ { "required": ["prop-a"] }, { "required": ["prop-b"] } ]            
        },
        "TypeC": {
            "type": "object",
            "properties": {
                "prop-c": { "type": "string"}
            }
        }
    }  
}
```

Some issues:

  - Property names start with numbers, contain whitespace (`1st Option`) or '-'
    characters (`prop-a`), all of which are not allowed in identifiers of many
    programming languages and therefore require some form of name mangling.
  - The `2nd Option` property is defined as an object that can be either of two
    types, `TypeA` or `TypeB`, or an object with properties whose names match a
    regular expression. While this may look like a type union, it's really not.
    The rule is that the object must either match the definition of `TypeA` or
    `TypeB` or have properties that match the regular expression and are of
    string type. But if "prop-a" from `TypeA` is present (a string), then
    "prop-b" must also be present and be an object that matches `TypeA`, because
    `{ "prop-a": "foo" }` matches both `TypeA` and the regular expression and
    then violates the `oneOf` rule. It's therefore a matching expression and
    cannot be expresses as a type union definition.
  - The `3rd Option` property is defined as an object that must match all of
    `TypeA`, `TypeC`, and may have an optional property `prop-d`. While that is
    very easily expressed in JSON Schema, it's fairly difficult to map to a
    programming language or database because the types are distinctly defined
    and used in other contexts, but are merged into a single definition in this
    type instance. With a single `allOf` rule entry, this is often used to model
    type-inheritance in JSON Schema, but the pattern breaks with multiple
    entries for languages that do not support multiple inheritance.
  - The `prop-a` property of `TypeA` is defined as a string or integer that must
    be either "foo" or 42. JSON Schema does permit mixing values of different
    types in an `enum` list that accompanies a type union and this feature is
    indeed used "in the wild", but this is quite tricky to map to most
    programming language's type systems.
  - The `anyOf` clause in `TypeA` is used to define that either `prop-a` or
    `prop-b` or both (!) must be present. The `allOf` clause in `TypeB` is used
    to define that both `prop-a` and `prop-b` must be present. However, this is
    achieved through composition of multiple `required` clauses, which is not a
    feature of most programming languages.
    

If you believe these issues are contrived, browsing
[schemastore.org](https://www.schemastore.org/json/) will hopefully convince you
otherwise. The ["JFrog Pipeline"
schema](https://json.schemastore.org/jfrog-pipelines.json) is a good example of
a schema whose types are very difficult to map to a programming language.

If you say "well, that's just a terribly complicated schema", then you're
absolutely correct.

JSON Schema allows you to write terribly complicated schemas and all tools that
try to map JSON Schema to programming language data structures or to database
tables simply throw up their hands and give up at some point of complexity. None
of them agree on where that point is and it's impossible for you to know ahead
of time whether a schema you write will work with a given toolchain unless you
limit yourself to a very small subset of JSON Schema.

JSON-CS aims to make it easier to write schemas that can be consistently
implemented in programming languages and databases and to put constraints in
place that don't leave the author guessing whether a schema can indeed be used
to describe data structures that can be used across a variety of tools.

A further motivation for JSON-CS is that the JSON Schema specifications are
written such that they need an extra documentation website to explain them to
practitioners. The JSON-CS specification is one self-contained document that
aims to be concrete and understandable to practitioners.

## Goals

A key design goal for JSON-CS is that schemas should look familiar and be
instantly understandable to someone who knows JSON Schema. 

However, the goal is not to be a replacement for JSON Schema, but to be a
simpler, far more constrained schema language that can describe data structures
that are expressible in JSON and that can be easily mapped to and from
programming language data structures and database tables. 

As such, it is not a goal to provide composition and validation features that
can cover all imaginable complexities that may occur in JSON documents. 

JSON-CS is not a subset of JSON Schema. JSON-CS puts substantial constraints on
definitions and adds a number of important features that are not present in JSON
Schema and that aim to improve the quality of the metadata that can be expressed
in a schema:

- **Strict Typing**: JSON-CS requires explicit type declarations for each
  object property.
- **Strict Naming**: JSON-CS imposes strict naming rules for properties and
  types that aim to be compatible with programming languages and databases. Also,
  the naming and namespace rules ensure that each declared type has a unique
  name.
- **Self-Contained**: JSON-CS schemas must be self-contained and do not allow
  external references to other schemas.
- **Modularity**: JSON-CS explicitly supports namespaces and allows organizaing
  a lage number of type definitions within a single file. It also supports type
  definition hierarchies [where types can reuse shared definitions from abstract
  types](spec/json-cs.md#376-reuse-of-type-definitions-with-restricted-polymorphism),
  but without imposing the complexity of full subtype-polymorphism.
- **Internationalization**: JSON-CS supports alternate names and alternate symbols
  for properties and enums to support
  [internationalization](spec/json-cs.md#3342-alternate-names-for-display-internationalization).
- **Alternate Identifiers**: JSON-CS supports alternate names for properties and
  types to support mapping to programming languages and databases and
  [serialization
  formats](spec/json-cs.md#3341-alternate-names-for-json-encoding), like you can
  define a serialization-specific identifier for a property that is different
  from the property name.
- **Precise semantics**: JSON-CS requires explicit type declarations for each
  property and adds a [`unit`](spec/json-cs.md#3772-the-unit-keyword) attribute
  for properties to declare SI units or other units of measure for the property.
- **Richer descriptions**: JSON-CS adds an
  [`examples`](spec/json-cs.md#3773-the-examples-keyword) attribute to
  properties to provide examples of a type's values.

## Examples

### Example 1: Basic Type Definition

This is a basic type definition for a `Person` object with a few properties.
The definition is quasi identical to a JSON Schema definition, but with the
addition of the `$schema` keyword that identifies the document as a JSON-CS
document.

```json
{
    "$schema": "https://schemas.microsoft.com/experimental/json-cs/v0",
    "name": "Person",
    "type": "object",
    "properties": {
        "id": { "type": "string" },
        "title": { "type": "string" },
        "firstName": { "type": "string" },
        "lastName": { "type": "string" },
        "dateOfBirth": { "type": "string", "format": "date" },
    },
    "required": ["id", "lastName"]
}
```

### Example 2: Reusing JSON Schema Definitions

JSON-CS processors [must recognize the schema identifiers of JSON
Schema](spec/json-cs.md#5-compatibility-with-json-schema-drafts) and process
them as JSON-CS documents, but within the constraints of JSON-CS. JSON-CS
processors will allow you to reuse many existing, simple JSON Schema documents
as JSON-CS documents.

The following example shows a JSON Schema document that defines an `Address`,
`Label`, and `Person` type. The `Person` type references the `Address` and
`Label` types, the latter as an array of `Label` objects.

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Person",
    "type": "object",
    "properties": {
        "id": { "type": "string" },
        "title": { "type": "string" },
        "firstName": { "type": "string" },
        "lastName": { "type": "string" },
        "dateOfBirth": { "type": "string", "format": "date" },
        "address": { "$ref": "#/definitions/Address" },
        "labels": {
            "type": "array",
            "items": { "$ref": "#/definitions/Label" }
        }
    },
    "required": ["id", "lastName"],
    "definitions": {
        "Address": {
            "type": "object",
            "properties": {
                "street": { "type": "string" },
                "city": { "type": "string" },
                "zip": { "type": "string" }
            },
            "required": ["street", "city", "zip"]
        },
        "Label": {
          "type": "object",
          "properties": {
              "name": { "type": "string" },
              "value": { "type": "string" },
          }
        }
    }
}
```	

This schema is a valid JSON-CS definition through the compatibility mapping,
with the types defined in the `definitions` section being placed into the 
empty (global) namespace.

That means that the vast majority of existing JSON Schema documents used 
to describe simple data structures can be used as JSON-CS documents without
modification, also for contexts like OpenAPI.

### Example 3: Using Alternate Names for Internationalization

This example shows how to use alternate names for properties to support
internationalization. The `name` property has alternate names for Spanish and
Chinese that can be shown as labels in a user interface instead of the technical
identifier.

```json
{
    "$schema": "https://schemas.microsoft.com/experimental/json-cs/v0",
    "Product": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "altnames": {
                    "display:es": "Nombre",
                    "display:zh": "名称"
                }
            }
        },
        "required": ["name"],
        "additionalProperties": false
    }
}
```

### Example 4: Using Alternate Names for Encodings

This example shows how to use alternate names for properties to support mapping
to programming languages and databases. The `productName` property has an
alternate name for JSON encoding that is different from the property name.

```json
{
    "$schema": "https://schemas.microsoft.com/experimental/json-cs/v0",
    "Product": {
        "type": "object",
        "properties": {
            "productName": {
                "type": "string",
                "altnames": {
                    "json": "product-name"
                }
            }
        },
        "required": ["name"],
        "additionalProperties": false
    }
}
```

For declaring types that can be consistently translated into Protocol Buffers
schemas, the `altnames` attribute could be used to declare the numeric tag for
the field in the Protocol Buffers schema. This mapping is not defined in the
specification, but can be defined as a convention for a JSON-CS to Proto
translation mapping. 

```json
{
    "$schema": "https://schemas.microsoft.com/experimental/json-cs/v0",
    "Product": {
        "type": "object",
        "properties": {
            "productName": {
                "type": "string",
                "altnames": {
                    "protoId": "1"
                }
            }
        },
        "required": ["name"],
        "additionalProperties": false
    }
}
```

### Example 5: Using Units of Measure

This example shows how to use the `unit` attribute to declare the unit of measure
for a property. The `weight` property is declared to be a number with a unit of
measure of kilograms.

```json
{
    "$schema": "https://schemas.microsoft.com/experimental/json-cs/v0",
    "Product": {
        "type": "object",
        "properties": {
            "weight": {
                "type": "number",
                "unit": "kg"
            }
        },
        "required": ["weight"],
        "additionalProperties": false
    }
}
```

### Example 6: Better Documentation with Examples

This example shows how to use the `examples` attribute to provide examples of
values for a property. The `weight` property is declared to be a number with a
unit of measure of kilograms. The `examples` attribute provides two examples of
values for the `weight` property.

```json
{
    "$schema": "https://schemas.microsoft.com/experimental/json-cs/v0",
    "Product": {
        "type": "object",
        "properties": {
            "weight": {
                "type": "number",
                "unit": "kg",
                "examples": [
                  { "value": 2.5, "description": "A typical weight for this product" },
                  { "value": 3.0, "description": "A heavier weight for this product" }
                ]
            }
        },
        "required": ["weight"],
        "additionalProperties": false
    }
}
```

### Example 7: Using Namespaces

This example shows how to use namespaces to organize type
definitions within a single file. 

```json
{
  "$schema": "https://schemas.microsoft.com/experimental/json-cs/v0",
  "Orders": {
    "Order": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "customer": { "$ref": "#/Customers/Customer" },
        "items": { "type": "array", "items": { "$ref": "#/Inventory/Item" } }
      },
      "required": ["id", "customer", "items"]
    },
    "Invoice": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "order": { "$ref": "#/Orders/Order" },
        "total": { "type": "number" }
      },
      "required": ["id", "order", "total"]
    },
    "Payment": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "invoice": { "$ref": "#/Orders/Invoice" },
        "amount": { "type": "number" }
      },
      "required": ["id", "invoice", "amount"]
    }
  },
  "Inventory": {
    "Item": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "price": { "type": "number" }
      },
      "required": ["id", "name", "price"]
    }
  },
  "Customers": {
    "Customer": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "email": { "type": "string" }
      },
      "required": ["id", "name", "email"]
    }
  }
}
```

### Example 8: Declaring the root type of a document

This example shows how to declare the root type of a document. The `Order` type
is declared as the root type of the document even though it is declared inside
the `Orders` namespace.

```json
{
  "$schema": "https://schemas.microsoft.com/experimental/json-cs/v0",
  "$root": "#/Orders/Order",
  "Orders" : {
    "Order": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "customer": { "$ref": "#/Customers/Customer" },
        "items": { "type": "array", "items": { "$ref": "#/Inventory/Item" } }
      },
      "required": ["id", "customer", "items"]
    }
  }
}
```

### Example 9: Sharing Definitions with Restricted Polymorphism

This example shows how to share definitions with restricted polymorphism. The
`Vehicle` type is an abstract type that defines a `make` property. The `Car` and
`Truck` types are concrete types that extend the `Vehicle` type and add
additional properties.

While this looks like subtype polymorphism at first glance, it's more
restricted. The `Vehicle` type is abstract and cannot be used directly. It must
only be used in the `$extends` clause of a concrete type. The `Car` and `Truck`
types are concrete types that extend the `Vehicle` type and add additional
properties. The `Car` and `Truck` types cannot be used interchangeably where a
`Vehicle` type is expected because it's not permitted to declare a property as
having a type of `Vehicle`.

```json
{
  "$schema": "https://schemas.microsoft.com/experimental/json-cs/v0",
  "Vehicle": {
    "type": "object",
    "abstract": true,
    "properties": {
      "make": { "type": "string" }
    },
    "required": ["make"]
  },
  "Car": {
      "type": "object",
      "$extends": "#/Vehicle",
      "properties": {
        "seats": { "type": "number" }
      },
      "required": ["seats"]
  },
  "Truck": {
      "type": "object",
      "$extends": "#/Vehicle",
      "properties": {
        "loadCapacity": { "type": "number" }
      },
      "required": ["loadCapacity"]
  }
}
```

It is possible to define a property that can be either a `Car` or a `Truck` by
using a union type. The items in the `vehicles` array of the `Fleet` type show
this. That means that polymorphism can be modeled, but it must be explicit and
restricted to the types that are defined in the schema.

```json
{
  "$schema": "https://schemas.microsoft.com/experimental/json-cs/v0",
  "Vehicle": {
    "type": "object",
    "abstract": true,
    "properties": {
      "make": { "type": "string" }
    },
    "required": ["make"]
  },
  "Car": {
      "type": "object",
      "$extends": "#/Vehicle",
      "properties": {
        "seats": { "type": "number" }
      },
      "required": ["seats"]
  },
  "Truck": {
      "type": "object",
      "$extends": "#/Vehicle",
      "properties": {
        "loadCapacity": { "type": "number" }
      },
      "required": ["loadCapacity"]
  },
  "Fleet": {
    "type": "object",
    "properties": {
      "vehicles": {
        "type" : "array",
        "items": [
          { "$ref": "#/Car" },
          { "$ref": "#/Truck" }
        ]
      }
    },
    "required": ["vehicles"]
  }
}
```

### Example 11: Disambiguating Type Unions with Discriminators

This example shows how to identify types and therefore disambiguate type unions
with discriminators. The `Vehicle` type is an abstract type that defines a
`make` property. The `Car` and `Truck` types are concrete types that extend the
`Vehicle` type and add additional properties. The `Vehicle` type has a `type`
property that is used as a discriminator to determine the concrete type of the
object.

The `const` keyword is used to declare the fixed value of the `type` property
that indicates the concrete type of the object. The `const` value is used at
design time and at runtime to ensure that the alternative types are mutually
exclusive even if all their properties are optional.

```json
{
  "$schema": "https://schemas.microsoft.com/experimental/json-cs/v0",
  "Vehicle": {
    "type": "object",
    "abstract": true,
    "properties": {
      "type": { "type": "string" },
      "make": { "type": "string" }
    },
    "required": ["type", "make"]
  },
  "Car": {
      "type": "object",
      "$extends": "#/Vehicle",
      "properties": {
        "type": { "type": "string", "const": "Car" },
        "seats": { "type": "number" }
      },
      "required": ["type"]
  },
  "Truck": {
      "type": "object",
      "$extends": "#/Vehicle",
      "properties": {
        "type": { "type": "string", "const": "Truck" },
        "loadCapacity": { "type": "number" }
      },
      "required": ["type"]
  }
}
```

## Full Specification

For the complete JSON-CS specification, please refer to the [JSON-CS (Compact Schema) Specification](spec/json-cs.md).


