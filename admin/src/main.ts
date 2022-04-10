import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import { createVuetify } from 'vuetify/lib/framework'

loadFonts()
const vuetify = createVuetify()

createApp(App)
  .use(router)
  .use(vuetify)
  .mount('#app')
