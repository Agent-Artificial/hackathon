# docker-hackathon


## Quick-Start

Edit /ngrok/.env.example to with your ngrok auth key
Save as /ngrok/.env

Copy (and edit passwords) all of the .env.example files in subfolders

```
docker network create dev
docker compose up -d
```

When using docker compose up -d, you will get zero feedback.  Just go to your ngrok portal and find your endpoint.  Example: https://2b90-11-111-111-111.ngrok-free.app
That is your link to your environment.

## Setup

### Setup Networking

Create a network for the dev
```
docker network create dev
```

