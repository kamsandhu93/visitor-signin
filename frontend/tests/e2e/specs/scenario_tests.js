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
            response: "OK",
            delay: 1000
        })

        cy.visit('/')
        cy.clickButton('signin-button')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/signin`)
        cy.formInput('#name').type('firstname')
        cy.formInput('#surname').type('surname')
        cy.formInput('#visiting').type('visiting person')
        cy.formInput('#company').type('company')
        cy.clickButton('confirm-button')
        cy.clickButton('dialog-confirm-button')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/loading?name=firstname%20surname&company=company&passId=00045a`)
        cy.wait(1000)
        cy.url().should('eq', `${Cypress.config().baseUrl}#/transition?transitionType=signin&name=firstname%20surname`)
        cy.get('#name').contains('firstname surname sign in success')
        cy.get('#msg').contains('Please collect your visitor pass from reception')
        cy.wait(6000)
        cy.url().should('eq', `${Cypress.config().baseUrl}#/`)
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
            status: 500,
            delay: 1000
        })

        cy.visit('/')
        cy.clickButton('signin-button')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/signin`)
        cy.formInput('#name').type('firstname')
        cy.formInput('#surname').type('surname')
        cy.formInput('#visiting').type('visiting person')
        cy.formInput('#company').type('company')
        cy.clickButton('confirm-button')
        cy.clickButton('dialog-confirm-button')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/loading?name=firstname%20surname&company=company&passId=00045a`)
        cy.wait(1000)
        cy.url().should('eq', `${Cypress.config().baseUrl}#/printerror?passId=00045a`)
        cy.get('#passId').contains('Please note down your Pass ID: 00045a')
        cy.contains('Home').click()
        cy.url().should('eq', `${Cypress.config().baseUrl}#/`)
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
        cy.clickButton('signout-button')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/signout`)
        cy.formInput('#passId').type('00045a')
        cy.clickButton('confirm-button')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/transition?transitionType=signout&name=test%20user`)
        cy.get('#name').contains('test user sign out success')
        cy.get('#msg').contains('Please return your visitor pass to reception')
        cy.wait(6000)
        cy.url().should('eq', `${Cypress.config().baseUrl}#/`)
    })
})
