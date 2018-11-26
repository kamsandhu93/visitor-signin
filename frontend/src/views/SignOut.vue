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
                    <form-item id="passId" maxlength="6" label="Pass ID" prop="passId" v-model="formData['passId']"></form-item>
                    <form-button formName="signOutForm" @submitForm="submitForm($event)" @resetForm="resetForm($event)" @changeRoute="changeRoute($event)"></form-button>
                </el-form>
            </el-col>
        </el-row>
    </el-main>
</template>

<script>
    import axios from 'axios'
    import FormItem from '@/components/common/FormItem.vue'
    import FormButton from '@/components/common/FormButton.vue'
    import RouteHelper from '@/mixins/route-helper.js'
    import NotificationHelper from '@/mixins/notification-helper.js'
    import FormHelper from '@/mixins/form-helper.js'
    import FailureTracker from '@/mixins/failure-tracker.js'
    import { QrcodeReader } from 'vue-qrcode-reader'
    import 'vue-qrcode-reader/dist/vue-qrcode-reader.css'

    export default {
        components: {
            FormItem,
            QrcodeReader,
            FormButton
        },
        mixins: [RouteHelper, NotificationHelper, FormHelper, FailureTracker],
        data () {
            return {
                formData: {
                    passId: ""
                },
                rules: {
                    passId: [{ validator: this.checkPassId, trigger: "blur" }]
                },
                qrVideoOptions: {
                    facingMode: 'user'
                }
            }
        },
        methods: {
            submitQR(decodedQr) {
                this.formData["passId"] = decodedQr
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
                axios.post(`${this.$store.getters.url}/logout`, this.formData)
                .then((response) => {
                    var name = `${response.data.firstname} ${response.data.surname}`
                    var query = {
                        transitionType: 'signout',
                        name: name
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
            },
            checkPassId(rule, value, callback) {
                var regex = new RegExp("^[0-9]{5}[a-z]$")
                this.checkFormValueEmpty(value, "Please input Pass ID", callback)
                this.checkFormValue(value, regex, "Pass ID has format: 0000a", callback)
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
