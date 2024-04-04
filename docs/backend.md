# Backend

Antes de trabajar con el proyecto del backend hay que tener un entorno virtual

```bash
# pwd: Ft_Transcendence/Backend/Api
python3 -m venv venv #
```

Para usarlo solo hay que ejecutar lo siguiente

```bash
# pwd: Ft_Transcendence/Backend/Api
source venv/bin/activate
```

También es necesario configurar una BBDD de PostgreSQL, y configurar las variables de entorno en un archivo `.env`.

```bash
# pwd: Ft_Transcendence/Backend/Api
cp env.example .env
```

A partir de ahí podemos utilizar el script `manage.py` de Django para administrar el proyecto y ejecutarlo

```bash
# pwd: Ft_Transcendence/Backend/Api
python3 manage.py <command>
```
