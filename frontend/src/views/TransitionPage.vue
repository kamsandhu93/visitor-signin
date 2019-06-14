<template>
    <nhs-main>
        <nhs-row v-if="$route.query.transitionType == 'signout'">
            <nhs-col>
                <nhs-heading id="name" size="xl">{{ $route.query.name }} sign out success</nhs-heading>
                <nhs-heading id="msg">Please return your visitor pass to reception</nhs-heading>
            </nhs-col>
        </nhs-row>
        <nhs-row v-if="$route.query.transitionType == 'signin'">
            <nhs-col>
                <nhs-heading id="name" size="xl">{{ $route.query.name }} sign in success</nhs-heading>
                <nhs-heading id="msg">Please collect your visitor pass from reception</nhs-heading>
            </nhs-col>
        </nhs-row>
        <nhs-row>
            <nhs-col>
                <nhs-button type="primary" @click="changeRoute('home')" name="home-button">Home</nhs-button>
            </nhs-col>
        </nhs-row>
    </nhs-main>
</template>

<script>
    import FailureTracker from '@/mixins/failure-tracker.js'
    import RouteHelper from '@/mixins/route-helper.js'

    export default {
        mixins: [FailureTracker, RouteHelper],
        mounted() {
            setTimeout(() => {
                this.changeRoute('home')
            }, 5000)
        }
    }
</script>
