# Hiper
Utilizo Scrapy para recolectar información de productos puclicados.

Los datos requeridos son:
- Nombre de producto
- Precio regular (Precio de lista o precio tachado)
- Precio publicado (Precio online o precio - promocional)
- Categoría
- SKU (Deseable)
- URL del producto
- Stock (Deseable)
- Descripción

En el archivo **"diario.txt"** se resume el proceso dia a dia.

Ejecuto el proyecto con:
>scrapy crawl hiper

Se pueden agregar configuraciones mediante argumentos:

- Configurar multiples hilos para peticiones (default=16)
>scrapy crawl hiper -s CONCURRENT_REQUESTS=300

- Configurar multiples hilos para items (default=100)
>scrapy crawl hiper -s CONCURRENT_ITEMS=100

- Configurar proxy
>scrapy crawl hiper -a proxy="proxy.com"

- Configurar numero de sucursal
>scrapy crawl hiper -a sucursal=1

- Configurar nombre de archivo de salida
>scrapy crawl hiper -o archivo.csv
>scrapy crawl hiper -o archivo -t csv
>scrapy crawl hiper -O archivo.csv
