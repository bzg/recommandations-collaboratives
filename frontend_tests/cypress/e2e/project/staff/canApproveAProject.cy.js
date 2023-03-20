describe('I can go to the dashboard and see the pending projects, and approve one', () => {
    beforeEach(() => {
        cy.login("staff");
    })

    it('approves a project', () => {

        cy.visit('/projects')

        cy.contains("Revenir sur l'ancien tableau de bord").click({ force: true })
        cy.contains("Projets en attente d'acceptation")
        cy.contains("Friche numéro 4")
        cy.get("#draft-projects").siblings().contains('Friche numéro 4').parents('tr').contains('Accepter').click({ force: true })
        cy.url().should('include', '/project/')
        cy.contains("Friche numéro 4")

        cy.visit('/projects')
        cy.contains("Revenir sur l'ancien tableau de bord").click({ force: true })
        cy.get("#draft-projects").siblings().contains('Friche numéro 4').should('not.exist')
    })
})
