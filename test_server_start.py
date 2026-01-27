#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback

try:
    from flask import Flask
    print("[OK] Flask importado")
    
    from pacientes_db import GestorPacientes
    print("[OK] GestorPacientes importado")
    
    from medical_ai import AnalisisAIMedico
    print("[OK] AnalisisAIMedico importado")
    
    print("\n[OK] TODAS LAS IMPORTACIONES EXITOSAS")
    
except Exception as e:
    print(f"[ERROR] {e}")
    traceback.print_exc()
    sys.exit(1)
