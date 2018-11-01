import Vue from 'vue'
import App from './App'
import router from './router.js'
import store from './store.js'

import './registerServiceWorker'
import './plugins/element.js'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
