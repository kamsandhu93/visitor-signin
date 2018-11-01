<template>
    <el-main>
        <main-logo></main-logo>
        <el-row>
            <h1>The Service is currently unavailable</h1>
            <h1>Please inform the receptionist</h1>
        </el-row>
    </el-main>
</template>

<script>
    import FailureTracker from '../mixins/failure-tracker.js'
    import RouteHelper from '../mixins/route-helper.js'
    import MainLogo from '../components/common/MainLogo.vue'

    export default {
        mixins: [FailureTracker, RouteHelper],
        components: {
            MainLogo
        }
    }
</script>

<style scoped>
    h1 {
        font-size: 36pt;
    }
</style>
