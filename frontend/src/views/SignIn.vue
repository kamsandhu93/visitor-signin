<template>
    <nhs-main>
        <nhs-row>
            <nhs-col>
                <nhs-heading size="xl">Sign In</nhs-heading>
            </nhs-col>
        </nhs-row>
        <nhs-row>
            <nhs-col>
                <form-item 
                    :label="labels['name']" :error="errors['name']"
                    v-model.trim="formData['name']" id="name" name="name" :maxlength="32"
                    @blur="checkFirstName()"
                ></form-item>

                <form-item 
                    :label="labels['surname']" :error="errors['surname']"
                    v-model.trim="formData['surname']" id="surname" name="surname" :maxlength="32"
                    @blur="checkLastName()"
                ></form-item>

                <form-item
                    :label="labels['visiting']" :error="errors['visiting']"
                    v-model.trim="formData['visiting']" id="visiting" name="visiting" :maxlength="32"
                    @blur="checkVisiting()"
                ></form-item>


                <form-item
                    :label="labels['company']" :error="errors['company']"
                    v-model.trim="formData['company']" id="company" name="company" :maxlength="32"
                    @blur="checkCompany()"
                ></form-item>

                <form-button @submitForm="submitForm()" @resetForm="resetForm()"></form-button>
            </nhs-col>
        </nhs-row>
        <div class="modal" v-show="confirmDialog">
            <nhs-care-card heading="Confirm Details"  class="confirmDialog">
                <nhs-row>
                    <nhs-col>
                        <p id="confirmName">Name: {{formData['name']}} {{formData['surname']}}</p>
                    </nhs-col>
                </nhs-row>

                <nhs-row>
                    <nhs-col>
                        <p id="confirmCompany">Company: {{formData['company']}}</p>
                    </nhs-col>
                </nhs-row>

                <nhs-row>
                    <nhs-col>
                        <p id="confirmVisiting">Visiting: {{formData['visiting']}}</p>
                    </nhs-col>
                </nhs-row>

                <nhs-row>
                    <nhs-col :span="50">
                        <nhs-button name="dialog-confirm-button" @click="sendSigninRequest()">Confirm</nhs-button>
                    </nhs-col>
                    <nhs-col :span="50">
                        <nhs-button color="secondary" name="dialog-cancel-button" @click="confirmDialog = false">Cancel</nhs-button>
                    </nhs-col>
                </nhs-row>
            </nhs-care-card>
        </div>
    </nhs-main>
</template>

<script>
    import axios from 'axios'
    import FormItem from '@/components/common/FormItem.vue'
    import FormButton from '@/components/common/FormButton.vue'
    import RouteHelper from '@/mixins/route-helper.js'
    import NotificationHelper from '@/mixins/notification-helper.js'
    import FailureTracker from '@/mixins/failure-tracker.js'

    export default {
        components: {
            FormItem,
            FormButton
        },
        mixins: [RouteHelper, NotificationHelper, FailureTracker],
        data() {
            return {
                formData: {
                    name: "",
                    surname: "",
                    visiting: "",
                    company: ""
                },
                confirmDialog: false,
                errors: {
                    name: { text: "" },
                    surname: { text: "" } ,
                    visiting: { text: "" },
                    company: { text: "" }
                },
                labels: {
                    name: { text: "First Name" },
                    surname: { text: "Surname" },
                    visiting: { text: "Visiting" },
                    company: { text: "Company" }
                }
            }
        },
        methods: {
            submitForm() {
                this.checkFirstName()
                this.checkLastName()
                this.checkVisiting()
                this.checkCompany()
                if (this.isFormValid()) {   
                    this.confirmDialog = true
                }
            },
            isFormValid() {
                for (var key in this.errors) {
                    if (this.errors[key].text) {
                        return false
                    }
                }
                return true
            },
            sendSigninRequest() {
                this.removeEmptyOptionalKeys(['company'])
                axios.post(`${this.$store.getters.url}/login`, this.formData)
                .then((response) => {
                    var query = {
                        name: this.getFullName(),
                        company: this.formData['company'],
                        passId: response.data.passId
                    }
                    this.changeRouteQuery('pass', query)
                })
                .catch((e) => {
                    this.notifyError("An error occured when signing in - please try again. If problem persists, please inform the receptionist.")
                })
            },
            removeEmptyOptionalKeys(keys) {
                for (var key of keys) {
                    if (!this.formData[key]) {
                        delete this.formData[key]
                    }
                }
            },
            getFullName() {
                return `${this.formData["name"]} ${this.formData["surname"]}`
            },
            resetForm() {
                for (var field in this.formData) {
                    this.formData[field] = ""
                }
                for (var error in this.errors) {
                    this.errors[error].text = ""
                }
            },
            checkFormData(name, regex, emptyErr, valueErr) {
                if (!this.formData[name]) {
                    this.errors[name].text = emptyErr
                }
                else if (!regex.test(this.formData[name])) {
                    this.errors[name].text = valueErr
                }
                else {
                    this.errors[name].text = ""
                }
            },       
            checkFirstName() {
                var regex = new RegExp("^[A-Za-z]{1,32}$")
                var emptyErr = "Please input your first name"
                var valueErr = "Accepted characters: A-Z, a-z"
                this.checkFormData("name", regex, emptyErr, valueErr)
            },
            checkLastName(rule, value, callback) {
                var regex = new RegExp("^[A-Za-z]{1,32}$")
                var emptyErr = "Please input your last name"
                var valueErr = "Accepted characters: A-Z, a-z"
                this.checkFormData("surname", regex, emptyErr, valueErr)
            },
            checkVisiting(rule, value, callback) {
                var regex = new RegExp("^[A-Za-z ]{1,32}$")
                var emptyErr = "Please input who you are visiting"
                var valueErr = "Accepted characters: A-Z, a-z and space"
                this.checkFormData("visiting", regex, emptyErr, valueErr)
            },
            checkCompany(rule, value, callback) {
                var regex = new RegExp("^[A-Za-z0-9 ]{1,32}$")
                if (this.formData["company"] && !regex.test(this.formData["company"])) {
                    this.errors["company"].text = "Accepted characters: A-Z, a-z, 0-9 and space"
                }
                else {
                    this.errors["company"].text = ""
                }
            }
        }
    }
</script>

<style scoped>
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        height: 100vh;
        width: 100%;
        background: rgba(0, 0, 0, 0.5);
        margin: 0;
        padding: 0;
        padding-left: 25%;
        padding-top: 100px;
        z-index: 10;
    }

    .confirmDialog {
        width: 50vw;
    }
</style>
