<template>
    <div>
        <div class="row">
            <div class="box">
                <div class="p1Header">
                    <b>Whitehall II Security: 0113 866 5735</b>
                </div>
                <div class="p1Main">
                    <div class="p1Img">
                        <div class="p1QrContainer">
                            <qrcode-vue :value="$route.query.passId" :size="75"></qrcode-vue>
                        </div>
                        <div class="p1LogoContainer">
                            <img class="logo" src="../assets/img/pass_logo.png"/>
                        </div>
                    </div>
                    <div class="visitor">VISITOR</div>
                    <h3 id="name" :style="{ fontSize: calculateFontSize($route.query.name) }">{{ $route.query.name }}</h3>
                    <h3 id="company" :style="{ fontSize: calculateFontSize($route.query.company) }">{{ $route.query.company }}</h3>
                </div>
                <div class="p1Secondary">
                    <div class="date">Date: {{ date }}</div><div class="passId">Pass ID: {{ $route.query.passId }}</div>
                </div>
                <div class="p1Footer">
                    IMPORTANT: <br>Please read the health &amp; safety regulations on this pass and return pass to reception on departure
                </div>
            </div>
            <div class="box">
                <div class="p2Header">
                    <span style="color: blue; font-size: 12pt;">Welcome to Whitehall II</span><br>
                    Whitehall Quay, LS1 4HR<br>
                    <span><b>Whilst on site please observe the following:</b></span><br>
                </div>
                <div class="p2Main">
                    <ul style="list-style-type: decimal;">
                        <li><span style="color:blue">HEALTH AND SAFETY AT WORK:</span> A safe working environment is provided and all visitors are requested to co-operate in the maintenance of the high standard of safe practice.</li>
                        <li><span style="color:blue">EMERGENCY PROCEDURE:</span> See reverse.</li>
                        <li><span style="color:blue">FIRST AID:</span> In the event of injury or illness contact Office Services on 0113 397 3970 (option 2).</li>
                        <li><span style="color:blue">FIRST AID:</span> SECURITY AND CCTV: This pass must be worn at all times whilst without their host. 24/7 live CCTV monitoring and recording is taking place for the purposes of security and crime prevention. All security incidents must be reported immediately to 0113 397 3970 (option 3).</li>
                        <li><span style="color:blue">CAMERAS:</span> Are not allowed without approval.</li>
                        <li><span style="color:blue">THIS IS A NON SMOKING ENVIRONMENT</span></li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="box">
                <div class="p3Header">
                    Fire Action Notice:
                </div>
                <div class="p3Main">
                    <ul>
                        <li>On hearing the alarm, please leave the building via the nearest route and await further instruction from fire marshall's.</li>
                        <li>The turnstiles will automatically release, for all other doors please press the green door release dutton.</li>
                        <li>Do not attempt to use the lifts.</li>
                        <li>Do not stop to collect personal belongings.</li>
                        <li>Do not re-enter the building until you are advised it is safe to do so.</li>
                        <li>Inform your host or security reception if you require any assistance evacuating the building.</li>
                    </ul>
                </div>
            </div>
            <div class="box">
                <div class="p4Header">
                    Emergency Assembly Point
                </div>
                <img class="diagram" src="../assets/img/diagram.png">
            </div>
        </div>
        <div v-show="!printing">
            Please read the information on this pass carefully
        </div>
    </div>
</template>

<script>
    import RouteHelper from '../mixins/route-helper.js'
    import QrcodeVue from 'qrcode.vue'

    export default {
        components: {
            QrcodeVue
        },
        mixins: [RouteHelper],
        data() {
            return {
                date: this.getDate(),
                printing: false
            }
        },
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
            },
            printPage() {
                var window = this.$electron.remote.getCurrentWindow()
                var contents = window.webContents
                contents.print({silent: true, deviceName: this.$store.getters.printer}, (response) => {
                    if (response) {
                        var query = {
                            transitionType: 'signin',
                            name: this.$route.query.name
                        }
                        this.changeRouteQuery('transition', query)
                    }
                })
            },
            calculateFontSize(text) {
                var nameLength = text.length
                if (40 > nameLength && nameLength > 20) {
                    return '11pt'
                }
                else if (50 > nameLength && nameLength >= 40) {
                    return '10pt'
                }
                else if (nameLength >= 50) {
                    return '9pt'
                }
            }
        },
        mounted() {
            setTimeout(() => {
                this.printing = true
                this.printPage()
            }, 3000)
        }
    }
</script>

<style scoped>
    @page {

    }

    .row {
        display: flex;
        flex-flow: row;
    }

    .box {
        width: 9.3cm;
        height: 7.5cm;
        display: flex;
        flex-flow: column;
        align-items: center;
        justify-content: flex-start;
        border: 2px solid #000000;
        padding: 0.3cm;
    }

    .p1Header {
        width: 100%;
        height: 0.5cm;
        line-height: 0.5cm;
        font-size: 11pt;
    }

    .p1Main {
        width: 100%;
        height: 5cm;
        text-align: center;
        word-wrap: break-word;
    }

    .p1Img {
        width: 100%;
        height: 2cm;
    }

    .p1LogoContainer {
        width: 50%;
        height: 100%;
        float: left;
    }

    .p1QrContainer {
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

    .p1Secondary {
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

    .p1Footer {
        width: 100%;
        height: 1.2cm;
        color: red;
        font-size: 9pt;
        font-weight: bold;
    }

    .p2Header {
        width: 100%;
        font-size: 9pt;
    }

    .p2Main {
        font-size: 9.8pt;
        text-align: justify;
        width: 100%;
    }

    .p3Header {
        font-size: 14pt;
        color: red;
    }

    .p3Main {
        text-align: justify;
        font-size: 11pt;
    }

    .p4Header {
        font-size: 14pt;
        color: red;
    }

    h3 {
        margin: 0.2cm;
        font-size: 12pt;
    }

    ul {
        margin-left: -0.6cm;
    }

    .diagram {
        width: 70%;
    }
</style>
