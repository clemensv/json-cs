# encoding: utf-8
"""
test_instance_validator.py

Pytest-based test suite for instance_validator.py,
which validates JSON document instances against full JSON Schema Core schemas,
including support for:
  - Primitive types and compound types.
  - Extended constructs: abstract types, $extends, $offers/$uses.
  - Import extension: $import and $importdefs with import map support.
  - $ref resolution via JSON Pointer.
  - Validation addins (numeric, string, array, object constraints, "has", dependencies, etc.)
  - Conditional composition (allOf, anyOf, oneOf, not, if/then/else).
  - Automatic addin enabling when using the extended metaschema.

This suite is designed to achieve 100% code coverage of the instance validator.
"""

import json
import pytest
import uuid
import os
from json_validator_core import JSONInstanceValidator

# -------------------------------------------------------------------
# Helper Schemas for $ref, $extends, and Add-ins
# -------------------------------------------------------------------

BASE_OBJECT_SCHEMA = {
    "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
    "$id": "https://example.com/schemas/base",
    "name": "BaseObject",
    "type": "object",
    "properties": {
        "baseProp": {"type": "string"}
    }
}

DERIVED_SCHEMA_VALID = {
    "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
    "$id": "https://example.com/schemas/derived",
    "name": "DerivedObject",
    "type": "object",
    "$extends": "#/$defs/BaseObject",
    "properties": {}  # Derived does not redefine inherited properties.
}

ABSTRACT_SCHEMA = {
    "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
    "$id": "https://example.com/schemas/abstract",
    "name": "AbstractType",
    "type": "object",
    "abstract": True,
    "properties": {
        "abstractProp": {"type": "string"}
    }
}

ADDIN_SCHEMA = {
    "properties": {
        "addinProp": {"type": "number"}
    }
}

ROOT_OFFERS_SCHEMA = {
    "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
    "$id": "https://example.com/schemas/root",
    "name": "RootSchema",
    "type": "object",
    "properties": {
        "main": {"type": "string"}
    },
    "$offers": {
        "Extra": ADDIN_SCHEMA
    }
}

# -------------------------------------------------------------------
# Primitive Types Tests
# -------------------------------------------------------------------


def test_string_valid():
    schema = {"type": "string", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "strSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("hello")
    assert errors == []


def test_string_invalid():
    schema = {"type": "string", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "strSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(123)
    assert any("Expected string" in err for err in errors)


def test_number_valid():
    schema = {"type": "number", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "numSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(3.14)
    assert errors == []


def test_number_invalid():
    schema = {"type": "number", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "numSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("3.14")
    assert any("Expected number" in err for err in errors)


def test_boolean_valid():
    schema = {"type": "boolean", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "boolSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(True)
    assert errors == []


def test_boolean_invalid():
    schema = {"type": "boolean", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "boolSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("true")
    assert any("Expected boolean" in err for err in errors)


def test_null_valid():
    schema = {"type": "null", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "nullSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(None)
    assert errors == []


def test_null_invalid():
    schema = {"type": "null", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "nullSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(0)
    assert any("Expected null" in err for err in errors)

# -------------------------------------------------------------------
# Integer and Floating Point Tests (Numeric Validation Addins)
# -------------------------------------------------------------------


def test_int32_valid():
    schema = {"type": "int32", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "int32Schema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(123)
    assert errors == []


def test_int32_out_of_range():
    schema = {"type": "int32", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "int32Schema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(2**31)
    assert any("out of range" in err for err in errors)


def test_uint32_valid():
    schema = {"type": "uint32", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "uint32Schema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(123)
    assert errors == []


def test_uint32_negative():
    schema = {"type": "uint32", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "uint32Schema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(-1)
    assert any("out of range" in err for err in errors)


def test_int64_valid():
    schema = {"type": "int64", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "int64Schema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("1234567890")
    assert errors == []


def test_int64_invalid_format():
    schema = {"type": "int64", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "int64Schema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(1234567890)
    assert any("Expected int64 as string" in err for err in errors)


def test_uint64_valid():
    schema = {"type": "uint64", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "uint64Schema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("1234567890")
    assert errors == []


def test_uint64_invalid_format():
    schema = {"type": "uint64", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "uint64Schema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(1234567890)
    assert any("Expected uint64 as string" in err for err in errors)


def test_float_valid():
    schema = {"type": "float", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "floatSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(1.23)
    assert errors == []


def test_float_invalid():
    schema = {"type": "float", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "floatSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("1.23")
    assert any("Expected float" in err for err in errors)


def test_decimal_valid():
    schema = {"type": "decimal", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "decimalSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("123.45")
    assert errors == []


def test_decimal_invalid():
    schema = {"type": "decimal", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "decimalSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(123.45)
    assert any("Expected decimal as string" in err for err in errors)


def test_numeric_minimum_fail():
    schema = {"type": "number", "minimum": 10,
              "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0", "$id": "dummy", "name": "numMin"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(5)
    assert any("less than minimum" in err for err in errors)


def test_numeric_minimum_pass():
    schema = {"type": "number", "minimum": 10,
              "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0", "$id": "dummy", "name": "numMin"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(10)
    assert errors == []


def test_numeric_maximum_fail():
    schema = {"type": "number", "maximum": 100,
              "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0", "$id": "dummy", "name": "numMax"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(150)
    assert any("greater than maximum" in err for err in errors)


def test_numeric_exclusiveMinimum_fail():
    schema = {"type": "number", "minimum": 10, "exclusiveMinimum": True,
              "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0", "$id": "dummy", "name": "numExMin"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(10)
    assert any("not greater than exclusive minimum" in err for err in errors)


def test_numeric_exclusiveMaximum_fail():
    schema = {"type": "number", "maximum": 100, "exclusiveMaximum": True,
              "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0", "$id": "dummy", "name": "numExMax"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(100)
    assert any("not less than exclusive maximum" in err for err in errors)


def test_numeric_multipleOf_fail():
    schema = {"type": "number", "multipleOf": 5,
              "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0", "$id": "dummy", "name": "numMult"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(12)
    assert any("not a multiple of" in err for err in errors)


def test_numeric_multipleOf_pass():
    schema = {"type": "number", "multipleOf": 5,
              "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0", "$id": "dummy", "name": "numMult"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(15)
    assert errors == []

# -------------------------------------------------------------------
# Date, Time, and Datetime Tests
# -------------------------------------------------------------------


def test_date_valid():
    schema = {"type": "date", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "dateSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("2025-03-05")
    assert errors == []


def test_date_invalid():
    schema = {"type": "date", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "dateSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("03/05/2025")
    assert any("Expected date" in err for err in errors)


def test_datetime_valid():
    schema = {"type": "datetime", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "datetimeSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("2025-03-05T12:34:56Z")
    assert errors == []


def test_datetime_invalid():
    schema = {"type": "datetime", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "datetimeSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("2025-03-05 12:34:56")
    assert any("Expected datetime" in err for err in errors)


def test_time_valid():
    schema = {"type": "time", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "timeSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("12:34:56")
    assert errors == []


def test_time_invalid():
    schema = {"type": "time", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "timeSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("123456")
    assert any("Expected time" in err for err in errors)

# -------------------------------------------------------------------
# UUID and URI Tests
# -------------------------------------------------------------------


def test_uuid_valid():
    valid_uuid = str(uuid.uuid4())
    schema = {"type": "uuid", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "uuidSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(valid_uuid)
    assert errors == []


def test_uuid_invalid():
    schema = {"type": "uuid", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "uuidSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("not-a-uuid")
    assert any("Invalid uuid format" in err for err in errors)


def test_uri_valid():
    schema = {"type": "uri", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "uriSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("https://example.com")
    assert errors == []


def test_uri_invalid():
    schema = {"type": "uri", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "uriSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("example.com")
    assert any("Invalid uri format" in err for err in errors)

# -------------------------------------------------------------------
# Binary and JSON Pointer Tests
# -------------------------------------------------------------------


def test_binary_valid():
    schema = {"type": "binary", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "binarySchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("YWJjMTIz")  # base64 for 'abc123'
    assert errors == []


def test_binary_invalid():
    schema = {"type": "binary", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "binarySchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(12345)
    assert any("Expected binary" in err for err in errors)


def test_jsonpointer_valid():
    schema = {"type": "jsonpointer", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "jpSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("#/a/b")
    assert errors == []


def test_jsonpointer_invalid():
    schema = {"type": "jsonpointer", "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
              "$id": "dummy", "name": "jpSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("a/b")
    assert any("Expected JSON pointer" in err for err in errors)

# -------------------------------------------------------------------
# Compound Types Tests: object, array, set, map, tuple
# -------------------------------------------------------------------


def test_object_valid():
    schema = {
        "type": "object",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "objSchema",
        "properties": {
            "a": {"type": "string"},
            "b": {"type": "number"}
        },
        "required": ["a"]
    }
    instance = {"a": "test", "b": 123}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert errors == []


def test_object_missing_required():
    schema = {
        "type": "object",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "objSchema",
        "properties": {"a": {"type": "string"}},
        "required": ["a"]
    }
    instance = {"b": "oops"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert any("Missing required property" in err for err in errors)


def test_object_additional_properties_false():
    schema = {
        "type": "object",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "objSchema",
        "properties": {"a": {"type": "string"}},
        "additionalProperties": False
    }
    instance = {"a": "ok", "b": "not allowed"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert any("Additional property 'b'" in err for err in errors)


def test_array_valid():
    schema = {
        "type": "array",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "arraySchema",
        "items": {"type": "string"}
    }
    instance = ["a", "b", "c"]
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert errors == []


def test_array_invalid():
    schema = {
        "type": "array",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "arraySchema",
        "items": {"type": "number"}
    }
    instance = [1, "two", 3]
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert any("Expected number" in err for err in errors)


def test_set_valid():
    schema = {
        "type": "set",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "setSchema",
        "items": {"type": "string"}
    }
    instance = ["a", "b", "c"]
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert errors == []


def test_set_duplicate():
    schema = {
        "type": "set",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "setSchema",
        "items": {"type": "string"}
    }
    instance = ["a", "b", "a"]
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert any("duplicate items" in err for err in errors)


def test_map_valid():
    schema = {
        "type": "map",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "mapSchema",
        "values": {"type": "number"}
    }
    instance = {"key1": 1, "key2": 2}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert errors == []


def test_tuple_valid():
    schema = {
        "type": "tuple",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "tupleSchema",
        "properties": {
            "first": {"type": "string"},
            "second": {"type": "number"}
        }
    }
    instance = ["hello", 42]
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert errors == []


def test_tuple_wrong_length():
    schema = {
        "type": "tuple",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "tupleSchema",
        "properties": {
            "first": {"type": "string"},
            "second": {"type": "number"}
        }
    }
    instance = ["only one"]
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert any("does not equal expected" in err for err in errors)

# -------------------------------------------------------------------
# Union Type Tests
# -------------------------------------------------------------------


def test_union_valid():
    schema = {
        "type": ["string", "number"],
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "unionSchema"
    }
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("a union")
    assert errors == []


def test_union_invalid():
    schema = {
        "type": ["string", "number"],
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "unionSchema"
    }
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(True)
    assert any("does not match any type in union" in err for err in errors)

# -------------------------------------------------------------------
# const and enum Tests
# -------------------------------------------------------------------


def test_const_valid():
    schema = {"type": "number", "const": 3.14,
              "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0", "$id": "dummy", "name": "constSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(3.14)
    assert errors == []


def test_const_invalid():
    schema = {"type": "number", "const": 3.14,
              "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0", "$id": "dummy", "name": "constSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(2.71)
    assert any("does not equal const" in err for err in errors)


def test_enum_valid():
    schema = {"type": "string", "enum": [
        "a", "b", "c"], "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0", "$id": "dummy", "name": "enumSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("b")
    assert errors == []


def test_enum_invalid():
    schema = {"type": "string", "enum": [
        "a", "b", "c"], "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0", "$id": "dummy", "name": "enumSchema"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance("d")
    assert any("not in enum" in err for err in errors)

# -------------------------------------------------------------------
# $ref Resolution Tests (using $defs)
# -------------------------------------------------------------------


def test_ref_resolution_valid():
    schema = {
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "refSchema",
        "type": "object",
        "properties": {
            "value": {"type": {"$ref": "#/$defs/RefType"}}
        },
        "$defs": {
            "RefType": {"name": "RefType", "type": "string"}
        }
    }
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance({"value": "test"})
    assert errors == []


def test_ref_resolution_invalid():
    schema = {
        "type": "object",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "refSchema",
        "properties": {
            "value": {"type": {"$ref": "#/$defs/NonExistent"}}
        },
        "$defs": {}
    }
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance({"value": "test"})
    assert any("Cannot resolve $ref" in err for err in errors)

# -------------------------------------------------------------------
# $extends Tests
# -------------------------------------------------------------------


def test_extends_valid():
    root_schema = {
        "type": "object",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "Root",
        "properties": {"child": DERIVED_SCHEMA_VALID},
        "$defs": {"BaseObject": BASE_OBJECT_SCHEMA}
    }
    instance = {"child": {"baseProp": "hello"}}
    validator = JSONInstanceValidator(root_schema)
    errors = validator.validate_instance(instance)
    assert errors == []


def test_extends_conflict():
    derived_conflict = {
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "DerivedConflict",
        "type": "object",
        "$extends": "#/$defs/BaseObject",
        "properties": {"baseProp": {"type": "number"}}
    }
    root_schema = {
        "type": "object",
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "Root",
        "properties": {"child": derived_conflict},
        "$defs": {"BaseObject": BASE_OBJECT_SCHEMA}
    }
    instance = {"child": {"baseProp": "should be string"}}
    validator = JSONInstanceValidator(root_schema)
    errors = validator.validate_instance(instance)
    assert any("inherited via $extends" in err for err in errors)

# -------------------------------------------------------------------
# Abstract Schema Test
# -------------------------------------------------------------------


def test_abstract_schema_usage():
    schema = ABSTRACT_SCHEMA
    instance = {"abstractProp": "hello"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert any("Abstract schema" in err for err in errors)

# -------------------------------------------------------------------
# $offers/$uses (Add-In Types) Tests
# -------------------------------------------------------------------


def test_uses_addin():
    schema = ROOT_OFFERS_SCHEMA
    instance = {"main": "hello", "$uses": ["Extra"], "extra": 123}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert errors == []


def test_uses_addin_conflict():
    schema = {
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "dummy",
        "name": "ConflictSchema",
        "type": "object",
        "properties": {"main": {"type": "string"}, "extra": {"type": "string"}},
        "$offers": {
            "Extra": {"properties": {"extra": {"type": "number"}}}
        }
    }
    instance = {"main": "hello", "$uses": ["Extra"], "extra": 123}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert any("conflicts with existing property" in err for err in errors)

# -------------------------------------------------------------------
# Import Extension Tests ($import and $importdefs)
# -------------------------------------------------------------------


def test_import_and_importdefs(tmp_path):
    external_person = {
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "https://example.com/people.json",
        "name": "Person",
        "type": "object",
        "properties": {
            "firstName": {"type": "string"},
            "lastName": {"type": "string"}
        }
    }
    external_importdefs = {
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "https://example.com/importdefs.json",
        "$defs": {
            "LibraryType": {"name": "LibraryType", "type": "string"}
        }
    }
    person_file = tmp_path / "people.json"
    person_file.write_text(json.dumps(external_person), encoding="utf-8")
    importdefs_file = tmp_path / "importdefs.json"
    importdefs_file.write_text(json.dumps(external_importdefs), encoding="utf-8")

    local_schema = {
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "https://example.com/schema/local",
        "name": "LocalSchema",
        "type": "object",
        "properties": {
            "person": {"type": {"$ref": "#/Person"}},
            "library": {"type": {"$ref": "#/LibraryType"}}
        },
        "$import": "https://example.com/people.json",
        "$importdefs": "https://example.com/importdefs.json"
    }
    import_map = {
        "https://example.com/people.json": str(person_file),
        "https://example.com/importdefs.json": str(importdefs_file)
    }
    instance = {
        "person": {"firstName": "Alice", "lastName": "Smith"},
        "library": "CentralLibrary"
    }
    validator = JSONInstanceValidator(local_schema, allow_import=True, import_map=import_map)
    errors = validator.validate_instance(instance)
    assert errors == []

# -------------------------------------------------------------------
# Validation Addins Tests
# -------------------------------------------------------------------


def test_validation_addins_numeric_fail():
    schema = {
        "type": "number",
        "minimum": 10,
        "maximum": 20,
        "multipleOf": 3,
        "$id": "dummy",
        "name": "numValidation"
    }
    instance = 8  # below minimum and not a multiple of 3
    instance_obj = {"value": instance, "$uses": ["Validation"]}
    # Wrap the number in an object for $uses to be available
    schema_obj = {
        "type": "object", "properties": {"value": schema},
        "$schema": "https://schemas.vasters.com/experimental/json-schema-validation/v0", 
        "$id": "dummy", "name": "wrapper"}
    validator = JSONInstanceValidator(schema_obj)
    errors = validator.validate_instance(instance_obj)
    assert any("less than minimum" in err for err in errors)
    instance_obj["value"] = 21  # above maximum and not a multiple of 3
    errors = validator.validate_instance(instance_obj)
    assert any("greater than maximum" in err for err in errors)


def test_validation_addins_string_fail():
    schema = {
        "type": "string",
        "minLength": 5,
        "pattern": "^[A-Z]+$",
        "$id": "dummy",
        "name": "strValidation"
    }
    instance = "abc"
    instance_obj = {"value": instance, "$uses": ["Validation"]}
    schema_obj = {"type": "object", "properties": {"value": schema},
                  "$schema": "https://schemas.vasters.com/experimental/json-schema-validation/v0", "$id": "dummy", "name": "wrapper"}
    validator = JSONInstanceValidator(schema_obj)
    errors = validator.validate_instance(instance_obj)
    assert any("shorter than minLength" in err for err in errors)
    instance_obj["value"] = "abcde"
    errors = validator.validate_instance(instance_obj)
    assert any("does not match pattern" in err for err in errors)


def test_validation_addins_array_fail():
    schema = {
        "type": "array",
        "minItems": 3,
        "maxItems": 5,
        "uniqueItems": True,
        "$id": "dummy",
        "name": "arrValidation"
    }
    instance = ["a", "b"]  # fewer than 3 items
    instance_obj = {"value": instance, "$uses": ["Validation"]}
    schema_obj = {"type": "object", "properties": {"value": schema},
                  "$schema": "https://schemas.vasters.com/experimental/json-schema-validation/v0", "$id": "dummy", "name": "wrapper"}
    validator = JSONInstanceValidator(schema_obj)
    errors = validator.validate_instance(instance_obj)
    assert any("fewer items than minItems" in err for err in errors)
    instance_obj["value"] = ["a", "b", "c", "d", "e", "f"]  # more than 5 items
    errors = validator.validate_instance(instance_obj)
    assert any("more items than maxItems" in err for err in errors)
    instance_obj["value"] = ["a", "b", "a"]  # duplicate items
    errors = validator.validate_instance(instance_obj)
    assert any("unique items" in err for err in errors)


def test_validation_addins_object_fail():
    schema = {
        "type": "object",
        "minProperties": 2,
        "maxProperties": 3,
        "name": "objValidation"
    }
    instance = {"a": "1"}  # fewer than 2 properties
    instance_obj = {"value": instance, "$uses": ["Validation"]}
    schema_obj = {"type": "object", "properties": {"value": schema},
                  "$schema": "https://schemas.vasters.com/experimental/json-schema-validation/v0", "$id": "dummy", "name": "wrapper"}
    validator = JSONInstanceValidator(schema_obj)
    errors = validator.validate_instance(instance_obj)
    assert any("fewer properties than minProperties" in err for err in errors)
    instance_obj["value"] = {"a": "1", "b": "2", "c": "3", "d": "4"}  # more than 3 properties
    errors = validator.validate_instance(instance_obj)
    assert any("more properties than maxProperties" in err for err in errors)


def test_validation_addins_object_dependencies():
    schema = {
        "type": "object",
        "properties": {
            "credit_card": {"type": "number"},
            "billing_address": {"type": "string"}
        },
        "dependentRequired": {"credit_card": ["billing_address"]},
        "name": "objDependencies"
    }
    instance = {"credit_card": 123456}
    instance_obj = {"value": instance, "$uses": ["Validation"]}
    schema_obj = {"type": "object", "properties": {"value": schema},
                  "$schema": "https://schemas.vasters.com/experimental/json-schema-validation/v0", "$id": "dummy", "name": "wrapper"}
    validator = JSONInstanceValidator(schema_obj)
    errors = validator.validate_instance(instance_obj)
    assert any("requires dependent property" in err for err in errors)


def test_validation_addins_object_patternProperties():
    schema = {
        "type": "object",
        "patternProperties": {"^[A-Z]": {"type": "string"}},
        "name": "objPatternProps"
    }
    instance = {"Aprop": "hello", "bprop": "world"}
    instance_obj = {"value": instance, "$uses": ["Validation"]}
    schema_obj = {"type": "object", "properties": {"value": schema},
                  "$schema": "https://schemas.vasters.com/experimental/json-schema-validation/v0", "$id": "dummy", "name": "wrapper"}
    validator = JSONInstanceValidator(schema_obj)
    errors = validator.validate_instance(instance_obj)
    # bprop does not match the pattern, but patternProperties doesn't force an error on non-matching keys.
    assert errors == []


def test_validation_addins_object_propertyNames_fail():
    schema = {
        "type": "object",
        "propertyNames": {"type": "string", "pattern": "^[a-z][a-zA-Z0-9]*$"},
        "name": "objPropNames"
    }
    instance = {"Aprop": "hello", "bprop": "world"}
    instance_obj = {"value": instance, "$uses": ["Validation"]}
    schema_obj = {"type": "object", "properties": {"value": schema},
                  "$schema": "https://schemas.vasters.com/experimental/json-schema-validation/v0", "$id": "dummy", "name": "wrapper"}
    validator = JSONInstanceValidator(schema_obj)
    errors = validator.validate_instance(instance_obj)
    assert any("does not match pattern" in err for err in errors)


def test_validation_addins_object_has_fail():
    schema = {
        "type": "object",
        "has": {"type": "string", "const": "required"},
        "name": "objHas"
    }
    instance = {"a": "foo", "b": 123}
    instance_obj = {"value": instance, "$uses": ["Validation"]}
    schema_obj = {"type": "object", "properties": {"value": schema},
                  "$schema": "https://schemas.vasters.com/experimental/json-schema-validation/v0", "$id": "dummy", "name": "wrapper"}
    validator = JSONInstanceValidator(schema_obj)
    errors = validator.validate_instance(instance_obj)
    assert any("does not have any property" in err for err in errors)

# -------------------------------------------------------------------
# Conditional Composition Tests
# -------------------------------------------------------------------


def test_if_then_else_then():
    schema = {
        "if": {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]},
        "then": {"type": "object", "properties": {"b": {"type": "number"}}, "required": ["b"]},
        "else": {"type": "object", "properties": {"c": {"type": "boolean"}}, "required": ["c"]},
        "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0",
        "$id": "dummy",
        "name": "ifThenElse"
    }
    instance = {"a": "hello", "b": 42, "$uses": ["Conditionals"]}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert errors == []


def test_if_then_else_else():
    schema = {
        "if": {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]},
        "then": {"type": "object", "properties": {"b": {"type": "number"}}, "required": ["b"]},
        "else": {"type": "object", "properties": {"c": {"type": "boolean"}}, "required": ["c"]},
        "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0",
        "$id": "dummy",
        "name": "ifThenElse"
    }
    instance = {"d": "not a", "c": False, "$uses": ["Conditionals"]}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert errors == []


def test_if_then_else_fail():
    schema = {
        "if": {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]},
        "then": {"type": "object", "properties": {"b": {"type": "number"}}, "required": ["b"]},
        "else": {"type": "object", "properties": {"c": {"type": "boolean"}}, "required": ["c"]},
        "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0",
        "$id": "dummy",
        "name": "ifThenElse"
    }
    instance = {"a": "hello", "c": True, "$uses": ["Conditionals"]}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert any("Missing required property 'b'" in err for err in errors)
    
def test_all_of():
    schema = {
        "allOf": [
            {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]},
            {"type": "object", "properties": {"b": {"type": "number"}}, "required": ["b"]}
        ],
        "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0",
        "$id": "dummy",
        "name": "allOf"
    }
    instance = {"a": "hello", "b": 42}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert errors == []
    
def test_all_of_fail():
    schema = {
        "allOf": [
            {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]},
            {"type": "object", "properties": {"b": {"type": "number"}}, "required": ["b"]}
        ],
        "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0",
        "$id": "dummy",
        "name": "allOf"
    }
    instance = {"a": "hello"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert any("Missing required property 'b'" in err for err in errors)
    
def test_any_of():
    schema = {
        "anyOf": [
            {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]},
            {"type": "object", "properties": {"b": {"type": "number"}}, "required": ["b"]}
        ],
        "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0",
        "$id": "dummy",
        "name": "anyOf"
    }
    instance = {"b": 42}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert errors == []
    
def test_any_of_fail():
    schema = {
        "anyOf": [
            {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]},
            {"type": "object", "properties": {"b": {"type": "number"}}, "required": ["b"]}
        ],
        "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0",
        "$id": "dummy",
        "name": "anyOf"
    }
    instance = {"c": 42}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert any("does not satisfy anyOf" in err for err in errors)
    
def test_one_of():
    schema = {
        "oneOf": [
            {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]},
            {"type": "object", "properties": {"b": {"type": "number"}}, "required": ["b"]}
        ],
        "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0",
        "$id": "dummy",
        "name": "oneOf"
    }
    instance = {"a": "hello"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert errors == []
    
def test_one_of_fail():
    schema = {
        "oneOf": [
            {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]},
            {"type": "object", "properties": {"b": {"type": "number"}}, "required": ["b"]}
        ],
        "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0",
        "$id": "dummy",
        "name": "oneOf"
    }
    instance = {"a": "hello", "b": 42}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert any("must match exactly one" in err for err in errors)
    
def test_not():
    schema = {
        "not": {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]},
        "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0",
        "$id": "dummy",
        "name": "not"
    }
    instance = {"b": 42}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert errors == []
    
def test_not_fail():
    schema = {
        "not": {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]},
        "$schema": "https://schemas.vasters.com/experimental/json-schema-extended/v0",
        "$id": "dummy",
        "name": "not"
    }
    instance = {"a": "hello"}
    validator = JSONInstanceValidator(schema)
    errors = validator.validate_instance(instance)
    assert any("should not validate against 'not' schema" in err for err in errors)


# -------------------------------------------------------------------
# End of tests.
