# encoding: utf-8
"""
Additional test-case for JSON Schema Import support.
This test spools two external schema files into a temporary directory and uses an import map
to load them for a local schema that uses $import and $importdefs.
"""

import json
from json_schema_validator_core import validate_json_schema_core

def test_import_with_temp_files(tmp_path):
    """
    Test that external schemas are correctly imported from files when using --allowimport
    and an import map.
    """
    # Define external schemas.
    external_schema_person = {
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "https://example.com/schema/person",
        "name": "Person",
        "type": "object",
        "properties": {
            "firstName": {"type": "string"},
            "lastName": {"type": "string"}
        }
    }
    external_schema_address = {
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "https://example.com/schema/address",
        "$root": "#/$defs/Address",
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
    }
    # Write external schemas to temporary files.
    person_file = tmp_path / "person.json"
    person_file.write_text(json.dumps(external_schema_person), encoding="utf-8")
    address_file = tmp_path / "address.json"
    address_file.write_text(json.dumps(external_schema_address), encoding="utf-8")
    
    # Create a local schema that uses $import and $importdefs.
    local_schema = {
        "$schema": "https://schemas.vasters.com/experimental/json-schema-core/v0",
        "$id": "https://example.com/schema/local",
        "name": "LocalSchema",
        "type": "object",
        "properties": {
            "person": {
                "type": { "$ref": "#/$defs/People/Person" }
            },
            "address": {
                "type": { "$ref": "#/$defs/Addresses/Address" }
            }
        },
        "$defs": {
            "People": {
                "$import": "https://example.com/schema/person"
            },
            "Addresses": {
                "$importdefs": "https://example.com/schema/address"
            }
        }
    }
    # Build an import map to override URI resolution.
    import_map = {
        "https://example.com/schema/person": str(person_file),
        "https://example.com/schema/address": str(address_file)
    }
    
    source_text = json.dumps(local_schema)
    errors = validate_json_schema_core(local_schema, source_text, allow_import=True, import_map=import_map)
    assert errors == []
