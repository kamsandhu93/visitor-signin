<template>
    <el-main>
        <main-logo></main-logo>
        <el-row>
            <h1>Visitor Registration</h1>
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
    import MainLogo from '../components/common/MainLogo.vue'

    export default {
        mixins: [RouteHelper, FailureTracker],
        components: {
            MainLogo
        }
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
</style>
