<template>
    <nhs-main>
        <nhs-row>
            <nhs-col>
                <nhs-heading size="xl">Visitor Registration</nhs-heading>
            </nhs-col>
        </nhs-row>
        <nhs-row>
            <nhs-col :span="50">
                <nhs-button @click="changeRoute('signin')" name="signin-button"><b>Sign In</b></nhs-button>
            </nhs-col>
            <nhs-col :span="50">
                <nhs-button color="secondary" @click="changeRoute('signout')" name="signout-button"><b>Sign Out</b></nhs-button>
            </nhs-col>
        </nhs-row>
    </nhs-main>
</template>

<script>
    import RouteHelper from '@/mixins/route-helper.js'
    import FailureTracker from '@/mixins/failure-tracker.js'

    export default {
        mixins: [RouteHelper, FailureTracker]
    }
</script>

<style scoped>


</style>
