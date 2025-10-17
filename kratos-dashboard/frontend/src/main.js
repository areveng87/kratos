import { createApp } from "vue"
import { createPinia } from "pinia"
import router from "./router"
import App from "./App.vue"
import "./style.css"

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)
app.use(router)

import { useThemeStore } from "./stores/theme"
const themeStore = useThemeStore()

app.mount("#app")

// Initialize theme after app is mounted
themeStore.initializeTheme()
