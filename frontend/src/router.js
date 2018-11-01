import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import SignIn from './views/SignIn.vue'
import SignOut from './views/SignOut.vue'
import Pass from './views/Pass.vue'
import ErrorPage from './views/Error.vue'
import TransitionPage from './views/TransitionPage.vue'

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
            name: 'signin',
            component: SignIn
        },
        {
            path: '/signout',
            name: 'signout',
            component: SignOut
        },
        {
            path: '*',
            redirect: '/'
        },
        {
            path: '/pass',
            name: 'pass',
            component: Pass
        },
        {
            path: '/error',
            name: 'error',
            component: ErrorPage
        },
        {
            path: '/transition',
            name: 'transition',
            component: TransitionPage
        }
    ]
})
