<template>
    <nhs-main>
        <nhs-row>
            <nhs-col>
                <nhs-heading size="xl">Sign Out</nhs-heading>
            </nhs-col>
        </nhs-row>
        <nhs-row v-if="qron">
            <nhs-col>
                <qrcode-reader @decode="submitQR" :camera="qrVideoOptions"></qrcode-reader>
            </nhs-col>
        </nhs-row>
        <nhs-row>
            <nhs-col>
                <form-item
                    id="passId" name="passId" :maxlength="6"
                    label="Pass ID" :error="errors['passId']"
                    v-model.trim="formData['passId']"
                    @blur="checkPassId()"
                ></form-item>

                <form-button @submitForm="submitForm()" @resetForm="resetForm()"></form-button>
            </nhs-col>
        </nhs-row>
    </nhs-main>
</template>

<script>
    import axios from 'axios'
    import FormItem from '@/components/common/FormItem.vue'
    import FormButton from '@/components/common/FormButton.vue'
    import RouteHelper from '@/mixins/route-helper.js'
    import NotificationHelper from '@/mixins/notification-helper.js'
    import FailureTracker from '@/mixins/failure-tracker.js'
    import { QrcodeReader } from 'vue-qrcode-reader'
    import 'vue-qrcode-reader/dist/vue-qrcode-reader.css'

    export default {
        components: {
            FormItem,
            QrcodeReader,
            FormButton
        },
        mixins: [RouteHelper, NotificationHelper, FailureTracker],
        data () {
            return {
                formData: {
                    passId: ""
                },
                errors: {
                    passId: ""
                },
                qrVideoOptions: {
                    facingMode: 'user'
                },
                qron: false
            }
        },
        methods: {
            submitQR(decodedQr) {
                this.formData["passId"] = decodedQr
                this.readerPaused = true
                this.submitForm('signOutForm')
            },
            submitForm(formName) {
                this.checkPassId()
                if (this.isFormValid()) {
                    this.sendSignoutRequest()
                }
            },
            isFormValid() {
                for (var key in this.errors) {
                    if (this.errors[key]) {
                        return false
                    }
                }
                return true
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
                    this.notifyError("An error occured when signing out - please try again. If problem persists, please inform the receptionist.")
                })
            },
            checkFormData(name, regex, emptyErr, valueErr) {
                if (!this.formData[name]) {
                    this.errors[name] = emptyErr
                }
                else if (!regex.test(this.formData[name])) {
                    this.errors[name] = valueErr
                }
                else {
                    this.errors[name] = ""
                }
            },
            checkPassId() {
                var regex = new RegExp("^[0-9]{5}[a-z]$")
                var emptyErr = "Please input Pass ID"
                var valueErr = "Pass ID has format: 00000a"
                this.checkFormData("passId", regex, emptyErr, valueErr)
            },
            resetForm() {
                for (var field in this.formData) {
                    this.formData[field] = ""
                }
                for (var error in this.errors) {
                    this.errors[error] = ""
                }
            }
        }
    }
</script>

<style scoped>
    .qrContainer {
        text-align: center;
    }
</style>
