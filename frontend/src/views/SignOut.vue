<template>
    <div>
        <button @click="back">back</button>
        <qrcode-reader @decode="onDecode" :paused="paused"></qrcode-reader>
        <el-form :model="formData" :rules="rules" ref="signOutForm">
            <el-form-item label="Pass ID" prop="pass_id">
                <el-input v-model="formData['pass_id']"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('signOutForm')">Create</el-button>
                <el-button @click="resetForm('signOutForm')">Reset</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    import { QrcodeReader } from 'vue-qrcode-reader'
    import axios from 'axios'

    export default {
        data () {
            return {
                formData: {
                    pass_id: ""
                },
                rules: {
                    pass_id: [{required: true, message: 'Please input Pass ID', trigger: 'blur'}]
                },
                paused: false
            }
        },
        components: {
            QrcodeReader
        },
        methods: {
            onDecode (decodedString) {
                this.paused = true
                this.formData["pass_id"] = decodedString
                this.submitForm("signOutForm")
            },
            back () {
                this.$router.push({path: "/"})
            },
            submitForm (formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        axios.post('http://localhost:5000/logout', {body: this.formData})
                        .then(response => {
                            this.$notify({
                                title: "Sign out success",
                                message: `${response.data.message}`,
                                type: 'success'
                            })
                            this.back()
                        })
                        .catch(e => {
                            this.$notify({
                                title: "Error",
                                message: `${e.response.data.message} - ${e.response.status}`,
                                type: "error"
                            })
                        })
                    }
                    else {
                        this.paused = false
                        return false
                    }
                })
            },
            resetForm (formName) {
                this.$refs[formName].resetFields()
                this.paused = false
            }
        }
    }
</script>

<style scoped>
</style>
