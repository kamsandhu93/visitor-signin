import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

var state = {
    config: {
        host: process.env.VUE_APP_REQUEST_HOST,
        dbapiPort: 5000,
        printerPort: 5002
    },
    failures: 0
}


export default new Vuex.Store({
    state: state,
    getters: {
        url(state) {
            var host = state.config['host']
            var port = state.config['dbapiPort']
            return `http://${host}:${port}`
        },
        printer(state) {
            var host = state.config['host']
            var port = state.config['printerPort']
            return `http://${host}:${port}/print`
        }
    },
    mutations: {
        recordFailure(state) {
            state.failures += 1
        },
        resetFailure(state) {
            state.failures = 0
        }
    }
})
