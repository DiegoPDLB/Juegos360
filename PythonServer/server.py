from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

# Leer el archivo del mapa
def cargar_mapa(path="final.txt"):
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    
    mapa = []
    for row in lines[:6]:  # Las primeras 6 líneas son el mapa
        fila = []
        for celda in row.split():
            fila.append({"paredes": celda})  # paredes: arriba, izquierda, abajo, derecha
        mapa.append(fila)
    return mapa

class Server(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        mapa = cargar_mapa("final.txt")  # asegúrate de tener final.txt en la misma carpeta

        response = {
            "mapa": mapa,
            "mensaje": "Mapa cargado con éxito desde Python"
        }

        self._set_response()
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"Servidor iniciado en puerto {port}...\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info("Servidor detenido.")

if __name__ == '__main__':
    run()
