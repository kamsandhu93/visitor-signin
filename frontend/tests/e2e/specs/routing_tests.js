// https://docs.cypress.io/api/introduction/api.html

describe('Routing Tests', () => {
    it('Check / is set to Home page', () => {
        cy.visit('/')
        cy.contains('h1', 'Visitor Registration')
    })

    it('Check /signin is set to SignIn page', () => {
        cy.visit('/#/signin')
        cy.contains('h1', 'Sign In')
    })

    it('Check /signout is set to SignOut page', () => {
        cy.visit('/#/signout')
        cy.contains('h1', 'Sign Out')
    })

    it('Check navigation buttons on three main pages', () => {
        cy.visit('/')
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/`)
        cy.contains('Sign In').click()
        cy.contains('h1', 'Sign In')
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/signin`)
        cy.contains('Cancel').click()
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/`)
        cy.contains('Sign Out').click()
        cy.contains('h1', 'Sign Out')
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/signout`)
        cy.contains('Cancel').click()
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/`)
    })

    it('Check redirect is working', () => {
        cy.visit('/#/adsfasdfdasf')
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/`)
    })

    it('Check print error page dynamic fields', () => {
        cy.visit('/#/printerror?passId=00045a')
        cy.contains('#passId', '00045a')
        cy.contains('Home').click()
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/`)
    })

    it('Check transition page dynamic fields', () => {
        //Sign in with name test
        cy.visit('/#/transition?transitionType=signin&name=test')
        cy.contains('#name', 'test')
        cy.contains('.blueFont', ' sign in success')
        cy.contains('Home').click()
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/`)

        //Sign out with name test
        cy.visit('/#/transition?transitionType=signout&name=test')
        cy.contains('#name', 'test')
        cy.contains('.blueFont', ' sign out success')
        cy.contains('Home').click()
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/`)

        //no query parameter
        cy.visit('/#/transition?name=test')
        cy.get('#name').should('not.exist')
        cy.get('.blueFont').should('not.exist')
        cy.contains('Home').click()
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}/#/`)
    })

    it(' Check pass page dynamic fields', () => {
        cy.server()
        cy.route({
            method: 'POST',
            url: 'http://127.0.0.1:5002/print',
            response: "Internal Server Error",
            status: 500
        })

        cy.visit('/#/pass?name=testName&company=testCompany&passId=00045a')
        cy.contains('#name', 'testName')
        cy.contains('#company', 'testCompany')
        cy.contains('.passId', '00045a')
    })
})
