"""Genera un informe de cobertura de documentación y trazabilidad.

Uso: python scripts/doc_report.py <min_cobertura> <salida.md>
Sale con código 1 si la cobertura de docstrings es menor al mínimo o si
Doxygen dejó advertencias, para que Jenkins marque el build como UNSTABLE.
"""
import ast
import datetime
import os
import subprocess
import sys

EXCLUIR = {'venv', 'docs', 'tests', 'jenkins', '.git'}


def git(*args):
    """Ejecuta un comando git y devuelve su salida, o 'n/d' si falla."""
    try:
        return subprocess.check_output(['git', *args], text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except Exception:
        return 'n/d'


def cobertura():
    """Cuenta funciones y clases con y sin docstring."""
    total, doc, faltan = 0, 0, []
    for raiz, dirs, archivos in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUIR]
        for a in archivos:
            if not a.endswith('.py'):
                continue
            ruta = os.path.join(raiz, a)
            arbol = ast.parse(open(ruta, encoding='utf-8').read())
            for nodo in ast.walk(arbol):
                if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    total += 1
                    if ast.get_docstring(nodo):
                        doc += 1
                    else:
                        faltan.append(f'{ruta}:{nodo.lineno} {nodo.name}')
    return total, doc, faltan


def main():
    """Genera el informe y devuelve código 1 si hay problemas."""
    minimo = float(sys.argv[1]) if len(sys.argv) > 1 else 80
    salida = sys.argv[2] if len(sys.argv) > 2 else 'docs/doc-report.md'
    total, doc, faltan = cobertura()
    pct = 100.0 * doc / total if total else 100.0
    log = 'docs/doxygen-warnings.log'
    warnings = []
    if os.path.exists(log):
        warnings = [l for l in open(log, encoding='utf-8') if l.strip()]

    os.makedirs(os.path.dirname(salida) or '.', exist_ok=True)
    with open(salida, 'w', encoding='utf-8') as f:
        f.write('# Informe de documentación y trazabilidad\n\n')
        f.write(f'- Fecha: {datetime.datetime.now().isoformat(timespec="seconds")}\n')
        f.write(f'- Build Jenkins: #{os.getenv("BUILD_NUMBER", "local")}\n')
        f.write(f'- Commit: {git("rev-parse", "--short", "HEAD")}\n')
        f.write(f'- Autor del commit: {git("log", "-1", "--format=%an <%ae>")}\n')
        f.write(f'- Mensaje: {git("log", "-1", "--format=%s")}\n')
        f.write(f'- Cobertura de docstrings: {doc}/{total} ({pct:.1f} %), mínimo {minimo:.0f} %\n')
        f.write(f'- Advertencias de Doxygen: {len(warnings)}\n\n')
        if faltan:
            f.write('## Elementos sin documentar\n\n')
            f.writelines(f'- {x}\n' for x in faltan)
        if warnings:
            f.write('\n## Advertencias de Doxygen\n\n')
            f.writelines(f'- {w.strip()}\n' for w in warnings)
        f.write('\n## Últimos commits\n\n')
        f.write(git('log', '-5', '--format=- %h %ad %an: %s', '--date=short') + '\n')

    print(open(salida, encoding='utf-8').read())
    if pct < minimo or warnings:
        print('ALERTA: problemas de documentación detectados')
        sys.exit(1)


if __name__ == '__main__':
    main()
