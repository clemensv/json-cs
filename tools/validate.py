import json
import argparse
import jsonschema
from jsonschema import Draft7Validator
import os

# Load the JSON-CS metaschema from an external file
METASCHEMA_PATH = os.path.join(os.path.dirname(__file__), "../metaschemas/jsons-draft-07.json")

def load_metaschema(path: str) -> dict:
    """
    Loads the JSON-CS metaschema from the specified file.

    Args:
        path (str): Path to the metaschema file.

    Returns:
        dict: The loaded metaschema.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_json_cs_document(document: dict, metaschema: dict) -> None:
    """
    Validates a JSON-CS document against the JSON-CS metaschema.

    Args:
        document (dict): The JSON-CS document to validate.
        metaschema (dict): The JSON-CS metaschema.

    Raises:
        jsonschema.exceptions.ValidationError: If the document is invalid.
        jsonschema.exceptions.SchemaError: If the metaschema is invalid.
    """
    validator = Draft7Validator(metaschema)
    validator.validate(document)
    print("The JSON-CS document is valid.")

def main():
    """
    Main function to validate a JSON-CS document.
    """
    parser = argparse.ArgumentParser(description="Validate a JSON-CS document against the JSON-CS metaschema.")
    parser.add_argument("input_file", help="Path to the JSON-CS document file to validate.")
    args = parser.parse_args()

    # Load the metaschema
    metaschema = load_metaschema(METASCHEMA_PATH)

    # Load the input JSON-CS document
    with open(args.input_file, "r", encoding="utf-8") as f:
        json_cs_document = json.load(f)

    try:
        validate_json_cs_document(json_cs_document, metaschema)
    except jsonschema.exceptions.ValidationError as e:
        print("Validation error:", e.message)
    except jsonschema.exceptions.SchemaError as e:
        print("Schema error:", e.message)

if __name__ == "__main__":
    main()
