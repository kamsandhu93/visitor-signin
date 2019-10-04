// https://docs.cypress.io/api/introduction/api.html

describe('Routing Tests', () => {
    it('Check / is set to Home page', () => {
        cy.visit('/')
        cy.contains('h1', 'Visitor Registration')
    })

    it('Check /signin is set to SignIn page', () => {
        cy.visit('/#/signin')
        cy.contains('h2', 'Sign In')
    })

    it('Check /signout is set to SignOut page', () => {
        cy.visit('/#/signout')
        cy.contains('h2', 'Sign Out')
    })

    it('Check navigation buttons on three main pages', () => {
        cy.visit('/')
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/`)
        cy.clickButton('signin-button')
        cy.contains('h2', 'Sign In')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/signin`)
        cy.clickButton('cancel-button')
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/`)
        cy.clickButton('signout-button')
        cy.contains('h2', 'Sign Out')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/signout`)
        cy.clickButton('cancel-button')
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/`)
    })

    it('Check redirect is working', () => {
        cy.visit('/#/adsfasdfdasf')
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/`)
    })

    it('Check print error page dynamic fields', () => {
        cy.visit('/#/printerror?passId=00045a')
        cy.contains('#passId', 'Please note down your Pass ID: 00045a')
        cy.clickButton('home-button')
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/`)
    })

    it('Check transition page dynamic fields', () => {
        //Sign in with name test
        cy.visit('/#/transition?transitionType=signin&name=test')
        cy.contains('#name', 'test sign in success')
        cy.clickButton('home-button')
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/`)

        //Sign out with name test
        cy.visit('/#/transition?transitionType=signout&name=test')
        cy.contains('#name', 'test sign out success')
        cy.clickButton('home-button')
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/`)

        //no query parameter
        cy.visit('/#/transition?name=test')
        cy.get('#name').should('not.exist')
        cy.clickButton('home-button')
        cy.contains('h1', 'Visitor Registration')
        cy.url().should('eq', `${Cypress.config().baseUrl}#/`)
    })
})
