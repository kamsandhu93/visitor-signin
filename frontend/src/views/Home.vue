<template>
    <el-main>
        <el-row>
            <h1>Visitior Registration</h1>
        </el-row>
        <el-row type="flex" justify="center" :gutter="20">
            <el-col :span="8">
                <el-button type="success" @click="changeRoute('/signin')"><b>Sign In</b></el-button>
            </el-col>
            <el-col :span="8">
                <el-button type="danger" @click="changeRoute('/signout')"><b>Sign Out</b></el-button>
            </el-col>
        </el-row>
    </el-main>
</template>

<script>

export default {
    methods: {
        changeRoute (route) {
            this.$router.push({path: route})
        }
    }
}
</script>

<style scoped>

    .el-row {
        margin: 10px;
    }

    button {
        font-size: 38pt;
        height: 200px;
        width: 400px;
    }


    h1 {
        font-size: 40pt;
    }
</style>
