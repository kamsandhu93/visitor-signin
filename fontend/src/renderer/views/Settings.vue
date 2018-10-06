<template>
    <el-main>
        <el-form ref="settingsForm">
            <form-item label="Host" prop="name" v-model="configData['host']"></form-item>
            <form-item label="Port" prop="name" v-model="configData['port']"></form-item>
            <el-form-item>
                <el-select v-model="configData['printer']" placeholder="please select printer">
                    <el-option v-for="printer in getPrinters()" :label="printer.name" :value="printer.name"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" icon="el-icon-check" @click="submitForm()">Sign In</el-button>
                <el-button type="info" icon="el-icon-refresh" @click="resetForm()" plain>Reset</el-button>
                <el-button type="danger" icon="el-icon-close" @click="backToHome()" plain>Cancel</el-button>
                <el-button @click="getPrinters()">printer</el-button>
            </el-form-item>
        </el-form>
    </el-main>
</template>

<script>
    import fs from 'fs'
    import FormItem from '../components/common/FormItem.vue'

    export default {
        components: {
            FormItem
        },
        data() {
            return {
                configPath: "./config.json",
                configData: this.$store.state.configData
            }
        },
        methods: {
            backToHome() {
                this.$router.push({path: '/'})
            },
            getPrinters() {
                var window = this.$electron.remote.getCurrentWindow()
                var contents = window.webContents
                var printers = contents.getPrinters()
                console.log(printers)
                return printers
            },
            resetForm() {
                this.$refs.settingsForm.resetFields()
            },
            submitForm(){
                this.$store.commit('saveConfig', this.configData)
                this.backToHome()
            }
        }
    }
</script>
