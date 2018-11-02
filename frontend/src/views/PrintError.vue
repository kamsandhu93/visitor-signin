<template>
    <el-main>
        <main-logo></main-logo>
        <el-row>
            <h1>Visitor pass print failed</h1>
            <span class="blueFont">Please note down your Pass ID: </span><span>{{ $route.query.passId }}</span>
            <h1>and inform the reception</h1>
        </el-row>
        <el-row>
            <el-button type="primary" @click="changeRoute('home')">Home</el-button>
        </el-row>
    </el-main>
</template>

<script>
    import RouteHelper from '../mixins/route-helper.js'
    import MainLogo from '../components/common/MainLogo.vue'

    export default {
        components: {
            MainLogo
        },
        mixins: [RouteHelper]
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

    .blueFont {
        color: var(--nhs-blue);
    }

    button {
        padding: 20px;
        font-size: 16pt;
    }
</style>
