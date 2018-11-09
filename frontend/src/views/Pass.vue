<template>
    <el-main>
        <el-row>
            <h1>Please read the health and safety information while your visitor pass prints</h1>
        </el-row>
        <el-row type="flex" justify="space-between">
            <el-col :span="7">
                <pass-welcome></pass-welcome>
            </el-col>
            <el-col :span="8">
                <pass-example :query="$route.query"></pass-example>
            </el-col>
            <el-col :span="7">
                <pass-fire></pass-fire>
            </el-col>
        </el-row>
    </el-main>
</template>

<script>
    import axios from 'axios'
    import RouteHelper from '../mixins/route-helper.js'
    import NotificationHelper from '../mixins/notification-helper.js'
    import QrcodeVue from 'qrcode.vue'
    import PassExample from '../components/pass/PassExample.vue'
    import PassWelcome from '../components/pass/PassWelcome.vue'
    import PassFire from '../components/pass/PassFire.vue'

    export default {
        components: {
            QrcodeVue,
            PassExample,
            PassWelcome,
            PassFire
        },
        mixins: [RouteHelper, NotificationHelper],
        methods: {
            printPage() {
                axios.post(this.$store.getters.printer, this.$route.query)
                .then((response) => {
                    var query = {
                        transitionType: 'signin',
                        name: this.$route.query.name
                    }
                    this.changeRouteQuery('transition', query)
                })
                .catch((error) => {
                    console.log(error)
                    this.changeRouteQuery('printerror', { passId: this.$route.query.passId })
                })
            }
        },
        mounted() {
            setTimeout(() => {
                this.printPage()
            }, 5000)
        }
    }
</script>

<style scoped>
    .el-row {
        margin: 5px;
    }
</style>
