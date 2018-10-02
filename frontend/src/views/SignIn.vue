<template>
    <el-main>
        <el-row type="flex" justify="center">
            <el-col :span="12">
                <el-form :model="formData" :rules="rules" ref="signInForm">
                    <el-form-item label="First Name" prop="name">
                        <el-input v-model="formData['name']"></el-input>
                    </el-form-item>
                    <el-form-item label="Surname" prop="surname">
                        <el-input v-model="formData['surname']"></el-input>
                    </el-form-item>
                    <el-form-item label="Visiting" prop="visiting">
                        <el-input v-model="formData['visiting']"></el-input>
                    </el-form-item>
                    <el-form-item label="Company" prop="company">
                        <el-input v-model="formData['company']"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="success" icon="el-icon-check" @click="submitForm('signInForm')">Sign In</el-button>
                        <el-button type="primary" icon="el-icon-refresh" @click="resetForm('signInForm')">Reset</el-button>
                        <el-button type="danger" icon="el-icon-close" @click="backToHome()">Cancel</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
        <el-row>
            <el-dialog
                title="Confirm Details"
                :visible.sync="dialogVisible"
                width="50%"
            >
                <confirm-dialog-item label="Name" :body="getFullName()"></confirm-dialog-item>
                <confirm-dialog-item label="Visiting" :body="formData['visiting']"></confirm-dialog-item>
                <confirm-dialog-item label="Company" :body="formData['company']"></confirm-dialog-item>
                <span slot="footer">
                    <el-button type="success" icon="el-icon-check" @click="sendSigninRequest()">Confirm</el-button>
                    <el-button type="danger" icon="el-icon-close" @click="dialogVisible = false">Cancel</el-button>
                </span>
            </el-dialog>
        </el-row>
    </el-main>
</template>

<script>
    import axios from 'axios'
    import ConfirmDialogItem from '../components/signin/ConfirmDialogItem.vue'

    export default {
        components: {
            ConfirmDialogItem
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
                    this.$notify({
                        title: "Sign in success",
                        message: `${response.data.message}`,
                        type: "success"
                    })
                    this.backToHome()
                })
                .catch(e => {
                    this.$notify({
                        title: "Error",
                        message: `${e.response.data.message} - ${e.response.status}`,
                        type: "error"
                    })
                })
            },
            getFullName() {
                return `${this.formData["name"]} ${this.formData["surname"]}`
            }
        }
    }
</script>

<style scoped>
</style>
