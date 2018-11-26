function getFormInput(id) {
    return cy.get(`${id} .el-form-item__content .el-input input`)
}

function getFormError(id) {
    return cy.get(`${id} .el-form-item__content .el-form-item__error`)
}

describe('Scenario Tests', () => {
    it('End to end sign in no error', () => {
        cy.server()
        cy.route({
            method: 'POST',
            url: 'http://127.0.0.1:5000/login',
            response: { passId: "00045a" }
        })

        cy.route({
            method: 'POST',
            url: 'http://127.0.0.1:5002/print',
            response: "OK"
        })

        cy.visit('/')
        cy.contains('Sign In').click()
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/signin`)
        getFormInput('#name').type('firstname')
        getFormInput('#surname').type('surname')
        getFormInput('#visiting').type('visiting person')
        getFormInput('#company').type('company')
        cy.get('#btnConfirm').click()
        cy.get('#btnDialogConfirm').click()
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/pass?name=firstname%20surname&company=company&passId=00045a`)
        cy.wait(6000)
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/transition?transitionType=signin&name=firstname%20surname`)
        cy.wait(6000)
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/`)
    })

    it('End to end sign in print error', () => {
        cy.server()
        cy.route({
            method: 'POST',
            url: 'http://127.0.0.1:5000/login',
            response: { passId: "00045a" }
        })

        cy.route({
            method: 'POST',
            url: 'http://127.0.0.1:5002/print',
            response: "Internal Server Error",
            status: 500
        })

        cy.visit('/')
        cy.contains('Sign In').click()
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/signin`)
        getFormInput('#name').type('firstname')
        getFormInput('#surname').type('surname')
        getFormInput('#visiting').type('visiting person')
        getFormInput('#company').type('company')
        cy.get('#btnConfirm').click()
        cy.get('#btnDialogConfirm').click()
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/pass?name=firstname%20surname&company=company&passId=00045a`)
        cy.wait(6000)
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/printerror?passId=00045a`)
        cy.contains('Home').click()
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/`)
    })

    it('End to end sign out no error', () => {
        cy.server()
        cy.route({
            method: 'POST',
            url: 'http://127.0.0.1:5000/logout',
            response: {
                firstname: "test",
                surname: "user"
            }
        })

        cy.visit('/')
        cy.contains('Sign Out').click()
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/signout`)
        getFormInput('#passId').type('00045a')
        cy.get('#btnConfirm').click()
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/transition?transitionType=signout&name=test%20user`)
        cy.wait(6000)
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/`)
    })
})
