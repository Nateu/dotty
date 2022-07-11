#!/bin/bash
poetry run coverage erase && \
poetry run coverage run --source bot -m pytest && \
poetry run coverage html && \
poetry run coverage report -m
