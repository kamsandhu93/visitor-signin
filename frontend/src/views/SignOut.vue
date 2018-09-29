<template>
    <div>
        <button @click="back">back</button>
        <qrcode-reader @decode="onDecode" :paused="paused"></qrcode-reader>
        {{ passId }}
    </div>
</template>

<script>
    import { QrcodeReader } from 'vue-qrcode-reader'
    import axios from 'axios'

    export default {
        data () {
            return {
                passId: "",
                paused: false
            }
        },
        components: {
            QrcodeReader
        },
        methods: {
            onDecode (decodedString) {
                this.paused = true
                this.passId = decodedString
                axios.post('http://localhost:5000/logout', {body: {pass_id: decodedString}})
                .then(response => {
                    console.log(response)
                    this.back()
                })
                .catch(e => {
                    console.log(e)
                    this.$message({
                        message: `${e}`,
                        type: "error"
                    })
                })
            },
            back () {
                this.$router.push({path: "/"})
            }
        }
    }
</script>

<style scoped>
</style>
