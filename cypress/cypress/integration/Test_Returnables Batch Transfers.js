/// <reference types="cypress" />

import 'cypress-real-events/support'

describe('Test Returnables Batch Transfers', () => {
  const login = () => {
    cy.session(`Administrator`, () => {
      cy.visit('login#email')
      cy.get('#login_email').type(Cypress.env('USR'))
      cy.get('#login_password').type(Cypress.env('PWD'))
      cy.get(`button.btn.btn-sm.btn-primary.btn-block.btn-login`).click()
      cy.url().should('contain', 'app')
    })
  }


  beforeEach(() => {
    login()
  })

  // it('logs in user : Administrator', () => {
  //   cy.session(`Administrator`, () => {
  //     cy.visit('login#email')
  //     cy.get('#login_email').type(`Administrator`)
  //     cy.get('#login_password').type(`plokplok+6+6+6`)
  //     cy.get(`button.btn.btn-sm.btn-primary.btn-block.btn-login`).click()
  //     cy.url().should('contain', 'app')
  //   })

  //   cy.visit('app/home')
  //   // cy.visit('app/serialized-batch-returns/b9d18e5702')
  //   // cy.get('[data-fieldname=delivery_trip]').type(`MAT-DT-2022-00001`)
  // })

  it('Supplies Delivery Trip ID', () => {   // 
    // cy.login(`Administrator`)
    cy.wait(500)

    cy.visit('app/returnables-batch-transfers/RET-BAT-2022-00002')
    // cy.get('.primary-action').click()
    // cy.get('.modal-footer > .standard-actions > .btn-primary').click()

    // cy.get('div.ql-editor.ql-blank').type(`Comment`)


    // cy.get(':nth-child(4) > .section-body > .form-column > form > .frappe-control > .form-group > .control-input-wrapper > .control-input > .input-with-feedback')
    cy.get('textarea[data-fieldname="serial_numbers"]')
      .type(`{moveToEnd}           IBAA480`)

    cy.get('input[data-target="Delivery Trip"]').type(`MAT-DT-2022-00001`)
      .realPress('Tab')
      
    // cy.get('[data-fieldname="customer"]').type(`IBAA480`).realPress('Tab')
  })

})

/*

//*[@id="page-login"]/div/main/div[2]/div/section[2]/div[1]/form/div[2]/button
#page-login > div > main > div.page_content > div > section.for-email-login > div.login-content.page-card > form > div.page-card-actions > button

*/