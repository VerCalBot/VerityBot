## Example JSON Entry
Response (truncated) following GET request to: https://api.verkada.com/events/v1/access
```json
{
        "events":
        [{  "device_id": "0e0cbec9-599b-48ee-b9ad-ee7504e75056",
            "device_type": "ACCESS_CONTROL",
            "end_timestamp": null,
            "event_id": "138e604c-e979-4dcb-8b56-e555098bd155",
            "event_info": {
                "accepted": true,
                "auxInputId": null,
                "auxInputName": null,
                "buildingId": "6f66d225-f748-48d1-bf21-b54a472aade6",
                "buildingName": "SHA - Bldg 19",
                "direction": null,
                "doorId": "0e0cbec9-599b-48ee-b9ad-ee7504e75056",
                "doorInfo": {
                    "accessControllerId": "15f0c39d-f3aa-4bad-b742-c86e3275b7a6",
                    "accessControllerName": "AC42 - SHA (by Fire Panel)",
                    "name": "SHA - Double Doors To Gym"
                },
                "entityId": "0e0cbec9-599b-48ee-b9ad-ee7504e75056",
                "entityName": "SHA - Double Doors To Gym",
                "entityType": "door",
                "eventType": "user_action",
                "floorId": "6eddace7-fa59-4aee-877c-cc7ca336f90c",
                "floorName": "FL1 - Main",
                "floors": null,
                "inputValue": "40|5990",
                "lockdownInfo": null,
                "message": "Keycard Entered",
                "organizationId": "819624eb-0f81-4f29-9909-17de555dd64c",
                "rawCard": "10010100000010111011001100",
                "siteId": "a02a6b27-85e6-41d5-90e6-88611802fd92",
                "siteName": "SHA",
                "type": "keycard_entered_accepted",
                "userId": "999e99bf-9999-9dd9-99e9-d9c9d99be9fc",
                "userInfo": {
                    "email": "johndoe@example.com",
                    "firstName": "John",
                    "lastName": "Doe",
                    "name": "John Doe",
                    "organizationId": "819624eb-0f81-4f29-9909-17de555dd64c",
                    "phone": "999-999-9999",
                    "userId": "999e99bf-9999-9dd9-99e9-d9c9d99be9fc"
                },
                "userName": "John Doe",
                "uuid": "138e604c-e979-4dcb-8b56-e555098bd155"
            },
            "event_type": "DOOR_KEYCARD_ENTERED_ACCEPTED",
            "organization_id": "819624eb-0f81-4f29-9909-17de555dd64c",
            "site_id": "a02a6b27-85e6-41d5-90e6-88611802fd92",
            "timestamp": "2026-01-26T22:22:34Z"
        }]
}
