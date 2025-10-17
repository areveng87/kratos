import { ref } from 'vue'

export function useConfirm() {
  const show = ref(false)
  const message = ref('')
  let resolver = null

  const confirmar = (msg = '¿Estás seguro?') => {

    console.log('[v0] Confirm message:', msg)

    message.value = msg
    show.value = true
    return new Promise((resolve) => { resolver = resolve })
  }

  const accept = () => { show.value = false; resolver?.(true) }
  const cancel = () => { show.value = false; resolver?.(false) }

  return { show, message, confirmar, accept, cancel }
}
