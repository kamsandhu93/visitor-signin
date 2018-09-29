import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import SignIn from './views/SignIn.vue'
import SignOut from './views/SignOut.vue'
import NotFound from './views/NotFound.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/signin',
            component: SignIn
        },
        {
            path: '/signout',
            component: SignOut
        },
        {
            path: '*',
            redirect: '/'
        }
    ],
    mode: 'history'
})
