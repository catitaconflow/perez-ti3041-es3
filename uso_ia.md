# uso_ia.md

## Parte 1: Registro de consultas realizadas a la IA

### Consulta 1
Prompt:
"¿Cómo proteger las vistas CRUD para que solo el administrador pueda acceder?"

Resumen de la respuesta:
Se sugirió utilizar sesiones para identificar al administrador y validar el acceso en las vistas crear, editar y eliminar.

Adaptación realizada:
Se añadió la variable de sesión "es_admin" al iniciar sesión y se restringieron las vistas CRUD mediante una validación previa.


### Consulta 2
Prompt:
"Crear un reporte ORM por categoría usando annotate y Count."

Resumen de la respuesta:
Se generó una consulta ORM utilizando values(), annotate(), Count() y Avg() para agrupar herramientas por categoría.

Adaptación realizada:
Se modificaron los nombres de los campos para ajustarlos al modelo Herramienta utilizado en el proyecto.


### Consulta 3
Prompt:
"Crear un reporte de stock crítico utilizando filter() y order_by()."

Resumen de la respuesta:
Se propuso una consulta ORM que filtra herramientas con stock bajo y las ordena de menor a mayor.

Adaptación realizada:
Se ajustó el umbral de stock crítico según los datos disponibles en la base de datos.


### Consulta 4
Prompt:
"Implementar login mediante sesiones y mostrar botones CRUD solo para administradores."

Resumen de la respuesta:
Se sugirió almacenar una variable de sesión tras validar usuario y contraseña y utilizarla para mostrar u ocultar opciones administrativas.

Adaptación realizada:
Se incorporó la sesión es_admin y se modificaron las plantillas para mostrar acciones solo al administrador.


### Consulta 5
Prompt:
"Implementar una funcionalidad de sesiones para cumplir el requisito de la evaluación."

Resumen de la respuesta:
Se propuso un contador de visitas utilizando request.session.

Adaptación realizada:
Se integró la funcionalidad en el listado principal y se mostró el número de visitas en la interfaz.


### Consulta 6
Prompt:
"Crear funcionalidad de últimos productos vistos utilizando sesiones."

Resumen de la respuesta:
Se sugirió almacenar los nombres de los productos visitados en una lista dentro de la sesión y mostrar los últimos tres.

Adaptación realizada:
Se integró la lógica en la vista de detalle de herramientas y se mostró la información en el template correspondiente.



###USO DE LA IA

Durante esta evaluación usé la IA principalmente para resolver dudas sobre django y mejorar algunas funciones. Le pedí ayuda para implementar el CRUD de herramientas en la web, restringir el acceso mediante login para que lo vea solo el administrador y desarrollar los reportes con ORM. También recibí ayuda para crear formularios, gestionar sesiones y agregar funciones como el contador de visitas y los últimos productos vistos.

Muchas veces las respuestas no funcionaron de inmediato y tuve que corregir errores de rutas de la IA, templates que no existian, y codigo mal escrito con variables que tampoco existian, imports y configuración de URLs. Esto me ayudó a comprender mejor cómo se conectan las vistas, modelos y templates dentro de django, donde va cada codigo, funcion, path, html, etc. 

Con la IA pude avanzar más rápido en la solución, pero siempre fue necesario revisar, probar y cambiar un poco el código antes de integrarlo al proyecto. Con este trabajo aprendí mejor el uso del ORM, el manejo de sesiones, la creación de formularios y la organización general de una aplicación Django, de todas formas rescato que como en las anteriores evaluaciones la IA comete fallos por lo que es necesario usar prompts especificos o volver a preguntar indicando los errores, o quiza simplemente pensar en cambiar a otra IA que pueda ser mas completa al momento de desarrollar codigo, en esta evaluación use Copilot pero encontre IA´s como Codex, ClaudeCode o el Git de VSCode integrado, las usaré en proyectos futuros. 
