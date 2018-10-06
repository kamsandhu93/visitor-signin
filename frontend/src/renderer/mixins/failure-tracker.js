import axios from 'axios'

export default {
    methods: {
        testService() {
            axios.get(`${this.$store.getters.url}/status`, {timeout: 1000})
            .then((response) => {
                this.$store.commit('resetFailure')
                if (this.$route.name === "error") {
                    this.changeRoute('home')
                }
            })
            .catch((e) => {
                this.$store.commit('recordFailure')
                if (this.$store.state.failures > 5) {
                    this.changeRoute('error')
                }
            })
        }
    },
    mounted() {
        setInterval(() => {
            this.testService()
        }, 60000)
    }
}
