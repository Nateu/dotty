#!/usr/bin/env bash
poetry run coverage erase && \
poetry run mamba --enable-coverage --format=documentation ./spec/*_spec.py && \
poetry run coverage html && \
poetry run coverage report -m
