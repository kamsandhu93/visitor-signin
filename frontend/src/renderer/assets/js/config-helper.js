import fs from 'fs'

const workDir = process.env['PORTABLE_EXECUTABLE_DIR'] || process.cwd()

class Config {
    constructor() {
        this.configPath = `${workDir}/config.json`
        this.defaultConfig = {
            host: "localhost",
            port: "5000",
            printer: "Microsoft Print to PDF"
        }
        this.keysToCheck = ["host", "port", "printer"]
    }

    read() {
        try {
            var config = JSON.parse(fs.readFileSync(this.configPath))
            this.checkKeys(config)
            return config
        }
        catch (e) {
            return this.defaultConfig
        }
    }

    checkKeys(config) {
        for (var key of this.keysToCheck) {
            if (!config[key]) {
                throw `Missing config key: ${key}`
            }
        }
    }
}

export default new Config()
