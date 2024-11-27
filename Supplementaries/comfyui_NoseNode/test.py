import JsonFileManipulator
import json
def test_json_file_manipulator():
    # Creating a sample JSON data to test the functionality
    sample_data = {
        "Private": {
            "id": "private_info",
            "name": "Alex Johnson",
            "gender": "Male",
            "age": 76,
            "occupation": "Retired Teacher",
            "interests": ["Reading", "Gardening", "Bird Watching"]
        },
        "Relations": [
            {
                "id": "relation_1",
                "relation": "Daughter",
                "name": "Emily Johnson",
                "contact": "555-1234",
                "notes": "Suffers from allergies"
            },
            {
                "id": "relation_2",
                "relation": "Son",
                "name": "Michael Johnson",
                "contact": "555-5678",
                "notes": "Likes sports"
            },
            {
                "id": "relation_3",
                "relation": "Primary Doctor",
                "name": "Dr. Sarah Lee",
                "contact": "555-4321",
                "specialty": "Neurologist",
                "notes": ""
            },
            {
                "id": "relation_4",
                "relation": "Friend",
                "name": "Robert Williams",
                "contact": "555-8765",
                "notes": "Likes to play chess"
            }
        ]
    }

    # Create an instance of JsonFileManipulator
    manipulator = JsonFileManipulator()

    # Test case 1: Query action
    input_str_query = json.dumps({
        "action": "query",
        "file": "sample",
        "path": "Relations[relation='Daughter'].contact"
    })
    folder_path = "."  # Assuming current directory, modify accordingly

    # Mock file reading operation
    with open("sample.json", "w") as f:
        json.dump(sample_data, f, indent=4)

    # Perform the query
    result_query = manipulator.manipulate_json(input_str_query, folder_path)
    print("Query Result:", result_query)

    # Test case 2: Update action
    input_str_update = json.dumps({
        "action": "update",
        "file": "sample",
        "path": "Relations[relation='Daughter'].contact",
        "new_value": "555-9999"
    })

    # Perform the update
    result_update = manipulator.manipulate_json(input_str_update, folder_path)
    print("Update Result:", result_update)

    # Verify the update
    with open("sample.json", "r") as f:
        updated_data = json.load(f)
    print("Updated JSON Data:", json.dumps(updated_data, indent=4))

if __name__ == "__main__":
    test_json_file_manipulator()
