export default {
    methods: {
        changeRoute(path) {
            this.$router.push({ name: path })
        },
        changeRouteQuery(path, query) {
            this.$router.push({ name: path, query: query })
        }
    }
}
