// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This is will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

Cypress.Commands.add('formInput', (id) => {
    return cy.get(id)
})

Cypress.Commands.add('formError', (id) => {
    return cy.get(`${id}-error`)
})

Cypress.Commands.add('notificationBanner', () => {
    return cy.get(".notification-content")
})

Cypress.Commands.add('notificationClose', () => {
    cy.get(".notification-content").click()
})

Cypress.Commands.add('clickButton', (name) => {
    cy.get(`button[name=${name}]`).click()
})
