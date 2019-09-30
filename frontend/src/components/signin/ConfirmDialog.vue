<template>
    <div class="modal">
        <nhs-main>
            <nhs-row>
                <nhs-col>
                    <nhs-care-card heading="Confirm Details">
                        <confirm-dialog-item id="confirmName">
                            Name: {{model['name']}} {{model['surname']}}
                        </confirm-dialog-item>
                        <confirm-dialog-item id="confirmCompany">
                            Company: {{model['company']}}
                        </confirm-dialog-item>
                        <confirm-dialog-item id="confirmVisiting">
                            Visiting: {{model['visiting']}}
                        </confirm-dialog-item>
                        <nhs-row>
                            <nhs-col :span="50">
                                <nhs-button
                                    name="dialog-confirm-button"
                                    :disabled="disabled" @click="$emit('confirm-details')"
                                >
                                    Confirm
                                </nhs-button>
                            </nhs-col>
                            <nhs-col :span="50">
                                <nhs-button
                                    color="secondary" name="dialog-cancel-button"
                                    :disabled="disabled" @click="$emit('close-dialog')"
                                >
                                    Cancel
                                </nhs-button>
                            </nhs-col>
                        </nhs-row>
                    </nhs-care-card>
                </nhs-col>
            </nhs-row>
        </nhs-main>
    </div>
</template>

<script>
    import ConfirmDialogItem from '@/components/signin/ConfirmDialogItem.vue'

    export default {
        components: { ConfirmDialogItem },
        props: [ 'value', 'disabled' ],
        data() {
            return {
                model: this.value
            }
        },
        watch: {
            model(val) {
                this.$emit('input', val)
            },
            value(val) {
                this.model = val
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
        width: 100vw;
        background: rgba(0, 0, 0, 0.5);
        margin: 0;
        padding: 0;
        padding-top: 100px;
        z-index: 10;
    }
</style>