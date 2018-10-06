<template>
    <el-main>
        <el-row>
            <h1>Sign In</h1>
        </el-row>
        <el-row type="flex" justify="center">
            <el-col :span="12">
                <el-form :model="formData" :rules="rules" ref="signInForm">
                    <form-item label="First Name" prop="name" v-model="formData['name']"></form-item>
                    <form-item label="Surname" prop="surname" v-model="formData['surname']"></form-item>
                    <form-item label="Visiting" prop="visiting" v-model="formData['visiting']"></form-item>
                    <form-item label="Company" prop="company" v-model="formData['company']"></form-item>
                    <el-form-item>
                        <el-button type="primary" icon="el-icon-check" @click="submitForm('signInForm')">Sign In</el-button>
                        <el-button type="info" icon="el-icon-refresh" @click="resetForm('signInForm')" plain>Reset</el-button>
                        <el-button type="danger" icon="el-icon-close" @click="backToHome()" plain>Cancel</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
        <el-row>
            <el-dialog :visible.sync="dialogVisible" width="50%">
                <span slot="title"><h2>Confirm Details</h2></span>
                <confirm-dialog-item label="Name" :body="getFullName()"></confirm-dialog-item>
                <confirm-dialog-item label="Visiting" :body="formData['visiting']"></confirm-dialog-item>
                <confirm-dialog-item label="Company" :body="formData['company']"></confirm-dialog-item>
                <span slot="footer">
                    <el-button type="primary" icon="el-icon-check" @click="sendSigninRequest()">Confirm</el-button>
                    <el-button type="danger" icon="el-icon-close" @click="dialogVisible = false" plain>Cancel</el-button>
                </span>
            </el-dialog>
        </el-row>
    </el-main>
</template>

<script>
    import axios from 'axios'
    import ConfirmDialogItem from '../components/signin/ConfirmDialogItem.vue'
    import FormItem from '../components/common/FormItem.vue'

    export default {
        components: {
            ConfirmDialogItem,
            FormItem
        },
        data() {
            return {
                formData: {
                    name: "",
                    surname: "",
                    visiting: "",
                    company: ""
                },
                rules: {
                    name: [{required: true, message: "Please input your first name", trigger: "blur"}],
                    surname: [{required: true, message: "Please input your surname", trigger: "blur"}],
                    visiting: [{required: true, message: "Please input who you are visiting", trigger: "blur"}]
                },
                dialogVisible: false
            }
        },
        methods: {
            backToHome() {
                this.$router.push({path: '/'})
            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.dialogVisible = true
                    }
                    else {
                        return false
                    }
                })
            },
            resetForm(formName) {
                this.$refs[formName].resetFields()
            },
            sendSigninRequest() {
                axios.post('http://localhost:5000/login', {body: this.formData})
                .then(response => {
                    this.notifySuccess(`${response.data.message}`)
                    this.backToHome()
                })
                .catch(e => {
                    if (e["response"]) {
                        this.notifyError(`${e.response.data.message} - ${e.response.status}`)
                    }
                    else {
                        this.notifyError(`${e}`)
                    }
                })
            },
            getFullName() {
                return `${this.formData["name"]} ${this.formData["surname"]}`
            },
            notifySuccess(msg) {
                this.$notify({
                    title: "Sign in success",
                    message: msg,
                    type: "success"
                })
            },
            notifyError(msg) {
                this.$notify({
                    title: "Error",
                    message: msg,
                    type: "error"
                })
            }
        }
    }
</script>

<style scoped>
    button {
        margin: 5px;
        padding: 20px;
        font-size: 16pt;
    }
</style>
