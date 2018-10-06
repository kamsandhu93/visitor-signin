<template>
    <el-main>
        <el-row>
            <h1>404 - Not Found</h1>
        </el-row>
        <el-row>
            <el-button type="primary" @click="backToHome()">Back to Home</el-button>
        </el-row>
    </el-main>
</template>

<script>
    export default {
        methods: {
            backToHome() {
                this.$router.push({path: '/'})
            }
        }
    }
</script>

<style scoped>
    h1 {
        font-size: 36pt;
    }

    button {
        font-size: 14pt;
    }
</style>
