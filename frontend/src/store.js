import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

var state = {
    config: {
        host: process.env.VUE_APP_REQUEST_HOST,
        port: 5000
    },
    failures: 0
}


export default new Vuex.Store({
    state: state,
    getters: {
        url(state) {
            var host = state.config['host']
            var port = state.config['port']
            return `http://${host}:${port}`
        },
        printer(state) {
            return state.config['printer']
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
