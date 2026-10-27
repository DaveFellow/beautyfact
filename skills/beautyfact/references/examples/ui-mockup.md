# Pattern: UI spec: a modal mockup that copies the real layout, and 💬 on every literal UI string

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

### ✅ En ambos casos 🔗 [L50–L61](Honsuki%20Specs.md#L50)

Tras seleccionar o soltar los archivos se muestra el modal de confirmación:

```text
 ┌───────────────────────────────────────────────┐
 │ Anexar páginas                                │
 │ Se agregarán X páginas al final de la mesa    │
 │ de trabajo.                                   │
 │ [x] Incluir en la transcripción general       │
 │                                               │
 │                    [Volver]  [Anexar páginas] │
 └───────────────────────────────────────────────┘
```

- Contenido del modal 🔗 [L51–L55](Honsuki%20Specs.md#L51)
  - Título: 💬 «**Anexar páginas**»
  - Texto: 💬 «**Se agregarán X páginas al final de la mesa de trabajo.**» (X es el número total de páginas que se van a añadir).
  - Checkbox: 💬 «**Incluir en la transcripción general**» (marcado por defecto).
  - Botones: 💬 «**Anexar páginas**» (acción principal) y 💬 «**Volver**» (acción secundaria).
- Si el usuario confirma 🔗 [L56](Honsuki%20Specs.md#L56): loader con 💬 «**Importando archivo**», barra de progreso 0% a 100% y botón 💬 «**Cancelar**», mientras se rasterizan las páginas.
- 📌 Las páginas se rasterizan y se agregan al final del arreglo de `Page` de la mesa de trabajo actual (después de la última página existente). 🔗 [L57](Honsuki%20Specs.md#L57)
- 📌 Las nuevas páginas heredan la configuración de columnas por defecto de la mesa de trabajo. 🔗 [L58](Honsuki%20Specs.md#L58)
- 📌 `includeInGeneralTranscription` de las nuevas páginas se establece según el checkbox del modal. 🔗 [L59](Honsuki%20Specs.md#L59)

### 🪟 Modal de progreso 🔗 [L107–L119](Honsuki%20Specs.md#L107)

Modal que no puede cerrarse, con un backdrop que bloquea cualquier interacción con los elementos detrás.

```text
 ┌─────────────────────────────────────────────┐
 │ Texto de estado                             │
 │ Barra de carga  0% ───────────────▶ 100%    │
 │ ┌─────────────────────────────────────────┐ │
 │ │ (amarillo, opcional) Error en las       │ │
 │ │ siguientes páginas: 3, 7                │ │
 │ └─────────────────────────────────────────┘ │
 │                                  [Cancelar] │
 └─────────────────────────────────────────────┘
```

- **Texto de estado** 🔗 [L108–L110](Honsuki%20Specs.md#L108)
  - Página en proceso: 💬 «**Transcribiendo página **» + número de página.
  - Problemas de conexión con la LLM: 💬 «**Esperando conexión con la LLM...**»
- **Barra de carga** 🔗 [L111–L113](Honsuki%20Specs.md#L111): progreso de 0% a 100% de la transcripción de todo el documento.
  - Fórmula: `[número de página actual en esta corrida] / [número total de páginas de esta corrida]`.
  - Con problemas de conexión con la LLM, no se muestra la barra hasta que se reestablezca.
- **Cuadro amarillo opcional** 🔗 [L114](Honsuki%20Specs.md#L114): aparece sólo si alguna página no pudo concretar su transcripción; texto 💬 «**Error en las siguientes páginas: **» y la lista de páginas con error, separadas por coma.
- **Botón para cancelar** 🔗 [L115–L119](Honsuki%20Specs.md#L115)
  - Si ya hay un procedimiento en marcha, éste no se completará.
    - Si hay una transcripción anterior.
