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
    #app {
        font-family: Arial;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #231f20;
    }

    button {
        font-size: 14pt;
    }

    h1 {
        color: #005EB8;
        font-size: 24pt;
    }

    h2 {
        color: #005EB8;
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
