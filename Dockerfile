FROM ubuntu:latest
LABEL authors="d.sergeev"

ENTRYPOINT ["top", "-b"]