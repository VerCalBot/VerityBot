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

### First Time docker compose notes
You need to set a password for kibana_system after you first run compose up or Kibana won't communicate properly due to an authentication issue. 
Run the following command 
docker exec -it elasticsearch bin/elasticsearch-reset-password -u kibana_system -i
Enter the new password, then compose down. If you see your .env with the password for kibana_system then compose back up and you should be good.


Additional setup might be needed as the project progresses.
