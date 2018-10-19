<template>
    <el-main>
        <el-row>
            <h1>Sign In</h1>
        </el-row>
        <el-row type="flex" justify="center">
            <el-col :span="20">
                <el-form :model="formData" :rules="rules" ref="signInForm">
                    <form-item label="First Name" prop="name" v-model="formData['name']"></form-item>
                    <form-item label="Surname" prop="surname" v-model="formData['surname']"></form-item>
                    <form-item label="Visiting" prop="visiting" v-model="formData['visiting']"></form-item>
                    <form-item label="Company" prop="company" v-model="formData['company']"></form-item>
                    <el-form-item>
                        <el-button type="primary" icon="el-icon-check" @click="submitForm('signInForm')">Sign In</el-button>
                        <el-button type="info" icon="el-icon-refresh" @click="resetForm('signInForm')" plain>Reset</el-button>
                        <el-button type="danger" icon="el-icon-close" @click="changeRoute('home')" plain>Cancel</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
        <el-row>
            <el-dialog :visible.sync="confirmDialog" width="50%">
                <span slot="title"><h2>Confirm Details</h2></span>
                <confirm-dialog-item label="Name" :body="getFullName()"></confirm-dialog-item>
                <confirm-dialog-item label="Visiting" :body="formData['visiting']"></confirm-dialog-item>
                <confirm-dialog-item label="Company" :body="formData['company']"></confirm-dialog-item>
                <span slot="footer">
                    <el-button type="primary" icon="el-icon-check" @click="sendSigninRequest()">Confirm</el-button>
                    <el-button type="danger" icon="el-icon-close" @click="confirmDialog = false" plain>Cancel</el-button>
                </span>
            </el-dialog>
        </el-row>
    </el-main>
</template>

<script>
    import axios from 'axios'
    import ConfirmDialogItem from '../components/signin/ConfirmDialogItem.vue'
    import FormItem from '../components/common/FormItem.vue'
    import RouteHelper from '../mixins/route-helper.js'
    import NotificationHelper from '../mixins/notification-helper.js'
    import FormHelper from '../mixins/form-helper.js'
    import FailureTracker from '../mixins/failure-tracker.js'

    export default {
        components: {
            ConfirmDialogItem,
            FormItem
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
                    name: [
                        { required: true, message: "Please input your first name", trigger: "blur" },
                        { min: 1, max: 32, message: 'Length should be 1 to 32 characters', trigger: 'blur' }
                    ],
                    surname: [
                        { required: true, message: "Please input your surname", trigger: "blur" },
                        { min: 1, max: 32, message: 'Length should be 1 to 32 characters', trigger: 'blur' }
                    ],
                    visiting: [
                        { required: true, message: "Please input who you are visiting", trigger: "blur" },
                        { min: 1, max: 32, message: 'Length should be 1 to 32 characters', trigger: 'blur' }
                    ],
                    company: [
                        { min: 1, max: 32, message: 'Length should be 1 to 32 characters', trigger: 'blur' }
                    ]
                },
                confirmDialog: false
            }
        },
        methods: {
            submitForm(formName) {
                this.validateForm(formName, (valid) => {
                    if (valid) {
                        this.captializeField('name')
                        this.captializeField('surname')
                        this.captializeField('visiting')
                        this.confirmDialog = true
                    }
                })
            },
            captializeField(field) {
                this.formData[field] = this.formData[field].charAt(0).toUpperCase() + this.formData[field].slice(1);
            },
            sendSigninRequest() {
                axios.post(`${this.$store.getters.url}/login`, { body: this.formData })
                .then((response) => {
                    var query = {
                        name: this.getFullName(),
                        company: this.formData['company'],
                        passId: response.data.passId
                    }
                    this.changeRouteQuery('pass', query)
                })
                .catch((e) => {
                    if (e["response"]) {
                        this.notifyError(`${e.response.data.message}`)
                    }
                    else {
                        this.notifyError("An error occured when signing in. Please try again. If problem persists, please inform the receptionist.")
                    }
                })
            },
            getFullName() {
                return `${this.formData["name"]} ${this.formData["surname"]}`
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
