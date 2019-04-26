<template>
    <nhs-main>
        <nhs-row>
            <nhs-col>
                <nhs-heading size="xl">The Service is currently unavailable</nhs-heading>
                <nhs-heading size="xl">Please inform the receptionist</nhs-heading>
            </nhs-col>
        </nhs-row>
    </nhs-main>
</template>

<script>
    import FailureTracker from '@/mixins/failure-tracker.js'
    import RouteHelper from '@/mixins/route-helper.js'

    export default {
        mixins: [FailureTracker, RouteHelper]
    }
</script>
