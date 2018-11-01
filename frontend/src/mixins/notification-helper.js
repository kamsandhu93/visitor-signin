export default {
    methods: {
        notifySuccess(msg) {
            this.$notify({
                title: "Success",
                message: msg,
                type: "success"
            })
        },
        notifyError(msg) {
            this.$notify({
                title: "Error",
                message: msg,
                type: "error"
            })
        }
    }
}
