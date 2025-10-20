// cypress/e2e/login.cy.js
describe('Login Flow', () => {
  it('should log in and redirect to home', () => {
    cy.visit('/login')
    cy.get('input[placeholder="Email"]').type('user@example.com')
    cy.get('input[placeholder="Password"]').type('password123')
    cy.get('button').contains('Sign In').click()

    // چک کن که به صفحه اصلی رفته
    cy.url().should('eq', 'http://localhost:3000/')

    // چک کن که توکن ذخیره شده
    cy.window().its('localStorage').invoke('getItem', 'accessToken')
      .should('exist')

    // چک کن که کامپوننت آپلود وجود دارد
    cy.get('input[type="file"]').should('exist')
  })
})