#!/usr/bin/env python3
"""Atalho: gera o site inteiro (blog incluído). Veja ferramentas/gerar_site.py."""
import runpy, pathlib
runpy.run_path(str(pathlib.Path(__file__).with_name("gerar_site.py")), run_name="__main__")
