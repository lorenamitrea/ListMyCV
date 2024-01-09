# ListMyCV
## Build and start project
1. update requirements.txt file if it is needed
2. install/start docker desktop
3. run `docker compose build` command to build the containers for the apps
4. run `docker compose up` command to start the containers
## Execute Flask CLI
`docker compose exec api-service flask get <cv_section>`

cv_section must be one of these values: `'personal', 'experience', 'skills', 'education', 'achievements'`
## Run unit tests
`docker compose exec api-service pytest /code/webapp/tests`