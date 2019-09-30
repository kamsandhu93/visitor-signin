<template>
    <div id="app">
        <notifications classes="notification" width="400px"></notifications>
        <nhs-header :show-search="false" :show-nav="false" :service="service"></nhs-header>
        <router-view></router-view>
        <nhs-footer></nhs-footer>
    </div>
</template>

<script>
    export default {
        name: 'app',
        data() {
            return {
                service: {
                    name: "Digital Delivery Centre"
                }
            }
        }
    }
</script>

<style>
    .notification {
        padding: 10px;
        margin: 5px 5px 0px;
        font-size: 12pt;
        color: #ffffff;
        background: #44A4FC;
        border-left: 5px solid #187FE7;
    }
    .notification.warn {
        background: #ffb648;
        border-left-color: #f48a06;
    }
    .notification.error {
        background: #da291c;
        border-left-color: #B82E24;
    }
    .notification.success {
        background: #007f3b;
        border-left-color: #005326;
    }
    .notification.notification-title{
        font-size: 14pt;
    }

    .main-container {
        min-height: calc(100vh - 172px);
    }
</style>
