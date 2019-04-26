describe('Notification Tests', () => {
    it('Test sign in error message', () => {
        cy.server()
        cy.route({
            method: 'POST',
            url: 'http://127.0.0.1:5000/login',
            response: 'Internal Server Error',
            status: 500
        })


        cy.visit('/#/signin')
        cy.formInput('#name').type('firstname')
        cy.formInput('#surname').type('surname')
        cy.formInput('#visiting').type('A Person')
        cy.formInput('#company').type('test company')
        cy.clickButton('confirm-button')
        cy.clickButton('dialog-confirm-button')
        cy.notificationBanner().contains('An error occured when signing in - please try again. If problem persists, please inform the receptionist.')
        cy.notificationClose()
        cy.notificationBanner().should('not.exist')
        cy.clickButton('dialog-confirm-button')
        cy.notificationBanner().contains('An error occured when signing in - please try again. If problem persists, please inform the receptionist.')
        cy.wait(9000)
        cy.notificationBanner().should('not.exist')
    })

    it('Test sign out error message', () => {
        cy.server()
        cy.route({
            method: 'POST',
            url: 'http://127.0.0.1:5000/logout',
            response: 'Internal Server Error',
            status: 500
        })

        cy.visit('/#/signout')
        cy.formInput('#passId').type('00045a')
        cy.clickButton('confirm-button')
        cy.notificationBanner().contains('An error occured when signing out - please try again. If problem persists, please inform the receptionist.')
        cy.notificationClose()
        cy.notificationBanner().should('not.exist')
        cy.clickButton('confirm-button')
        cy.notificationBanner().contains('An error occured when signing out - please try again. If problem persists, please inform the receptionist.')
        cy.wait(9000)
        cy.notificationBanner().should('not.exist')
    })
})
