#!/bin/bash
poetry run coverage erase && \
poetry run coverage run --source dotty -m pytest && \
poetry run coverage html && \
poetry run coverage report -m
