# proyectoIntegradorCM_upateco

## Proyecto integrador presentado (27/03/2023) para la materia de Programacion I, de la carrera "Tecnicatura en Desarrollo de Software" de la UPATecO (Universidad Provincial de Administración, Tecnología y Oficios)

### Proyecto:

![118](https://user-images.githubusercontent.com/113145320/229177729-ee98103a-5ea8-4cd9-a624-b6980e88f046.png)

### Detalles:
![121](https://user-images.githubusercontent.com/113145320/229181752-86dd0be2-92e9-472d-b6ce-6820a14d64fb.png)

Calendario: Un calendario que por defecto muestra el dia actual

Buscar Evento: Boton que llama a una funcion, y muestra todos los eventos que coincida con la fecha seleccionada en el calendario. Se abre una nueva ventana, y en un Text Area se insertan los datos.


![124](https://user-images.githubusercontent.com/113145320/229358279-f3fca6f2-ff4e-4ab2-bafe-a2b6e532d974.png)

Buscar: Muestra todos los eventos que coincidan a las palabras ingresadas (etiquetas). Se abre una ventana y los valores se insertan en un Text Area


![125](https://user-images.githubusercontent.com/113145320/229358297-8b0d67dc-e80d-42e4-be67-50620146f4c1.png)

Agregar Evento: Abre una ventana para ingrensar los datos de un nuevo evento, y posteriomente, agregarlo a la lista. No se deben dejar campos vacios (A excepcion del campo "Descripcion")

![126](https://user-images.githubusercontent.com/113145320/229358336-1127f105-3112-4885-97a4-a2b5f111efcd.png)

Modificar Evento: Se abre una ventana para modificar los datos de un determinado evento. Primero se debe seleccionar un elemento de la tabla (Sino, se muestra un message.showerror), y esos datos seran introducidos en los "entry" correspondientes. No se deben dejar campos vacios (A excepcion del campo "Descripcion")


![127](https://user-images.githubusercontent.com/113145320/229358341-370bde2e-04ae-4b9c-9e9d-1d3abf294cce.png)

Aclaracion: Al momento de ingresar datos en "Agregar Evento" y "Modificar Evento", se debe respetar el como se deben ingresar los datos (especialmente en "Fecha"), ya que no se cuentan con metodos de validacion de datos (por si el usuario no ingresa un formato de "dd/mm/aaaa".)

Eliminar Evento: Elimina un determinado evento. Se debe seleccionar un elemento de la tabla (Sino, se lanza un message.showerror) y posteriormente presionar el buton de eliminar.

Vista Semanal: Abre una ventana, en la cual se muestra los eventos de la semana actual. Tambien se puede navegar de semana en semana.

![128](https://user-images.githubusercontent.com/113145320/229358632-09adfa42-546b-4d1b-bf5a-a03bc0903647.png)

![129](https://user-images.githubusercontent.com/113145320/229358636-81b984af-4d82-4189-9ea6-199de5c7593a.png)

Salir: Cierra la aplicacion.
Reloj: Al lado del boton salir se encuentra un Label que muestra la fecha y hora actual. Se actualiza cada segundo.

![123](https://user-images.githubusercontent.com/113145320/229359023-23023552-80b6-4372-89bb-15c5f004e0ab.png)

Pestaña Vista General: Los datos provienen de un archivo csv ("agenda.csv") y se insertan en la tabla. Se resaltan los eventos importantes

![122](https://user-images.githubusercontent.com/113145320/229359378-77e71056-b852-4660-b90c-fd4cc65a5f54.png)

Pestaña Vista Mensual: Se muestran los eventos del mes actual.
