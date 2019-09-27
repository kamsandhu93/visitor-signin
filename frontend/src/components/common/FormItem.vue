<template>
    <nhs-input
        v-model="body" :label="label" :name="name"
        :id="id" :maxlength="maxlength"
        :rules="rules" ref="input"
        v-bind="$attrs"
    >
    </nhs-input>
</template>

<script>
    export default {
        props: ["label", "value", "id", "name", "maxlength", "rules"],
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
        methods: {
            validate() {
                return this.$refs.input.validate()
            },
            focus() {
                this.$refs.input.focus()
            }
        }
    }
</script>
