# Plan final de pruebas de DCCuote

## Application Overview

Seis flujos de usuario priorizados, no redundantes con los tests manuales
(crear frase OK, formulario incompleto, borrar desde el grid, bug filtro+búsqueda).
Reglas comunes: textos y nombres únicos por test (corren en paralelo), no asumir
cantidad exacta de tarjetas (otros tests crean datos), y limpiar todo lo creado
vía API (DELETE /quotes/delete/<id>, /characters/delete/<id>, /tags/delete/<id>).
Datos seed: "Albert Einstein" (frase con "bicycle") y "Uncle Iroh" (2 frases).

## Test Scenarios

### 1. Frase diaria

**Seed:** `tests/seed.spec.ts`

#### 1.1. La frase diaria muestra frase, personaje y etiquetas

**File:** `tests/daily-quote.spec.ts`

**Steps:**
  1. Pedir GET /quotes/daily a la API y abrir /.
    - expect: Se muestra el texto de la frase devuelta por la API.
    - expect: Se muestra "- <personaje>" y las etiquetas de esa frase.
    - expect: El botón Add Tag está visible.

### 2. Colección: búsqueda y filtros

**Seed:** `tests/seed.spec.ts`

#### 2.1. Buscar por texto filtra las tarjetas y limpiar las restaura

**File:** `tests/collection.spec.ts`

**Steps:**
  1. Abrir /quotes y escribir "bicycle" en "Buscar frases...".
    - expect: La frase de Albert Einstein ("Life is like riding a bicycle") queda visible.
    - expect: La frase "Nothing in life is to be feared" deja de verse.
  2. Borrar el texto del campo.
    - expect: Ambas frases vuelven a estar visibles.

#### 2.2. Filtrar por personaje y volver a "Todos"

**File:** `tests/collection.spec.ts`

**Steps:**
  1. Abrir /quotes, abrir el combobox y elegir "Uncle Iroh".
    - expect: Se ven las 2 frases de Uncle Iroh.
    - expect: La frase de Einstein no se ve.
  2. Abrir el combobox y elegir "Todos".
    - expect: La frase de Einstein vuelve a estar visible.

### 3. Creación de frases

**Seed:** `tests/seed.spec.ts`

#### 3.1. Crear frase con un personaje nuevo

**File:** `tests/create-quote.spec.ts`

**Steps:**
  1. Abrir "Nueva frase", escribir una frase única, crear el personaje
     (escribir nombre único y elegir 'Create "<nombre>"'), fuente y una etiqueta.
  2. Pulsar Añadir y luego "Ver" en la notificación.
    - expect: Aparece "Frase añadida exitosamente".
    - expect: El detalle muestra la frase y el personaje nuevo.
  3. Ir a /quotes y abrir el combobox.
    - expect: El personaje nuevo aparece como opción.
  4. Limpieza vía API: borrar la frase y luego el personaje.

#### 3.2. Frase duplicada es rechazada

**File:** `tests/create-quote.spec.ts`

**Steps:**
  1. Abrir "Nueva frase" y completar con el texto exacto de una frase seed
     ("Do what you can, with what you have, where you are."), personaje y fuente.
  2. Pulsar Añadir.
    - expect: Aparece "Error al añadir la frase." con el mensaje "La cita ya existe".
    - expect: El diálogo sigue abierto.
    - expect: GET /quotes sigue teniendo una sola frase con ese texto.
  (No crea datos, no requiere limpieza.)

### 4. Etiquetas

**Seed:** `tests/seed.spec.ts`

#### 4.1. Agregar una etiqueta nueva desde el detalle

**File:** `tests/tags.spec.ts`

**Steps:**
  1. Crear por API una frase propia y abrir /quotes/<id>.
  2. Pulsar "Add Tag", escribir una etiqueta única y confirmar.
    - expect: Aparece "Etiquetas añadidas exitosamente".
    - expect: La etiqueta se ve una vez en el detalle.
  3. Recargar la página.
    - expect: La etiqueta sigue ahí (persistió en el backend).
  4. Limpieza vía API: borrar la frase y la etiqueta.