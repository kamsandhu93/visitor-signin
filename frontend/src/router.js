import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home.vue'
import SignIn from '@/views/SignIn.vue'
import SignOut from '@/views/SignOut.vue'
import PrintLoading from '@/views/PrintLoading.vue'
import ErrorPage from '@/views/Error.vue'
import TransitionPage from '@/views/TransitionPage.vue'
import PrintError from '@/views/PrintError.vue'

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
            path: '/loading',
            name: 'loading',
            component: PrintLoading
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
        },
        {
            path: '/printerror',
            name: 'printerror',
            component: PrintError
        }
    ]
})
