<template>
    <div>
        <div class="row">
            <div class="box">
                <h5>Whitehall II Security: 0113 866 5735</h5>
                <div class="presentation">
                    <div class="info">
                        <img src="../assets/img/pass_logo.png">
                        <div class="visitor">VISITOR</div>
                        <h3 id="name" v-bind:style="{ fontSize: computedFontSize }">{{ $route.query.name }}</h3>
                        <h3 id="company">{{ $route.query.company }}</h3>
                        <h3 id="date">{{ date }}</h3>
                    </div>
                    <div class="passid" id="passid">Pass ID: {{ $route.query.passId }}</div>
                </div>
                <div class="red">IMPORTANT: <br>Please read the health & safety regulations on this pass and return pass to reception on departure</div>
            </div>
            <div>
                <div class="box">
                    <div style="font-size: 9.8pt;">
                        <span style="color:blue;font-size: 13px;">Welcome to Whitehall II<br></span>
                        Whitehall Quay, LS1 4HR<br>
                        <span style="font-weight: bold;">Whilst on site please observe the following:<br></span>
                        <ul style="list-style-type: decimal; margin-left: -0.7cm;">
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
        </div>
        <div class="row">
            <div class="box">
                <div style="font-size: 14">
                    <span style="color: red; font-size: 18px;">Fire Action Notice:</span>
                    <br>
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
                <span style="color: red; font-size: 18px;">Emergency Assembly Point</span>
                <img src="../assets/img/diagram.png" style="width: 70%">
            </div>
        </div>
        <div v-show="!printing">
            Please read the information on this pass carefully
        </div>
    </div>
</template>

<script>
    import RouteHelper from '../mixins/route-helper.js'

    export default {
        mixins: [RouteHelper],
        data() {
            return {
                date: this.getDate(),
                computedFontSize: this.calculateFontSize(),
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
                            transitionType: 'signin'
                        }
                        this.changeRouteQuery('transition', query)
                    }
                })
            },
            calculateFontSize() {
                var nameLength = this.$route.query.name.length
                if(40 > nameLength > 30){
                    return 18
                }else if(50 > nameLength > 40){
                    return 15
                }else if(65 > nameLength > 50){
                    return 12
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

    div.row{
        display: flex;
        flex-flow: row;
    }
    div.presentation {
        width: auto;
        height: auto;
        display: flex;
        flex-flow: row;
        align-items: center;
        justify-content: center;
    }
    div.box {
        width: 9.3cm;
        height: 7.5cm;
        display: flex;
        flex-flow: column;
        align-items: center;
        justify-content: flex-start;
        border: 2px solid #000000;
        padding: 0.3cm;
    }

    div.box img {
        width: 30%;
        height: auto;
        margin-top: 0cm;
    }
    div.box div.info{
        display: flex;
        flex-flow: column;
        align-items: center;
    }
    div.box h3{
        margin: 0cm;
    }
    div.visitor{
        font-size: 45px;
        font-weight: 900;
        color: black;
    }
    div.red {
        margin-left: 0.2cm;
        color: red;
        font-size: 12px;
        font-weight: bold;
    }
    div.box h5{
        margin: 0cm;
    }
    div.passid {
        width: 5cm;
        height: 0.5cm;
        transform: rotate(-90deg);
        font-size: 16pt;
        margin-left: -2.5cm;
        margin-right: -1cm;
    }
</style>
