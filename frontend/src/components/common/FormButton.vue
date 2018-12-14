<template>
    <el-form-item>
        <el-button id="btnConfirm" type="primary" icon="el-icon-check" @click="$emit('submitForm', formName)">Confirm</el-button>
        <el-button id="btnReset" type="info" icon="el-icon-refresh" @click="$emit('resetForm', formName)" plain>Reset</el-button>
        <el-button id="btnCancel" type="danger" icon="el-icon-close" @click="$emit('changeRoute', 'home')" plain>Cancel</el-button>
    </el-form-item>
</template>

<script>
    export default {
        props: ["formName"]
    }
</script>
