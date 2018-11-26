<template>
    <el-card class="passContainer">
        <div class="header">
            <b>Whitehall II Security: 0113 866 5735</b>
        </div>
        <div class="main">
            <div class="imgContainer">
                <div class="qrContainer">
                    <qrcode-vue :value="query.passId" :size="75"></qrcode-vue>
                </div>
                <div class="logoContainer">
                    <img class="logo" src="@/assets/img/pass_logo.png"/>
                </div>
            </div>
            <div class="visitor">VISITOR</div>
            <h3 id="name">{{ query.name }}</h3>
            <h3 id="company">{{ query.company }}</h3>
        </div>
        <div class="secondary">
            <div class="date">Date: {{ getDate() }}</div><div class="passId">Pass ID: {{ query.passId }}</div>
        </div>
        <div class="footer">
            IMPORTANT: <br>Please read the health &amp; safety regulations on this pass and return pass to reception on departure
        </div>
    </el-card>
</template>

<script>
    import QrcodeVue from 'qrcode.vue'

    export default {
        components: {
            QrcodeVue
        },
        props: ["query"],
        methods: {
            getDate() {
                var today = new Date()
                var dd = today.getDate();
                var mm = today.getMonth() + 1; //January is 0!
                var yyyy = today.getFullYear();
                if(dd<10) {
                    dd = '0'+dd
                }

                if(mm<10) {
                    mm = '0'+mm
                }

                return mm + '/' + dd + '/' + yyyy;
            }
        }
    }
</script>

<style scoped>
    .header {
        width: 100%;
        height: 0.5cm;
        line-height: 0.5cm;
        font-size: 11pt;
    }

    .main {
        width: 100%;
        height: 5cm;
        text-align: center;
        word-wrap: break-word;
    }

    .imgContainer {
        width: 100%;
        height: 2cm;
    }

    .logoContainer {
        width: 50%;
        height: 100%;
        float: left;
    }

    .qrContainer {
        width: 50%;
        height: 100%;
        float: left;
    }

    .logo {
        margin: 0;
        height: 100%;
    }

    .visitor{
        font-size: 32pt;
        font-weight: 900;
        color: black;
    }

    .secondary {
        height: 0.7cm;
        line-height: 0.7cm;
        width: 100%;
        font-size: 11pt;
        margin-top: 0.1cm;
    }

    .date {
        width: 50%;
        float: left;
    }

    .passId {
        width: 50%;
        float: left;
    }

    .footer {
        width: 100%;
        height: 1.2cm;
        color: red;
        font-size: 9pt;
        font-weight: bold;
    }

    h3 {
        margin: 0.2cm;
        font-size: 12pt;
    }
</style>
