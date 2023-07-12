#!/usr/bin/python3
""" Class foor review"""

from models.base_model import BaseModel

class Review(BaseModel):
    """ Reps review class"""
    place_id = ""
    user_id = ""
    text = ""
