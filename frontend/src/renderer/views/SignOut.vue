<template>
    <el-main>
        <el-row>
            <h1>Sign Out</h1>
        </el-row>
        <el-row>
            <qrcode-reader @decode="submitQR" :camera="qrVideoOptions"></qrcode-reader>
        </el-row>
        <el-row type="flex" justify="center">
            <el-col :span="20">
                <el-form :model="formData" :rules="rules" ref="signOutForm">
                    <form-item label="Pass ID" prop="pass_id" v-model="formData['pass_id']"></form-item>
                    <el-form-item>
                        <el-button type="primary" icon="el-icon-check" @click="submitForm('signOutForm')">Sign Out</el-button>
                        <el-button type="info" icon="el-icon-refresh" @click="resetForm('signOutForm')" plain>Reset</el-button>
                        <el-button type="danger" icon="el-icon-close" @click="changeRoute('home')" plain>Cancel</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </el-main>
</template>

<script>
    import axios from 'axios'
    import FormItem from '../components/common/FormItem.vue'
    import RouteHelper from '../mixins/route-helper.js'
    import NotificationHelper from '../mixins/notification-helper.js'
    import FormHelper from '../mixins/form-helper.js'
    import FailureTracker from '../mixins/failure-tracker.js'
    import { QrcodeReader } from 'vue-qrcode-reader'
    import 'vue-qrcode-reader/dist/vue-qrcode-reader.css'

    export default {
        components: {
            FormItem,
            QrcodeReader
        },
        mixins: [RouteHelper, NotificationHelper, FormHelper, FailureTracker],
        data () {
            return {
                formData: {
                    pass_id: ""
                },
                rules: {
                    pass_id: [
                        { required: true, message: 'Please input Pass ID', trigger: 'blur' },
                        { min: 6, max: 6, message: 'Pass ID should be 6 characters long', trigger: 'blur' }
                    ]
                },
                qrVideoOptions: {
                    facingMode: 'user'
                }
            }
        },
        methods: {
            submitQR(decodedQr) {
                this.formData["pass_id"] = decodedQr
                this.readerPaused = true
                this.submitForm('signOutForm')
            },
            submitForm(formName) {
                this.validateForm(formName, (valid) => {
                    if (valid) {
                        this.sendSignoutRequest()
                    }
                })
            },
            sendSignoutRequest() {
                axios.post(`${this.$store.getters.url}/logout`, {body: this.formData})
                .then((response) => {
                    var query = {
                        transitionType: 'signout'
                    }
                    this.changeRouteQuery('transition', query)
                })
                .catch((e) => {
                    if (e['response']) {
                        this.notifyError(`${e.response.data.message}`)
                    }
                    else {
                        this.notifyError("An error occured when signing out. Please try again. If problem persists, please inform the receptionist.")
                    }
                })
            }
        }
    }
</script>

<style scoped>
    button {
        font-size: 16pt;
        padding: 20px;
    }

    .qrContainer {
        text-align: center;
    }
</style>
