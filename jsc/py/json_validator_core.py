# encoding: utf-8
"""
instance_validator.py

Validates JSON document instances against JSON schemas conforming to the experimental
JSON Schema Core specification (C. Vasters, Microsoft, February 2025), including
all constructs from the core spec: primitive types, compound types, abstract types,
$extends, $offers, $uses, as well as the JSON Schema Import extensions ($import and $importdefs).

Additionally, if the instance provides a "$uses" clause containing "Conditionals" and/or "Validation",
the corresponding conditional composition and validation addin constraints are enforced.
Extensions such as "Altnames" or "Units" are generally ignored for validation.

Furthermore, when the root schema’s "$schema" equals 
    "https://schemas.vasters.com/experimental/json-schema-extended/v0"
all addins (i.e. all keys offered in "$offers") are automatically enabled.

This implementation also supports extended validation keywords as defined in the 
"JSON Schema Validation" spec, including numeric, string, array, object constraints,
and the "has" keyword.

Usage:
    python instance_validator.py <schema_file> <instance_file>

The code sections are annotated with references to the metaschema constructs.
"""

import sys
import json
import re
import datetime
import uuid
from urllib.parse import urlparse

# Regular expressions for date, datetime, time and JSON pointer.
_DATE_REGEX = re.compile(r'^\d{4}-\d{2}-\d{2}$')
_DATETIME_REGEX = re.compile(
    r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+\-]\d{2}:\d{2})$'
)
_TIME_REGEX = re.compile(r'^\d{2}:\d{2}:\d{2}(?:\.\d+)?$')
_JSONPOINTER_REGEX = re.compile(r'^#(\/[^\/]+)*$')


class JSONInstanceValidator:
    """
    Validator for JSON document instances against full JSON Schema Core schemas.
    Implements all core constructs including abstract types, $extends, $offers, $uses,
    the Import extension ($import and $importdefs), as well as conditional composition
    (allOf, anyOf, oneOf, not, if/then/else) and validation addin constraints.
    """
    ABSOLUTE_URI_REGEX = re.compile(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://')

    def __init__(self, root_schema, allow_import=False, import_map=None):
        """
        Initializes the validator.
        :param root_schema: The JSON schema (as dict).
        :param allow_import: Enables processing of $import/$importdefs.
        :param import_map: Dict mapping URIs to local filenames.
        """
        self.root_schema = root_schema
        self.errors = []
        self.allow_import = allow_import
        self.import_map = import_map if import_map is not None else {}
        # Process $import and $importdefs if enabled. [Metaschema: Import extension constructs]
        if self.allow_import:
            self._process_imports(self.root_schema, "#")

    def validate_instance(self, instance, schema=None, path="#", meta=None):
        """
        Validates an instance against a schema.
        Resolves $ref, processes $extends, rejects abstract schemas, applies $uses,
        then validates based on type. Finally, conditionally validates conditional composition
        and validation addin constraints.
        :param instance: The JSON instance.
        :param schema: The schema to validate against (defaults to root schema).
        :param path: JSON Pointer for error reporting.
        :return: List of error messages.
        """
        if schema is None:
            schema = self.root_schema

        # --- Automatically enable all addins if using extended metaschema ---
        if self.root_schema.get("$schema") == "https://schemas.vasters.com/experimental/json-schema-extended/v0":
            # Automatically enable all addins offered in the root schema.
            all_addins = ["Conditionals", "Validation", "Units", "Altnames"]
            schema.setdefault("$uses", [])
            for addin in all_addins:
                if addin not in schema["$uses"]:
                    schema["$uses"].append(addin)
            # [Metaschema: Extended metaschema automatically enables all addins]

        if isinstance(instance, dict) and "$uses" in instance and self.root_schema.get("$schema") == "https://schemas.vasters.com/experimental/json-schema-validation/v0":
            # Automatically enable the Validation addin.
            schema.setdefault("$uses", [])
            if "Validation" in instance["$uses"] and not "Validation" in schema["$uses"]:
                schema["$uses"].append("Validation")
            if "Conditionals" in instance["$uses"] and not "Conditionals" in schema["$uses"]:
                schema["$uses"].append("Conditionals")
            # [Metaschema: Validation metaschema automatically enables Validation addin]

        # the core schema https://schemas.vasters.com/experimental/json-schema-validation/v0 has no Conditionals or Validation addins
        # an instance referencing these addins will be rejected
        if isinstance(instance, dict) and "$uses" in instance and self.root_schema.get("$schema") == "https://schemas.vasters.com/experimental/json-schema-core/v0":
            if "Validation" in instance["$uses"] or "Conditionals" in instance["$uses"]:
                self.errors.append(
                    f"Instance at {path} references Conditionals or Validation addins but the schema does not support them")

        # Resolve $ref at schema level. [Metaschema: TypeReference]
        if "$ref" in schema:
            ref = schema["$ref"]
            resolved = self._resolve_ref(ref)
            if resolved is None:
                self.errors.append(f"Cannot resolve $ref {ref} at {path}")
                return self.errors
            return self.validate_instance(instance, resolved, path)
        
        hasConditionals = False
        if "$uses" in self.root_schema:
            if "Conditionals" in self.root_schema["$uses"]:
                hasConditionals = self._validate_conditionals(schema, instance, path)
        
        # Handle case where "type" is a dict with a $ref. [Metaschema: PrimitiveOrReference]
        schema_type = schema.get("type")
        if not schema_type:
            if hasConditionals: # non-schema with conditionals
                return self.errors
            self.errors.append(f"Schema at {path} has no 'type'")
            
        if isinstance(schema_type, dict):
            if "$ref" in schema_type:
                resolved = self._resolve_ref(schema_type["$ref"])
                if resolved is None:
                    self.errors.append(f"Cannot resolve $ref {schema_type['$ref']} at {path}/type")
                    return self.errors
                new_schema = dict(schema)
                new_schema["type"] = resolved.get("type")
                if "properties" in resolved:
                    merged_props = dict(resolved.get("properties"))
                    merged_props.update(new_schema.get("properties", {}))
                    new_schema["properties"] = merged_props
                schema = new_schema
                schema_type = schema.get("type")
            else:
                self.errors.append(f"Schema at {path} has invalid 'type'")
                return self.errors

        # Handle union types. [Metaschema: TypeUnion]
        if isinstance(schema_type, list):
            union_valid = False
            union_errors = []
            for t in schema_type:
                backup = list(self.errors)
                self.errors = []
                self.validate_instance(instance, {"type": t}, path)
                if not self.errors:
                    union_valid = True
                    break
                else:
                    union_errors.extend(self.errors)
                self.errors = backup
            if not union_valid:
                self.errors.append(f"Instance at {path} does not match any type in union: {union_errors}")
            return self.errors

        if not isinstance(schema_type, str):
            self.errors.append(f"Schema at {path} has invalid 'type'")
            return self.errors

        # Process $extends. [Metaschema: $extends in ObjectType/TupleType]
        if "$extends" in schema:
            base = self._resolve_ref(schema["$extends"])
            if base is None:
                self.errors.append(f"Cannot resolve $extends {schema['$extends']} at {path}")
                return self.errors
            base_props = base.get("properties", {})
            derived_props = schema.get("properties", {})
            for key in base_props:
                if key in derived_props:
                    self.errors.append(
                        f"Property '{key}' is inherited via $extends and must not be redefined at {path}")
            merged = dict(base)
            merged.update(schema)
            merged.pop("$extends", None)
            schema = merged

        # Reject abstract schemas. [Metaschema: abstract property]
        if schema.get("abstract") is True:
            self.errors.append(f"Abstract schema at {path} cannot be used for instance validation")
            return self.errors

        # Process $uses add-in. [Metaschema: $offers and $uses]
        if isinstance(instance, dict) and "$uses" in instance:
            schema = self._apply_uses(schema, instance)
            instance.pop("$uses")

        # --- Begin type-based validation ---
        # Primitive types.
        if schema_type == "any":
            pass
        elif schema_type == "string":
            if not isinstance(instance, str):
                self.errors.append(f"Expected string at {path}, got {type(instance).__name__}")
        elif schema_type == "number":
            if isinstance(instance, bool) or not isinstance(instance, (int, float)):
                self.errors.append(f"Expected number at {path}, got {type(instance).__name__}")
        elif schema_type == "boolean":
            if not isinstance(instance, bool):
                self.errors.append(f"Expected boolean at {path}, got {type(instance).__name__}")
        elif schema_type == "null":
            if instance is not None:
                self.errors.append(f"Expected null at {path}, got {type(instance).__name__}")
        elif schema_type == "int32":
            if not isinstance(instance, int):
                self.errors.append(f"Expected int32 at {path}, got {type(instance).__name__}")
            elif not (-2**31 <= instance <= 2**31 - 1):
                self.errors.append(f"int32 value at {path} out of range")
        elif schema_type == "uint32":
            if not isinstance(instance, int):
                self.errors.append(f"Expected uint32 at {path}, got {type(instance).__name__}")
            elif not (0 <= instance <= 2**32 - 1):
                self.errors.append(f"uint32 value at {path} out of range")
        elif schema_type == "int64":
            if not isinstance(instance, str):
                self.errors.append(f"Expected int64 as string at {path}, got {type(instance).__name__}")
            else:
                try:
                    value = int(instance)
                    if not (-2**63 <= value <= 2**63 - 1):
                        self.errors.append(f"int64 value at {path} out of range")
                except ValueError:
                    self.errors.append(f"Invalid int64 format at {path}")
        elif schema_type == "uint64":
            if not isinstance(instance, str):
                self.errors.append(f"Expected uint64 as string at {path}, got {type(instance).__name__}")
            else:
                try:
                    value = int(instance)
                    if not (0 <= value <= 2**64 - 1):
                        self.errors.append(f"uint64 value at {path} out of range")
                except ValueError:
                    self.errors.append(f"Invalid uint64 format at {path}")
        elif schema_type in ("float", "double"):
            if not isinstance(instance, (int, float)):
                self.errors.append(f"Expected {schema_type} at {path}, got {type(instance).__name__}")
        elif schema_type == "decimal":
            if not isinstance(instance, str):
                self.errors.append(f"Expected decimal as string at {path}, got {type(instance).__name__}")
            else:
                try:
                    float(instance)
                except ValueError:
                    self.errors.append(f"Invalid decimal format at {path}")
        elif schema_type == "date":
            if not isinstance(instance, str) or not _DATE_REGEX.match(instance):
                self.errors.append(f"Expected date (YYYY-MM-DD) at {path}")
        elif schema_type == "datetime":
            if not isinstance(instance, str) or not _DATETIME_REGEX.match(instance):
                self.errors.append(f"Expected datetime (RFC3339) at {path}")
        elif schema_type == "time":
            if not isinstance(instance, str) or not _TIME_REGEX.match(instance):
                self.errors.append(f"Expected time (HH:MM:SS) at {path}")
        elif schema_type == "duration":
            if not isinstance(instance, str):
                self.errors.append(f"Expected duration as string at {path}")
        elif schema_type == "uuid":
            if not isinstance(instance, str):
                self.errors.append(f"Expected uuid as string at {path}")
            else:
                try:
                    uuid.UUID(instance)
                except ValueError:
                    self.errors.append(f"Invalid uuid format at {path}")
        elif schema_type == "uri":
            if not isinstance(instance, str):
                self.errors.append(f"Expected uri as string at {path}")
            else:
                parsed = urlparse(instance)
                if not parsed.scheme:
                    self.errors.append(f"Invalid uri format at {path}")
        elif schema_type == "binary":
            if not isinstance(instance, str):
                self.errors.append(f"Expected binary (base64 string) at {path}")
        elif schema_type == "jsonpointer":
            if not isinstance(instance, str) or not _JSONPOINTER_REGEX.match(instance):
                self.errors.append(f"Expected JSON pointer format at {path}")
        # Compound types.
        elif schema_type == "object":
            if not isinstance(instance, dict):
                self.errors.append(f"Expected object at {path}, got {type(instance).__name__}")
            else:
                props = schema.get("properties", {})
                req = schema.get("required", [])
                for r in req:
                    if r not in instance:
                        self.errors.append(f"Missing required property '{r}' at {path}")
                for prop, prop_schema in props.items():
                    if prop in instance:
                        self.validate_instance(instance[prop], prop_schema, f"{path}/{prop}")
                if "additionalProperties" in schema:
                    addl = schema["additionalProperties"]
                    if addl is False:
                        for key in instance.keys():
                            if key not in props:
                                self.errors.append(f"Additional property '{key}' not allowed at {path}")
                    elif isinstance(addl, dict):
                        for key in instance.keys():
                            if key not in props:
                                self.validate_instance(instance[key], addl, f"{path}/{key}")
                # Extended object constraint: "has" keyword. [Metaschema: ObjectValidationAddIn]
                if "has" in schema:
                    has_schema = schema["has"]
                    valid = any(len(self.validate_instance(val, has_schema, f"{path}/{prop}")) == 0
                                for prop, val in instance.items())
                    if not valid:
                        self.errors.append(f"Object at {path} does not have any property satisfying 'has' schema")
                # dependencies (dependentRequired) validation
                if "dependentRequired" in schema and isinstance(schema["dependentRequired"], dict):
                    for prop_name, required_deps in schema["dependentRequired"].items():
                        if prop_name in instance and isinstance(required_deps, list):
                            for dep in required_deps:
                                if dep not in instance:
                                    self.errors.append(
                                        f"Property '{prop_name}' at {path} requires dependent property '{dep}'")
        elif schema_type == "array":
            if not isinstance(instance, list):
                self.errors.append(f"Expected array at {path}, got {type(instance).__name__}")
            else:
                items_schema = schema.get("items")
                if items_schema:
                    for idx, item in enumerate(instance):
                        self.validate_instance(item, items_schema, f"{path}[{idx}]")
        elif schema_type == "set":
            if not isinstance(instance, list):
                self.errors.append(f"Expected set (unique array) at {path}, got {type(instance).__name__}")
            else:
                serialized = [json.dumps(x, sort_keys=True) for x in instance]
                if len(serialized) != len(set(serialized)):
                    self.errors.append(f"Set at {path} contains duplicate items")
                items_schema = schema.get("items")
                if items_schema:
                    for idx, item in enumerate(instance):
                        self.validate_instance(item, items_schema, f"{path}[{idx}]")
        elif schema_type == "map":
            if not isinstance(instance, dict):
                self.errors.append(f"Expected map (object) at {path}, got {type(instance).__name__}")
            else:
                values_schema = schema.get("values")
                if values_schema:
                    for key, val in instance.items():
                        self.validate_instance(val, values_schema, f"{path}/{key}")
        elif schema_type == "tuple":
            if not isinstance(instance, list):
                self.errors.append(f"Expected tuple (array) at {path}, got {type(instance).__name__}")
            else:
                props = schema.get("properties", {})
                expected_len = len(props)
                if len(instance) != expected_len:
                    self.errors.append(f"Tuple at {path} length {len(instance)} does not equal expected {expected_len}")
                else:
                    for (prop, prop_schema), item in zip(props.items(), instance):
                        self.validate_instance(item, prop_schema, f"{path}/{prop}")
        else:
            self.errors.append(f"Unsupported type '{schema_type}' at {path}")

        # Conditionally validate conditionals if "Conditionals" addin is enabled.
        if "$uses" in self.root_schema:
            # Conditionally validate validation addins if "Validation" addin is enabled.
            if "Validation" in self.root_schema["$uses"]:
                self._validate_validation_addins(schema, instance, path)

        if "const" in schema:
            if instance != schema["const"]:
                self.errors.append(f"Value at {path} does not equal const {schema['const']}")
        if "enum" in schema:
            if instance not in schema["enum"]:
                self.errors.append(f"Value at {path} not in enum {schema['enum']}")
        return self.errors

    def _validate_conditionals(self, schema, instance, path) -> bool:
        """
        Validates conditional composition keywords: allOf, anyOf, oneOf, not, if/then/else.
        [Metaschema: JSON Schema Conditional Composition]
        returns True if the instance contains any conditional composition keywords
        """
        hasConditionals = False
        if "allOf" in schema:
            hasConditionals = True
            subschemas = schema["allOf"]
            for idx, subschema in enumerate(subschemas):
                backup = list(self.errors)
                self.validate_instance(instance, subschema, f"{path}/allOf[{idx}]")
                if self.errors:
                    self.errors = backup + self.errors
        if "anyOf" in schema:
            hasConditionals = True
            subschemas = schema["anyOf"]
            valid = False
            errors_any = []
            for idx, subschema in enumerate(subschemas):
                backup = list(self.errors)
                self.errors = []
                self.validate_instance(instance, subschema, f"{path}/anyOf[{idx}]")
                if not self.errors:
                    valid = True
                    break
                else:
                    errors_any.append(f"anyOf[{idx}]: {self.errors}")
                self.errors = backup
            if not valid:
                self.errors.append(f"Instance at {path} does not satisfy anyOf: {errors_any}")
        if "oneOf" in schema:
            hasConditionals = True	
            subschemas = schema["oneOf"]
            valid_count = 0
            errors_one = []
            for idx, subschema in enumerate(subschemas):
                backup = list(self.errors)
                self.errors = []
                self.validate_instance(instance, subschema, f"{path}/oneOf[{idx}]")
                if not self.errors:
                    valid_count += 1
                else:
                    errors_one.append(f"oneOf[{idx}]: {self.errors}")
                self.errors = backup
            if valid_count != 1:
                self.errors.append(
                    f"Instance at {path} must match exactly one subschema in oneOf; matched {valid_count}. Details: {errors_one}")
        if "not" in schema:
            hasConditionals = True
            subschema = schema["not"]
            backup = list(self.errors)
            self.errors = []
            self.validate_instance(instance, subschema, f"{path}/not")
            if not self.errors:
                self.errors = backup + [f"Instance at {path} should not validate against 'not' schema"]
            else:
                self.errors = backup
        if "if" in schema:
            hasConditionals = True
            backup = list(self.errors)
            self.errors = []
            self.validate_instance(instance, schema["if"], f"{path}/if")
            if_valid = not self.errors
            self.errors = backup
            if if_valid:
                if "then" in schema:
                    self.validate_instance(instance, schema["then"], f"{path}/then")
            else:
                if "else" in schema:
                    self.validate_instance(instance, schema["else"], f"{path}/else")
        return hasConditionals

    def _validate_validation_addins(self, schema, instance, path):
        """
        Validates additional constraints defined by the Validation addins.
        [Metaschema: JSON Schema Validation]
        """
        # Numeric constraints.
        if schema.get("type") in ("number", "integer", "float", "double", "decimal", "int32", "uint32", "int64", "uint64", "int128", "uint128"):
            if "minimum" in schema:
                try:
                    if instance < schema["minimum"]:
                        self.errors.append(f"Value at {path} is less than minimum {schema['minimum']}")
                except Exception:
                    self.errors.append(f"Cannot compare value at {path} with minimum constraint")
            if "maximum" in schema:
                try:
                    if instance > schema["maximum"]:
                        self.errors.append(f"Value at {path} is greater than maximum {schema['maximum']}")
                except Exception:
                    self.errors.append(f"Cannot compare value at {path} with maximum constraint")
            if schema.get("exclusiveMinimum") is True:
                try:
                    if instance <= schema.get("minimum", float("-inf")):
                        self.errors.append(
                            f"Value at {path} is not greater than exclusive minimum {schema.get('minimum')}")
                except Exception:
                    self.errors.append(f"Cannot evaluate exclusiveMinimum constraint at {path}")
            if schema.get("exclusiveMaximum") is True:
                try:
                    if instance >= schema.get("maximum", float("inf")):
                        self.errors.append(
                            f"Value at {path} is not less than exclusive maximum {schema.get('maximum')}")
                except Exception:
                    self.errors.append(f"Cannot evaluate exclusiveMaximum constraint at {path}")
            if "multipleOf" in schema:
                try:
                    if instance % schema["multipleOf"] != 0:
                        self.errors.append(f"Value at {path} is not a multiple of {schema['multipleOf']}")
                except Exception:
                    self.errors.append(f"Cannot evaluate multipleOf constraint at {path}")
        # String constraints.
        if schema.get("type") == "string":
            if "minLength" in schema:
                if len(instance) < schema["minLength"]:
                    self.errors.append(f"String at {path} shorter than minLength {schema['minLength']}")
            if "maxLength" in schema:
                if len(instance) > schema["maxLength"]:
                    self.errors.append(f"String at {path} longer than maxLength {schema['maxLength']}")
            if "pattern" in schema:
                pattern = re.compile(schema["pattern"])
                if not pattern.search(instance):
                    self.errors.append(f"String at {path} does not match pattern {schema['pattern']}")
            if "format" in schema:
                fmt = schema["format"]
                if fmt == "email":
                    if "@" not in instance:
                        self.errors.append(f"String at {path} does not appear to be a valid email")
                elif fmt == "uri":
                    parsed = urlparse(instance)
                    if not parsed.scheme:
                        self.errors.append(f"String at {path} does not appear to be a valid uri")
        # Array constraints.
        if schema.get("type") == "array":
            if "minItems" in schema:
                if len(instance) < schema["minItems"]:
                    self.errors.append(f"Array at {path} has fewer items than minItems {schema['minItems']}")
            if "maxItems" in schema:
                if len(instance) > schema["maxItems"]:
                    self.errors.append(f"Array at {path} has more items than maxItems {schema['maxItems']}")
            if schema.get("uniqueItems") is True:
                serialized = [json.dumps(x, sort_keys=True) for x in instance]
                if len(serialized) != len(set(serialized)):
                    self.errors.append(f"Array at {path} does not have unique items")
        # Object constraints.
        if schema.get("type") == "object":
            if "minProperties" in schema:
                if len(instance.keys()) < schema["minProperties"]:
                    self.errors.append(
                        f"Object at {path} has fewer properties than minProperties {schema['minProperties']}")
            if "maxProperties" in schema:
                if len(instance.keys()) > schema["maxProperties"]:
                    self.errors.append(
                        f"Object at {path} has more properties than maxProperties {schema['maxProperties']}")
            
            # patternProperties validation
            if "patternProperties" in schema and isinstance(schema["patternProperties"], dict):
                for pattern_str, pattern_schema in schema["patternProperties"].items():
                    try:
                        pattern = re.compile(pattern_str)
                        for prop_name, prop_value in instance.items():
                            if pattern.search(prop_name):
                                self.validate_instance(prop_value, pattern_schema, f"{path}/{prop_name}")
                    except re.error:
                        self.errors.append(f"Invalid regular expression '{pattern_str}' in patternProperties at {path}")
            
            # propertyNames validation
            if "propertyNames" in schema:
                property_names_schema = schema["propertyNames"]
                if not isinstance(property_names_schema, dict) or property_names_schema.get("type") != "string":
                    self.errors.append(f"propertyNames schema must be of type string at {path}")
                else:
                    for prop_name in instance.keys():
                        self.validate_instance(prop_name, property_names_schema, f"{path}/propertyName({prop_name})")
                        
            # dependencies (dependentRequired) validation
            if "dependentRequired" in schema and isinstance(schema["dependentRequired"], dict):
                for prop_name, required_deps in schema["dependentRequired"].items():
                    if prop_name in instance and isinstance(required_deps, list):
                        for dep in required_deps:
                            if dep not in instance:
                                self.errors.append(
                                    f"Property '{prop_name}' at {path} requires dependent property '{dep}'")

        # Map constraints
        if schema.get("type") == "map":
            # patternKeys validation
            if "patternKeys" in schema and isinstance(schema["patternKeys"], dict):
                for pattern_str, pattern_schema in schema["patternKeys"].items():
                    try:
                        pattern = re.compile(pattern_str)
                        for key_name, key_value in instance.items():
                            if pattern.search(key_name):
                                self.validate_instance(key_value, pattern_schema, f"{path}/{key_name}")
                    except re.error:
                        self.errors.append(f"Invalid regular expression '{pattern_str}' in patternKeys at {path}")
            
            # keyNames validation
            if "keyNames" in schema:
                key_names_schema = schema["keyNames"]
                if not isinstance(key_names_schema, dict) or key_names_schema.get("type") != "string":
                    self.errors.append(f"keyNames schema must be of type string at {path}")
                else:
                    for key_name in instance.keys():
                        self.validate_instance(key_name, key_names_schema, f"{path}/keyName({key_name})")

    def _resolve_ref(self, ref):
        """
        Resolves a $ref within the root schema using JSON Pointer syntax.
        [Metaschema: TypeReference]
        :param ref: A JSON pointer string starting with '#'.
        :return: The referenced schema object or None.
        """
        if not ref.startswith("#"):
            return None
        parts = ref.lstrip("#").split("/")
        target = self.root_schema
        for part in parts:
            if part == "":
                continue
            part = part.replace("~1", "/").replace("~0", "~")
            if isinstance(target, dict) and part in target:
                target = target[part]
            else:
                return None
        return target

    def _process_imports(self, obj, path):
        """
        Recursively processes $import and $importdefs keywords in the schema.
        [Metaschema: Import extension constructs]
        Merges imported definitions into the current object as if defined locally.
        Uses self.import_map if the URI is mapped to a local file.
        """
        if isinstance(obj, dict):
            for key in list(obj.keys()):
                if key in ("$import", "$importdefs"):
                    if not self.allow_import:
                        self.errors.append(
                            f"Import keyword '{key}' encountered but allow_import not enabled at {path}/{key}")
                        continue
                    uri = obj[key]
                    if not isinstance(uri, str):
                        self.errors.append(f"Import keyword '{key}' value must be a string URI at {path}/{key}")
                        continue
                    if not self.ABSOLUTE_URI_REGEX.search(uri):
                        self.errors.append(f"Import keyword '{key}' value must be an absolute URI at {path}/{key}")
                        continue
                    external = self._fetch_external_schema(uri)
                    if external is None:
                        self.errors.append(f"Unable to fetch external schema from {uri} at {path}/{key}")
                        continue
                    if key == "$import":
                        imported_defs = {}
                        if "type" in external and "name" in external:
                            imported_defs[external["name"]] = external
                        if "$defs" in external and isinstance(external["$defs"], dict):
                            imported_defs.update(external["$defs"])
                    else:  # $importdefs
                        if "$defs" in external and isinstance(external["$defs"], dict):
                            imported_defs = external["$defs"]
                        else:
                            imported_defs = {}
                    for k, v in imported_defs.items():
                        if k not in obj:
                            obj[k] = v
                    del obj[key]
            for k, v in obj.items():
                self._process_imports(v, f"{path}/{k}")
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                self._process_imports(item, f"{path}[{idx}]")

    def _fetch_external_schema(self, uri):
        """
        Fetches an external schema from a URI.
        [Metaschema: Import extension resolution]
        If the URI is in self.import_map, loads the schema from the specified file.
        Otherwise, uses a simulated lookup.
        """
        if uri in self.import_map:
            try:
                with open(self.import_map[uri], "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.errors.append(f"Failed to load imported schema from {self.import_map[uri]}: {e}")
                return None
        SIMULATED_SCHEMAS = {
            "https://example.com/people.json": {
                "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
                "$id": "https://example.com/people.json",
                "name": "Person",
                "type": "object",
                "properties": {
                    "firstName": {"type": "string"},
                    "lastName": {"type": "string"},
                    "address": {"$ref": "#/Address"}
                },
                "$defs": {
                    "Address": {
                        "name": "Address",
                        "type": "object",
                        "properties": {
                            "street": {"type": "string"},
                            "city": {"type": "string"}
                        }
                    }
                }
            },
            "https://example.com/importdefs.json": {
                "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
                "$id": "https://example.com/importdefs.json",
                "$defs": {
                    "LibraryType": {
                        "name": "LibraryType",
                        "type": "string"
                    }
                }
            }
        }
        return SIMULATED_SCHEMAS.get(uri)

    def _apply_uses(self, schema, instance):
        """
        Applies add-in types to the effective schema if the instance declares "$uses".
        [Metaschema: $offers and $uses in SchemaDocument]
        The $uses keyword is expected to be an array of add-in names.
        The root schema must have a "$offers" mapping.
        :param schema: The current schema.
        :param instance: The instance dict containing "$uses".
        :return: The merged schema with add-ins applied.
        """
        uses = instance.get("$uses")
        if not uses:
            return schema
        if not isinstance(uses, list):
            uses = [uses]
        offers = self.root_schema.get("$offers", {})
        merged = dict(schema)
        merged.setdefault("properties", {})
        for use in [u for u in uses if not u in ["Validation", "Conditionals", "Altnames", "Units"]]:
            if use not in offers:
                self.errors.append(f"Add-in '{use}' not offered in $offers")
                continue
            addin = offers[use]
            if isinstance(addin, list):
                for ref in addin:
                    resolved = self._resolve_ref(ref) if isinstance(ref, str) else ref
                    if isinstance(resolved, dict):
                        addin_props = resolved.get("properties", {})
                        for prop in addin_props:
                            if prop in merged["properties"]:
                                self.errors.append(
                                    f"Add-in property '{prop}' from add-in '{use}' conflicts with existing property")
                        merged["properties"].update(addin_props)
            elif isinstance(addin, dict) and "$ref" in addin:
                resolved = self._resolve_ref(addin["$ref"])
                if isinstance(resolved, dict):
                    addin_props = resolved.get("properties", {})
                    for prop in addin_props:
                        if prop in merged["properties"]:
                            self.errors.append(
                                f"Add-in property '{prop}' from add-in '{use}' conflicts with existing property")
                    merged["properties"].update(addin_props)
            elif isinstance(addin, dict):
                addin_props = addin.get("properties", {})
                for prop in addin_props:
                    if prop in merged["properties"]:
                        self.errors.append(
                            f"Add-in property '{prop}' from add-in '{use}' conflicts with existing property")
                merged["properties"].update(addin_props)
            else:
                self.errors.append(f"Invalid add-in definition for '{use}'")
        return merged

    def main():
        """
        Command line entry point.
        Usage: python instance_validator.py <schema_file> <instance_file>
        Loads the schema and instance from files and prints validation errors if any.
        """
        if len(sys.argv) != 3:
            print("Usage: python instance_validator.py <schema_file> <instance_file>")
            sys.exit(1)
        schema_file = sys.argv[1]
        instance_file = sys.argv[2]
        try:
            with open(schema_file, "r", encoding="utf-8") as f:
                schema = json.load(f)
        except Exception as e:
            print(f"Error loading schema: {e}")
            sys.exit(1)
        try:
            with open(instance_file, "r", encoding="utf-8") as f:
                instance = json.load(f)
        except Exception as e:
            print(f"Error loading instance: {e}")
            sys.exit(1)
        # Enable import processing.
        validator = JSONInstanceValidator(schema, allow_import=True)
        errors = validator.validate_instance(instance)
        if errors:
            print("Instance is invalid:")
            for err in errors:
                print(" -", err)
            sys.exit(1)
        else:
            print("Instance is valid.")

    if __name__ == "__main__":
        main()
