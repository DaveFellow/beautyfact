# Pattern: UI spec: cases ──▶ responses table, and an outcomes table with the exact copy

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

## 6. ⚠️ Edge cases de importación

🔗 Source: [Honsuki Specs.md L63–L86](Honsuki%20Specs.md#L63)

| Caso | Respuesta |
| --- | --- |
| corrupto o ilegible | toast de error, se omite ese archivo |
| PDF con contraseña | modal 💬 «**PDF protegido**» |
| MIME no soportado | toast de error, se omite ese archivo |
| supera «**advertencia**» | modal 💬 «**Archivo grande**» |
| supera «**no importar**» | modal 💬 «**Límite excedido**» |
| resolución extrema | modal 💬 «**Imagen de alta resolución**» |

- ⚠️ **Archivo corrupto o no legible** 🔗 [L66](Honsuki%20Specs.md#L66): toast de error indicando que ese archivo no pudo importarse. Con varios archivos, se continúa con los válidos y solo se omiten los que fallaron.
- ⚠️ **PDF protegido con contraseña** 🔗 [L67–L71](Honsuki%20Specs.md#L67)

### 🏁 Desenlaces 🔗 [L122–L128](Honsuki%20Specs.md#L122)

| Desenlace | Respuesta |
| --- | --- |
| fin sin cancelar | cierra modal + toast verde 💬 «**¡Todas las páginas fueron transcritas exitosamente!**» |
| fin con alguna falla | 💬 «**Proceso de transcripción finalizado, algunas páginas no pudieron ser transcritas**» |
| error en una página | no detiene el proceso; se marca en su data interna |
| error de conexión | pausa; cancelar detiene al instante y cancela la petición actual a la LLM, si existe |
