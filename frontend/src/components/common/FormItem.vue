<template>
    <el-form-item :prop="prop" ref="test">
        <span slot="label"><b>{{ label }}</b></span>
        <el-input v-model="body" clearable></el-input>
    </el-form-item>
</template>

<script>
    export default {
        props: ["label", "prop", "value"],
        data() {
            return {
                body: this.value
            }
        },
        watch: {
            body(val) {
                this.$emit("input", val)
            },
            value(val) {
                this.body = val
            }
        }
    }
</script>

<style scoped>
    span {
        font-size: 14pt;
    }

    .el-input {
        font-size: 12pt;
        padding-top: 5px;
        padding-bottom: 5px;
    }
</style>
