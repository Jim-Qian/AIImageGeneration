#!/bin/bash
source /home/ec2-user/AIImageGeneration/env/bin/activate
export PYTHONPATH=Backend
export FLASK_APP=controller2
flask run --host=0.0.0.0