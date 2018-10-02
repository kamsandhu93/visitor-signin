<template>
    <el-main>
        <el-row>
            <p>404 - Not Found</p>
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
