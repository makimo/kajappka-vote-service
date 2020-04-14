# kajappka-vote-service

## Development
Use following command to start development server:

```
docker-compose -f docker/development/docker-compose.yml up
```

then go to `http://localhost:8000` to verify if the containers has started.

## Build production image
```
docker build -f .\docker\production\Dockerfile -t kajappka-vote-service:latest .
```

## Run production image
```
docker run --rm -it -p 8080:8080 -e DATABASE_URI=mongodb://<username>:<password>@<host>:27017 -e AUTH_URL=http://localhost:8080/mock-auth/token-response -e DATABASE=votes kajappka-vote-service:latest
```
