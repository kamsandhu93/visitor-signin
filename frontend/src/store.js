import Vue from 'vue'
import Vuex from 'vuex'
import config from './assets/js/config-helper.js'

Vue.use(Vuex)

var state = {
    config: config.read(),
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
