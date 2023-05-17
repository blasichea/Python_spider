import json

# Función para generar parte de las urls de categorias

f = open("hiper.txt", "r")
leer = f.read()
f.close()

json_cat = json.loads(leer)

# Toma un string y lo convierte en minusculas.
# Luego si encuentra no_admitido, lo cambia por reemplazo
def formato_url(camino):
	no_admitido = ['á', 'é', 'í', 'ó', 'ú', 'ñ', '!', ' ', ',']
	reemplazo = ['a', 'e', 'i', 'o', 'u', 'n', '-', '-', '']
	camino = camino.lower()
	for caracter in no_admitido:
		camino = camino.replace(caracter, reemplazo[no_admitido.index(caracter)])
	return camino


# Explora un dict concatenando el name y el de sus hijos
# Le da formato apto para una url
def caminar(dic, camino):
	camino += formato_url(dic.get("name")) + "/"
	if dic.get("hasChildren"):
		for child in dic.get("children"):
			caminar(child, camino)
	else:
		print(camino)

for child in json_cat:
	caminar(child, "")

