<template>
    <nhs-input
        v-model="body" :name="name"
        @blur="$emit('blur')" :id="id" :maxlength="maxlength"
    >
        <nhs-error-text slot="error" v-if="error">{{error}}</nhs-error-text>
        <nhs-label slot="label">{{label}}</nhs-label>
    </nhs-input>
</template>

<script>
    export default {
        props: ["label", "value", "error", "id", "name", "maxlength"],
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
        },
        computed: {
            showError() {
                if (this.error) {
                    return true
                }
                return false
            }
        }
    }
</script>
