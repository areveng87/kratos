<template>
  <Sidebar>
    <header class="header-bg header-border px-6 py-4">
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold theme-text">
          {{ isNew ? 'Nueva Estructura' : 'Editar Estructura' }}
        </h1>
        <button
          @click="goBack"
          class="btn-secondary flex items-center space-x-2"
        >
          <ArrowLeft class="h-4 w-4" />
          <span>Volver</span>
        </button>
      </div>
    </header>

    <main class="flex-1 overflow-y-auto main-content p-6 space-y-6">
      <div class="card p-6 space-y-4">
        <div>
          <label class="block text-sm font-medium theme-text mb-2">
            Nombre de la Estructura *
          </label>
          <input
            v-model="estructura.nombre"
            type="text"
            required
            class="input-field"
            placeholder="Ingrese el nombre de la estructura"
          />
        </div>

        <div class="flex items-center space-x-2">
          <input
            v-model="estructura.activa"
            type="checkbox"
            id="activa"
            class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <label for="activa" class="text-sm font-medium theme-text">
            Estructura Activa
          </label>
        </div>

        <div class="flex justify-end space-x-2">
          <button
            @click="goBack"
            class="btn-secondary"
          >
            Cancelar
          </button>
          <button
            @click="guardar"
            class="btn-primary"
          >
            Guardar
          </button>
        </div>
      </div>

      <div v-if="!isNew" class="card p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold theme-text">Árbol de Carpetas y Archivos</h2>
          <div class="flex space-x-2">
            <button
              @click="agregarCarpeta"
              class="btn-icon btn-success"
              title="Agregar Carpeta"
            >
              <FolderPlus class="h-5 w-5" />
            </button>
            <button
              @click="mostrarInputArchivo"
              class="btn-icon btn-primary"
              title="Agregar Archivo"
            >
              <FilePlus class="h-5 w-5" />
            </button>
             <input
              ref="fileInput"
              type="file"
              @change="handleFileSelect"
              class="hidden"
            />
          </div>
        </div>

        <div v-if="breadcrumbs.length > 0" class="breadcrumbs mb-4 flex items-center space-x-2">
          <button
            @click="navegarACarpeta(null)"
            class="breadcrumb-item"
            title="Raíz"
          >
            <Home class="h-4 w-4" />
          </button>
          <ChevronRight class="h-4 w-4 text-gray-400" />
          <template v-for="(crumb, index) in breadcrumbsVisibles" :key="crumb.idcarpeta">
            <button
              @click="navegarACarpeta(crumb)"
              class="breadcrumb-item"
            >
              {{ crumb.nombre }}
            </button>
            <ChevronRight v-if="index < breadcrumbsVisibles.length - 1" class="h-4 w-4 text-gray-400" />
          </template>
        </div>

        <div class="table-container"
          :class="{ 'drag-over': isDragging }"
          @dragover.prevent="handleDragOver"
          @dragleave="handleDragLeave"
          @drop.prevent="handleDrop"
        >
          <div v-if="carpetasActuales.length === 0" class="text-gray-400 text-center py-8">
            No hay carpetas o archivos en esta ubicación. Agregue uno para comenzar o arrastre un archivo aquí.
          </div>
          <table v-else class="w-full">
            <thead class="table-header table-border">
              <tr>
                <th class="text-left py-3 px-4 theme-text font-semibold">Nombre</th>
                <th class="text-left py-3 px-4 theme-text font-semibold">Tipo</th>
                <th class="text-left py-3 px-4 theme-text font-semibold">Tamaño</th>
                <th class="text-right py-3 px-4 theme-text font-semibold">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in carpetasActuales"
                :key="item.idcarpeta"
                class="transition-colors hover:bg-[#6366f3] hover:text-white cursor-pointer"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <button
                    v-if="!item.archivo"
                    @click="navegarACarpeta(item)"
                    class="flex items-center space-x-2"
                  >
                    <!-- <Folder class="h-4 w-4" /> -->
                    <img :src="getIconUrl(item)" class="h-5 w-5" alt="" />
                    <span>{{ item.nombre }}</span>
                  </button>
                  <a
                    v-else
                    :href="`http://localhost:8000${item.archivo_url}`"
                    target="_blank"
                    class="flex items-center space-x-2">
                  <!-- <div v-else class="flex items-center space-x-2 theme-text"> -->
                    <!-- <File class="h-4 w-4" /> -->
                    <img :src="getIconUrl(item)" class="h-5 w-5" alt="" />
                    <span>{{ item.nombre }}</span>
                  <!-- </div> -->
                   </a>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  {{ item.archivo ? 'Archivo' : 'Carpeta' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  {{ item.archivo && item.archivo_size ? formatFileSize(item.archivo_size) : '-' }}
                </td>
                <td class="text-right px-6 py-4 whitespace-nowrap">
                  <button
                    v-if="item.archivo"
                    @click="descargarArchivo(item)"
                    class="text-green-600 hover:text-green-800 dark:text-green-400 mr-3"
                    title="Descargar"
                  >
                    <Download class="h-4 w-4" />
                  </button>
                  <button v-else
                    @click="editarNodo(item)"
                    class="text-blue-600 hover:text-blue-800 dark:text-blue-400 mr-3"
                    title="Editar"
                  >
                    <Edit class="h-4 w-4" />
                  </button>
                  <button
                    @click="eliminarNodo(item)"
                    class="text-red-600 hover:text-red-800 dark:text-red-400"
                    title="Eliminar"
                  >
                    <Trash2 class="h-4 w-4" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div
        v-if="showModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click.self="showModal = false"
      >
        <div class="modal-content rounded-lg p-6 w-96">
          <h3 class="text-lg font-semibold mb-4 theme-text">
            {{ modalNodo.idcarpeta ? 'Editar' : 'Nueva' }} {{ modalNodo.archivo ? 'Archivo' : 'Carpeta' }}
          </h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium theme-text mb-2">
                Nombre *
              </label>
              <input
                v-model="modalNodo.nombre"
                type="text"
                class="input-field"
              />
            </div>
            <div v-if="!modalNodo.idcarpeta && modalNodo.archivo">
              <label class="block text-sm font-medium theme-text mb-2">
                Archivo (máx 10MB)
              </label>
              <input
                type="file"
                @change="handleFileUpload"
                class="input-field"
              />
            </div>
            <div class="flex justify-end space-x-2">
              <button
                @click="showModal = false"
                class="btn-secondary"
              >
                Cancelar
              </button>
              <!-- <button @click="guardarNodo" class="btn-primary"> -->
              <button @click="guardarCarpeta" class="btn-primary">
                Guardar
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </Sidebar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../../api'
import Sidebar from '../../components/Sidebar.vue'
import TreeNode from '../../components/TreeNode.vue'
import { ArrowLeft, FolderPlus, FilePlus, Plus, Edit, Trash2, X, Folder, File, Home, ChevronRight, Download 
 } from 'lucide-vue-next'

import { useFileIcons } from '../../composables/useFileIcons'
const { getIconUrl, getIconComponent, getTipoLabel } = useFileIcons()

const router = useRouter()
const route = useRoute()

const isNew = computed(() => !route.params.id || route.params.id === 'nueva')

const estructura = ref({
  nombre: '',
  activa: true,
  idcarpetapadre: null,
  archivo: false
})

const arbolCarpetas = ref([])
const showModal = ref(false)
const modalNodo = ref({})
const selectedFile = ref(null)
const fileInput = ref(null)

const isDragging = ref(false)
let dragCounter = 0

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const currentFolder = ref(null)
const breadcrumbs = ref([])

const carpetasActuales = computed(() => {
  if (!currentFolder.value) {
    return arbolCarpetas.value
  }
  
  const findFolder = (items, id) => {
    for (const item of items) {
      if (item.idcarpeta === id) {
        return item
      }
      if (item.hijos && item.hijos.length > 0) {
        const found = findFolder(item.hijos, id)
        if (found) return found
      }
    }
    return null
  }
  
  const folder = findFolder(arbolCarpetas.value, currentFolder.value.idcarpeta)
  return folder?.hijos || []
})

const breadcrumbsVisibles = computed(() => {
  if (breadcrumbs.value.length <= 3) {
    return breadcrumbs.value
  }
  return breadcrumbs.value.slice(-3)
})

const navegarACarpeta = (carpeta) => {
  if (!carpeta) {
    currentFolder.value = null
    breadcrumbs.value = []
    return
  }
  
  const breadcrumbIndex = breadcrumbs.value.findIndex(b => b.idcarpeta === carpeta.idcarpeta)
  if (breadcrumbIndex !== -1) {
    breadcrumbs.value = breadcrumbs.value.slice(0, breadcrumbIndex + 1)
    currentFolder.value = carpeta
  } else {
    breadcrumbs.value.push(carpeta)
    currentFolder.value = carpeta
  }
}

const cargarEstructura = async () => {
  if (isNew.value) {
    console.log('[v0] Creating new structure, skipping tree load')
    return
  }
  
  if (!route.params.id) {
    console.log('[v0] No ID provided, cannot load structure')
    return
  }
  
  try {
    console.log('[v0] Loading structure tree for ID:', route.params.id)
    const res = await api.estructuras.getTree(route.params.id)
    console.log('[v0] Structure tree response:', res)

    if (res.data) {
      estructura.value = {
        nombre: res.data.nombre,
        activa: res.data.activa,
        idcarpetapadre: res.data.idcarpetapadre,
        archivo: res.data.archivo
      }

      console.log('hijos: ', res.data.hijos)

      arbolCarpetas.value = res.data.hijos || []
      currentFolder.value = null
      breadcrumbs.value = []
    }
  } catch (error) {
    console.error('[v0] Error al cargar estructura:', error)
    alert('Error al cargar la estructura')
  }
}

const guardar = async () => {
  if (!estructura.value.nombre.trim()) {
    alert('El nombre es obligatorio')
    return
  }
  
  try {
    if (isNew.value) {

      console.log('[v0] Creating new structure with data:', estructura.value)

      const res = await api.estructuras.create(estructura.value)
      alert('Estructura creada correctamente')
      router.push(`/admin/arbol-carpetas/${res.data.idcarpeta}`)
    } else {
      await api.estructuras.update(route.params.id, estructura.value)
      alert('Estructura actualizada correctamente')
    }
  } catch (error) {
    console.error('Error al guardar:', error)
    if (error.response?.data?.detail?.includes('único')) {
      alert('Ya existe una estructura con ese nombre')
    } else {
      alert('Error al guardar la estructura')
    }
  }
}

const handleFileSelect = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // Validar tamaño
  if (file.size > 10 * 1024 * 1024) {
    alert('El archivo no puede superar los 10MB')
    event.target.value = ''
    return
  }
  
  try {
    const formData = new FormData()
    formData.append('file', file)
    if (currentFolder.value) {
      formData.append('idcarpetapadre', currentFolder.value.idcarpeta)
    }

    console.log('Uploading file with data:', {
      idestructura: route.params.id,
      idcarpetapadre: currentFolder.value ? currentFolder.value.idcarpeta : null,
      file: file.name,
      size: file.size
    })
    console.log('estructura id:', route.params.id)
    await api.estructuras.uploadFile(route.params.id, formData)
    // await api.estructuras.uploadFile(
    //   route.params.id,
    //   {
    //     file,
    //     idcarpetapadre: currentFolder.value?.idcarpeta ?? null,
    //   },
    //   {
    //     onUploadProgress: (e) => {
    //       const pct = Math.round((e.loaded * 100) / e.total)
    //       console.log('Progreso:', pct, '%')
    //     }
    //   }
    // )

    alert('Archivo subido correctamente')
    event.target.value = ''
    await cargarEstructura()
  } catch (error) {
    console.error('Error al subir archivo:', error)
    alert(error.response?.data?.detail || 'Error al subir el archivo')
    event.target.value = ''
  }
}

const guardarCarpeta = async () => {
  if (!modalNodo.value.nombre.trim()) {
    alert('El nombre es obligatorio')
    return
  }
  
  try {
    await api.estructuras.createCarpeta(route.params.id, {
      nombre: modalNodo.value.nombre,
      archivo: false,
      idcarpetapadre: modalNodo.value.idcarpetapadre
    })
    
    showModal.value = false
    await cargarEstructura()
  } catch (error) {
    console.error('Error al crear carpeta:', error)
    alert('Error al crear la carpeta')
  }
}

const descargarArchivo = (item) => {
  window.open(`http://localhost:8000${item.archivo_url}`, '_blank')
}

// const eliminarNodo = async (nodo) => {
//   if (!confirm(`¿Está seguro de eliminar "${nodo.nombre}"?`)) return
  
//   try {
//     if (nodo.archivo) {
//       await api.estructuras.deleteFile(nodo.idcarpeta)
//     } else {
//       await api.estructuras.delete(nodo.idcarpeta)
//     }
//     await cargarEstructura()
//   } catch (error) {
//     console.error('Error al eliminar:', error)
//     alert('Error al eliminar')
//   }
// }

const agregarCarpeta = () => {
  modalNodo.value = {
    nombre: '',
    archivo: false,
    idcarpetapadre: currentFolder.value?.idcarpeta || route.params.id,//route.params.id,
    activa: true
  }
  showModal.value = true
}

const mostrarInputArchivo = () => {
  fileInput.value.click()
}

const subirArchivo = () => {
  modalNodo.value = {
    nombre: '',
    archivo: true,
    idcarpetapadre: currentFolder.value?.idcarpeta || route.params.id,//route.params.id,
    activa: true
  }
  showModal.value = true
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 10 * 1024 * 1024) {
      alert('El archivo no puede superar los 10MB')
      event.target.value = ''
      return
    }
    selectedFile.value = file
    modalNodo.value.nombre = file.name
  }
}

const guardarNodo = async () => {
  if (!modalNodo.value.nombre.trim()) {
    alert('El nombre es obligatorio')
    return
  }
  
  try {
    if (modalNodo.value.idcarpeta) {
      // Editar
      await api.estructuras.update(modalNodo.value.idcarpeta, modalNodo.value)
    } else {
      // Crear
      const formData = new FormData()
      formData.append('idestructura', route.params.id)
      formData.append('nombre', modalNodo.value.nombre)
      formData.append('archivo', modalNodo.value.archivo)
      formData.append('idcarpetapadre', modalNodo.value.idcarpetapadre)
      formData.append('activa', modalNodo.value.activa)

      if (selectedFile.value) {
        formData.append('file', selectedFile.value)
      }
      
      console.log('file to upload:', selectedFile.value)
      console.log('formdata:', formData)


      console.log('[v0] Creating new node with data:', {
        idestructura: parseInt(route.params.id),
        nombre: modalNodo.value.nombre,
        archivo: modalNodo.value.archivo,
        idcarpetapadre: parseInt(modalNodo.value.idcarpetapadre),
        activa: modalNodo.value.activa,
        file: selectedFile.value ? selectedFile.value.name : null
      })

      console.log('estructura id:', route.params.id)

      await api.estructuras.createCarpeta(route.params.id, formData)
    }
    
    showModal.value = false
    selectedFile.value = null
    await cargarEstructura()
  } catch (error) {
    console.error('Error al guardar nodo:', error)
    alert('Error al guardar')
  }
}

const editarNodo = (nodo) => {
  modalNodo.value = { ...nodo }
  showModal.value = true
}

const eliminarNodo = async (nodo) => {
  if (!confirm(`¿Está seguro de eliminar "${nodo.nombre}"?`)) return
  
  try {
    if (nodo.archivo) {
      await api.estructuras.deleteFile(nodo.idcarpeta)
    } else {
      await api.estructuras.delete(nodo.idcarpeta)
    }
    await cargarEstructura()
  } catch (error) {
    console.error('Error al eliminar:', error)
    alert('Error al eliminar')
  }
}


const handleDragOver = (e) => {
  e.preventDefault()
  if (!isDragging.value) {
    isDragging.value = true
  }
  dragCounter++
}
const handleDragLeave = (e) => {
  dragCounter--
  if (dragCounter === 0) {
    isDragging.value = false
  }
}
const handleDrop = async (e) => {
  e.preventDefault()
  isDragging.value = false
  dragCounter = 0
  
  const files = e.dataTransfer.files
  if (files.length === 0) return
  
  const file = files[0]
  
  // Validar tamaño
  if (file.size > 10 * 1024 * 1024) {
    alert('El archivo no puede superar los 10MB')
    return
  }
  
  try {
    const formData = new FormData()
    formData.append('file', file)
    if (currentFolder.value) {
      formData.append('idcarpetapadre', currentFolder.value.idcarpeta)
    }
    
    await api.estructuras.uploadFile(route.params.id, formData)
    alert('Archivo subido correctamente')
    await cargarEstructura()
  } catch (error) {
    console.error('Error al subir archivo:', error)
    alert(error.response?.data?.detail || 'Error al subir el archivo')
  }
}

const goBack = () => {
  router.push('/admin/arbol-carpetas')
}

onMounted(() => {
  cargarEstructura()
})
</script>

<style scoped>
.header-bg {
  background-color: var(--color-bg-secondary);
}

.header-border {
  border-bottom: 1px solid var(--color-border);
}

.main-content {
  background-color: var(--color-bg-primary);
}

.card {
  background-color: var(--color-bg-secondary);
  border-radius: 0.5rem;
  border: 1px solid var(--color-border);
}

.theme-text {
  color: var(--color-text-primary);
}

.input-field {
  width: 100%;
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 0.375rem;
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
  transition: all 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.btn-primary {
  padding: 0.5rem 1rem;
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  opacity: 0.9;
}

.btn-secondary {
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  background-color: transparent;
  color: var(--color-text-primary);
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background-color: var(--color-bg-tertiary);
}

.btn-icon {
  padding: 0.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-success {
  background-color: #10b981;
  color: white;
}

.btn-success:hover {
  background-color: #059669;
}

.tree-container {
  border: 1px solid var(--color-border);
  border-radius: 0.375rem;
  padding: 1rem;
  background-color: var(--color-bg-primary);
}

.table-container {
  border: 1px solid var(--color-border);
  border-radius: 0.375rem;
  overflow: hidden;
  background-color: var(--color-bg-primary);
  position: relative;
  transition: all 0.2s;
}

.table-container.drag-over {
  border-color: var(--color-primary);
  border-width: 2px;
  background-color: rgba(59, 130, 246, 0.05);
}

.drag-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(59, 130, 246, 0.1);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  pointer-events: none;
}

.drag-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: var(--color-primary);
  padding: 2rem;
  border: 2px dashed var(--color-primary);
  border-radius: 0.5rem;
  background-color: var(--color-bg-secondary);
}

.modal-content {
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
}
.breadcrumbs {
  padding: 0.75rem;
  background-color: var(--color-bg-tertiary);
  border-radius: 0.375rem;
  border: 1px solid var(--color-border);
}

.breadcrumb-item {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  color: var(--color-text-secondary);
  transition: all 0.2s;
  display: flex;
  align-items: center;
}

.breadcrumb-item:hover {
  background-color: var(--color-bg-secondary);
  color: var(--color-primary);
}
.table-row-hover {
  cursor: pointer;
  transition: background-color 0.3s;
}

.table-row-hover:hover {
  background-color: var(--color-row-hover);
}
</style>
