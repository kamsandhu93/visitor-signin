describe('Form Tests', () => {
    //Signin tests
    it('Test empty fields error message sign in', () => {
        cy.visit('/#/signin')
        cy.get('#btnConfirm').click()
        cy.formError('#name').contains('Please input your first name')
        cy.formError('#surname').contains('Please input your last name')
        cy.formError('#visiting').contains('Please input who you are visiting')
        cy.formError('#company').should('not.exist')
        })

    it('Test input field length sign in', () => {
        cy.visit('/#/signin')
        cy.formInput('#name').type('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        cy.formInput('#surname').type('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        cy.formInput('#visiting').type('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        cy.formInput('#company').type('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        cy.formInput('#name').should('have.value', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        cy.formInput('#surname').should('have.value', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        cy.formInput('#visiting').should('have.value', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        cy.formInput('#company').should('have.value', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    })

    it('Test name input validation', () => {
        cy.visit('/#/signin')
        cy.formInput('#name').type('123')
        cy.get('#btnConfirm').click()
        cy.formError('#name').contains('Accepted characters: A-Z, a-z')
        cy.get('#btnReset').click()
        cy.formInput('#name').type('test name')
        cy.get('#btnConfirm').click()
        cy.formError('#name').contains('Accepted characters: A-Z, a-z')
        cy.get('#btnReset').click()
        cy.formInput('#name').type('test-name')
        cy.get('#btnConfirm').click()
        cy.formError('#name').contains('Accepted characters: A-Z, a-z')
        cy.get('#btnReset').click()
        cy.formInput('#name').type('testname')
        cy.get('#btnConfirm').click()
        cy.formError('#name').should('not.exist')
        cy.get('#btnReset').click()
        cy.formInput('#name').type('TESTNAME')
        cy.get('#btnConfirm').click()
        cy.formError('#name').should('not.exist')
    })

    it('Test surname input validation', () => {
        cy.visit('/#/signin')
        cy.formInput('#surname').type('123')
        cy.get('#btnConfirm').click()
        cy.formError('#surname').contains('Accepted characters: A-Z, a-z')
        cy.get('#btnReset').click()
        cy.formInput('#surname').type('test surname')
        cy.get('#btnConfirm').click()
        cy.formError('#surname').contains('Accepted characters: A-Z, a-z')
        cy.get('#btnReset').click()
        cy.formInput('#surname').type('test-surname')
        cy.get('#btnConfirm').click()
        cy.formError('#surname').contains('Accepted characters: A-Z, a-z')
        cy.get('#btnReset').click()
        cy.formInput('#surname').type('testsurname')
        cy.get('#btnConfirm').click()
        cy.formError('#surname').should('not.exist')
        cy.get('#btnReset').click()
        cy.formInput('#surname').type('TESTSURNAME')
        cy.get('#btnConfirm').click()
        cy.formError('#surname').should('not.exist')
    })

    it('Test visiting input validation', () => {
        cy.visit('/#/signin')
        cy.formInput('#visiting').type('123')
        cy.get('#btnConfirm').click()
        cy.formError('#visiting').contains('Accepted characters: A-Z, a-z and space')
        cy.get('#btnReset').click()
        cy.formInput('#visiting').type('test-visiting')
        cy.get('#btnConfirm').click()
        cy.formError('#visiting').contains('Accepted characters: A-Z, a-z and space')
        cy.get('#btnReset').click()
        cy.formInput('#visiting').type('testvisiting')
        cy.get('#btnConfirm').click()
        cy.formError('#visiting').should('not.exist')
        cy.get('#btnReset').click()
        cy.formInput('#visiting').type('test visiting')
        cy.get('#btnConfirm').click()
        cy.formError('#visiting').should('not.exist')
        cy.get('#btnReset').click()
        cy.formInput('#visiting').type('TEST VISITING')
        cy.get('#btnConfirm').click()
        cy.formError('#visiting').should('not.exist')
    })

    it('Test company input validation', () => {
        cy.visit('/#/signin')
        cy.formInput('#company').type('test-company')
        cy.get('#btnConfirm').click()
        cy.formError('#company').contains('Accepted characters: A-Z, a-z, 0-9 and space')
        cy.get('#btnReset').click()
        cy.formInput('#company').type('testcompany')
        cy.get('#btnConfirm').click()
        cy.formError('#company').should('not.exist')
        cy.get('#btnReset').click()
        cy.formInput('#company').type('test company')
        cy.get('#btnConfirm').click()
        cy.formError('#company').should('not.exist')
        cy.get('#btnReset').click()
        cy.formInput('#company').type('test company123')
        cy.get('#btnConfirm').click()
        cy.formError('#company').should('not.exist')
        cy.get('#btnReset').click()
        cy.formInput('#company').type('TEST COMPANY')
        cy.get('#btnConfirm').click()
        cy.formError('#company').should('not.exist')
    })

    it('Test confirm dialog', () => {
        cy.visit('/#/signin')
        cy.formInput('#name').type('firstname')
        cy.formInput('#surname').type('surname')
        cy.formInput('#visiting').type('visiting')
        cy.formInput('#company').type('company')
        cy.get('#btnConfirm').click()
        cy.get('#confirmName').contains('firstname surname')
        cy.get('#confirmVisiting').contains('visiting')
        cy.get('#confirmCompany').contains('company')
    })

    it('Test white space trim', () => {
        cy.visit('/#/signin')
        cy.formInput('#name').type('   firstname  ')
        cy.formInput('#surname').type('   surname   ')
        cy.formInput('#visiting').type('   visiting   ')
        cy.formInput('#company').type(' test company ')
        cy.get('#btnConfirm').click()
        cy.formInput('#name').should('have.value', 'firstname')
        cy.formInput('#surname').should('have.value', 'surname')
        cy.formInput('#visiting').should('have.value', 'visiting')
        cy.formInput('#company').should('have.value', 'test company')
    })

    //SignOut tests
    it('Test empty fields error message sign out', () => {
        cy.visit('/#/signout')
        cy.get('#btnConfirm').click()
        cy.formError('#passId').contains('Please input Pass ID')
    })

    it('Test input field length sign out', () => {
        cy.visit('/#/signout')
        cy.formInput('#passId').type('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        cy.formInput('#passId').should('have.value', 'aaaaaa')
    })

    it('Test pass id input validation', () => {
        cy.visit('/#/signout')
        cy.formInput('#passId').type('111111')
        cy.get('#btnConfirm').click()
        cy.formError('#passId').contains('Pass ID has format: 0000a')
        cy.get('#btnReset').click()
        cy.formInput('#passId').type('aaaaaa')
        cy.get('#btnConfirm').click()
        cy.formError('#passId').contains('Pass ID has format: 0000a')
        cy.get('#btnReset').click()
        cy.formInput('#passId').type('aaa111')
        cy.get('#btnConfirm').click()
        cy.formError('#passId').contains('Pass ID has format: 0000a')
        cy.get('#btnReset').click()
        cy.formInput('#passId').type('111aaa')
        cy.get('#btnConfirm').click()
        cy.formError('#passId').contains('Pass ID has format: 0000a')
        cy.get('#btnReset').click()
        cy.formInput('#passId').type('11111A')
        cy.get('#btnConfirm').click()
        cy.formError('#passId').contains('Pass ID has format: 0000a')
    })
})
