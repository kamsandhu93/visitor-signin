<template>
    <el-row type="flex" justify="center" :gutter="10" class="row">
        <el-col :span="5" class="label">
            <b>{{ label }}</b>
        </el-col>
        <el-col :span="10" class="body">
            {{ text }}
        </el-col>
    </el-row>
</template>

<script>
    export default {
        props: ["label", "body"],
        data() {
            return {
                text: this.body
            }
        },
        watch: {
            body(val) {
                this.text = val
            }
        }
    }
</script>

<style scoped>
    .label {
        text-align: right;
        font-size: 16pt;
    }

    .body {
        text-align: left;
        font-size: 16pt;
    }

    .row {
        margin: 10px;
    }
</style>
