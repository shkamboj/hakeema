import os
import argparse


def validate_file_path(file_path):
    if not os.path.exists(file_path):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError(f"{file_path} does not exist")
    return file_path
