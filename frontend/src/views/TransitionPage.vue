<template>
    <el-main>
        <main-logo></main-logo>
        <el-row v-if="$route.query.transitionType == 'signout'">
            <span class="signinName">{{ $route.query.name }}</span><span class="signinMsg"> sign out success</span>
            <h1>Please return your visitor pass to reception</h1>
        </el-row>
        <el-row v-if="$route.query.transitionType == 'signin'">
            <span class="signinName">{{ $route.query.name }}</span><span class="signinMsg"> sign in success</span>
            <h1>Please collect your visitor pass from reception</h1>
        </el-row>
        <el-row>
            <el-button type="primary" @click="changeRoute('home')">Home</el-button>
        </el-row>
    </el-main>
</template>

<script>
    import FailureTracker from '../mixins/failure-tracker.js'
    import RouteHelper from '../mixins/route-helper.js'
    import MainLogo from '../components/common/MainLogo.vue'

    export default {
        components: {
            MainLogo
        },
        mixins: [FailureTracker, RouteHelper],
        mounted() {
            setTimeout(() => {
                this.changeRoute('home')
            }, 5000)
        }
    }
</script>

<style scoped>
    h1 {
        font-size: 36pt;
    }

    span {
        font-size: 36pt;
        font-weight: bold;
    }

    .signinMsg {
        color: var(--nhs-blue);
    }

    button {
        padding: 20px;
        font-size: 16pt;
    }
</style>
