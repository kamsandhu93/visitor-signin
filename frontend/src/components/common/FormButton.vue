<template>
    <nhs-row>
        <nhs-col :span="33">
            <nhs-button @click="$emit('submitForm')" name="confirm-button" :disabled="disabled">Confirm</nhs-button>
        </nhs-col>
        <nhs-col :span="33">
            <nhs-button color="secondary" @click="$emit('resetForm')" name="reset-button" :disabled="disabled">Reset</nhs-button>
        </nhs-col>
        <nhs-col :span="33">
            <nhs-button color="secondary" @click="$router.push({path: '/'})" name="cancel-button" :disabled="disabled">Cancel</nhs-button>
        </nhs-col>
    </nhs-row>
</template>

<script>
    export default {
        props: {
            disabled: {
                type: Boolean,
                default: false
            }
        }
    }
</script>