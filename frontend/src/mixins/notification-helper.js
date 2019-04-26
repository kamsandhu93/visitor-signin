export default {
    methods: {
        notifySuccess(msg) {
            this.$notify({
                title: "Success",
                text: msg,
                type: "success",
                duration: 8000
            })
        },
        notifyError(msg) {
            this.$notify({
                title: "Error",
                text: msg,
                type: "error",
                duration: 8000
            })
        }
    }
}
