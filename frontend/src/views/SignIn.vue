<template>
    <el-main>
        <el-row>
            <h1>Sign In</h1>
        </el-row>
        <el-row type="flex" justify="center">
            <el-col :span="20">
                <el-form :model="formData" :rules="rules" ref="signInForm">
                    <form-item maxlength="32" label="First Name" prop="name" v-model="formData['name']" id="name"></form-item>
                    <form-item maxlength="32" label="Surname" prop="surname" v-model="formData['surname']" id="surname"></form-item>
                    <form-item maxlength="32" label="Visiting" prop="visiting" v-model="formData['visiting']" id="visiting"></form-item>
                    <form-item maxlength="32" label="Company" prop="company" v-model="formData['company']" id="company"></form-item>
                    <form-button formName="signInForm" @submitForm="submitForm($event)" @resetForm="resetForm($event)" @changeRoute="changeRoute($event)"></form-button>
                </el-form>
            </el-col>
        </el-row>
        <el-row>
            <el-dialog :visible.sync="confirmDialog" width="50%">
                <span slot="title"><h2>Confirm Details</h2></span>
                <confirm-dialog-item id="confirmName" label="Name" :body="getFullName()"></confirm-dialog-item>
                <confirm-dialog-item id="confirmVisiting" label="Visiting" :body="formData['visiting']"></confirm-dialog-item>
                <confirm-dialog-item id="confirmCompany" label="Company" :body="formData['company']"></confirm-dialog-item>
                <span slot="footer">
                    <el-button id="btnDialogConfirm" type="primary" icon="el-icon-check" @click="sendSigninRequest()">Confirm</el-button>
                    <el-button id="btnDialogCancel" type="danger" icon="el-icon-close" @click="confirmDialog = false" plain>Cancel</el-button>
                </span>
            </el-dialog>
        </el-row>
    </el-main>
</template>

<script>
    import axios from 'axios'
    import ConfirmDialogItem from '@/components/signin/ConfirmDialogItem.vue'
    import FormItem from '@/components/common/FormItem.vue'
    import FormButton from '@/components/common/FormButton.vue'
    import RouteHelper from '@/mixins/route-helper.js'
    import NotificationHelper from '@/mixins/notification-helper.js'
    import FormHelper from '@/mixins/form-helper.js'
    import FailureTracker from '@/mixins/failure-tracker.js'

    export default {
        components: {
            ConfirmDialogItem,
            FormItem,
            FormButton
        },
        mixins: [RouteHelper, NotificationHelper, FormHelper, FailureTracker],
        data() {
            return {
                formData: {
                    name: "",
                    surname: "",
                    visiting: "",
                    company: ""
                },
                rules: {
                    name: [{ validator: this.checkFirstName, trigger: "blur" }],
                    surname: [{ validator: this.checkLastName, trigger: "blur" }],
                    visiting: [{ validator: this.checkVisiting, trigger: "blur" }],
                    company: [{ validator: this.checkCompany, trigger: "blur" }]
                },
                confirmDialog: false
            }
        },
        methods: {
            submitForm(formName) {
                this.validateForm(formName, (valid) => {
                    if (valid) {
                        this.removeSpaces()
                        this.confirmDialog = true
                    }
                })
            },
            removeSpaces() {
                for (var key in this.formData) {
                    this.formData[key] = this.formData[key].trim()
                }
            },
            sendSigninRequest() {
                this.removeEmptyOptionalKeys(['company'])
                axios.post(`${this.$store.getters.url}/login`, this.formData)
                .then((response) => {
                    var query = {
                        name: this.getFullName(),
                        company: this.formData['company'],
                        passId: response.data.passId
                    }
                    this.changeRouteQuery('pass', query)
                })
                .catch((e) => {
                    this.notifyError("An error occured when signing in - please try again. If problem persists, please inform the receptionist.")
                })
            },
            removeEmptyOptionalKeys(keys) {
                for (var key of keys) {
                    if (!this.formData[key]) {
                        delete this.formData[key]
                    }
                }
            },
            getFullName() {
                return `${this.formData["name"]} ${this.formData["surname"]}`
            },
            checkFirstName(rule, value, callback) {
                var regex = new RegExp("^[A-Za-z]{1,32}$")
                this.checkFormValueEmpty(value, "Please input your first name", callback)
                this.checkFormValue(value, regex, "Accepted characters: A-Z, a-z", callback)
            },
            checkLastName(rule, value, callback) {
                var regex = new RegExp("^[A-Za-z]{1,32}$")
                this.checkFormValueEmpty(value, "Please input your last name", callback)
                this.checkFormValue(value, regex, "Accepted characters: A-Z, a-z", callback)
            },
            checkVisiting(rule, value, callback) {
                var regex = new RegExp("^[A-Za-z ]{1,32}$")
                this.checkFormValueEmpty(value, "Please input who you are visiting", callback)
                this.checkFormValue(value, regex, "Accepted characters: A-Z, a-z and space", callback)
            },
            checkCompany(rule, value, callback) {
                var regex = new RegExp("^[A-Za-z0-9 ]{1,32}$")
                if (!value) {
                    return callback()
                }
                this.checkFormValue(value, regex, "Accepted characters: A-Z, a-z, 0-9 and space", callback)
            }
        }
    }
</script>

<style scoped>
    button {
        padding: 20px;
        font-size: 16pt;
    }
</style>
