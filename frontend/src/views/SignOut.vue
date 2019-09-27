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
                    label="Pass ID" :rules="rules['passId']"
                    v-model.trim="formData['passId']"
                    ref="passId" @keydown.enter.native="submitForm()"
                ></form-item>

                <form-button @submitForm="submitForm()" @resetForm="resetForm()" :disabled="disableBtn"></form-button>
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
                rules: {
                    passId: [
                        (v) => this.validatePassId(v) || 'Pass ID has format: 00000a',
                        (v) => !!v || 'Please input Pass ID'
                    ]
                },
                qrVideoOptions: {
                    facingMode: 'user'
                },
                qron: false,
                disableBtn: false
            }
        },
        methods: {
            submitQR(decodedQr) {
                this.formData["passId"] = decodedQr
                this.readerPaused = true
                this.submitForm()
            },
            submitForm() {
                if (this.$refs.passId.validate()) {
                    this.sendSignoutRequest()
                }
            },
            sendSignoutRequest() {
                this.disableBtn = true
                axios.post(`${this.$store.getters.url}/logout`, this.formData)
                .then((response) => {
                    var name = `${response.data.firstName} ${response.data.surname}`
                    var query = {
                        transitionType: 'signout',
                        name: name
                    }
                    this.disableBtn = false
                    this.changeRouteQuery('transition', query)
                })
                .catch((e) => {
                    this.disableBtn = false
                    if (e.response.status === 409) {
                        this.notifyError(`PassID: ${this.formData['passId']} has already signed out`)
                    }
                    else {
                        this.notifyError("An error occured when signing out - please try again. If problem persists, please inform the receptionist.")
                    }
                })
            },
            resetForm() {
                for (var field in this.formData) {
                    this.formData[field] = ""
                }
            },
            validatePassId(passId) {
                if (passId.length < 6) {
                    return !!passId.match(/^[0-9a-z]+$/i)
                }
                else {
                    return !!passId.match(/^[0-9]{5}[a-z]$/)
                }
            }
        },
        mounted() {
            this.$refs.passId.focus()
        }
    }
</script>

<style scoped>
    .qrContainer {
        text-align: center;
    }
</style>
