<template>
    <nhs-row>
        <nhs-col>
            <p :id="id">
                <slot></slot>
            </p>
        </nhs-col>
    </nhs-row>
</template>

<script>
    export default {
        props: [ 'id' ]
    }
</script>
