<template>
    <el-main>
        <el-row class="imgContainer">
            <img src="../assets/img/nhs_digital_logo.png" />
        </el-row>
        <el-row>
            <h1>Visitior Registration</h1>
        </el-row>
        <el-row type="flex" justify="center" :gutter="20">
            <el-col :span="12">
                <el-button type="success" @click="changeRoute('signin')" class="btnMain"><b>Sign In</b></el-button>
            </el-col>
            <el-col :span="12">
                <el-button type="danger" @click="changeRoute('signout')" class="btnMain"><b>Sign Out</b></el-button>
            </el-col>
        </el-row>
    </el-main>
</template>

<script>
    import RouteHelper from '../mixins/route-helper.js'
    import FailureTracker from '../mixins/failure-tracker.js'

    export default {
        mixins: [RouteHelper, FailureTracker]
    }
</script>

<style scoped>
    .el-row {
        margin: 5px;
    }

    .btnMain {
        font-size: 38pt;
        height: 200px;
        width: 350px;
    }


    h1 {
        font-size: 40pt;
    }

    img {
        width: 150px;
    }

    .imgContainer {
        text-align: left;
    }
</style>
