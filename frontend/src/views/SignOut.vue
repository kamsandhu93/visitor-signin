<template>
    <el-main>
        <el-row>
            <h1>Sign Out</h1>
        </el-row>
        <el-row>
            <qrcode-reader @decode="onDecode" :paused="paused" :camera="cameraOpts"></qrcode-reader>
        </el-row>
        <el-row type="flex" justify="center">
            <el-col :span="12">
                <el-form :model="formData" :rules="rules" ref="signOutForm">
                    <form-item label="Pass ID" prop="pass_id" v-model="formData['pass_id']"></form-item>
                    <el-form-item>
                        <el-button type="primary" icon="el-icon-check" @click="submitForm('signOutForm')">Sign Out</el-button>
                        <el-button type="info" icon="el-icon-refresh" @click="resetForm('signOutForm')" plain>Reset</el-button>
                        <el-button type="danger" icon="el-icon-close" @click="backToHome()" plain>Cancel</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </el-main>
</template>

<script>
    import { QrcodeReader } from 'vue-qrcode-reader'
    import axios from 'axios'
    import FormItem from '../components/common/FormItem.vue'

    export default {
        components: {
            QrcodeReader,
            FormItem
        },
        data () {
            return {
                formData: {
                    pass_id: ""
                },
                rules: {
                    pass_id: [{required: true, message: 'Please input Pass ID', trigger: 'blur'}]
                },
                paused: false,
                cameraOpts: {
                    facingMode: { ideal: "environment" },
                    width: { min: 360, ideal: 680, max: 800 },
                    height: { min: 240, ideal: 480, max: 600 }
                }
            }
        },
        methods: {
            onDecode(decodedString) {
                this.paused = true
                this.formData["pass_id"] = decodedString
                this.submitForm("signOutForm")
            },
            backToHome() {
                this.$router.push({path: "/"})
            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.sendSignoutRequest()
                    }
                    else {
                        this.paused = false
                        return false
                    }
                })
            },
            resetForm(formName) {
                this.$refs[formName].resetFields()
                this.paused = false
            },
            sendSignoutRequest() {
                axios.post('http://localhost:5000/logout', {body: this.formData})
                .then(response => {
                    this.$notify({
                        title: "Sign out success",
                        message: `${response.data.message}`,
                        type: 'success'
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
            }
        }
    }
</script>

<style scoped>
    button {
        margin: 5px;
        font-size: 16pt;
        padding: 20px;
    }
</style>
