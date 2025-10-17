# Frontend Setup Instructions

## Instalación

1. **Instalar dependencias:**
   \`\`\`bash
   npm install
   \`\`\`

2. **Iniciar servidor de desarrollo:**
   \`\`\`bash
   npm run dev
   \`\`\`

3. **Ejecutar linter:**
   \`\`\`bash
   npm run lint
   \`\`\`

## Configuración del Linter

El proyecto usa ESLint configurado específicamente para Vue.js 3 con Composition API. 

### Reglas principales:
- Vue 3 Essential rules
- Composition API support
- Prettier integration
- Deshabilitadas las reglas de React hooks

### Archivos de configuración:
- \`.eslintrc.json\` - Configuración principal de ESLint
- \`.prettierrc\` - Configuración de formato de código
- \`.eslintignore\` - Archivos ignorados por el linter

## Solución de Problemas

Si ves errores de "useHookAtTopLevel", esto indica que el linter está aplicando reglas de React a código Vue. La configuración en este proyecto debería resolver estos problemas.

### Para VS Code:
Instala las siguientes extensiones:
- Vue Language Features (Volar)
- ESLint
- Prettier

### Para otros editores:
Asegúrate de que tu editor esté configurado para usar:
- Vue 3 language server
- ESLint con la configuración del proyecto
- Prettier para formato automático
\`\`\`
