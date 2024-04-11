
# Frontend

## PageManager

La clase `PageManager` es la encargada de cargar las páginas de la aplicación.
Su funcionamiento es muy sencillo:

1. Se le pasa un `path`
2. Se lanza una petición al back, que renderiza la página y la devuelve
3. Se inserta el HTML devuelto en el DOM en el contenedor `#root`
4. Se comprueba si hay algún callback asociado a la página anterior y se ejecuta
5. Se comprueba si hay algún callback asociado a la página nueva y se ejecuta
6. Se actualiza el historial de navegación

## Páginas

Para añadir una nueva página a la aplicación, se debe seguir los siguientes pasos:

1. Crear un nuevo archivo HTML en `templates` con el nombre de la página:
2. Si la página requiere CSS, añadirlo en `static/css`, y enlazarlo con el HTML siguiendo el patrón de Django
3. Si la página requiere JS, añadirlo en `static/js`, y enlazarlo al final del `body` del archivo `templates/index.html`. Si se importa algún módulo, el tipo de módulo debe ser `module` para que funcione correctamente.
4. Si la página requiere algún recurso adicional, añadirlo en `static` y enlazarlo en el HTML.
5. Si la página requiere contexto adicional, sigue los pasos de la sección [`Páginas con contexto`](#Paginas-con-contexto)

### Ejemplo

Para añadir una página de ejemplo llamada `example`, se deben seguir los siguientes pasos:

1. Crear un nuevo archivo `example.html` en `templates` con el siguiente contenido:

    ```html
    {% load static %}
    
    <link rel="stylesheet" href="{% static 'css/example.css' %}">
    <div id="example">
      <h1>Example</h1>
      <p>This is an example page</p>
      <button id="example-button" onclick="window.global.pageHandler.load('home')">Go home!</button>
      <button id="example-button2">Say hello world</button>
    </div>
    ```

2. Crear un nuevo archivo `example.css` en `static/css` con el siguiente contenido:

    ```css
    #example {
      text-align: center;
      margin-top: 50px;
    }
    ```

3. Crear un nuevo archivo `example.js` en `static/js` con el siguiente contenido:

    ```javascript
    import { PageManager } from './page-manager.js';
    
    document.getElementById('example-button2').addEventListener('click', () => {
      alert('Hello world!');
    });
    
    PageManager.getInstance().setOnPageLoad('example', () => {
      console.log('Example page loaded');
    });
    
    PageManager.getInstance().setOnPageUnload('example', () => {
      console.log('Example page unloaded');
    });
    ```

4. Añadir el siguiente enlace al final del `body` del archivo `templates/index.html`:

    ```html
    ...
    <script src="{% static 'js/example.js' %}" type="module"></script>
    ```

## Páginas con contexto

Para añadir contexto a una página, se debe seguir los siguientes pasos:

1. Crear una nueva vista en `views.py` que renderice la página con el contexto necesario.
2. Modificar la función `protected_page_view` para que pase la petición a la vista creada en el paso anterior.
3. Utilizar el contexto en el HTML de la página. [Aquí](https://docs.djangoproject.com/en/3.2/topics/templates/) puedes encontrar más información sobre cómo utilizar el contexto en Django.
