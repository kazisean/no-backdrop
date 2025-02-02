#!/bin/bash


docker build -t nobgimg .
docker tag nobgimg us-east4-docker.pkg.dev/no-backdrop/nobg/nobgimg:v1.0.0
docker push us-east4-docker.pkg.dev/no-backdrop/nobg/nobgimg:v1.0.0
