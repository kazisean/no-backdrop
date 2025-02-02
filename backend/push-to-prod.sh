#!/bin/bash


docker build -t nobgimg .
docker tag nobgimg us-east4-docker.pkg.dev/no-backdrop/nobg/nobgimg:latest
docker push us-east4-docker.pkg.dev/no-backdrop/nobg/nobgimg:latest