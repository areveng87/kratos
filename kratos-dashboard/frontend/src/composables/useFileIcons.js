// src/composables/useFileIcons.js
import { 
  Folder, File, FileText, FileArchive, FileImage, FileAudio, FileVideo, FileCode, FileSpreadsheet, FileType 
} from 'lucide-vue-next'

// Grupos de extensiones
const imageExts = ['png','jpg','jpeg','gif','webp','svg', 'ico']
const videoExts = ['mpg','mp4','mov','avi','mkv','webm']
const audioExts = ['mp3','wav','ogg','m4a']
const wordExts  = ['doc','docx']
const excelExts = ['xls','xlsx','csv']
const pptExts   = ['ppt','pptx']
const codeExts  = ['js','ts','json','xml','html','css','py','java','c','cpp','cs','sql','md']

const getExt = (name = '') => {
  const i = name.lastIndexOf('.')
  return i === -1 ? '' : name.slice(i + 1).toLowerCase()
}

// Variante A: devolver URL de icono (usa assets locales)
// Coloca tus SVG/PNG en src/assets/filetypes/...
const getIconUrl = (item) => {

  console.log("getIconUrl item:", item)

  if (!item || !item.archivo) {
    return new URL('../assets/filetypes/folder.svg', import.meta.url).href
  }
  const ext = getExt(item.nombre)

  console.log("getIconUrl ext:", ext)

  if (imageExts.includes(ext) && item.archivo_url) {
    // Miniatura real del archivo si es imagen
    return `http://localhost:8000${item.archivo_url}`
  }

  if (ext === 'pdf')                    return new URL('../assets/filetypes/pdf.svg', import.meta.url).href
  if (wordExts.includes(ext))           return new URL('../assets/filetypes/word.svg', import.meta.url).href
  if (excelExts.includes(ext))          return new URL('../assets/filetypes/excel.svg', import.meta.url).href
  if (pptExts.includes(ext))            return new URL('../assets/filetypes/ppt.svg', import.meta.url).href
  if (videoExts.includes(ext))          return new URL('../assets/filetypes/video.svg', import.meta.url).href
  if (audioExts.includes(ext))          return new URL('../assets/filetypes/audio.svg', import.meta.url).href
  if (codeExts.includes(ext))           return new URL('../assets/filetypes/code.svg', import.meta.url).href
  if (['zip','rar','7z'].includes(ext)) return new URL('../assets/filetypes/zip.svg', import.meta.url).href
  if (ext === 'txt')                    return new URL('../assets/filetypes/txt.svg', import.meta.url).href

  return new URL('../assets/filetypes/file.svg', import.meta.url).href
}

// Variante B: devolver componente de icono (lucide)
const getIconComponent = (item) => {
  if (!item || !item.archivo) return Folder
  const ext = getExt(item.nombre)
  if (ext === 'pdf')                    return FileType
  if (wordExts.includes(ext))           return FileText
  if (excelExts.includes(ext))          return FileSpreadsheet
  if (pptExts.includes(ext))            return FileType
  if (['zip','rar','7z'].includes(ext)) return FileArchive
  if (imageExts.includes(ext))          return FileImage
  if (audioExts.includes(ext))          return FileAudio
  if (videoExts.includes(ext))          return FileVideo
  if (codeExts.includes(ext))           return FileCode
  if (ext === 'txt')                    return FileText
  return File
}

const getTipoLabel = (item) => {
  if (!item || !item.archivo) return 'Carpeta'
  const ext = getExt(item.nombre)
  if (imageExts.includes(ext))          return 'Imagen'
  if (videoExts.includes(ext))          return 'Video'
  if (audioExts.includes(ext))          return 'Audio'
  if (wordExts.includes(ext))           return 'Word'
  if (excelExts.includes(ext))          return 'Excel'
  if (pptExts.includes(ext))            return 'PowerPoint'
  if (ext === 'pdf')                    return 'PDF'
  if (ext === 'txt')                    return 'Texto'
  if (['zip','rar','7z'].includes(ext)) return 'Comprimido'
  if (codeExts.includes(ext))           return 'Código'
  return 'Archivo'
}

export function useFileIcons () {
  return {
    getExt,
    getIconUrl,
    getIconComponent,
    getTipoLabel,
  }
}
