<template>
    <el-container id="app">
        <router-view></router-view>
    </el-container>
</template>

<script>
    export default {
        name: 'app'
    }
</script>

<style>
    @import './assets/css/colors.css';

    #app {
        font-family: Arial;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: var(--nhs-black);
    }

    button {
        font-size: 14pt;
    }

    h1 {
        color: var(--nhs-blue);
        font-size: 24pt;
    }

    h2 {
        color: var(--nhs-blue);
    }
</style>

<style scoped>
    .logo {
        width: 180px;
        position: absolute;
        display: block;
        top: 50px;
        left: 50px;
    }
</style>
