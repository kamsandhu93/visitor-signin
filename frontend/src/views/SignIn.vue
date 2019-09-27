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
                    label="First Name" :rules="rules['name']"
                    v-model.trim="formData['name']" id="name" name="name" :maxlength="32"
                    ref="name" @keydown.enter.native="switchFocus('surname')"
                ></form-item>

                <form-item
                    label="Surname" :rules="rules['surname']"
                    v-model.trim="formData['surname']" id="surname" name="surname" :maxlength="32"
                    ref="surname" @keydown.enter.native="switchFocus('visiting')"
                ></form-item>

                <form-item
                    label="Visiting" :rules="rules['visiting']"
                    v-model.trim="formData['visiting']" id="visiting" name="visiting" :maxlength="32"
                    ref="visiting" @keydown.enter.native="switchFocus('company')"
                ></form-item>


                <form-item
                    label="Company" :rules="rules['company']"
                    v-model.trim="formData['company']" id="company" name="company" :maxlength="32"
                    ref="company" @keydown.enter.native="submitForm()"
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
                        <nhs-button name="dialog-confirm-button" :disabled="disableBtn" @click="sendSigninRequest()">
                            Confirm
                        </nhs-button>
                    </nhs-col>
                    <nhs-col :span="50">
                        <nhs-button color="secondary" name="dialog-cancel-button" :disabled="disableBtn" @click="confirmDialog = false">
                            Cancel
                        </nhs-button>
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
                disableBtn: false,
                rules: {
                    name: [
                        (v) => !!v.match(/^[A-Za-z]{1,32}$/) || 'Accepted characters: A-Z, a-z',
                        (v) => !!v || 'Please input your first name'
                    ],
                    surname: [
                        (v) => !!v.match(/^[A-Za-z]{1,32}$/) || 'Accepted characters: A-Z, a-z',
                        (v) => !!v || 'Please input your last name'
                    ],
                    visiting: [
                        (v) => !!v.match(/^[A-Za-z ]{1,32}$/) || 'Accepted characters: A-Z, a-z and space',
                        (v) => !!v || 'Please input who you are visiting'
                    ],
                    company: [
                        (v) => !!v.match(/^[A-Za-z0-9 ]{0,32}$/) || 'Accepted characters: A-Z, a-z, 0-9 and space'
                    ]
                }
            }
        },
        methods: {
            submitForm() {
                if (this.isFormValid()) {
                    this.confirmDialog = true
                }
            },
            isFormValid() {
                var valid = true
                for (var key in this.$refs) {
                    if (!this.$refs[key].validate()) {
                        valid = false
                    }
                }
                return valid
            },
            sendSigninRequest() {
                this.removeEmptyOptionalKeys(['company'])
                this.disableBtn = true
                axios.post(`${this.$store.getters.url}/login`, this.formData)
                .then((response) => {
                    var query = {
                        name: this.getFullName(),
                        company: this.formData['company'],
                        passId: response.data.passId
                    }
                    this.disableBtn = false
                    this.changeRouteQuery('loading', query)
                })
                .catch((e) => {
                    this.disableBtn = false
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
            },
            switchFocus(element) {
                this.$refs[element].focus()
            }
        },
        mounted() {
            this.$refs.name.focus()
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
