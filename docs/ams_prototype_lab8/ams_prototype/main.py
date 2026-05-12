"""
Entry point para o AMS Intake Platform — Desktop Prototype.
Corre a partir desta pasta:
    python main.py
"""
import sys
import os

# Garante que os imports relativos funcionam quando se corre a partir de fora
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app import main

if __name__ == "__main__":
    main()
