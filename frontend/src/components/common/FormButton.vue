<template>
    <nhs-row>
        <nhs-col :span="33">
            <nhs-button @click="$emit('submitForm')" name="confirm-button">Confirm</nhs-button>
        </nhs-col>
        <nhs-col :span="33">
            <nhs-button color="secondary" @click="$emit('resetForm')" name="reset-button">Reset</nhs-button>
        </nhs-col>
        <nhs-col :span="33">
            <nhs-button color="secondary" @click="$router.push({path: '/'})" name="cancel-button">Cancel</nhs-button>
        </nhs-col>
    </nhs-row>
</template>

<script>
    export default {
        props: ["formName"]
    }
</script>
