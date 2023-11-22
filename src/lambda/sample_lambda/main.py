"""Sample Lambda."""
import json

def lambda_handler(
    event: dict,
    context: dict
) -> None:
    """This is the main of our lambda."""
    # Do something here

    return {
        "status": 200,
        "body": json.dumps("Hello from Lambda!")
    }