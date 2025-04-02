#!/bin/bash
uvicorn classify:app --host 0.0.0.0 --port $PORT
