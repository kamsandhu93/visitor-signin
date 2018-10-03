<template>
    <el-main>
        <el-row>
            <h1>Visitior Sign In</h1>
        </el-row>
        <el-row type="flex" justify="center" class="btnContainer">
            <el-col :span="8">
                <el-button type="success" @click="changeRoute('/signin')">Sign In</el-button>
            </el-col>
            <el-col :span="8">
                <el-button type="danger" @click="changeRoute('/signout')">Sign Out</el-button>
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
    .btnContainer {
        margin-top: calc(35vh - 100px);
    }

    button {
        font-size: 32pt;
        height: 200px;
        width: 400px;
    }
</style>
