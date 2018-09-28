<template>
    <div>
        <button @click="back">back</button><br>
        First Name: <input v-model="formData['name']"></input><br>
        Surname: <input v-model="formData['surname']"></input><br>
        Visiting: <input v-model="formData['visiting']"></input><br>
        Company: <input v-model="formData['company']"></input><br>
        <button @click="submitForm">Submit</button>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        data () {
            return {
                formData: {
                    name: "",
                    surname: "",
                    visiting: "",
                    company: ""
                }
            }
        },
        methods: {
            back () {
                this.$router.push({path: '/'})
            },
            submitForm () {
                axios.post('http://localhost:5000/login', {body: this.formData})
                .then(response => {
                    console.log(response)
                })
                .catch(e => {
                    console.log(e)
                })
            }
        }
    }
</script>

<style scoped>
</style>
