import Vue from 'vue'
import App from './App'
import router from './router.js'
import store from './store.js'
import NhsukFrontendVue from 'nhsuk-frontend-vue'
import Notifications from 'vue-notification'

import './registerServiceWorker'

Vue.use(NhsukFrontendVue)
Vue.use(Notifications)
Vue.config.productionTip = false

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
