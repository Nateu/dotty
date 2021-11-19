#!/usr/bin/env bash
poetry run coverage erase && \
poetry run coverage run --source pascal -m pytest && \
poetry run coverage html && \
poetry run coverage report -m
