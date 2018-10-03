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
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
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
</style>
