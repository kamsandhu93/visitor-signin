<template>
    <nhs-main class="main-container">
        <nhs-row>
            <nhs-col>
                <nhs-heading>Please wait while your pass prints...</nhs-heading>
            </nhs-col>
        </nhs-row>
    </nhs-main>
</template>

<script>
    import axios from 'axios'
    import RouteHelper from '@/mixins/route-helper.js'
    import NotificationHelper from '@/mixins/notification-helper.js'
    import PassExample from '@/components/pass/PassExample.vue'
    import PassWelcome from '@/components/pass/PassWelcome.vue'
    import PassFire from '@/components/pass/PassFire.vue'

    export default {
        components: {
            PassExample,
            PassWelcome,
            PassFire
        },
        mixins: [RouteHelper, NotificationHelper],
        methods: {
            printPage() {
                axios.post(this.$store.getters.printer, this.$route.query)
                .then((response) => {
                    var query = {
                        transitionType: 'signin',
                        name: this.$route.query.name
                    }
                    this.changeRouteQuery('transition', query)
                })
                .catch((error) => {
                    console.log(error)
                    this.changeRouteQuery('printerror', { passId: this.$route.query.passId })
                })
            }
        },
        mounted() {
            this.printPage()
        }
    }
</script>
