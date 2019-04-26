<template>
    <nhs-main>
        <nhs-row>
            <nhs-col>
                <nhs-heading size="xl">Visitor pass print failed</nhs-heading>
                <nhs-heading id="passId">Please note down your Pass ID: {{ $route.query.passId }}</nhs-heading>
                <nhs-heading>and inform the reception</nhs-heading>
            </nhs-col>
        </nhs-row>
        <nhs-row>
            <nhs-col>
                <nhs-button @click="changeRoute('home')" name="home-button">Home</nhs-button>
            </nhs-col>
        </nhs-row>
    </nhs-main>
</template>

<script>
    import RouteHelper from '@/mixins/route-helper.js'

    export default {
        mixins: [RouteHelper]
    }
</script>
