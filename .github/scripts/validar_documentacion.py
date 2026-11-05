"""Valida estructura Markdown y enlaces internos sin depender de la red."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

RAIZ = Path(__file__).resolve().parents[2]
PATRON_ENLACE = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
PATRON_TITULO = re.compile(r"^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$")


def slug(texto: str) -> str:
    texto = re.sub(r"<[^>]+>", "", texto).lower()
    texto = re.sub(r"[`*_~]", "", texto)
    texto = re.sub(r"[^\w\s-]", "", texto, flags=re.UNICODE)
    return re.sub(r"\s", "-", texto).strip("-")


def anclas(archivo: Path) -> set[str]:
    vistas: dict[str, int] = {}
    resultado: set[str] = set()
    en_bloque = False
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        if linea.strip().startswith("```"):
            en_bloque = not en_bloque
            continue
        if en_bloque:
            continue
        coincidencia = PATRON_TITULO.match(linea)
        if not coincidencia:
            continue
        base = slug(coincidencia.group(2))
        numero = vistas.get(base, 0)
        vistas[base] = numero + 1
        resultado.add(base if numero == 0 else f"{base}-{numero}")
    return resultado


def destino(origen: Path, enlace: str) -> tuple[Path, str] | None:
    enlace = enlace.strip().strip("<>")
    if not enlace or enlace.startswith(("http://", "https://", "mailto:", "tel:")):
        return None
    ruta, separador, fragmento = unquote(enlace).partition("#")
    ruta = ruta.split("?", 1)[0]
    archivo = (origen.parent / ruta).resolve() if ruta else origen.resolve()
    return archivo, fragmento if separador else ""


def main() -> int:
    errores: list[str] = []
    argumentos = [Path(argumento) for argumento in sys.argv[1:]]
    archivos = sorted((RAIZ / archivo).resolve() for archivo in argumentos) if argumentos else sorted(RAIZ.rglob("*.md"))
    for archivo in archivos:
        if not archivo.is_file() or archivo.suffix.lower() != ".md" or RAIZ not in archivo.parents:
            errores.append(f"Archivo Markdown inválido: {archivo}")
    if errores:
        print("Validación fallida:", *errores, sep="\n- ")
        return 1
    cache_anclas: dict[Path, set[str]] = {}
    for archivo in archivos:
        relativo = archivo.relative_to(RAIZ)
        lineas = archivo.read_text(encoding="utf-8").splitlines()
        en_bloque = False
        titulos_h1 = 0
        for linea in lineas:
            if linea.strip().startswith("```"):
                en_bloque = not en_bloque
                continue
            if not en_bloque and re.match(r"^ {0,3}#\s+", linea):
                titulos_h1 += 1
        if titulos_h1 != 1:
            errores.append(f"{relativo}: debe tener exactamente un título H1 (actual: {titulos_h1}).")
        for numero, linea in enumerate(lineas, start=1):
            for coincidencia in PATRON_ENLACE.finditer(linea):
                referencia = destino(archivo, coincidencia.group(1))
                if referencia is None:
                    continue
                objetivo, fragmento = referencia
                if not objetivo.exists():
                    errores.append(f"{relativo}:{numero}: no existe el destino local «{coincidencia.group(1)}».")
                    continue
                if fragmento:
                    disponibles = cache_anclas.setdefault(objetivo, anclas(objetivo))
                    if fragmento not in disponibles:
                        errores.append(f"{relativo}:{numero}: no existe el ancla «#{fragmento}» en {objetivo.relative_to(RAIZ)}.")
    if errores:
        print("Validación fallida:", *errores, sep="\n- ")
        return 1
    print(f"Validación correcta: {len(archivos)} archivos Markdown y sus enlaces locales.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
