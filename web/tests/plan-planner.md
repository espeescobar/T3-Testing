# Plan de pruebas de DCCuote

## Application Overview

Plan único y exhaustivo de pruebas funcionales, negativas y de experiencia para DCCuote. Incluye más casos de los necesarios para priorizar al refinar. Todos los escenarios asumen el estado inicial de tests/seed.spec.ts.

## Test Scenarios

### 1. Navegación y estructura general

**Seed:** `tests/seed.spec.ts`

#### 1.1. Navegación principal desde todas las vistas

**File:** `tests/navigation.spec.ts`

**Steps:**
  1. Abrir la app y recorrer Frases, Frase diaria y Nueva frase.
    - expect: Los enlaces principales están visibles.
    - expect: Frases abre /quotes y Frase diaria abre /.
    - expect: No aparecen errores de navegación.
  2. Repetir la navegación varias veces.
    - expect: Cada vista conserva su estructura.
    - expect: Los enlaces siguen funcionando.

#### 1.2. Historial del navegador

**File:** `tests/navigation.spec.ts`

**Steps:**
  1. Ir de Frase diaria a Frases, abrir una tarjeta y pulsar Atrás.
    - expect: Se vuelve a la colección.
    - expect: Usar Atrás otra vez vuelve a la frase diaria.

#### 1.3. Ruta de detalle válida e inválida

**File:** `tests/navigation.spec.ts`

**Steps:**
  1. Abrir tarjetas válidas y luego navegar manualmente a /quotes/id-inexistente.
    - expect: Las válidas muestran datos coherentes.
    - expect: La ruta inválida muestra un estado controlado sin datos ajenos ni pantalla rota.
    - expect: Es posible volver con la navegación principal.

### 2. Frase diaria

**Seed:** `tests/seed.spec.ts`

#### 2.1. Visualización inicial

**File:** `tests/daily.spec.ts`

**Steps:**
  1. Abrir /.
    - expect: Se muestra una frase completa, autor y etiquetas.
    - expect: No hay controles fuera de contexto ni errores visibles.

#### 2.2. Abrir diálogo desde la frase diaria

**File:** `tests/daily.spec.ts`

**Steps:**
  1. Pulsar Nueva frase desde /.
    - expect: Se abre el diálogo Nueva frase.
    - expect: Cancelar y Close cierran sin guardar.
    - expect: La frase diaria permanece intacta tras cerrar.

#### 2.3. Navegar de etiqueta y volver

**File:** `tests/daily.spec.ts`

**Steps:**
  1. Interactuar con una etiqueta y volver a la frase diaria.
    - expect: La acción es coherente con la etiqueta.
    - expect: No se pierden ni duplican datos.
    - expect: La frase vuelve a mostrarse correctamente.

#### 2.4. Contenido largo o con caracteres especiales

**File:** `tests/daily.spec.ts`

**Steps:**
  1. Mostrar una frase con texto largo, comillas, &, acentos y emoji.
    - expect: Se renderiza completa y literalmente.
    - expect: No hay desbordes ni superposiciones.
    - expect: No se interpreta HTML ni JavaScript.

#### 2.5. Consistencia al navegar y recargar

**File:** `tests/daily.spec.ts`

**Steps:**
  1. Anotar la frase, navegar a Frases y volver; después recargar.
    - expect: La vista mantiene o aplica consistentemente la regla diaria.
    - expect: La recarga no deja pantalla en blanco ni datos incoherentes.

### 3. Colección y búsqueda

**Seed:** `tests/seed.spec.ts`

#### 3.1. Inventario inicial de tarjetas

**File:** `tests/collection.spec.ts`

**Steps:**
  1. Abrir /quotes.
    - expect: Se muestran las frases disponibles.
    - expect: Cada tarjeta muestra texto y autor.
    - expect: Las tarjetas con fuente muestran personaje y obra.

#### 3.2. Buscar por texto existente

**File:** `tests/collection.spec.ts`

**Steps:**
  1. Buscar bicycle.
    - expect: Solo aparecen coincidencias relevantes.
    - expect: Albert Einstein queda visible.
    - expect: Borrar el campo restaura todas las tarjetas.

#### 3.3. Buscar por personaje y fuente

**File:** `tests/collection.spec.ts`

**Steps:**
  1. Buscar Uncle Iroh y después Mistborn.
    - expect: La primera muestra frases de Uncle Iroh.
    - expect: La segunda muestra las frases cuya fuente es Mistborn.
    - expect: Las búsquedas reemplazan correctamente resultados anteriores.

#### 3.4. Buscar sin resultados

**File:** `tests/collection.spec.ts`

**Steps:**
  1. Buscar texto inexistente con mayúsculas y símbolos.
    - expect: No aparecen coincidencias falsas.
    - expect: Existe un estado vacío o mensaje controlado.
    - expect: El texto permanece editable.

#### 3.5. Espacios, mayúsculas, parcial y Unicode

**File:** `tests/collection.spec.ts`

**Steps:**
  1. Buscar con mayúsculas, fragmentos cortos, espacios extremos y acentos.
    - expect: Las coincidencias relevantes funcionan.
    - expect: Los espacios extremos no producen resultados falsos.
    - expect: Acentos y caracteres especiales no generan errores.

#### 3.6. Filtro por personaje existente

**File:** `tests/collection.spec.ts`

**Steps:**
  1. Elegir Uncle Iroh y luego Albert Einstein.
    - expect: El resultado cambia inmediatamente a las frases del personaje elegido.
    - expect: El combobox muestra la selección.
    - expect: Borrar o limpiar el filtro restaura la colección.

#### 3.7. Combinación de búsqueda y personaje

**File:** `tests/collection.spec.ts`

**Steps:**
  1. Buscar life y seleccionar Albert Einstein.
    - expect: Solo aparecen tarjetas que cumplen ambos criterios.
    - expect: Buscar Gandalf con ese personaje produce estado vacío.
    - expect: Quitar un criterio restaura coincidencias válidas.

#### 3.8. Psycho Killer Mode

**File:** `tests/collection.spec.ts`

**Steps:**
  1. Activar y desactivar el switch.
    - expect: El estado cambia visualmente de inmediato.
    - expect: No se crean ni eliminan frases.
    - expect: Los filtros siguen siendo coherentes con el modo activo o normal.

#### 3.9. Persistencia al abrir detalle

**File:** `tests/collection.spec.ts`

**Steps:**
  1. Aplicar búsqueda y personaje, abrir una coincidencia y volver.
    - expect: El detalle coincide con la tarjeta.
    - expect: Los filtros permanecen aplicados tras volver.
    - expect: Las tarjetas siguen cumpliendo ambos criterios.

#### 3.10. Recarga y rutas directas

**File:** `tests/collection.spec.ts`

**Steps:**
  1. Recargar /quotes con filtros activos.
    - expect: La vista carga sin pantalla en blanco.
    - expect: El estado final es coherente y los filtros pueden limpiarse.
    - expect: No hay errores de ruta o datos contradictorios.

### 4. Creación de frases

**Seed:** `tests/seed.spec.ts`

#### 4.1. Abrir y cerrar Nueva frase

**File:** `tests/create.spec.ts`

**Steps:**
  1. Pulsar Nueva frase y revisar los campos.
    - expect: Se muestran Frase, Personaje, Fuente, Etiquetas y las acciones.
    - expect: Frase recibe el foco.
  2. Probar Cancelar y Close.
    - expect: Ambos cierran sin crear datos.
    - expect: Reabrir muestra un estado limpio.

#### 4.2. Crear una frase completa

**File:** `tests/create.spec.ts`

**Steps:**
  1. Completar frase, personaje, fuente y etiquetas separadas por comas.
    - expect: Añadir crea una sola frase.
    - expect: La colección contiene autor, fuente y etiquetas ingresados.
    - expect: El nuevo registro puede encontrarse con búsqueda.

#### 4.3. Crear personaje nuevo

**File:** `tests/create.spec.ts`

**Steps:**
  1. Escribir o crear un personaje nuevo en el combobox y completar el formulario.
    - expect: El personaje queda asociado a la frase.
    - expect: El personaje aparece como opción de filtro.
    - expect: No se crea un personaje vacío.

#### 4.4. Campos vacíos y obligatorios

**File:** `tests/create.spec.ts`

**Steps:**
  1. Enviar con todos los campos vacíos.
    - expect: No se crea ninguna frase.
    - expect: Se muestran validaciones claras.
    - expect: El diálogo permanece abierto.
  2. Variar dejando vacío solo Frase, personaje o fuente.
    - expect: Los campos requeridos se validan independientemente.
    - expect: Los datos ingresados no se pierden al corregir.

#### 4.5. Espacios en blanco

**File:** `tests/create.spec.ts`

**Steps:**
  1. Completar los campos con espacios solamente.
    - expect: Los espacios no cuentan como datos válidos.
    - expect: No se crean etiquetas vacías ni frases incompletas.

#### 4.6. Texto largo

**File:** `tests/create.spec.ts`

**Steps:**
  1. Ingresar una frase y etiquetas considerablemente largas.
    - expect: Se respeta el límite definido o se admite con renderizado estable.
    - expect: No hay cortes que oculten datos ni desbordes.

#### 4.7. Caracteres especiales y HTML

**File:** `tests/create.spec.ts`

**Steps:**
  1. Ingresar comillas, apóstrofes, &, acentos, emoji y texto tipo HTML.
    - expect: Todo se guarda y muestra literalmente.
    - expect: No se ejecuta HTML ni JavaScript.
    - expect: Las etiquetas no incluyen elementos accidentales.

#### 4.8. Etiquetas con formato inconsistente

**File:** `tests/create.spec.ts`

**Steps:**
  1. Ingresar etiquetas con comas, espacios y duplicados.
    - expect: Se normalizan los extremos.
    - expect: No se crean etiquetas vacías ni duplicados visibles.
    - expect: Las etiquetas válidas quedan asociadas.

#### 4.9. Duplicado y doble envío

**File:** `tests/create.spec.ts`

**Steps:**
  1. Crear una frase idéntica a una existente y pulsar Añadir varias veces rápidamente.
    - expect: El duplicado se rechaza o se identifica claramente.
    - expect: No hay múltiples registros por doble clic.
    - expect: El usuario conserva datos para corregir.

#### 4.10. Cancelar después de modificar

**File:** `tests/create.spec.ts`

**Steps:**
  1. Completar parcialmente el diálogo y cancelar.
    - expect: La colección no cambia.
    - expect: Reabrir muestra valores limpios.
    - expect: Navegar fuera no guarda cambios accidentales.

### 5. Etiquetas

**Seed:** `tests/seed.spec.ts`

#### 5.1. Abrir diálogo de etiquetas

**File:** `tests/tags.spec.ts`

**Steps:**
  1. Abrir Add Tag desde una frase.
    - expect: Se muestra Nuevas etiquetas para la frase.
    - expect: El campo recibe el foco.
    - expect: Cancelar, Agregar etiquetas y Close están disponibles.

#### 5.2. Agregar una etiqueta

**File:** `tests/tags.spec.ts`

**Steps:**
  1. Ingresar una etiqueta válida y confirmar.
    - expect: La etiqueta aparece una vez en el detalle.
    - expect: Permanece tras salir y volver.
    - expect: Se informa visualmente el resultado si existe notificación.

#### 5.3. Agregar varias etiquetas

**File:** `tests/tags.spec.ts`

**Steps:**
  1. Ingresar varias etiquetas separadas por comas y con espacios.
    - expect: Se crean todas las válidas normalizadas.
    - expect: No se crean entradas vacías.
    - expect: No se superponen elementos.

#### 5.4. Etiquetas vacías o duplicadas

**File:** `tests/tags.spec.ts`

**Steps:**
  1. Enviar vacío, solo comas o una etiqueta ya existente.
    - expect: No se generan etiquetas vacías.
    - expect: El duplicado no se muestra dos veces.
    - expect: Se muestra validación o se impide el envío.

#### 5.5. Cancelar adición

**File:** `tests/tags.spec.ts`

**Steps:**
  1. Escribir etiquetas y pulsar Cancelar o Close.
    - expect: Las etiquetas no se guardan.
    - expect: El conjunto original queda intacto.
    - expect: El detalle sigue operativo.

#### 5.6. Interacción con etiquetas existentes

**File:** `tests/tags.spec.ts`

**Steps:**
  1. Hacer clic en una etiqueta existente.
    - expect: La interacción cumple su comportamiento previsto.
    - expect: No se pierde la frase ni se produce una ruta incorrecta.
    - expect: El conjunto no cambia por una acción no destructiva.

#### 5.7. Caracteres especiales en etiquetas

**File:** `tests/tags.spec.ts`

**Steps:**
  1. Agregar etiquetas con acentos, &, comillas y texto tipo HTML.
    - expect: Se muestran literalmente.
    - expect: No se ejecuta código.
    - expect: Se separan solo por la regla definida de comas.

### 6. Accesibilidad, responsive y resiliencia

**Seed:** `tests/seed.spec.ts`

#### 6.1. Diseño responsive en escritorio

**File:** `tests/resilience.spec.ts`

**Steps:**
  1. Ejecutar vistas principales a 1280x720.
    - expect: Controles y tarjetas caben sin superposición.
    - expect: No hay desplazamiento horizontal accidental.
    - expect: Diálogos permanecen accesibles.

#### 6.2. Diseño responsive en móvil

**File:** `tests/resilience.spec.ts`

**Steps:**
  1. Repetir vistas y diálogos en ancho móvil.
    - expect: El contenido se apila o ajusta sin superposiciones.
    - expect: Los botones siguen alcanzables.
    - expect: La navegación permanece usable.

#### 6.3. Navegación por teclado

**File:** `tests/resilience.spec.ts`

**Steps:**
  1. Recorrer enlaces, controles y campos con Tab.
    - expect: Todos los elementos interactivos reciben foco visible.
    - expect: Los diálogos pueden cerrarse y los formularios enviarse por teclado.
    - expect: No hay trampas de foco evidentes.

#### 6.4. Recarga directa

**File:** `tests/resilience.spec.ts`

**Steps:**
  1. Recargar /, /quotes y una URL de detalle válida.
    - expect: Cada ruta carga datos válidos.
    - expect: No quedan pantallas blancas ni 404 propios.
    - expect: La navegación principal sigue disponible.

#### 6.5. Fallo o lentitud de datos

**File:** `tests/resilience.spec.ts`

**Steps:**
  1. Simular respuesta lenta o fallida si el entorno lo permite.
    - expect: Se muestra carga o error controlado.
    - expect: No aparecen datos parciales contradictorios.
    - expect: Reintentar restaura el estado disponible.

#### 6.6. Acciones rápidas repetidas

**File:** `tests/resilience.spec.ts`

**Steps:**
  1. Pulsar rápidamente Añadir, Agregar etiquetas y los switches.
    - expect: No se producen duplicados por doble acción.
    - expect: La interfaz no queda con diálogos superpuestos.
    - expect: El estado final corresponde a una sola operación válida.

#### 6.7. Contenido largo en tarjetas

**File:** `tests/resilience.spec.ts`

**Steps:**
  1. Crear una frase larga y volver a la colección.
    - expect: La tarjeta aplica recorte o crecimiento consistente.
    - expect: Autor y etiquetas siguen asociados.
    - expect: No tapa filtros ni otras tarjetas.

#### 6.8. Estado vacío y recuperación

**File:** `tests/resilience.spec.ts`

**Steps:**
  1. Aplicar filtros sin resultados y luego limpiar.
    - expect: El estado vacío es comprensible.
    - expect: Limpiar búsqueda y personaje recupera todas las tarjetas.
    - expect: No quedan estados obsoletos.
