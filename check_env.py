import sys
import platform
import random
import math
import unittest

def test_environment():
    print("=" * 50)
    print("COMPILER GA OPTIMIZER - ENVIRONMENT STATUS")
    print("=" * 50)
    print(f"Python Executable : {sys.executable}")
    print(f"Python Version    : {sys.version.split()[0]}")
    print(f"Platform          : {platform.system()} ({platform.machine()})")
    print("Standard Libraries: OK (random, math, unittest loaded)")
    print("=" * 50)
    print("STATUS: Environment is verified and ready.")

if __name__ == '__main__':
    test_environment()
