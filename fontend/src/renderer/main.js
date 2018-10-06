import Vue from 'vue'
import axios from 'axios'

import App from './App'
import router from './router.js'
import store from './store.js'

import './plugins/element.js'

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
    components: { App },
    router,
    store,
    template: '<App/>'
}).$mount('#app')
