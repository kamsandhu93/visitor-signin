export default {
    methods: {
        validateForm(formName, callback) {
            this.$refs[formName].validate(callback)
        },
        resetForm(formName) {
            this.$refs[formName].resetFields()
        },
        checkFormValue(value, regex, errorMsg, callback) {
            if (value.trim().match(regex)) {
                callback()
            }
            else {
                callback(new Error(errorMsg))
            }
        },
        checkFormValueEmpty(value, errorMsg, callback) {
            if (!value) {
                callback(new Error(errorMsg))
            }
        }
    }
}
