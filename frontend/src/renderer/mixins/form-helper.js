export default {
    methods: {
        validateForm(formName, callback) {
            this.$refs[formName].validate(callback)
        },
        resetForm(formName) {
            this.$refs[formName].resetFields()
        }
    }
}
