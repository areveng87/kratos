<template>
  <div class="space-y-6">
    <!-- Modal -->
    <div v-if="show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="rounded-lg p-6 w-96"
          style="background-color: var(--color-bg-secondary); border:1px solid var(--color-border);">
        <h3 class="text-lg font-semibold theme-text mb-3">Confirmar acción</h3>
        <p class="theme-text mb-6">{{ message }}</p>
        <div class="flex justify-end gap-2">
          <button @click="cancel" class="btn-secondary">Cancelar</button>
          <button @click="accept" class="btn-primary">Aceptar</button>
        </div>
      </div>
    </div>
    <!-- Sección superior: Importe Total, Moneda, Tributación -->
    <div class="grid grid-cols-4 gap-4 p-4 rounded-lg" 
      style="background-color: var(--color-bg-secondary); border: 1px solid var(--color-border)">
      <div>
        <label class="block text-sm font-medium mb-1 theme-text">Importe Total *</label>
        <input
          v-model.number="importeTotal"
          type="number"
          step="0.01"
          class="w-full px-3 py-2 rounded-md theme-input"
          style="border: 1px solid var(--color-border)"
        />
      </div>
      <div>
        <label class="block text-sm font-medium mb-1 theme-text">Moneda *</label>
        <!-- Eliminado @change para no guardar inmediatamente -->
        <select v-model="moneda" class="w-full px-3 py-2 rounded-md theme-input" style="border: 1px solid var(--color-border)">
          <option value="">Seleccionar...</option>
          <option v-for="m in monedas" :key="m.id" :value="m.id">
            {{ m.nombre }} ({{ m.simbolo }})
          </option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium mb-1 theme-text">Tributación *</label>
        <!-- Eliminado @change para no guardar inmediatamente -->
        <select v-model="tributacion" class="w-full px-3 py-2 rounded-md theme-input" 
          style="border: 1px solid var(--color-border)"
          required
          >
          <option value="">Seleccionar...</option>
          <option v-for="t in tributaciones" :key="t.id" :value="t.id">
            {{ t.descripcion }} ({{ t.valor }}%)
          </option>
        </select>
      </div>
      <div>
         <button @click="guardarImporteTarea" class="block px-3 py-2 text-white rounded-md transition-colors" style="background-color: var(--color-primary)">
          Guardar importe
        </button>
      </div>
    </div>

    <!-- Botones de acción -->
    <div class="flex gap-2">
      <button
        @click="showFormularioHito"
        class="px-4 py-2 text-white rounded-md transition-colors"
        style="background-color: var(--color-primary)"
        :style="{ opacity: hayHitosActivados ? 0.5 : 1 }"
        :disabled="hayHitosActivados"
      >
        Nuevo Hito
      </button>
      <button
        @click="activarHito"
        class="px-4 py-2 rounded-md transition-colors"
        :class="!hitoSeleccionado || hayHitosActivados ? 'opacity-50 cursor-not-allowed' : ''"
        style="background-color: #10b981; color: white"
        :disabled="!hitoSeleccionado || hayHitosActivados"
      >
        Activar Hito
      </button>
    </div>

    <!-- Formulario de nuevo/editar hito -->
    <div v-if="mostrarFormularioHito" class="p-4 rounded-lg" style="background-color: var(--color-bg-secondary); border: 1px solid var(--color-border)">
      <h3 class="text-lg font-semibold mb-4 theme-text">{{ editandoHito ? "Editar Hito" : "Nuevo Hito" }}</h3>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1 theme-text">Tipo de Pago *</label>
          <select v-model="formularioHito.idtipopago" 
            class="w-full px-3 py-2 rounded-md theme-input" 
            style="border: 1px solid var(--color-border)"
            required
          >
            <option value="">Seleccionar...</option>
            <option v-for="tp in tiposPago" :key="tp.id" :value="tp.id">
              {{ tp.descripcion }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1 theme-text">Importe ({{ monedaSimboloActual }}) *</label>
          <input
            v-model.number="formularioHito.importe"
            type="number"
            step="0.01"
            class="w-full px-3 py-2 rounded-md theme-input"
            style="border: 1px solid var(--color-border)"
            required
          />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1 theme-text">Fecha Firma *</label>
          <!-- <input v-model="formularioHito.fecha" 
          type="date" class="w-full px-3 py-2 rounded-md theme-input" 
          style="border: 1px solid var(--color-border)"
          :min="today"
          required
          @change="clampToToday"
           /> -->

            <DatePicker v-model="formularioHito.fecha" :min-date="today" class="w-full rounded-md theme-input" required />
             <!-- <Calendar class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 theme-text-secondary pointer-events-none" /> -->
        </div>
      </div>
      <div class="flex gap-2 mt-4">
        <button @click="guardarHito" class="px-4 py-2 text-white rounded-md transition-colors" style="background-color: var(--color-primary)">
          Guardar
        </button>
        <button @click="cancelarFormularioHito" class="px-4 py-2 rounded-md transition-colors theme-text" style="background-color: var(--color-bg-tertiary); border: 1px solid var(--color-border)">
          Cancelar
        </button>
      </div>
    </div>

    <!-- Tabla de hitos -->
    <div class="rounded-lg overflow-hidden" style="border: 1px solid var(--color-border)">
      <table class="w-full">
        <thead style="background-color: var(--color-bg-secondary)">
          <tr>
            <th class="px-4 py-2 text-left theme-text">Nº</th>
            <th class="px-4 py-2 text-left theme-text">Tipo de Pago</th>
            <th class="px-4 py-2 text-right theme-text">Importe</th>
            <th class="px-4 py-2 text-left theme-text">Fecha Firma</th>
            <th class="px-4 py-2 text-left theme-text">Solicitado por</th>
            <th class="px-4 py-2 text-left theme-text">Fecha</th>
            <th class="px-4 py-2 text-center theme-text">Situación</th>
            <th class="px-4 py-2 text-center theme-text">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(hito, index) in hitos"
            :key="hito.idtareaplazo"
            :class="[
              'cursor-pointer transition-colors',
              hitoSeleccionado?.idtareaplazo === hito.idtareaplazo ? 'selected-row' : 'hover-row',
            ]"
            @click="seleccionarHito(hito)"
            draggable="true"
            @dragstart="onDragStart(index)"
            @dragover.prevent
            @drop="onDrop(index)"
          >
            <td class="px-4 py-2 theme-text">{{ hito.numhito }}</td>
            <td class="px-4 py-2 theme-text">{{ hito.descripcion }}</td>
            <td class="px-4 py-2 text-right theme-text">{{ formatearImporte(hito.importe) }}</td>
            <td class="px-4 py-2 theme-text">{{ formatearFecha(hito.fecha) }}</td>
            <td class="px-4 py-2 theme-text-secondary">{{ hito.solicitador_nombre || "-" }}</td>
            <td class="px-4 py-2 theme-text-secondary">{{ formatearFecha(hito.fechasolicitud_pbc) }}</td>
            <td class="px-4 py-2 text-center">
              <Check v-if="hito.aprobado" class="w-5 h-5 text-green-600 mx-auto" />
              <X v-else class="w-5 h-5 mx-auto theme-text-secondary" />
            </td>
            <td class="px-4 py-2">
              <div class="flex gap-2 justify-center">
                <button
                  @click.stop="editarHito(hito)"
                  :disabled="hayHitosActivados"
                  class="p-1 rounded transition-colors action-button"
                  :class="{ 'opacity-50 cursor-not-allowed': hayHitosActivados }"
                >
                  <Edit class="w-4 h-4 theme-text" />
                </button>
                <button
                  @click.stop="eliminarHito(hito)"
                  :disabled="hayHitosActivados"
                  class="p-1 rounded transition-colors action-button"
                  :class="{ 'opacity-50 cursor-not-allowed': hayHitosActivados }"
                >
                  <Trash2 class="w-4 h-4 text-red-600" />
                </button>
                <button
                  v-if="!hayHitosActivados && index > 0"
                  @click.stop="moverHito(index, -1)"
                  class="p-1 rounded transition-colors action-button"
                >
                  <ChevronUp class="w-4 h-4 theme-text" />
                </button>
                <button
                  v-if="!hayHitosActivados && index < hitos.length - 1"
                  @click.stop="moverHito(index, 1)"
                  class="p-1 rounded transition-colors action-button"
                >
                  <ChevronDown class="w-4 h-4 theme-text" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Totales -->
    <div class="grid grid-cols-2 gap-4 p-4 rounded-lg" style="background-color: var(--color-bg-secondary); border: 1px solid var(--color-border)">
      <div>
        <label class="block text-sm font-medium mb-1 theme-text-secondary">Importe (Suma de Hitos)</label>
        <div class="text-lg font-semibold theme-text">{{ formatearImporte(totalHitos) }}</div>
      </div>
      <div>
        <label class="block text-sm font-medium mb-1 theme-text-secondary">Diferencia</label>
        <div class="text-lg font-semibold" :class="diferencia < 0 ? 'text-red-600' : 'text-green-600'">
          {{ formatearImporte(diferencia) }}
        </div>
      </div>
    </div>
    <!-- Modal para capturar detalles de documentación -->
    <TextInputModal
      v-if="mostrarModalDocumentacion"
      title="Detalles de documentación requerida"
      description="Por favor, especifique los detalles de la documentación que se requiere para este hito."
      placeholder="Ingrese los detalles de la documentación..."
      :required="true"
      @save="guardarDetallesDocumentacion"
      @cancel="guardarDetallesDocumentacion('', true)"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { Check, X, Edit, Trash2, ChevronUp, ChevronDown, Calendar } from "lucide-vue-next"
import api from "../api"
import { useToastStore } from '../stores/toast'
import { useConfirm } from "../composables/useConfirm"
import TextInputModal from "./TextInputModal.vue"
import { defineProps, defineEmits } from 'vue'

// import Datepicker from '@vuepic/vue-datepicker'
// import '@vuepic/vue-datepicker/dist/main.css'

import DatePicker from "./DatePicker.vue"

const { show, message, confirmar, accept, cancel } = useConfirm()
const toast = useToastStore()

const props = defineProps({
  idtarea: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(["update"])

const { confirm } = useConfirm()

// Catálogos
const monedas = ref([])
const tributaciones = ref([])
const tiposPago = ref([])

// Datos de la tarea
const importeTotal = ref(0)
const moneda = ref("")
const tributacion = ref(null)

// Hitos
const hitos = ref([])
const hitoSeleccionado = ref(null)
const mostrarFormularioHito = ref(false)
const editandoHito = ref(false)
const formularioHito = ref({
  idtipopago: "",
  importe: 0,
  fecha: "",
})

// Drag and drop
const draggedIndex = ref(null)

// Modal para documentación
const mostrarModalDocumentacion = ref(false)
const hitoActivadoTemp = ref(null)
const idAccionTemp = ref(null)
const detallesDocumentacion = ref("")

// hoy en YYYY-MM-DD (hora local)
const today = new Date()
  .toISOString()
  .slice(0, 10) // "YYYY-MM-DD"

// (opcional) si quieres reforzar que no se pueda poner menos que hoy incluso escribiendo a mano
function clampToToday(e) {
  const v = e.target.value
  if (v && v < today) {
    e.target.value = today
    formularioHito.value.fecha = today
  }
}

// Computed
const hayHitosActivados = computed(() => hitos.value.some((h) => h.aprobado))

const monedaSimboloActual = computed(() => {
  //const m = monedas.value.find((m) => m.codigo_iso === moneda.value)
  const m = monedas.value.find((m) => m.id === moneda.value)
  return m ? m.simbolo : ""
})

const totalHitos = computed(() => hitos.value.reduce((sum, h) => sum + (h.importe || 0), 0))

const diferencia = computed(() => importeTotal.value - totalHitos.value)

// Métodos
const cargarCatalogos = async () => {
  try {
    const [monedasRes, tributacionesRes, tiposPagoRes] = await Promise.all([
      api.hitos.getMonedas(),
      api.hitos.getTributaciones(),
      api.hitos.getTiposPago(),
    ])
    monedas.value = monedasRes.data.data || []
    tributaciones.value = tributacionesRes.data.data || []
    tiposPago.value = tiposPagoRes.data.data || []

    console.log("Catálogos cargados:", {
      monedas: monedas.value,
      tributaciones: tributaciones.value,
      tiposPago: tiposPago.value,
    })

  } catch (error) {
    console.error("Error cargando catálogos:", error)
  }
}

const cargarDatosTarea = async () => {
  try {

    const response = await api.tareas.getById(props.idtarea)

    console.log("Datos de tarea cargados:", response.data)
    
    const tarea = response.data.data

    console.log("Tarea ext_importe:", tarea.ext_importe, "idmoneda:", tarea.idmoneda, "idtributacion:", tarea.idtributacion)

    importeTotal.value = tarea.ext_importe || 0
    // moneda.value = tarea.ext_moneda || ""
    // tributacion.value = tarea.ext_tributacion || null
    moneda.value = tarea.idmoneda || null
    tributacion.value = tarea.idtributacion || null
  } catch (error) {
    console.error("Error cargando datos de tarea:", error)
  }
}

const showFormularioHito = () => {
  if (!importeTotal.value || !moneda.value || !tributacion.value) {

    toast.push("Por favor, complete todos los campos de importe antes de crear un hito.", "error")

    return

  }
  mostrarFormularioHito.value = true
}

const guardarImporteTarea = async () => {
if (!importeTotal.value || !moneda.value || !tributacion.value) {
    toast.push("Por favor, complete todos los campos antes de guardar.", "error")
    return
  }

  try {
   console.log("Guardando importe de tarea...", {
      ext_importe: importeTotal.value,
      idmoneda: moneda.value,
      idtributacion: tributacion.value,
    })
    await api.tareas.update(props.idtarea, {
      ext_importe: importeTotal.value,
      idmoneda: moneda.value,
      idtributacion: tributacion.value,
    })
    toast.push("Importe de tarea guardado correctamente", "success")
    emit("update")
  } catch (error) {
    console.error("Error guardando importe de tarea:", error)
    toast.push("Error guardando importe de tarea", "error")
  }
 } 

const cargarHitos = async () => {
  try {
    const response = await api.hitos.getByTarea(props.idtarea)
    hitos.value = response.data.data || []
  } catch (error) {
    console.error("Error cargando hitos:", error)
  }
}

const guardarHito = async () => {
  if (!importeTotal.value || !moneda.value || !tributacion.value) {
    toast.push("Por favor, complete todos los campos antes de guardar.", "error")
    return
  }

  if (!formularioHito.value.idtipopago || !formularioHito.value.importe || !formularioHito.value.fecha) {
    toast.push("Por favor, complete todos los campos del formulario del hito.", "error")
    return
  }

  console.log("Guardando hito...", formularioHito.value)
  try {
    const tipoPago = tiposPago.value.find((tp) => tp.id === formularioHito.value.idtipopago)
    const data = {
      idtarea: props.idtarea,
      descripcion: tipoPago?.descripcion || "",
      idtipopago: tipoPago?.id || null,
      importe: formularioHito.value.importe,
      //fecha_alta: formularioHito.value.fecha || Date.now().toISOString().split("T")[0],
      fecha: formularioHito.value.fecha || Date.now().toISOString().split("T")[0],
    }

    console.log("Guardando hito con datos: ", data)
    console.log("Tarea: ", props.idtarea)

    if (editandoHito.value) {
      await api.hitos.update(hitoSeleccionado.value.idtareaplazo, data)
    } else {
      await api.hitos.create(props.idtarea, data)
    }

    await cargarHitos()
    cancelarFormularioHito()
    emit("update")
  } catch (error) {
    console.error("Error guardando hito:", error)
  }
}

const editarHito = (hito) => {
  if (hayHitosActivados.value) return
  hitoSeleccionado.value = hito
  editandoHito.value = true

  console.log("Editando hito:", hito)

  const tipoPago = tiposPago.value.find((tp) => tp.descripcion === hito.descripcion)

  formularioHito.value = {
    idtipopago: tipoPago?.id || "",
    importe: hito.importe,
    fecha: hito.fecha,
  }
  mostrarFormularioHito.value = true
}

const eliminarHito = async (hito) => {
  if (hayHitosActivados.value) return
  
  const confirmado = await confirm("¿Está seguro de eliminar este hito?")
  if (!confirmado) return

  try {
    await api.hitos.delete(props.idtarea, hito.idtareaplazo)
    await cargarHitos()
    emit("update")
  } catch (error) {
    console.error("Error eliminando hito:", error)
  }
}

const cancelarFormularioHito = () => {
  mostrarFormularioHito.value = false
  editandoHito.value = false
  formularioHito.value = {
    idtipopago: "",
    importe: 0,
    fecha: "",
  }
  hitoSeleccionado.value = null
}

const seleccionarHito = (hito) => {
  hitoSeleccionado.value = hitoSeleccionado.value?.idtareaplazo === hito.idtareaplazo ? null : hito
}

const activarHito = async () => {
  if (!hitoSeleccionado.value || hayHitosActivados.value) return

  const ok = await confirmar("¿Desea activar este hito?")
  if (!ok) 
    return

  try {
    // await api.hitos.update(props.idtarea, hitoSeleccionado.value.idtareaplazo, {
    //   aprobado: true,
    //   solicitado_pbc: true,
    //   fechasolicitud_pbc: new Date().toISOString().split("T")[0],
    // })

    const result = await api.hitos.activate(props.idtarea, hitoSeleccionado.value.idtareaplazo)
    console.log("Resultado de activar hito:", result)
    if (result != null) {
        const data = result.data.data
        const idaccion = data['idaccion']
        const descripcion_accion = data['descripcion_accion']
        console.log("Activating hito resulted in idaccion:", idaccion, "descripcion_accion:", descripcion_accion)

        idAccionTemp.value = idaccion

        if (idaccion == 63 || descripcion_accion.trim().toLowerCase().startsWith('solicitar documen')) {
          //Hito activado requiere documentación. Mostrar modal para capturar detalles.
          hitoActivadoTemp.value = true
          mostrarModalDocumentacion.value = true
        }
        //enviar emails
    }
    
    await cargarHitos()
    hitoSeleccionado.value = null
    emit("update")

    toast.push("Hito activado correctamente", "success")

  } catch (error) {
    console.error("Error activando hito:", error)

    toast.push("Error activando hito", "error")
  }
}

const guardarDetallesDocumentacion = async (detalles, sinMensaje = false) => {
  try {
    detallesDocumentacion.value = null
    if(!sinMensaje && detalles && detalles.length > 0) {
         detallesDocumentacion.value = detalles
    }
    // Aquí guardarías los detalles en el backend, asociado al hito activado
    console.log("Detalles de documentación guardados:", detalles)
    
    await api.logs.crearLogTarea(props.idtarea, hitoSeleccionado.value.idtareaplazo, {
        idaccion: idAccionTemp.value,
        comentario: detallesDocumentacion.value || "No se especificaron detalles de documentación.",
    })
    detallesDocumentacion.value = null
    mostrarModalDocumentacion.value = false
    await cargarHitos()

    toast.push("Detalles de documentación guardados", "success")

  } catch (error) {
    console.error("Error guardando detalles de documentación:", error)
    toast.push("Error guardando detalles de documentación", "error")
  } finally {
    
  }
}

const moverHito = async (index, direccion) => {
  if (hayHitosActivados.value) return
  const newIndex = index + direccion
  if (newIndex < 0 || newIndex >= hitos.value.length) return

  const hitosReordenados = [...hitos.value]
  const [hitoMovido] = hitosReordenados.splice(index, 1)
  hitosReordenados.splice(newIndex, 0, hitoMovido)

  try {
    const orden = hitosReordenados.map((h, i) => ({
      idtareaplazo: h.idtareaplazo,
      numhito: i + 1,
    }))
    await api.hitos.reorder(props.idtarea, { hitos: orden })
    await cargarHitos()
    emit("update")
  } catch (error) {
    console.error("Error reordenando hitos:", error)
  }
}

const onDragStart = (index) => {
  if (hayHitosActivados.value) return
  draggedIndex.value = index
}

const onDrop = async (dropIndex) => {
  if (hayHitosActivados.value || draggedIndex.value === null) return
  await moverHito(draggedIndex.value, dropIndex - draggedIndex.value)
  draggedIndex.value = null
}

const formatearImporte = (valor) => {
  if (!valor) return "0.00"
  return new Intl.NumberFormat("es-ES", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(valor)
}

const formatearFecha = (fecha) => {
  if (!fecha) return "-"
  return new Date(fecha).toLocaleDateString("es-ES")
}

const getDatosActuales = () => {
  return {
    ext_importe: importeTotal.value,
    // ext_moneda: moneda.value,
    // ext_tributacion: tributacion.value,
    idmoneda: moneda.key,
    idtributacion: tributacion.key,
  }
}

defineExpose({
  getDatosActuales,
})

onMounted(async () => {

  console.log("ImportesHitos mounted for idtarea:", props.idtarea)

  await cargarCatalogos()
  await cargarDatosTarea()
  await cargarHitos()
})
</script>

<style scoped>
.theme-text {
  color: var(--color-text-primary);
}

.theme-text-secondary {
  color: var(--color-text-secondary);
}

.theme-input {
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
}

.theme-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.hover-row:hover {
  background-color: var(--color-bg-hover);
}

.selected-row {
  background-color: var(--color-bg-selected);
}

.action-button:hover:not(:disabled) {
  background-color: var(--color-bg-hover);
}
</style>
