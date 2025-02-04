# JSON Schema Import Extensions  
C. Vasters (Microsoft) February 2024

## Abstract

This document specifies JSON Schema Import Extensions, which introduce two new keywords:  
- `$import`: Imports the root type from an external JSON Schema Core document.  
- `$importdefs`: Imports all definitions (`$defs`) from the referenced external schema.

These keywords enable modular reuse of external schema definitions by mapping them into designated namespaces in the local `$defs` section.

## 1. Introduction

JSON Schema Import Extensions allow schema authors to incorporate external JSON Schema documents into a local schema. By mapping external schemas into local namespaces via `$import` and `$importdefs`, all type definitions and reusable components become available for reference using local JSON Pointers.

## 2. Keywords Specification

### 2.1. `$import`

- **Definition:**  
  The `$import` keyword is a reference expression whose value is an absolute URI pointing to an external JSON Schema Core document. It imports the external schema's root type into a local namespace.

- **Usage:**  
  The `$import` keyword SHALL appear as the sole property of an object within the local `$defs` section. The property name under which it appears becomes the local namespace for the imported root type.

- **Mapping Semantics:**  
  When `$import` is encountered, the external schema is fetched and validated. The external schema's root type (as designated by its `$root` keyword or defined by its document structure) is imported into the local namespace.  
  **Example:**  
  ```json
  {
    "$defs": {
      "ExternalRoot": {
        "$import": "https://example.com/external-schema.json"
      }
    }
  }
  ```  
  The external schema’s root type is then accessible via:
  ```json
  { "$ref": "#/$defs/ExternalRoot/RootType" }
  ```

### 2.2. `$importdefs`

- **Definition:**  
  The `$importdefs` keyword is a reference expression whose value is an absolute URI pointing to an external JSON Schema Core document. It imports the entire `$defs` section from the referenced schema into a local namespace.

- **Usage:**  
  The `$importdefs` keyword SHALL appear as the sole property of an object within the local `$defs` section. The property name under which it appears becomes the local namespace for all imported definitions.

- **Mapping Semantics:**  
  When `$importdefs` is encountered, the external schema is fetched and its top-level `$defs` section is imported. Every definition within that section is mapped into the local namespace.  
  **Example:**  
  ```json
  {
    "$defs": {
      "ExternalDefinitions": {
        "$importdefs": "https://example.com/external-schema.json"
      }
    }
  }
  ```  
  If the external schema’s `$defs` contains definitions such as `TypeA` and `TypeB`, they become accessible via:
  ```json
  { "$ref": "#/$defs/ExternalDefinitions/TypeA" }
  ```
  and
  ```json
  { "$ref": "#/$defs/ExternalDefinitions/TypeB" }
  ```

### 2.3. Conflict and Circular Import Handling

- **Name Conflicts:**  
  If an imported type (via `$import`) or definition (via `$importdefs`) conflicts with an existing definition in the same namespace, the import SHALL result in a validation error.

- **Circular Imports:**  
  Circular or recursive import chains MUST be detected. If a circular import is detected, schema validation SHALL fail with an appropriate error.

## 3. Usage Example

The following JSON Schema document demonstrates the use of both `$import` and `$importdefs`:

```json
{
  "$schema": "https://schemas.vasters.com/experimental/json-core/v0",
  "$defs": {
    "LocalTypes": {
      "MyLocalType": {
        "name": "MyLocalType",
        "type": "object",
        "properties": {
          "id": { "type": "string" }
        },
        "required": ["id"]
      }
    },
    "ExternalRoot": {
      "$import": "https://example.com/external-schema.json"
    },
    "ExternalDefinitions": {
      "$importdefs": "https://example.com/external-schema.json"
    }
  },
  "name": "RootType",
  "type": "object",
  "properties": {
    "local": { "$ref": "#/$defs/LocalTypes/MyLocalType" },
    "externalRoot": { "$ref": "#/$defs/ExternalRoot/RootType" },
    "externalDef": { "$ref": "#/$defs/ExternalDefinitions/SomeExternalType" }
  },
  "required": ["local", "externalRoot", "externalDef"]
}
```

In this example:
- The external schema's root type is imported into the `ExternalRoot` namespace using `$import`.
- All definitions from the external schema’s `$defs` section are imported into the `ExternalDefinitions` namespace using `$importdefs`.

## 4. Implementation Considerations

- Schema processing engines MUST resolve the absolute URIs specified in `$import` and `$importdefs`, fetch the external schemas, and validate them as JSON Schema Core documents.
- Imported definitions shall be merged into the local `$defs` under the designated namespace without altering the external definitions.
- Implementations SHOULD employ caching and robust error handling for remote schema retrieval.

## 5. Security Considerations

- External schema URIs MUST originate from trusted sources.
- Remote fetching of schemas SHOULD be performed over secure protocols (e.g., HTTPS) to mitigate tampering.
- Excessively deep or circular import chains MUST be detected and mitigated to avoid performance degradation and potential denial-of-service conditions.

## 6. IANA Considerations

This document does not require any IANA actions.

## 7. References

- [RFC2119] Bradner, S., “Key words for use in RFCs to Indicate Requirement Levels”, RFC 2119.
- [RFC8174] Leiba, B., “Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words”, RFC 8174.
- [JSON Schema Core] C. Vasters, “JSON Schema Core”, February 2024.

## 8. Author's Address

**Clemens Vasters**  
Microsoft  
Email: clemensv@microsoft.com