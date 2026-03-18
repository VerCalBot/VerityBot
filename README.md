# **VerityBot - Subject to change**
The project will allow for exploration of data pulled from the Verkada API.

## Requirements
Python 3.x

## Environment Variables
This project uses an external API and requires environment variables to be set refer to .env.example.

## Project Structure
src\
    main.py
    utils.py
    Verkada.py
.env.example
.gitignore
compose.yaml
Dockerfile
README.md
requirements.txt


## Notes

### First Time Setup

Clone the repository.

Create your environment file from the .env template. \
```cp .env.example .env```

Open the ```.env``` and set secrets.

Make the setup script executable. \
```chmod +x ./scripts/initial_script.sh```

run the script. \
```./scripts/initial_script.sh```

When prompted enter the password for the user account ```kibana_system```. \
**Note**: This should be the same password as the one you placed in ```.env``` for ```KIBANA_SYSTEM_PASSWORD```.

When you see *Setup Complete*, wait until the containers finish starting. \
Use ```docker compose ps``` to check each containers status.

Once containers are fully running, then open Kibana. \
```https://localhost:5601```

log in with the following:
Username: elastic
Password: The value you set in your ```.env``` file for ```ELASTIC_PASSWORD```